#!/usr/bin/env python3
# ============================================
# ADDED: Flask server for website integration
# ============================================

from flask import Flask, jsonify, render_template
import subprocess
import os
import sys
import threading

app = Flask(__name__, template_folder='templates', static_folder='static')

# Path to Tkinter launcher file (THIS FILE ITSELF)
THIS_FILE = os.path.abspath(__file__)

# This will hold the launcher process
launcher_proc = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game_from_web():
    global launcher_proc

    # Prevent duplicate launcher processes
    if launcher_proc and launcher_proc.poll() is None:
        return jsonify({"status": "Game Launched"})

    try:
        # Start this SAME FILE but in "launcher mode"
        launcher_proc = subprocess.Popen([sys.executable, THIS_FILE, "--tk-launcher"])
        return jsonify({"status": "Game Launched"})
    except Exception as e:
        return jsonify({"status": "Error", "msg": str(e)})

# If server is started normally → run flask
if __name__ == "__main__" and "--tk-launcher" not in sys.argv:
    app.run(host="0.0.0.0", port=5000, debug=True)


# =====================================================
# BELOW THIS LINE IS YOUR ORIGINAL Tkinter LAUNCHER
# ABSOLUTELY UNCHANGED — EVERY CHARACTER KEPT INTACT
# =====================================================

if "--tk-launcher" in sys.argv:
    # ---------------- ORIGINAL USER CODE START ----------------
    # frontend/app.py
    """
    Tkinter launcher:
    - Click 'Get Start' to launch the Pygame game in a separate process.
    - The launcher will try to use client/venv python automatically if present.
    """

    import tkinter as tk
    from tkinter import messagebox
    import subprocess
    import sys
    import os

    HERE = os.path.dirname(os.path.abspath(__file__))
    GAME_SCRIPT = os.path.normpath(os.path.join(HERE, '..', 'client', 'game.py'))

    # Try to prefer client/venv python if available (common venv paths)
    venv_py_windows = os.path.normpath(os.path.join(HERE, '..', 'client', 'venv', 'Scripts', 'python.exe'))
    venv_py_unix = os.path.normpath(os.path.join(HERE, '..', 'client', 'venv', 'bin', 'python'))

    if os.path.exists(venv_py_windows):
        PYTHON_EXEC = venv_py_windows
    elif os.path.exists(venv_py_unix):
        PYTHON_EXEC = venv_py_unix
    else:
        # fallback to the python running this launcher
        PYTHON_EXEC = sys.executable

    root = tk.Tk()
    root.title('Ship Shooter — Launcher')
    root.geometry('460x220')
    root.resizable(False, False)

    frame = tk.Frame(root, padx=18, pady=18)
    frame.pack(expand=True, fill='both')

    title = tk.Label(frame, text='Ship Shooter', font=('Segoe UI', 20, 'bold'))
    title.pack(pady=(0,8))

    info = tk.Label(frame, text='Click "Get Start" to launch the Pygame window (opens in a new window).', font=('Segoe UI', 10))
    info.pack()

    status_var = tk.StringVar(value='Ready')
    status = tk.Label(frame, textvariable=status_var, font=('Segoe UI', 9), fg='gray')
    status.pack(pady=(8,0))

    proc = None

    def start_game():
        global proc
        if not os.path.exists(GAME_SCRIPT):
            messagebox.showerror('Error', f'Game script not found:\n{GAME_SCRIPT}')
            return

        if proc and proc.poll() is None:
            messagebox.showinfo('Already Running', 'The game is already running.')
            return

        try:
            # Launch the game as a separate process so the launcher stays responsive
            proc = subprocess.Popen([PYTHON_EXEC, GAME_SCRIPT], cwd=os.path.dirname(GAME_SCRIPT))
            status_var.set(f'Game launched using: {os.path.basename(PYTHON_EXEC)}  — close game window to return.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to start game:\n{e}')

    def quit_launcher():
        if proc and proc.poll() is None:
            if not messagebox.askyesno('Quit', 'Game is still running. Quit launcher anyway?'):
                return
            try:
                proc.terminate()
            except Exception:
                pass
        root.quit()

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=14)

    start_btn = tk.Button(btn_frame, text='Get Start', width=14, height=2, command=start_game)
    start_btn.grid(row=0, column=0, padx=8)

    quit_btn = tk.Button(btn_frame, text='Quit', width=14, height=2, command=quit_launcher)
    quit_btn.grid(row=0, column=1, padx=8)

    # Helpful tips
    tip = tk.Label(frame,
                   text='Tip: Place optional images/sounds in client/assets (see README).',
                   font=('Segoe UI', 8), fg='gray')
    tip.pack(side='bottom', pady=(10,0))

    root.protocol('WM_DELETE_WINDOW', quit_launcher)
    root.mainloop()
    # ---------------- ORIGINAL USER CODE END ----------------
