import os
import pickle
import time
import threading
from pynput import mouse, keyboard
import pyautogui

recordings_folder = 'recordings'
if not os.path.exists(recordings_folder):
    os.makedirs(recordings_folder)

actions = []

# Record mouse actions
def on_click(x, y, button, pressed):
    timestamp = time.time()
    actions.append(('mouse_click', x, y, button, pressed, timestamp))

# Record keyboard actions
def on_press(key):
    timestamp = time.time()
    actions.append(('keyboard_press', key, timestamp))

def on_release(key):
    timestamp = time.time()
    actions.append(('keyboard_release', key, timestamp))

# Save actions to a file
def save_actions(filename):
    with open(os.path.join(recordings_folder, filename), 'wb') as f:
        pickle.dump(actions, f)

# Load actions from a file
def load_actions(filename):
    with open(os.path.join(recordings_folder, filename), 'rb') as f:
        return pickle.load(f)

# Replay actions
def replay_actions(actions):
    start_time = actions[0][-1]
    for action in actions:
        time.sleep(action[-1] - start_time)
        start_time = action[-1]
        if action[0] == 'mouse_click':
            x, y, button, pressed = action[1], action[2], action[3], action[4]
            if pressed:
                pyautogui.mouseDown(x=x, y=y, button=button.name)
            else:
                pyautogui.mouseUp(x=x, y=y, button=button.name)
        elif action[0] in ['keyboard_press', 'keyboard_release']:
            key = action[1]
            if action[0] == 'keyboard_press':
                pyautogui.press(str(key).replace("'", ""))
            else:
                pyautogui.keyUp(str(key).replace("'", ""))

# Record actions
def record():
    actions.clear()
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener.start()
    keyboard_listener.start()
    print("Recording... Press ESC to stop.")
    
    def stop_recording(key):
        if key == keyboard.Key.esc:
            mouse_listener.stop()
            keyboard_listener.stop()
            return False

    with keyboard.Listener(on_press=stop_recording) as listener:
        listener.join()

# Menu-driven interface
def menu():
    while True:
        print("\nMenu:")
        print("1. Record actions")
        print("2. Save actions")
        print("3. Load actions")
        print("4. Replay actions")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            record()
        elif choice == '2':
            filename = input("Enter filename to save: ")
            save_actions(filename)
        elif choice == '3':
            filename = input("Enter filename to load: ")
            global actions
            actions = load_actions(filename)
            print("Actions loaded.")
        elif choice == '4':
            replay_actions(actions)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
