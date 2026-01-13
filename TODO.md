# TODO

## Completed
- [x] pyproject.toml instead of requirements.txt (poetry?) - *Note: still using setup.py, needs migration*
- [x] build system
- [x] black and flake8 reports

---

## Critical (Blocking Issues)

### Security & Portability
- [ ] **Replace hardcoded `/home/seed/` paths with dynamic user home detection** - App is completely broken for any user other than "seed". Use `os.path.expanduser('~')` or `Path.home()`
- [ ] **Add input validation for configuration values** - Malformed config can crash the app or cause unexpected behavior
- [ ] **Handle subprocess extraction failures** - `--appimage-extract` can fail silently; check return code and handle errors

### Legal & Documentation (Required for Public Release)
- [ ] **Add LICENSE file content** - File exists but is empty (0 bytes). Add MIT license text
- [ ] **Add README.md content** - File exists but is empty. Must include: description, installation, usage, configuration

---

## High Impact (Core Functionality)

### Bugs to Fix
- [ ] **Remove duplicate import** - `from watchdog.observers import Observer` appears twice (lines 12-13)
- [ ] **Remove duplicate extensions in image list** - `.png`, `.svg`, `.xpm`, `.ico` appear twice in `list_of_image_extensions`
- [ ] **Remove unused import** - `FileSystemEvent` imported but never used
- [ ] **Fix or remove unused methods** - `is_valid_image()` and `find_icon_file()` are defined but never called
- [ ] **Fix `unmask()` KeyError** - Can raise KeyError if event not in set; use `discard()` instead of `remove()`
- [ ] **Fix setup.py placeholder URL** - Still shows `https://github.com/yourusername/my_package`
- [ ] **Fix author name typo** - "Wikor Lukasik" should be "Wiktor Lukasik" in setup.py

### Missing Core Features
- [ ] **Add uninstall/removal feature** - Users cannot remove integrated AppImages
- [ ] **Add CLI argument parsing** - No way to configure via command line (use argparse or click)
- [ ] **Validate target directories exist** - Fail gracefully if `~/.local/share/applications` or `~/.local/share/icons` don't exist (see existing TODO item)
- [ ] **Create target directories if missing** - Auto-create icon/application directories with proper permissions

### Packaging & Distribution
- [ ] **Migrate to pyproject.toml** - Modern Python packaging standard; setup.py is deprecated
- [ ] **Add console script entry point** - Define `appimage-integrator` command in package config
- [ ] **Separate dev dependencies** - Move black/flake8 from requirements.txt to dev dependencies
- [ ] **Add installation instructions** - Document pip install, manual install, and distro packages
- [ ] **Publish to PyPI using twine**

---

## Medium Impact (Code Quality & Reliability)

### Error Handling & Logging
- [ ] **Replace print statements with proper logging** - Use Python `logging` module with configurable levels
- [ ] **Add comprehensive error handling** - Wrap file operations, subprocess calls, D-Bus in try/except
- [ ] **Add structured error messages** - Include context (file path, operation) in error messages

### Code Quality
- [ ] **Add type hints** - Improve IDE support and catch bugs early
- [ ] **Write docstrings (PEP 257)** - Document all public methods and classes
- [ ] **Use @staticmethod and @classmethod** - Methods like `is_appimage()`, `file_exists()` don't use self
- [ ] **Rename `algorithm()` method** - Poor name; rename to `process_appimage()` or `integrate_appimage()`
- [ ] **Extract magic strings to constants** - App name "Wiktor's AppImage Installer", paths, etc.

### Configuration
- [ ] **Support XDG directories for icons/applications** - Use `$XDG_DATA_HOME` instead of hardcoded `~/.local/share`
- [ ] **Add configuration validation** - Validate paths exist, intervals are positive integers, etc.
- [ ] **Add ignore patterns config** - Allow users to exclude directories (e.g., `~/.local/share/lutris/**`)

### Testing & CI
- [ ] **Add unit tests** - Test core functions: `is_appimage()`, `find_desktop_file()`, `copy_desktop_file()`
- [ ] **Add integration tests** - Test full workflow with sample AppImages
- [ ] **Add GitHub Actions CI** - Run tests, linting on PR/push
- [ ] **Add test coverage reporting**

---

## Low Impact (Polish & Nice-to-Have)

### Documentation
- [ ] **Add CONTRIBUTING.md** - Guidelines for contributors
- [ ] **Add CHANGELOG.md** - Track version history
- [ ] **Add code comments for complex logic** - Event masking, queue processing

### Development Experience
- [ ] **Populate .gitignore** - Currently empty; add Python patterns (`__pycache__`, `*.pyc`, `.env`, etc.)
- [ ] **Add pre-commit hooks** - Auto-run black, flake8 before commits
- [ ] **Add Makefile or task runner** - Common commands: `make install`, `make test`, `make lint`

### Deployment
- [ ] **Add systemd service file** - Enable running as background service
- [ ] **Add systemd user service installation script**
- [ ] **Add desktop autostart entry** - `~/.config/autostart/appimage-integrator.desktop`

### Metrics & Observability
- [ ] **Add optional metrics/telemetry** - Count integrations, errors (opt-in only)
- [ ] **Add health check endpoint** - For monitoring daemon status

---

## Future Features (Differentiation from Competitors)

### High Value - Unique Features
- [ ] **Version management & rollback** - Keep old versions, one-click rollback
- [ ] **Theme auto-fix** - Auto-detect DE and set `QT_QPA_PLATFORMTHEME` for Qt apps on GTK
- [ ] **Argument preservation** - Store custom Exec= arguments, preserve across re-integration
- [ ] **Electron sandbox fix** - Auto-detect Electron apps, add `--no-sandbox` when needed

### Medium Value
- [ ] **Ignore directory patterns** - Blacklist directories from integration (Lutris, itch.io)
- [ ] **Portable mode toggle** - Enable/disable portable mode per-app with config migration
- [ ] **FUSE version detection** - Warn users if libfuse2 missing on Ubuntu 23.04+
- [ ] **App data location tracking** - Show where AppImage stores config/data

### Lower Value
- [ ] **Trust/security indicators** - Show signed/unsigned status, publisher info
- [ ] **Drag-and-drop integration** - GUI for manual integration
- [ ] **Multiple watch directories** - Monitor more than one directory

---

## Code Review Notes

### Files Reviewed
- `pyappimg/appimage-integrator.py` (284 lines) - Main application logic
- `pyappimg/event.py` - Empty file
- `pyappimg/watcher.py` - Empty file
- `pyappimg/__init__.py` - Empty file
- `setup.py` - Package configuration
- `requirements.txt` - Dependencies

### Summary Statistics
- **Critical issues:** 5
- **High impact issues:** 14
- **Medium impact issues:** 15
- **Low impact issues:** 11
- **Future features:** 11

### Priority for Public Release
1. Fix hardcoded paths (Critical - app broken for others)
2. Add README.md content (Critical - users need docs)
3. Add LICENSE content (Critical - legal requirement)
4. Fix duplicate imports/unused code (High - code quality)
5. Add CLI arguments (High - usability)
6. Add proper logging (Medium - debugging)
7. Add tests (Medium - reliability)
