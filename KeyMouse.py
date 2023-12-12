import keyboard
import pyautogui
import json

macros = []

# Try to open the macro file
def load_macros():
    try:
        with open("macros.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_macros():
    with open("macros.txt", "w") as file:
        json.dump(macros, file)

# Add new macro and create macros.txt file if not found
def add_macro():
    name = input("Enter macro name: ")
    keybind = input("Enter keybind: ")

    # Capture mouse location
    print("Move your mouse cursor to the desired click spot and then press 'spacebar'.")
    while True:
        if keyboard.is_pressed('space'):
            x, y = pyautogui.position()
            print(f"Captured coordinates: X={x}, Y={y}")
            break

    # Test click selected position
    while True:
        action = input("Test click at these coordinates? (y/n): ").strip().lower()
        if action == 'y':
            original_pos = pyautogui.position()  # Capture current cursor position
            pyautogui.click(x, y)  # Perform the test click
            pyautogui.moveTo(original_pos)  # Return cursor to original position
            print("Test click performed.")
        elif action == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    # Validate input
    while True:
        click_type = input("Single click or double click (s/d): ").strip().lower()
        if click_type in ['s', 'd']:
            break
        else:
            print("Invalid input. Please enter 's' for single click or 'd' for double click.")

    macros.append({"name": name, "keybind": keybind, "x": x, "y": y, "click_type": click_type})
    save_macros()

# Delete macro functionality
def delete_macro():
    if not macros:
        print("No macros available to delete.")
        return

    for i, macro in enumerate(macros):
        print(f"{i + 1}: {macro['name']}")

    while True:
        try:
            choice = int(input("Enter the number of the macro to delete (or 0 to cancel): "))
            if 0 <= choice <= len(macros):
                break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if choice == 0:
        return
    else:
        del macros[choice - 1]
        save_macros()
        print("Macro deleted.")

def execute_macro(macro):
    # Save the current mouse position
    current_x, current_y = pyautogui.position()

    # Display macro details
    print(f"Executing Macro: {macro['name']} - Keybind: {macro['keybind']}, Click Type: {'Double Click' if macro['click_type'] == 'd' else 'Single Click'} | Press Ctrl+C to exit.")

    # Move cursor to the specified pos
    pyautogui.moveTo(macro["x"], macro["y"], duration=0.1)

    if macro["click_type"] == "d":
        # Double click
        pyautogui.doubleClick()
    else:
        # Single click
        pyautogui.click()

    # Move cursor back to original pos
    pyautogui.moveTo(current_x, current_y, duration=0.1)

#Start the bot
def start_bot():
    print("Starting bot. Press Ctrl+C to exit.")
    try:
        while True:
            for macro in macros:
                if keyboard.is_pressed(macro["keybind"]):
                    execute_macro(macro)
    except KeyboardInterrupt:
        print("Bot stopped.")

#Main loop
def main():
    global macros
    macros = load_macros()

    print("----------")
    print("Keybind Mouseclick Bot")
    print("--- By: Wangthunder ---")
    print("Follow the prompts to set up your macros. Macros are saved in a file called *macros.txt* in the bot directory.")
    print("----------")
    
    while True:
        print("\nMacros:")
        for i, macro in enumerate(macros):
            print(f"Macro #{i+1}: {macro['name']} - {macro['keybind']}, {macro['x']}/{macro['y']}, {'Double Click' if macro['click_type'] == 'd' else 'Single Click'}")

        choice = input("Add new macro (a), start bot (s), delete macro (d), or exit (e): ")
        if choice == "a":
            add_macro()
        elif choice == "s":
            start_bot()
        elif choice == "d":
            delete_macro()
        elif choice == "e":
            break

if __name__ == "__main__":
    main()
