import tkinter as tk

from .radio_button import RadioButton, RadioVar
from .check_button import CheckButton
from .toggle_button import ToggleButton

import os
if os.name == "nt":
    import ctypes
    ctypes.OleDLL('shcore').SetProcessDpiAwareness(1)

root = tk.Tk()
root.title("TkWidgets")

frame1 = tk.Frame(root)
frame1.pack(padx=80, pady=10, side=tk.TOP)

toggle1 = CheckButton(frame1, width=24, start=2)
toggle1.pack()

label1 = tk.Label(
    frame1, text="ON" if toggle1.get() else "OFF",
    font=("Courier New", 20, "bold"))
label1.pack(pady=(0, 10))

toggle1.set_command(
    lambda: label1.config(text="ON" if toggle1.get() else "OFF"))

frame2 = tk.Frame(root)
frame2.pack(padx=80, pady=0, side=tk.TOP, anchor=tk.N)

var = RadioVar()

radio1 = RadioButton(frame2, variable=var)
radio1.pack()

radio2 = RadioButton(frame2, variable=var)
radio2.pack()

radio3 = RadioButton(frame2, variable=var)
radio3.pack()

label1 = tk.Label(
    frame2, text="None", font=("", 20))
label1.pack(pady=(0, 10))

var.set_command(lambda: label1.config(text=str(var.get())))

frame3 = tk.Frame(root)
frame3.pack(padx=(60, 40), side=tk.LEFT)

toggle1 = ToggleButton(frame3)
toggle1.pack()

label2 = tk.Label(
    frame3, text="ON" if toggle1.get() else "OFF",
    font=("Courier New", 20, "bold"))
label2.pack(pady=(0, 10))

toggle1.set_command(
    lambda: label2.config(text="ON" if toggle1.get() else "OFF"))

frame3 = tk.Frame(root)
frame3.pack(padx=(0, 60), side=tk.LEFT)

toggle3 = ToggleButton(
    frame3, radius=20, width=52, height=12, start=True,
    outline=True, gray=True, bg2="skyblue")
toggle3.pack()

label3 = tk.Label(
    frame3, text="ON" if toggle3.get() else "OFF",
    font=("Courier New", 20, "bold"))
label3.pack(pady=(0, 10))

toggle3.set_command(
    lambda: label3.config(text="ON" if toggle3.get() else "OFF"))

root.mainloop()