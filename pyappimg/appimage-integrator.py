#!/usr/bin/env python3

import dbus
import os
import shutil
import subprocess
import tempfile
import time

from PIL import Image
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers import Observer


class FileCreatedEventHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.event_queue = set()
        self.masked = set()

    def mask(self, event):
        if event:
            self.masked.add(event)

    def unmask(self, event):
        self.masked.remove(event)

    def add_event(self, event, event_path):
        if (
            event
            and event_path
            and not event.is_directory
            and event.src_path not in self.masked
        ):
            self.event_queue.add(event_path)

    def on_created(self, event):
        self.add_event(event, event.src_path)

    def on_moved(self, event):
        self.add_event(event, event.dest_path)

    def has_more_events(self):
        return len(self.event_queue) > 0

    def size(self):
        return len(self.event_queue)

    def get_next_event(self):
        if self.has_more_events():
            return self.event_queue.pop()
        return None


class AppImageInstaller:

    def __init__(self):
        self.list_of_image_extensions = [
            ".png",
            ".svg",
            ".xpm",
            ".ico",
            ".jpg",
            ".jpeg",
        ]

    def is_valid_image(self, file_path):
        """Check if the file is a valid image"""
        try:
            with Image.open(file_path) as img:
                return True
        except IOError:
            return False

    def is_appimage(self, file_path):
        """Check if the file is an AppImage"""
        return file_path.endswith(".AppImage")

    def file_exists(self, file_path):
        """Check if the file exists"""
        return os.path.exists(file_path)

    def is_file_executable(self, file_path):
        """Check if the file is executable"""
        return os.access(file_path, os.X_OK)

    def is_file(self, file_path):
        """Check if the path is a file"""
        return os.path.isfile(file_path)

    def find_icon_file(self, directory):
        """Find the icon file in the directory"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                file = file.lower()
                if any(file.endswith(ext) for ext in self.list_of_image_extensions):
                    return os.path.join(root, file)
        return None

    def find_desktop_file(self, directory):
        """Find the desktop file in the directory"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".desktop"):
                    return os.path.join(root, file)
        return None

    def copy_icons(self, squash_dir):
        """Copy icons to the user's icons directory"""
        icon_dir = os.path.join(squash_dir, "usr", "share", "icons")

        if os.path.exists(icon_dir):
            for root, dirs, files in os.walk(icon_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in self.list_of_image_extensions):
                        shutil.copy2(
                            os.path.join(root, file), "/home/seed/.local/share/icons"
                        )
        else:
            print("Icon directory does not exist: " + icon_dir)

        # copy all image files directly in squash_dir
        list_of_files = os.listdir(squash_dir)
        for file in list_of_files:
            if any(file.endswith(ext) for ext in self.list_of_image_extensions):
                print(f"Copying icon file: {file} to /home/seed/.local/share/icons")
                shutil.copy2(
                    os.path.join(squash_dir, file), "/home/seed/.local/share/icons"
                )

    def copy_desktop_file(self, squash_dir, desktop_file, event_file):
        copy_desktop_dest = os.path.join(
            "/home/seed/.local/share/applications", os.path.basename(desktop_file)
        )
        if self.file_exists(copy_desktop_dest):
            print(f"Desktop file already exists: {copy_desktop_dest}")
            # backup the existing desktop file
            shutil.copy2(copy_desktop_dest, copy_desktop_dest + ".bak")

        shutil.copy2(desktop_file, copy_desktop_dest)
        with open(copy_desktop_dest, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("Exec="):
                    lines[i] = "Exec=" + event_file + "\n"
                    break
        with open(copy_desktop_dest, "w") as file:
            file.writelines(lines)

    def send_notification(self, title, message):
        try:
            # Connect to the session bus
            bus = dbus.SessionBus()

            # Get the notification interface
            notify_obj = bus.get_object(
                "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
            )
            notify_interface = dbus.Interface(
                notify_obj, "org.freedesktop.Notifications"
            )

            # Send the notification
            notify_interface.Notify(
                "Wiktor's AppImage Installer",  # App name (empty string for default)
                0,  # Replaces existing notification with ID 0
                "dialog-information",  # Icon (empty string for default)
                title,
                message,
                ["ack", "Got it"],
                {"Ok": "OKAY"},  # Hints (empty dict for no hints)
                0,  # Timeout in milliseconds
            )
            print("Notification sent successfully!")
        except dbus.exceptions.DBusException as e:
            print(f"Failed to send notification: {e}")

    def algorithm(self, event_file):
        # if event is a file and event is an AppImage
        if (
            event_file
            and event_file.strip()
            and self.is_file(event_file)
            and self.is_appimage(event_file)
        ):

            print(f"Processing AppImage: {event_file}")

            # Create a temporary directory and change to it
            temp_dir = tempfile.mkdtemp()

            # copy the AppImage to the temp dir
            shutil.copy2(event_file, temp_dir)
            temp_appimage_file = os.path.join(temp_dir, os.path.basename(event_file))

            # Make it and the original executable
            os.chmod(temp_appimage_file, 0o755)
            os.chmod(event_file, 0o755)

            # Extract the AppImage in the temp dir
            subprocess.run(
                [temp_appimage_file, "--appimage-extract"],
                cwd=temp_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            squash_dir = os.path.join(temp_dir, "squashfs-root")

            # Find all *.desktop and icon files in the temp dir's squashfs-root directory
            desktop_file = self.find_desktop_file(squash_dir)
            # icon_file = find_icon_file(squash_dir)

            print(f"Desktop file: {desktop_file}")
            # print(f"Icon file: {icon_file}")
            if desktop_file:
                # copy desktop file to ~/.local/share/applications replacing Exec= line with the new path
                self.copy_desktop_file(squash_dir, desktop_file, event_file)

            # Copy icons to ~/.local/share/icons
            self.copy_icons(squash_dir)

            # Remove the temporary directory
            shutil.rmtree(temp_dir)

            # Send dbus signal to send a notification to the user
            self.send_notification(
                "AppImage Installed", f"AppImage {event_file} has been installed."
            )

    def main_loop(self):
        sleep_interval = 5  # TODO: move to config
        dir_to_monitor = "/home/seed/apps"  # TODO: move to config

        event_handler = FileCreatedEventHandler()
        observer = Observer()
        observer.schedule(event_handler, dir_to_monitor, recursive=False)
        observer.start()

        try:
            while True:
                while event_handler.has_more_events():
                    event = event_handler.get_next_event()
                    event_handler.mask(event)
                    self.algorithm(event)
                    event_handler.unmask(event)
                time.sleep(sleep_interval)
        finally:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    print("Starting AppImage Installer...")
    app = AppImageInstaller()
    app.main_loop()
