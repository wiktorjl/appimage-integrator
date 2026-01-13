# appimage-integrator

A daemon that automatically integrates AppImages into your Linux desktop environment. When you download or move an AppImage into a watched directory, it extracts the desktop entry and icons, registers the application with your desktop, and sends a notification when complete.

## Features

- Monitors a directory for new AppImage files
- Extracts and installs desktop entries to `~/.local/share/applications/`
- Extracts and installs icons to `~/.local/share/icons/`
- Automatically sets executable permissions on AppImages
- Sends desktop notifications on successful integration
- Backs up existing desktop files before overwriting
- Configurable watch directory and polling interval

## Installation

### From source

```bash
git clone https://github.com/wiktorjl/appimage-integrator.git
cd appimage-integrator
pip install -r requirements.txt
```

### Dependencies

- Python 3.6+
- watchdog
- pillow
- dbus-python

On Debian/Ubuntu, you may need to install the D-Bus development libraries first:

```bash
sudo apt install libdbus-1-dev libglib2.0-dev
```

## Usage

### Running

```bash
python pyappimg/appimage-integrator.py
```

The daemon will start monitoring the configured directory (default: `~/apps`) for AppImage files.

### Configuration

Configuration is stored in `~/.config/appimage-integrator/.env`. The file is created automatically on first run with default values.

Available options:

| Option | Default | Description |
|--------|---------|-------------|
| `DIR_TO_MONITOR` | `/home/seed/apps` | Directory to watch for AppImages |
| `SLEEP_INTERVAL` | `5` | Seconds between queue checks |

Edit the `.env` file to change the watch directory:

```bash
DIR_TO_MONITOR=/home/yourusername/Applications
SLEEP_INTERVAL=5
```

### How it works

1. Place or download an AppImage file into the watched directory
2. The daemon detects the new file
3. The AppImage is extracted to a temporary directory
4. Desktop entry is copied to `~/.local/share/applications/` with the correct `Exec=` path
5. Icons are copied to `~/.local/share/icons/`
6. A desktop notification confirms the integration
7. The application appears in your desktop's application menu

## License

MIT
