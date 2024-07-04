from pyautogui import screenshot
import pygetwindow as gw
import time
import keyboard
import random
from pynput.mouse import Button, Controller

# Initialize mouse controller
mouse = Controller()

# Function to print a greeting message
def display_greeting():
    print("""
  |      |                         |             |   
  __ \   |  |   |  __ `__ \        __ \    _ \   __| 
  |   |  |  |   |  |   |   | ____|  |   |  (   |  |   
  _.__/  _| \__,_| _|  _|  _|       _.__/  \___/  \__| 
    """)

# Display greeting and author info
display_greeting()
print("Author: Geniousta")
print("Contact me on telegram: Geniousta")
print("Support Me (TON Wallet Address): UQC1ZJYba20_P_35Hevr_vHj3CztfQePJjCGam6s00xU9h4I ")
print()

# Authentication Step 1: Warning
print("Note: For the bot to work, you'll need to have TelegramDesktop installed and open on your computer.")
response = input("Enter '1' if you have TelegramDesktop open: ")

if response != '1':
    print("Please make sure TelegramDesktop is installed and open before running the bot.")
    exit()

# Check if TelegramDesktop window is open
window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)
if not check:
    print("[>] | TelegramDesktop window not found! Please open TelegramDesktop and try again.")
    exit()

# Authentication Step 2: Check for Blum Bot screen
response = input("Enter '1' if you have the Blum Bot screen visible in TelegramDesktop: ")

if response != '1':
    print("Please make sure the Blum Bot screen is visible in TelegramDesktop.")
    exit()

# Confirm readiness to start the bot
response = input("Press 'S' to start the autoclicker: ")

if response.lower() != 's':
    print("Autoclicker not started. Exiting.")
    exit()

telegram_window = check[0]
paused = False
no_pixel_found_duration = 0

# Function to click at a specific position
def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

print("Bot started. Press 'P' to pause, 'S' to start again, and 'X' to exit.")

while True:
    # Exit the program when 'X' is pressed
    if keyboard.is_pressed('X'):
        print("Exiting the autoclicker. Goodbye!")
        exit()

    # Toggle pause when 'P' is pressed
    if keyboard.is_pressed('P'):
        paused = True
        print("Bot paused... Press 'S' to continue or 'X' to exit.")
        while True:
            if keyboard.is_pressed('S'):
                paused = False
                print("Bot continue working... Press 'P' to pause again.")
                time.sleep(0.2)
                break
            if keyboard.is_pressed('X'):
                print("Exiting the autoclicker. Goodbye!")
                exit()

    if paused:
        continue

    # Get the window dimensions
    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    # Activate the window
    if telegram_window:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    # Take a screenshot of the window
    scrn = screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False

    # Scan the window for specific pixel colors with reduced step size for accuracy
    step = 20  # Reduce step size to scan more pixels
    for x in range(0, width, step):
        for y in range(0, height, step):
            r, g, b = scrn.getpixel((x, y))
            if (b in range(180, 220)) and (g in range(180, 220)) and (r in range(max(g + 10, 200), 230)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x + 4, screen_y)
                pixel_found = True
                no_pixel_found_duration = 0
                break

    # If no pixel is found, increment the duration counter
    if not pixel_found:
        no_pixel_found_duration += 0.1

    # Auto-pause if no pixel is found for more than 2 seconds
    if no_pixel_found_duration >= 10:
        paused = True
        print("Bot auto-paused... No target pixels found. Press 'S' to continue.")
        no_pixel_found_duration = 0
        while True:
            if keyboard.is_pressed('S'):
                paused = False
                print("Bot continue working... Press 'P' to pause again.")
                time.sleep(0.2)
                break
            if keyboard.is_pressed('X'):
                print("Exiting the autoclicker. Goodbye!")
                exit()

    # time.sleep(0.0001)  # Adjust sleep for CPU usage gives abt 200 Blum points
    # time.sleep(0.001)
