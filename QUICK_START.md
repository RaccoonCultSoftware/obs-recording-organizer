# Quick Start Guide

⚡ **TL;DR:** Use the `.lua` file - it works immediately with no setup!

## Installation (1 minute)

### Lua Version (Recommended - Works Immediately!)

1. **Open OBS Studio** → `Tools` → `Scripts`
2. **Click `+`** (Add Scripts)
3. **Select** `obs_recording_organizer.lua`
4. **Done!** The script is now active (no Python required)

**What you should see:**
- Description: "Recording Organizer by Window Name"
- Properties with dropdowns and settings
- If you see "No properties available" - you loaded the wrong file!

### Python Version

1. **Open OBS Studio** → `Tools` → `Scripts`
2. **Check Python Settings tab** (needs Python 3.6-3.10)
3. **Click `+`** (Add Scripts)
4. **Select** `obs_recording_organizer.py`
5. **Done!** The script is now active

## Configuration

### Basic Setup (Use OBS Default Path)
- No configuration needed!
- Recordings will be organized in your default OBS recording folder

### Custom Recording Path
1. In script settings, click **Browse** next to "Base Recordings Folder"
2. Select your desired folder
3. All organized recordings will go here

### Choosing a Capture Source
**When to use this:** You have multiple Window/Game Capture sources in your scene

1. Find the **"Capture Source for Folder Naming"** dropdown
2. Select:
   - **Auto-detect** (default) - Uses the first capture source found
   - **Your specific source** - Choose from the list

## How It Works

```
Recording stops → Script detects window name → Creates folder → Moves file
```

### Example Workflow

**Before:**
```
📁 Videos/
├── recording-2025-10-05-16-30-45.mp4
├── recording-2025-10-05-17-15-22.mp4
└── recording-2025-10-05-18-00-10.mp4
```

**After (Automatic Organization):**
```
📁 Videos/
├── 📁 Google Chrome/
│   └── recording-2025-10-05-16-30-45.mp4
├── 📁 Visual Studio Code/
│   └── recording-2025-10-05-17-15-22.mp4
└── 📁 League of Legends/
    └── recording-2025-10-05-18-00-10.mp4
```

## Common Issues

### Issue: No properties available (shows blank)
**Lua Version:**
- This shouldn't happen with Lua! Check Script Log for errors
- Make sure you loaded the `.lua` file, not `.py`

**Python Version:**
- **Solution:** Switch to the Lua version (no setup needed!)
- Or install Python 3.6-3.10 and configure in Python Settings tab

### Issue: Dropdown is empty
**Solution:** 
- Add a Window Capture or Game Capture source to your scene
- Click the refresh button (🔄) to reload the script

### Issue: Recordings go to "Unknown" folder
**Solution:** 
- Use the source dropdown to manually select your Window/Game Capture
- Make sure you're using Window Capture, not Display Capture
- For Game Capture, use "Capture specific window" mode

### Issue: Wrong window name detected
**Solution:**
- Use the **"Capture Source for Folder Naming"** dropdown
- Select the specific source you want to use
- Don't rely on auto-detect with multiple sources

### Issue: Script not working / Files not moving
**Solution:**
1. Check **Script Log** button in Scripts window
2. Look for "Recording Organizer:" messages
3. Check file permissions (try running OBS as administrator)
4. Verify base folder path exists

## Tips

✅ **Name your capture sources descriptively** (e.g., "Main Game" instead of "Game Capture")  
✅ **Check the log** after your first recording to verify it's working  
✅ **Use Window Capture or Game Capture** for best results  
❌ **Avoid Display Capture** (can't extract window names)

## Need More Help?

See the full [README.md](README.md) for detailed documentation.
