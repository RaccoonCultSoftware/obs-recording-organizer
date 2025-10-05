# OBS Recording Organizer

Automatically organizes your OBS Studio recordings into subdirectories based on the captured window or application name.

**Available in both Lua and Python versions** - Lua version recommended for ease of use (no external dependencies).

---

## 🚀 Quick Start (30 seconds)

1. Download `obs_recording_organizer.lua`
2. Open OBS → `Tools` → `Scripts` → Click `+`
3. Select the `.lua` file
4. Done! Recordings will now be organized automatically.

See [QUICK_START.md](QUICK_START.md) for details.

---

## Features

- **Automatic Organization**: Runs automatically after each recording finishes
- **Smart Naming**: Detects the captured window/application name and creates appropriately named folders
- **Source Selection**: Choose a specific Window/Game Capture source or use auto-detect mode
- **No Manual Work**: Recordings are moved into the correct subdirectory without any user intervention
- **Handles Edge Cases**: Creates directories if they don't exist, handles duplicate filenames, and sanitizes folder names
- **Multi-Source Support**: Works with Window Capture, Game Capture, and XComposite (Linux)

## Which Version Should I Use?

| Feature | Lua Version | Python Version |
|---------|------------|----------------|
| **Setup Required** | ✅ None | ❌ Requires Python 3.6-3.10 |
| **Works Immediately** | ✅ Yes | ❌ May need configuration |
| **Cross-Platform** | ✅ Yes | ⚠️ Version dependent |
| **Performance** | ✅ Fast | ✅ Fast |
| **Functionality** | ✅ Full | ✅ Full |

**Recommendation:** Use the **Lua version** unless you specifically need Python for other customizations.

## Files in This Project

- 📄 **`obs_recording_organizer.lua`** ⭐ - **USE THIS FILE** - Lua version (recommended)
- 📄 `obs_recording_organizer.py` - Python version (requires Python 3.6-3.10)
- 📄 `README.md` - Full documentation (this file)
- 📄 `QUICK_START.md` - Quick installation guide
- 📄 `FILES.md` - File guide for beginners

**You only need ONE script file!** Choose either `.lua` (recommended) or `.py`

## Installation

### Option 1: Lua Version (Recommended - No Setup Required)

1. **Open OBS Studio**

2. **Navigate to Scripts**:
   - Click `Tools` → `Scripts`

3. **Add the Script**:
   - Click the `+` button (Add Scripts)
   - Browse to `obs_recording_organizer.lua`
   - Select it and click `Open`

4. **Done!** - Lua scripts work immediately with no additional setup

### Option 2: Python Version (Requires Python 3.6-3.10)

1. **Open OBS Studio**

2. **Navigate to Scripts**:
   - Click `Tools` → `Scripts`

3. **Check Python Settings**:
   - Click the `Python Settings` tab
   - Ensure a valid Python installation path is set (Python 3.6-3.10)

4. **Add the Script**:
   - Click the `+` button (Add Scripts)
   - Browse to `obs_recording_organizer.py`
   - Select it and click `Open`

### Configuration (Both Versions)

Once the script is loaded, you should see:
- **Description** panel showing "Recording Organizer by Window Name"
- **Properties** panel with configuration options

Configure these settings in the script properties:

- **Base Recordings Folder**: Set a custom folder for recordings (leave empty to use OBS default)
- **Capture Source for Folder Naming**: Select which capture source to use:
  - **Auto-detect (first found)**: Automatically uses the first Window/Game Capture found in your scene
  - **Specific Source**: Choose a specific capture source from the dropdown (your Window/Game Capture sources will appear here)

### Verifying It's Working

1. **Check the Script Log**: Click **"Script Log"** button in the Scripts window
2. **Look for**: `"Recording Organizer: Script loaded successfully"`
3. **Test with a recording**:
   - Make a short test recording
   - Stop the recording
   - Check the log for: `"Recording Organizer: Recording stopped, processing..."`
   - Your recording should now be in a subdirectory named after your captured window

## How It Works

### Detection Process

1. When a recording stops, the script is triggered
2. It examines your current scene for capture sources (Window Capture, Game Capture)
3. It extracts the window or application name from the capture source
4. It creates a subdirectory named after that window/app
5. The recording file is moved into that subdirectory

### Example

If you're recording:
- **Google Chrome**: Recordings go to `[Base Folder]/Google Chrome/`
- **League of Legends**: Recordings go to `[Base Folder]/League of Legends/`
- **Visual Studio Code**: Recordings go to `[Base Folder]/Visual Studio Code/`

### Folder Structure

```
📁 Recordings/
├── 📁 Google Chrome/
│   ├── 2025-10-05 16-30-45.mp4
│   └── 2025-10-05 17-15-22.mp4
├── 📁 League of Legends/
│   ├── 2025-10-05 18-00-10.mp4
│   └── 2025-10-05 19-45-30.mp4
└── 📁 Unknown/
    └── 2025-10-05 20-00-00.mp4
```

## Source Selection

### Why Use Source Selection?

If your scene contains multiple Window Capture or Game Capture sources, you may want to control which one is used for naming the recording folders.

### How to Select a Source

1. Open the script settings in OBS (`Tools` → `Scripts`)
2. Select your script from the list
3. Find the **"Capture Source for Folder Naming"** dropdown
4. Choose from:
   - **Auto-detect (first found)**: Default behavior, uses the first capture source it finds
   - **Your capture sources**: All Window/Game Capture sources in your OBS will appear here

### Examples

**Scenario 1: Recording multiple games**
- You have both "Main Game" (Game Capture) and "Discord" (Window Capture) in your scene
- Select "Main Game (Game Capture)" to name folders after the game, not Discord

**Scenario 2: Streaming with webcam overlay**
- You have "Gameplay" (Game Capture) and "Webcam" (Video Capture Device)
- Select "Gameplay (Game Capture)" to organize by game name

**Scenario 3: Multi-window recording**
- You have "Browser 1" and "Browser 2" (both Window Capture)
- Select whichever window you want to use for folder names

### Window Name Detection

The script automatically extracts readable names from OBS capture strings:
- **`[chrome.exe]: Google Chrome`** → Folder: `Google Chrome`
- **`[League of Legends.exe]: League Client`** → Folder: `League Client`
- **`[notepad.exe]`** → Folder: `notepad` (when no window title is available)

## Supported Capture Types

- **Window Capture** (Windows)
- **Game Capture** (Windows)
- **XComposite** (Linux)

If no capture source is detected, recordings will be placed in an "Unknown" folder.

## Requirements

### Lua Version
- **OBS Studio** (version 27.0 or higher recommended)
- No additional requirements! Lua is built into OBS

### Python Version
- **OBS Studio** (version 27.0 or higher recommended)
- **Python 3.6-3.10** (OBS must be configured with Python scripting support)
  - Windows: OBS typically includes Python, or install separately
  - Linux: May need to install `python3` and configure OBS to use it
  - macOS: May need to install Python 3.x

## Troubleshooting

### No Properties Available / Script Not Loading

**Lua Version:**
- Lua should work immediately with no configuration
- If the script doesn't load, check **Script Log** for errors
- Make sure you selected the `.lua` file, not `.py`

**Python Version:**
- **No Properties Available** means Python isn't configured or wrong version
- Go to `Tools` → `Scripts` → `Python Settings` tab
- Ensure Python installation path is correctly set (Python 3.6-3.10 required)
- **Python 3.13+ is NOT compatible with OBS**
- **Solution**: Use the Lua version instead (no Python required)

### Dropdown is Empty (No Capture Sources Listed)

This happens when you don't have any Window/Game Capture sources in your OBS:
- **Add a capture source**: Add a Window Capture or Game Capture to any scene
- **Reload the script**: Click the refresh button (🔄) in the Scripts window
- The dropdown should now show your capture sources

### Recordings Aren't Being Moved

1. **Check the Script Log**: 
   - Click **"Script Log"** button in Scripts window
   - Or go to `Help` → `Log Files` → `View Current Log`
2. **Look for messages** starting with "Recording Organizer:"
3. **Common issues**:
   - File permissions in the recordings folder (run OBS as administrator if needed)
   - Recording is still being finalized when the script tries to move it
   - Antivirus blocking file moves
   - Base folder path doesn't exist or is invalid

### Recordings Go to "Unknown" Folder

This happens when the script can't detect a window/game capture source.

**Possible causes:**
- You're using **Display Capture** instead of Window Capture (Display Capture doesn't provide window names)
- The capture source is nested inside a group or scene
- The source type isn't recognized
- Auto-detect is finding the wrong source
- The window string from OBS is empty or invalid

**Solutions:**
1. Make sure you're using **Window Capture** or **Game Capture** as your source
2. Use the **"Capture Source for Folder Naming"** dropdown to manually select your capture source
3. Check the Script Log to see what window string is being detected
4. For Game Capture in "Capture any fullscreen application" mode, try switching to "Capture specific window"

### Wrong Window Name Detected

If the wrong window name is being used for folders:
- Use the **"Capture Source for Folder Naming"** dropdown
- Select the specific capture source you want to use
- Don't rely on auto-detect if you have multiple capture sources

### Characters in Folder Names Look Strange

The script automatically sanitizes folder names to remove invalid characters (`< > : " / \ | ? *`). These are replaced with underscores. This is normal and ensures compatibility with all file systems.

## Customization

You can modify the script behavior by editing the script file:

### Lua Version (`obs_recording_organizer.lua`)
- **Change sanitization rules**: Edit the `sanitize_folder_name()` function
- **Support additional source types**: Add them to the `find_capture_source_name()` function
- **Change folder structure**: Modify the `organize_recording()` function

### Python Version (`obs_recording_organizer.py`)
- **Change sanitization rules**: Edit the `sanitize_folder_name()` function
- **Support additional source types**: Add them to the `find_capture_source_name()` function
- **Change folder structure**: Modify the `organize_recording()` function

## Script Output (Console)

The script prints informational messages to the OBS log:

```
Recording Organizer: Script loaded successfully
Recording Organizer: Recording stopped, processing...
Recording Organizer: Found recording at: C:\Videos\2025-10-05_16-30-45.mp4
Recording Organizer: Detected window/app: Google Chrome
Recording Organizer: Target folder: C:\Videos\Google Chrome
Recording Organizer: Successfully moved recording to: C:\Videos\Google Chrome\2025-10-05_16-30-45.mp4
```

## License

This script is provided as-is for use with OBS Studio. Feel free to modify and distribute.

## Support

If you encounter issues:
1. Check the OBS log for error messages
2. Ensure your OBS version is up to date
3. Verify Python scripting is properly configured
4. Test with a simple Window Capture source first

---

**Tip**: For best results, name your capture sources descriptively in OBS (e.g., "Game - Minecraft" instead of just "Game Capture").
