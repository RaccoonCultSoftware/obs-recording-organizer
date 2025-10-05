import obspython as obs
import os
import shutil
from pathlib import Path

# Global variables to store script settings
recordings_base_folder = ""
last_recording_path = ""
selected_source_name = ""  # The capture source to use for naming

# ============================================================================
# OBS Script Callbacks (Required by OBS)
# ============================================================================

def script_description():
    """
    Returns the description shown in OBS when the script is loaded.
    """
    return """<h2>Recording Organizer by Window Name</h2>
    <p>Automatically organizes finished recordings into subdirectories based on 
    the captured window or application name.</p>
    <ul>
        <li>Runs automatically after each recording finishes</li>
        <li>Creates subdirectories named after the captured window/app</li>
        <li>Moves recordings into the appropriate subdirectory</li>
        <li>Select specific capture source or use auto-detect</li>
    </ul>
    <p><b>Note:</b> Ensure your recording output path is set in OBS Settings.</p>"""


def script_properties():
    """
    Defines the properties/settings shown in the OBS Scripts UI.
    """
    props = obs.obs_properties_create()
    
    # Add a folder path property for the base recordings folder
    obs.obs_properties_add_path(
        props,
        "base_folder",
        "Base Recordings Folder",
        obs.OBS_PATH_DIRECTORY,
        "",
        None
    )
    
    # Add informational text for folder path
    obs.obs_properties_add_text(
        props,
        "info_text",
        "Info: Leave empty to use OBS default recording path",
        obs.OBS_TEXT_INFO
    )
    
    # Add dropdown to select which capture source to use
    source_list = obs.obs_properties_add_list(
        props,
        "selected_source",
        "Capture Source for Folder Naming",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    
    # Add "Auto-detect" option (default)
    obs.obs_property_list_add_string(source_list, "Auto-detect (first found)", "")
    
    # Populate the dropdown with available capture sources
    try:
        # Get all sources
        sources = obs.obs_enum_sources()
        
        if sources:
            for source in sources:
                source_id = obs.obs_source_get_id(source)
                
                # Only add window capture and game capture sources
                if source_id in ["window_capture", "game_capture", "xcomposite_input"]:
                    source_name = obs.obs_source_get_name(source)
                    
                    # Determine display name based on source type
                    if source_id == "window_capture":
                        source_type = "Window Capture"
                    elif source_id == "game_capture":
                        source_type = "Game Capture"
                    else:
                        source_type = "XComposite"
                    
                    # Add to dropdown with descriptive name
                    display_name = f"{source_name} ({source_type})"
                    obs.obs_property_list_add_string(source_list, display_name, source_name)
            
            obs.source_list_release(sources)
    except Exception as e:
        print(f"Recording Organizer: Error populating source list: {e}")
    
    # Add informational text for source selection
    obs.obs_properties_add_text(
        props,
        "source_info",
        "Select which Window/Game Capture source to use for naming folders. Auto-detect uses the first capture source found.",
        obs.OBS_TEXT_INFO
    )
    
    return props


def script_update(settings):
    """
    Called when script settings are updated by the user.
    """
    global recordings_base_folder, selected_source_name
    
    # Get the base folder from settings
    folder = obs.obs_data_get_string(settings, "base_folder")
    recordings_base_folder = folder if folder else ""
    
    # Get the selected capture source
    source = obs.obs_data_get_string(settings, "selected_source")
    selected_source_name = source if source else ""
    
    print(f"Recording Organizer: Settings updated - Base folder: '{recordings_base_folder}', Selected source: '{selected_source_name}'")


def script_load(settings):
    """
    Called when the script is loaded. Set up event handlers here.
    """
    # Connect to the recording stopped signal
    obs.obs_frontend_add_event_callback(on_event)
    print("Recording Organizer: Script loaded successfully")


def script_unload():
    """
    Called when the script is unloaded. Clean up here.
    """
    print("Recording Organizer: Script unloaded")


# ============================================================================
# Event Handlers
# ============================================================================

def on_event(event):
    """
    Callback function triggered by OBS frontend events.
    We're specifically interested in OBS_FRONTEND_EVENT_RECORDING_STOPPED.
    """
    global last_recording_path
    
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        print("Recording Organizer: Recording stopped, processing...")
        
        # Get the last recording file path
        last_recording_path = obs.obs_frontend_get_last_recording()
        
        if last_recording_path:
            print(f"Recording Organizer: Found recording at: {last_recording_path}")
            organize_recording(last_recording_path)
        else:
            print("Recording Organizer: Could not retrieve recording path")


# ============================================================================
# Core Functionality
# ============================================================================

def get_active_window_name():
    """
    Attempts to get the name of the captured window or source.
    Returns a cleaned folder-safe name, or "Unknown" if unable to determine.
    """
    # Get the current scene
    current_scene_source = obs.obs_frontend_get_current_scene()
    
    if not current_scene_source:
        return "Unknown"
    
    # Get the scene as an obs_scene_t
    scene = obs.obs_scene_from_source(current_scene_source)
    
    if not scene:
        obs.obs_source_release(current_scene_source)
        return "Unknown"
    
    # Try to find window capture or game capture sources
    # If user selected a specific source, use that; otherwise auto-detect
    if selected_source_name:
        print(f"Recording Organizer: Using selected source: {selected_source_name}")
        window_name = find_specific_capture_source(scene, selected_source_name)
    else:
        print("Recording Organizer: Auto-detecting capture source")
        window_name = find_capture_source_name(scene)
    
    # Release the scene source
    obs.obs_source_release(current_scene_source)
    
    if window_name:
        # Clean the name to be folder-safe
        return sanitize_folder_name(window_name)
    
    return "Unknown"


def find_specific_capture_source(scene, source_name):
    """
    Finds a specific capture source by name and extracts its window title.
    Returns the window title or application name if found.
    """
    class SceneItemData:
        def __init__(self):
            self.window_name = None
    
    data = SceneItemData()
    
    def scene_item_callback(scene, scene_item, param):
        """Callback function that processes each scene item"""
        source = obs.obs_sceneitem_get_source(scene_item)
        
        if not source:
            return True  # Continue iteration
        
        # Check if this is the source we're looking for
        current_source_name = obs.obs_source_get_name(source)
        if current_source_name != source_name:
            return True  # Continue iteration
        
        source_id = obs.obs_source_get_id(source)
        
        # Check if this is a capture source
        if source_id in ["window_capture", "game_capture", "xcomposite_input"]:
            # Get the source settings to extract window information
            settings = obs.obs_source_get_settings(source)
            window_title = extract_window_info_from_settings(source_id, settings, source)
            obs.obs_data_release(settings)
            
            if window_title:
                param.window_name = window_title
                return False  # Stop iteration
        
        return True  # Continue iteration
    
    # Enumerate all scene items
    obs.obs_scene_enum_items(scene, scene_item_callback, data)
    
    return data.window_name


def find_capture_source_name(scene):
    """
    Searches through scene items to find any window/game capture source (auto-detect).
    Returns the window title or application name if found.
    """
    class SceneItemData:
        def __init__(self):
            self.window_name = None
    
    data = SceneItemData()
    
    def scene_item_callback(scene, scene_item, param):
        """Callback function that processes each scene item"""
        source = obs.obs_sceneitem_get_source(scene_item)
        
        if not source:
            return True  # Continue iteration
        
        source_id = obs.obs_source_get_id(source)
        
        # Check if this is a window capture or game capture source
        if source_id in ["window_capture", "game_capture", "xcomposite_input"]:
            # Get the source settings to extract window information
            settings = obs.obs_source_get_settings(source)
            window_title = extract_window_info_from_settings(source_id, settings, source)
            obs.obs_data_release(settings)
            
            if window_title:
                param.window_name = window_title
                return False  # Stop iteration, we found what we need
        
        return True  # Continue iteration
    
    # Enumerate all scene items
    obs.obs_scene_enum_items(scene, scene_item_callback, data)
    
    return data.window_name


def extract_window_info_from_settings(source_id, settings, source):
    """
    Extracts window information from capture source settings.
    Handles different source types (window_capture, game_capture, xcomposite_input).
    """
    window_title = None
    
    if source_id == "window_capture":
        # Windows: window property format is "[executable.exe]: Window Title"
        window_str = obs.obs_data_get_string(settings, "window")
        print(f"Recording Organizer: Window Capture - raw string: '{window_str}'")
        
        if window_str:
            window_title = extract_window_title(window_str)
    
    elif source_id == "game_capture":
        # Game capture: check mode and extract window info
        mode = obs.obs_data_get_int(settings, "mode")
        print(f"Recording Organizer: Game Capture - mode: {mode}")
        
        # Mode 0: Capture any fullscreen application
        # Mode 1: Capture specific window
        # Mode 2: Capture foreground window with hotkey
        
        if mode == 1:  # Specific window mode
            window_str = obs.obs_data_get_string(settings, "window")
            print(f"Recording Organizer: Game Capture - raw string: '{window_str}'")
            
            if window_str:
                window_title = extract_window_title(window_str)
        
        # Fallback to source name if no window string found or in fullscreen mode
        if not window_title:
            source_name = obs.obs_source_get_name(source)
            # Only use source name if user customized it
            if source_name and source_name != "Game Capture":
                window_title = source_name
    
    elif source_id == "xcomposite_input":
        # Linux: capture_window property
        window_str = obs.obs_data_get_string(settings, "capture_window")
        print(f"Recording Organizer: XComposite - raw string: '{window_str}'")
        
        if window_str:
            window_title = extract_window_title(window_str)
    
    if window_title:
        print(f"Recording Organizer: Extracted window title: '{window_title}'")
    
    return window_title


def extract_window_title(window_string):
    """
    Extracts a readable window title from the OBS window identifier string.
    
    OBS window strings often have format like:
    - Windows Window Capture: "[program.exe]: Window Title"
    - Windows Game Capture: "[program.exe]: Window Title"
    - Or just: "Window Title"
    """
    if not window_string:
        return None
    
    # Try to extract title after "]:" pattern (common Windows format)
    if "]:" in window_string:
        parts = window_string.split("]:", 1)
        if len(parts) > 1:
            title = parts[1].strip()
            if title:  # Only return if non-empty
                return title
    
    # Try to extract executable name from "[executable.exe]" if no title after colon
    if window_string.startswith("[") and "]" in window_string:
        exe_part = window_string[1:window_string.index("]")]
        if exe_part:
            # Remove .exe extension and return
            return exe_part.replace(".exe", "").replace(".EXE", "")
    
    # Try to extract from colon separator (simple format)
    if ":" in window_string:
        parts = window_string.split(":", 1)
        if len(parts) > 1:
            title = parts[1].strip()
            if title:
                return title
    
    # Return the whole string if no pattern matched
    return window_string.strip()


def sanitize_folder_name(name):
    """
    Removes or replaces characters that are invalid in folder names.
    """
    # Characters not allowed in Windows folder names
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    
    cleaned = name
    for char in invalid_chars:
        cleaned = cleaned.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    cleaned = cleaned.strip('. ')
    
    # If the name is empty after cleaning, return a default
    if not cleaned:
        return "Unknown"
    
    return cleaned


def organize_recording(recording_path):
    """
    Main function that organizes the recording into a subdirectory.
    
    Steps:
    1. Get the captured window/app name
    2. Determine the base recordings folder
    3. Create a subdirectory with the window name
    4. Move the recording file into that subdirectory
    """
    try:
        # Get the window/app name
        window_name = get_active_window_name()
        print(f"Recording Organizer: Detected window/app: {window_name}")
        
        # Determine the base folder
        if recordings_base_folder:
            base_folder = recordings_base_folder
        else:
            # Use the directory where the recording was saved
            base_folder = os.path.dirname(recording_path)
        
        # Create the subdirectory path
        target_folder = os.path.join(base_folder, window_name)
        
        # Create the directory if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)
        print(f"Recording Organizer: Target folder: {target_folder}")
        
        # Get the filename
        filename = os.path.basename(recording_path)
        target_path = os.path.join(target_folder, filename)
        
        # Handle duplicate filenames
        if os.path.exists(target_path):
            target_path = get_unique_filename(target_path)
        
        # Move the file
        shutil.move(recording_path, target_path)
        print(f"Recording Organizer: Successfully moved recording to: {target_path}")
        
    except Exception as e:
        print(f"Recording Organizer: ERROR - {str(e)}")
        import traceback
        print(f"Recording Organizer: Traceback - {traceback.format_exc()}")


def get_unique_filename(filepath):
    """
    If a file already exists, append a number to make it unique.
    Example: video.mp4 -> video_1.mp4 -> video_2.mp4, etc.
    """
    path = Path(filepath)
    directory = path.parent
    stem = path.stem
    extension = path.suffix
    
    counter = 1
    while True:
        new_path = directory / f"{stem}_{counter}{extension}"
        if not new_path.exists():
            return str(new_path)
        counter += 1
