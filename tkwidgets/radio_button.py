
# ©2021-2024 Ryo Fujinami.

import tkinter as tk
from typing import List


class RadioButton(tk.Canvas):
    """
    A custom radio button implementation using tkinter's Canvas widget.

    Args:
        master (Optional[tk.Widget]): The parent widget.
        bg (str): Background color of the button.
        width (int): The width of the button.
        variable (Optional[RadioVar]): Associated RadioVar for button grouping.
        radius (int): The radius of the inner circle for the selected state.
        line (int): The thickness of the border line.
        margin (int): The margin between the button and the border.
        binding (bool): If True, binds events for keyboard and mouse interactions.
    """
    def __init__(
            self, master=None, /,
            bg="#F0F0F0", width=18, variable=None, radius=4,
            line=2, margin=4, binding=True):

        self.color1 = bg
        self.color2 = "black"
        self.color3 = "white"
        self.width = width
        self.radius = radius
        self.line = line
        self.current = False
        self.variable: RadioVar = variable
        self.margin = margin
        self.binding = binding
        self.button_widget: RadioButton = []

        self.variable.widgets.append(self)

        if master is not None:
            tk.Canvas.__init__(
                self, master, width=width+self.margin*2,
                height=width+self.margin*2, takefocus=self.binding,
                bg=self.color1, highlightbackground=self.color1)
        else:
            tk.Canvas.__init__(
                self, width=width+self.margin*2,
                height=width+self.margin*2, takefocus=self.binding,
                bg=self.color1, highlightbackground=self.color1)

        self.redraw_check()

        if self.binding is True:
            self.bind("<KeyRelease-space>", self.check_press)
            self.tag_bind("radio", "<Enter>", self.check_hand_enter)
            self.tag_bind("radio", "<Leave>", self.check_hand_leave)
            self.tag_bind("radio", "<ButtonPress-1>", self.check_press)

    def bind_instead_master(self, widget: tk.Widget):
        widget.bind("<KeyRelease-space>", self.check_press)
        widget.bind("<ButtonPress-1>", self.check_press)
        widget.configure(
            cursor="hand2", takefocus=True,
            highlightthickness=2,
            highlightbackground=self.color1)

    def bind_instead_child(self, widget: tk.Widget):
        widget.bind("<ButtonPress-1>", self.check_press)

    def redraw_check(self):
        self.delete("radio")
        if self.current:
            self.create_oval(
                self.margin, self.margin,
                self.width+self.margin, self.width+self.margin,
                width=self.line, fill=self.color3, tag="radio")
            self.create_oval(
                self.margin+self.width//2-self.radius,
                self.margin+self.width//2-self.radius,
                self.margin+self.width//2+self.radius,
                self.margin+self.width//2+self.radius,
                fill=self.color2, tag="radio")
        else:
            self.create_oval(
                self.margin, self.margin,
                self.width+self.margin, self.width+self.margin,
                width=self.line, fill=self.color3, tag="radio")

    def check_press(self, event):
        self.variable.set(self)

    def check_hand_enter(self, event):
        self.config(cursor="hand2")

    def check_hand_leave(self, event):
        self.config(cursor="")

    def set_variable(self, widget):
        self.variable = widget
        self.sync_variable()

    def forget_variable(self):
        self.variable = None

    def set(self, value):
        if value == self.current:
            return
        self.current = value
        self.redraw_check()
        if self.variable is not None:
            self.variable.current = self


class RadioVar:
    def __init__(self):
        self.widgets: List[RadioButton] = []
        self.current: RadioButton = None
        self.command = None

    def set(self, widget: RadioButton):
        if widget not in self.widgets:
            raise ValueError(f"Widget {widget} is not registered in this RadioVar.")
        for w in self.widgets:
            w.set(False)
        widget.set(True)
        self.current = widget
        if self.command is not None:
            self.command()

    def get(self):
        return self.current

    def set_command(self, command):
        self.command = command
