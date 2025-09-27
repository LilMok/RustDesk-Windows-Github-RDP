import pywinauto
from pywinauto.application import Application
import time
import pyautogui
import os
import json
import subprocess
import sys

CONFIG_FILE = "config.json"

def setup_environment():
    # Check if venv exists, create if not
    venv_path = os.path.join(os.path.dirname(__file__), "venv")
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("Virtual environment created.")

    # Activate venv and install requirements
    activate_script = os.path.join(venv_path, "Scripts", "activate.bat") if os.name == 'nt' else os.path.join(venv_path, "bin", "activate")
    requirements = ["pywinauto", "pyautogui"]
    
    for req in requirements:
        try:
            subprocess.check_call([os.path.join(venv_path, "Scripts", "pip"), "install", req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}. Please install manually or check your internet connection.")
    print("Requirements installed.")

def load_or_calibrate_coordinates():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        print("Loaded saved relative coordinates.")
        return config['rel_x'], config['rel_y']
    else:
        print("Calibration mode: Ensure the RustDesk 'Admin' window is open and visible.")
        print("If the window title differs, note it for manual adjustment.")
        try:
            print("Attempting to connect using UIA backend...")
            app = Application(backend="uia").connect(title_re=".*Admin.*", timeout=30)
            dlg = app.window(title_re=".*Admin.*")
        except Exception:
            print("Falling back to win32 backend...")
            app = Application(backend="win32").connect(title_re=".*Admin.*", timeout=30)
            dlg = app.window(title_re=".*Admin.*")
        
        if not dlg.exists():
            print("Window not found. Printing all open windows for debugging...")
            from pywinauto.findwindows import find_windows
            windows = find_windows()
            for w in windows:
                print(f"Window title: {pywinauto.findwindows.window_title(w)}")
            raise Exception("Could not find the Admin window. Check the printed window titles and adjust the script if needed.")

        dlg.set_focus()
        print("Position your mouse over the 'Accept' button (hover, do not click yet) and press Enter to capture the position.")
        input()  # Wait for user to press Enter
        
        mouse_x, mouse_y = pyautogui.position()
        win_rect = dlg.rectangle()
        
        rel_x = mouse_x - win_rect.left
        rel_y = mouse_y - win_rect.top
        
        config = {'rel_x': rel_x, 'rel_y': rel_y}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        
        print(f"Relative coordinates saved: ({rel_x}, {rel_y}). Proceeding to auto-click for testing.")
        return rel_x, rel_y

def auto_click_accept():
    try:
        rel_x, rel_y = load_or_calibrate_coordinates()
        
        try:
            print("Attempting to connect using UIA backend...")
            app = Application(backend="uia").connect(title_re=".*Admin.*", timeout=30)
        except Exception:
            print("Falling back to win32 backend...")
            app = Application(backend="win32").connect(title_re=".*Admin.*", timeout=30)
        
        dlg = app.window(title_re=".*Admin.*")
        dlg.set_focus()
        
        if not dlg.is_visible():
            raise Exception("Admin window is not visible")
        
        win_rect = dlg.rectangle()
        abs_x = win_rect.left + rel_x
        abs_y = win_rect.top + rel_y
        
        screenshot_width = 100
        screenshot_height = 40
        screenshot_left = abs_x - (screenshot_width // 2)
        screenshot_top = abs_y - (screenshot_height // 2)
        screenshot = pyautogui.screenshot(region=(screenshot_left, screenshot_top, screenshot_width, screenshot_height))
        screenshot.save(os.path.join(os.path.dirname(__file__), "accept_button_screenshot.png"))
        
        pyautogui.click(abs_x, abs_y)
        
        print("Successfully auto-clicked the Accept button.")
    
    except pywinauto.timings.TimeoutError:
        print("Failed to find the Admin window within the timeout period.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    setup_environment()
    auto_click_accept()
