import tkinter as tk
from tkinter import messagebox
from pyautogui import screenshot
import pygetwindow as gw
import time
import keyboard
import random
from pynput.mouse import Button, Controller

# Initialize mouse controller
mouse = Controller()

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker App")

        self.paused = True
        self.no_pixel_found_duration = 0
        self.sleep_enabled = False
        self.sleep_time = 0.001  # Default sleep time
        self.telegram_window = None

        # Create UI elements
        self.create_ui()

        # Bind keyboard shortcuts
        self.root.bind('<Shift-S>', lambda event: self.start_bot())
        self.root.bind('<Shift-P>', lambda event: self.pause_bot())
        self.root.bind('<Shift-X>', lambda event: self.exit_bot())

        # Initial authentication checks
        self.auth_checks()

    def create_ui(self):
        # Greeting
        greeting = """
  |      |                         |             |   
  __ \   |  |   |  __ `__ \        __ \    _ \   __| 
  |   |  |  |   |  |   |   | ____|  |   |  (   |  |   
  _.__/  _| \__,_| _|  _|  _|       _.__/  \___/  \__| 
        """
        greeting_label = tk.Label(self.root, text=greeting, font=("Courier", 10))
        greeting_label.pack()

        # Author info
        author_info = (
            "Author: Geniousta\n"
            "Contact me on telegram: Geniousta\n"
            "Support Me (TON Wallet Address): UQC1ZJYba20_P_35Hevr_vHj3CztfQePJjCGam6s00xU9h4I\n"
        )
        author_label = tk.Label(self.root, text=author_info, font=("Courier", 10))
        author_label.pack()

        # Buttons and shortcuts
        self.start_button = tk.Button(self.root, text="Start (Shift+S)", command=self.start_bot, bg="grey")
        self.start_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause (Shift+P)", command=self.pause_bot, bg="grey")
        self.pause_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit (Shift+X)", command=self.exit_bot)
        self.exit_button.pack()

        # Sleep settings
        self.sleep_var = tk.BooleanVar()
        self.sleep_check = tk.Checkbutton(self.root, text="Enable sleep", variable=self.sleep_var, command=self.toggle_sleep)
        self.sleep_check.pack()

        self.sleep_time_label = tk.Label(self.root, text="Sleep time (seconds):")
        self.sleep_time_label.pack()

        self.sleep_time_entry = tk.Entry(self.root)
        self.sleep_time_entry.pack()
        self.sleep_time_entry.insert(0, str(self.sleep_time))

        self.save_sleep_time_button = tk.Button(self.root, text="Save Sleep Time", command=self.save_sleep_time)
        self.save_sleep_time_button.pack()

    def auth_checks(self):
        if not self.check_telegram_open():
            if not self.ask_retry_scan():
                self.root.quit()

        if not self.check_blum_bot_open():
            self.root.quit()

    def check_telegram_open(self):
        window_name = "TelegramDesktop"
        self.telegram_window = gw.getWindowsWithTitle(window_name)
        return bool(self.telegram_window)

    def ask_retry_scan(self):
        retry = tk.messagebox.askretrycancel("Error", "TelegramDesktop not found. Please open it and try again.")
        if retry:
            return self.check_telegram_open()
        return False

    def check_blum_bot_open(self):
        response = tk.messagebox.askyesno("Blum Bot", "Is the Blum Bot screen visible in TelegramDesktop?")
        return response

    def toggle_sleep(self):
        self.sleep_enabled = self.sleep_var.get()

    def save_sleep_time(self):
        try:
            self.sleep_time = float(self.sleep_time_entry.get())
            tk.messagebox.showinfo("Success", f"Sleep time set to {self.sleep_time} seconds.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid sleep time. Please enter a valid number.")

    def start_bot(self):
        self.paused = False
        self.update_button_states()
        self.run_bot()

    def pause_bot(self):
        self.paused = True
        self.update_button_states()

    def exit_bot(self):
        self.root.quit()

    def update_button_states(self):
        if self.paused:
            self.start_button.config(bg="green")
            self.pause_button.config(bg="grey")
        else:
            self.start_button.config(bg="grey")
            self.pause_button.config(bg="green")

    def run_bot(self):
        if not self.telegram_window:
            return

        telegram_window = self.telegram_window[0]

        while not self.paused:
            if keyboard.is_pressed('Shift+X'):
                tk.messagebox.showinfo("Exiting", "Exiting the autoclicker. Goodbye!")
                self.root.quit()

            if keyboard.is_pressed('Shift+P'):
                self.pause_bot()
                tk.messagebox.showinfo("Paused", "Bot paused. Press 'Start' or Shift+S to continue.")
                break

            window_rect = (
                telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
            )

            if telegram_window:
                try:
                    telegram_window.activate()
                except:
                    telegram_window.minimize()
                    telegram_window.restore()

            scrn = screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

            width, height = scrn.size
            pixel_found = False

            step = 20
            for x in range(0, width, step):
                for y in range(0, height, step):
                    r, g, b = scrn.getpixel((x, y))
                    if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                        screen_x = window_rect[0] + x
                        screen_y = window_rect[1] + y
                        self.click(screen_x + 4, screen_y)
                        pixel_found = True
                        self.no_pixel_found_duration = 0
                        break

            if not pixel_found:
                self.no_pixel_found_duration += 0.1

            if self.no_pixel_found_duration >= 10:
                self.pause_bot()
                tk.messagebox.showinfo("Auto-paused", "Bot auto-paused... No target pixels found. Press 'Start' or Shift+S to continue.")
                self.no_pixel_found_duration = 0
                break

            if self.sleep_enabled:
                time.sleep(self.sleep_time)
            else:
                time.sleep(0.001)

        if not self.paused:
            self.root.after(100, self.run_bot)

    def click(self, x, y):
        mouse.position = (x, y + random.randint(1, 3))
        mouse.press(Button.left)
        mouse.release(Button.left)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
