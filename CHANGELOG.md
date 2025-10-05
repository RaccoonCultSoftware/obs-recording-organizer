# Changelog

## Version 1.0.0 (2025-10-05)

### Initial Release

**Features:**
- ✅ Automatic recording organization by captured window/application name
- ✅ Smart window name detection from Window Capture and Game Capture sources
- ✅ Dropdown to select specific capture source or use auto-detect mode
- ✅ Custom base folder configuration
- ✅ Automatic folder creation
- ✅ Duplicate filename handling
- ✅ Folder name sanitization for file system compatibility
- ✅ Support for Window Capture (Windows)
- ✅ Support for Game Capture (Windows)
- ✅ Support for XComposite (Linux)

**Available Versions:**
- 🎯 **Lua version** - No dependencies, works immediately
- 🐍 **Python version** - Requires Python 3.6-3.10

**Documentation:**
- 📄 Complete README with installation and troubleshooting
- 📄 Quick Start guide for fast setup
- 📄 File guide for beginners

**Example Folder Structure:**
```
📁 Recordings/
├── 📁 Google Chrome/
├── 📁 League of Legends/
├── 📁 Visual Studio Code/
└── 📁 Unknown/
```

---

## Known Issues

- Game Capture in "Capture any fullscreen application" mode may not always detect window names (use "Capture specific window" mode instead)
- Display Capture sources cannot provide window names (use Window Capture instead)
- Python 3.11+ has limited compatibility, Python 3.13+ is not supported (use Lua version)

---

## Future Improvements

Potential features for future versions:
- Date-based subfolder organization (e.g., `2025-10/Chrome/recording.mp4`)
- Custom naming templates
- Multi-language support for folder names
- Integration with streaming platforms
- Automatic cleanup of empty folders

---

## Credits

Created for the OBS Studio community to simplify recording organization.

**License:** Free to use and modify
