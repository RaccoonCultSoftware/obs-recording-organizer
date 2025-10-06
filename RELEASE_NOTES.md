# Release Notes

## v1.3.0 - Real-Time Split Recording Support (2025-10-06)

### 🎉 Major Features

#### Real-Time Split Recording Tracking
**Automatic tracking and organization of split recordings with zero configuration!**

- **Active monitoring** during recording (checks every 2 seconds)
- **Real-time detection** of new segments as OBS creates them
- **Automatic organization** of ALL segments when recording stops
- **Works with any split size** or time-based splitting

**Before:** Only the last segment was moved, earlier segments were left behind  
**After:** All segments from the entire recording session are moved together

**Example:**
```
Recording starts → Script begins tracking
├─ 11:50:20.mov created (50MB) → Tracked
├─ 11:51:28.mov created (50MB) → Tracked  
└─ 11:52:34.mov created (final) → Tracked

Recording stops → All 3 files moved to organized folder
```

### Technical Changes

- **ADDED:** Timer-based segment monitoring (`check_for_new_segments()`)
- **ADDED:** Event handling for `OBS_FRONTEND_EVENT_RECORDING_STARTING`
- **CHANGED:** Organization strategy from pattern matching to active tracking
- **IMPROVED:** Log output shows segment detection in real-time
- **FIXED:** Split recordings now properly move all segments together

### Log Output Example
```
Recording Organizer: Recording starting, tracking segments...
Recording Organizer: Detected new segment: 2025-10-06 11-50-20.mov
Recording Organizer: Detected new segment: 2025-10-06 11-51-28.mov
Recording Organizer: Recording stopped, processing...
Recording Organizer: Found 3 segment(s) to organize
Recording Organizer: Successfully moved: 2025-10-06 11-50-20.mov
Recording Organizer: Successfully moved: 2025-10-06 11-51-28.mov
Recording Organizer: Successfully moved: 2025-10-06 11-52-34.mov
Recording Organizer: Moved 3/3 file(s) to: Recordings/pycharm
```

---

## v1.2.0 - Initial Split Recording Support (2025-10-06)

### Features

- **ADDED:** Split recording detection via pattern matching
- **ADDED:** `find_split_recordings()` function for segment discovery
- **NOTE:** This approach was superseded by v1.3.0's real-time tracking

---

## v1.1.0 - macOS Support (2025-10-06)

### 🎉 Major Features

#### Full macOS Support
**Recording Organizer now works on macOS!**

- ✅ **macOS Screen Capture** source type detection (`screen_capture`)
- ✅ **Application capture** extracts app names from bundle IDs
  - Example: `com.jetbrains.pycharm` → `pycharm`
- ✅ **Window & Display modes** supported with fallback to source names
- ✅ **Bundle ID parsing** for automatic app name extraction
- ✅ Unix-style directory handling (`mkdir -p`)

### Technical Changes

- **ADDED:** `screen_capture` source type support in detection functions
- **ADDED:** `extract_app_name_from_bundle()` function
- **ADDED:** macOS-specific window title extraction patterns
- **ADDED:** `.app` extension removal in folder name sanitization
- **UPDATED:** Source type list to include "macOS Screen Capture"
- **UPDATED:** Comments to clarify Unix/macOS compatibility

### Setup for macOS Users

For best results with macOS Screen Capture:

1. Open source properties
2. Set **Method** to **"Application"** (not Window or Display)
3. Select the application you're capturing
4. The script will automatically extract the app name for folders

**Alternative:** Rename your Screen Capture source to match what you're recording (e.g., "Blender Project").

### Documentation Updates

- Added macOS Screen Capture setup section
- Updated troubleshooting with macOS-specific guidance
- Added cross-platform compatibility notes
- Updated feature list to include macOS

---

## v1.0.0 - Initial Release

### Features

- **Automatic organization** of recordings after each session
- **Smart window detection** from Window Capture and Game Capture sources
- **Clean folder names** - removes `UnrealWindow:`, `-Win64-Shipping`, `.exe`, etc.
- **Source selection** - Auto-detect or choose specific capture source
- **Duplicate handling** - Auto-increments filenames if conflicts occur
- **Cross-platform** - Windows and Linux support

### Supported Capture Types

- Windows: `window_capture`, `game_capture`
- Linux: `xcomposite_input`

### Technical Implementation

- Event-driven: `OBS_FRONTEND_EVENT_RECORDING_STOPPED`
- Lua-based: No external dependencies
- Scene enumeration for source detection
- Settings persistence via OBS data

---

## Upgrade Instructions

1. **Download** the latest `recording_organizer.lua`
2. In OBS: **Tools** → **Scripts**
3. **Remove** old version (click ➖)
4. **Add** new version (click ➕)
5. **Done!** Settings are preserved

---

## Platform Support Matrix

| Platform | Supported | Capture Types | Notes |
|----------|-----------|---------------|-------|
| Windows  | ✅ | Window Capture, Game Capture | Full support |
| Linux    | ✅ | XComposite | Full support |
| macOS    | ✅ | Screen Capture | Use "Application" mode for best results |

---

## Known Issues

### v1.3.0
No known issues.

### Previous Versions
- **v1.2.0:** Pattern matching failed with OBS timestamp-based split naming (fixed in v1.3.0)
- **v1.1.0:** Initial macOS implementation required script reload

---

## Contributing

Found a bug? Have a feature request? 

- **GitHub:** [RaccoonCultSoftware/recording-organizer](https://github.com/RaccoonCultSoftware/recording-organizer)
- **Issues:** [Submit an issue](https://github.com/RaccoonCultSoftware/recording-organizer/issues)

---

## Credits

**Author:** Strychnine  
**GitHub:** [@rabbitcannon](https://github.com/rabbitcannon)  
**Website:** [RaccoonCult.com](https://raccooncult.com)

**License:** MIT

---

**Made with ❤️ for the OBS community**
