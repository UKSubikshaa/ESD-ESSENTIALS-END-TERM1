import tkinter as tk
from tkinter import filedialog
import pyautogui
import subprocess
import threading
import time
import platform
import sys
import os

# ============================================================
# 🔧 Optional: Auto-install dependencies
# ============================================================
required = ["pyautogui"]
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# ============================================================
# 🪟 Cross-platform “focus VLC” helper
# ============================================================
def focus_vlc():
    """Bring VLC window to the foreground."""
    try:
        system = platform.system()
        if system == "Linux":  # Raspberry Pi / Ubuntu etc.
            # requires: sudo apt install xdotool
            subprocess.run(
                ["xdotool", "search", "--sync", "--onlyvisible", "--class", "vlc", "windowactivate"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif system == "Windows" or system == "Darwin":
            try:
                import pygetwindow as gw
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pygetwindow"])
                import pygetwindow as gw
            for w in gw.getWindowsWithTitle("VLC"):
                if w.isMinimized:
                    w.restore()
                w.activate()
                break
    except Exception as e:
        print("⚠️ Could not focus VLC:", e)

# ============================================================
# 🎬 Launch VLC with selected file
# ============================================================
def open_file():
    path = filedialog.askopenfilename(
        title="Choose media file",
        filetypes=[
            ("Media files", "*.mp4 *.mp3 *.mkv *.avi *.wav *.flac"),
            ("All files", "*.*"),
        ],
    )
    if path:
        # run VLC in background
        threading.Thread(
            target=lambda: subprocess.Popen(["vlc", "--play-and-exit", path])
        ).start()
        time.sleep(1.5)
        focus_vlc()

# ============================================================
# 🎹 Hotkey sender
# ============================================================
def send_hotkey(*keys):
    focus_vlc()
    time.sleep(0.15)
    pyautogui.hotkey(*keys)
    time.sleep(0.05)

# ============================================================
# 🎛️ Create control buttons
# ============================================================
def make_controls(win):
    controls = [
        ("⏪  -5 s", lambda: send_hotkey("shift", "left")),
        ("⏩  +5 s", lambda: send_hotkey("shift", "right")),
        ("⏮️  -10 s", lambda: send_hotkey("alt", "left")),
        ("⏭️  +10 s", lambda: send_hotkey("alt", "right")),
        ("🎞️  Subtitles", lambda: send_hotkey("shift", "v")),
        ("📸  Snapshot", lambda: send_hotkey("shift", "s")),
        ("⏺️  Record", lambda: send_hotkey("shift", "r")),
        ("🔍  Zoom In", lambda: send_hotkey("z")),
        ("🔎  Zoom Out", lambda: send_hotkey("shift", "z")),
        ("📂  Open File", lambda: send_hotkey("ctrl", "o")),
        ("⚙️  Prefs", lambda: send_hotkey("ctrl", "p")),
        ("⏰  Go to Time", lambda: send_hotkey("ctrl", "t")),
        ("🎧  Audio Menu", lambda: send_hotkey("alt", "a")),
        ("📺  View Menu", lambda: send_hotkey("alt", "i")),
        ("▶️  Playback Menu", lambda: send_hotkey("alt", "l")),
        ("❓  Help Menu", lambda: send_hotkey("alt", "h")),
    ]
    for i, (label, func) in enumerate(controls):
        b = tk.Button(
            win,
            text=label,
            width=14,
            command=func,
            bg="#222",
            fg="white",
            relief="raised",
            font=("DejaVu Sans", 10, "bold"),
        )
        b.grid(row=i // 2 + 1, column=i % 2, padx=4, pady=3)

# ============================================================
# 🖥️ GUI setup
# ============================================================
def main():
    root = tk.Tk()
    root.title("🎮 VLC Floating Controller")
    root.configure(bg="#111")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    tk.Label(
        root,
        text="VLC Floating Controller",
        bg="#111",
        fg="#0f0",
        font=("Courier", 14, "bold"),
    ).grid(row=0, column=0, columnspan=2, pady=5)

    make_controls(root)

    tk.Button(
        root,
        text="🎵 Play Audio / Video",
        command=open_file,
        bg="#0a0",
        fg="white",
        width=30,
        font=("Courier", 11, "bold"),
    ).grid(row=20, column=0, columnspan=2, pady=10)

    root.mainloop()

# ============================================================
# 🚀 Main entry
# ============================================================
if __name__ == "__main__":
    main()

	
D 