
# ©2021-2024 Ryo Fujinami.

import tkinter as tk


class ToggleButton(tk.Canvas):
    """
    A custom ToggleButton widget implemented using Tkinter Canvas.
    
    Parameters:
    master : widget, optional
        The parent widget.
    fg : str, optional
        Foreground color for the toggle button.
    bg1 : str, optional
        Background color when in the 'off' state.
    bg2 : str, optional
        Background color when in the 'on' state.
    radius : int, optional
        Radius of the slider in pixels.
    width : int, optional
        Width of the slider's track in pixels.
    height : int, optional
        Height of the toggle button in pixels.
    start : bool, optional
        Initial state of the button (True for 'on', False for 'off').
    smooth : int, optional
        Defines the smoothness of the sliding animation.
    outline : bool, optional
        If True, draws an outline around the slider.
    margin : int, optional
        Margin around the slider track.
    gray : bool, optional
        If True, adds a gray background track.
    binding : bool, optional
        If True, binds key and mouse events to the toggle button.
    command : callable, optional
        A function to be called when the toggle state changes.
    """
    def __init__(
            self, master=None, /,
            fg="white", bg1="lightgray", bg2="lightgreen",
            radius=16, width=32, height=44, start=False, smooth=12,
            outline=False, margin=8, gray=False, binding=True, command=None):

        self.foreground = fg
        self.background1 = bg1
        self.background2 = bg2
        self.radius = radius
        self.width = width
        self.height = height
        self.current = start
        self.smooth = smooth
        self.outline = "silver" if outline else fg
        self.margin = margin
        self.binding = binding
        self.command = command

        self.cvh = (radius*2 if radius*2 > height else height)+self.margin*2
        self.cvw = self.cvh + width

        if master is not None:
            tk.Canvas.__init__(
                self, master, width=self.cvw, height=self.cvh,
                takefocus=self.binding, highlightbackground=bg1)
        else:
            tk.Canvas.__init__(
                self, width=self.cvw, height=self.cvh,
                takefocus=self.binding, highlightbackground=bg1)

        if gray:
            self.draw_gray()

        self.redraw_background()

        self.position = self.width if self.current else 0
        self.redraw_slider()

        if self.binding is True:
            self.bind("<KeyRelease-space>", self.slider_press)

            self.tag_bind("background", "<Enter>", self.check_hand_enter)
            self.tag_bind("background", "<Leave>", self.check_hand_leave)
            self.tag_bind("background", "<ButtonPress-1>", self.slider_press)

            self.tag_bind("slider", "<Enter>", self.check_hand_enter)
            self.tag_bind("slider", "<Leave>", self.check_hand_leave)
            self.tag_bind("slider", "<ButtonPress-1>", self.slider_press)

    def bind_instead_master(self, widget: tk.Widget):
        widget.bind("<KeyRelease-space>", self.slider_press)
        widget.bind("<ButtonPress-1>", self.slider_press)
        widget.configure(
            cursor="hand2", takefocus=True,
            highlightthickness=2,
            highlightbackground=self.color1)

    def bind_instead_child(self, widget: tk.Widget):
        widget.bind("<ButtonPress-1>", self.slider_press)

    def draw_gray(self):
        self.delete("gray")
        background = "silver"
        width = 2
        if self.radius*2 >= self.height:
            self.create_rectangle(
                self.radius+self.margin,
                self.radius+self.margin-self.height//2-width,
                self.radius+self.width+self.margin,
                self.radius+self.margin+self.height//2+width+1,
                width=0, fill=background, tag="gray")

            self.create_arc(
                self.radius-self.height//2+self.margin-width,
                self.radius-self.height//2+self.margin-width,
                self.radius+self.height//2+self.margin+width,
                self.radius+self.height//2+self.margin+width,
                outline=background, fill=background,
                start=90, extent=180, tag="gray")

            self.create_arc(
                self.radius-self.height//2+self.margin+self.width-width,
                self.radius-self.height//2+self.margin-width,
                self.radius+self.height//2+self.margin+self.width+width,
                self.radius+self.height//2+self.margin+width,
                outline=background, fill=background,
                start=-90, extent=180, tag="gray")
        else:
            self.create_rectangle(
                self.height//2+self.margin, self.margin-width,
                self.height//2+self.width+self.margin,
                self.height+self.margin+width+1,
                width=0, fill="gray", tag="gray")

            self.create_arc(
                self.margin-width, self.margin-width,
                self.height+self.margin+width, self.height+self.margin+width,
                outline="gray", fill="gray",
                start=90, extent=180, tag="gray")

            self.create_arc(
                self.margin+self.width-width, self.margin-width,
                self.height+self.margin+self.width+width,
                self.height+self.margin+width,
                outline="gray", fill="gray",
                start=-90, extent=180, tag="gray")

    def redraw_background(self):
        self.delete("background")
        background = self.background2 if self.current else self.background1
        if self.radius*2 > self.height:
            self.create_rectangle(
                self.radius+self.margin,
                self.radius+self.margin-self.height//2,
                self.radius+self.width+self.margin,
                self.radius+self.margin+self.height//2+1,
                width=0, fill=background, tag="background")

            self.create_arc(
                self.radius-self.height//2+self.margin,
                self.radius-self.height//2+self.margin,
                self.radius+self.height//2+self.margin,
                self.radius+self.height//2+self.margin,
                outline=background, fill=background,
                start=90, extent=180, tag="background")

            self.create_arc(
                self.radius-self.height//2+self.margin+self.width,
                self.radius-self.height//2+self.margin,
                self.radius+self.height//2+self.margin+self.width,
                self.radius+self.height//2+self.margin,
                outline=background, fill=background,
                start=-90, extent=180, tag="background")
        else:
            self.create_rectangle(
                self.height//2+self.margin, self.margin,
                self.height//2+self.width+self.margin,
                self.height+self.margin+1,
                width=0, fill=background, tag="background")

            self.create_arc(
                self.margin, self.margin,
                self.height+self.margin, self.height+self.margin,
                outline=background, fill=background,
                start=90, extent=180, tag="background")

            self.create_arc(
                self.margin+self.width, self.margin,
                self.height+self.margin+self.width, self.height+self.margin,
                outline=background, fill=background,
                start=-90, extent=180, tag="background")

    def redraw_slider(self):
        self.delete("slider")
        if self.radius*2 > self.height:
            self.slider = self.create_oval(
                self.margin+self.position, self.margin,
                self.radius*2+self.margin+self.position,
                self.radius*2+self.margin,
                fill=self.foreground, tag="slider",
                outline=self.outline, width=2)
        else:
            self.slider = self.create_oval(
                self.height//2-self.radius+self.margin+self.position,
                self.height//2-self.radius+self.margin,
                self.height//2+self.radius+self.margin+self.position,
                self.height//2+self.radius+self.margin,
                fill=self.foreground, tag="slider",
                outline=self.outline, width=2)

    def slider_press(self, event):
        self.frompos = self.width if self.current else 0
        self.current = not self.current
        self.topos = self.width if self.current else 0
        self.redraw_background()
        self.move = 0
        self.move_slider()
        if self.command is not None:
            self.command()

    def move_slider(self):
        if self.move >= self.smooth:
            return
        self.move += 1
        self.position = (self.frompos * (
            self.smooth - self.move) + self.topos * self.move) // self.smooth
        self.redraw_slider()
        self.after(10, self.move_slider)

    def check_hand_enter(self, event):
        self.config(cursor="hand2")

    def check_hand_leave(self, event):
        self.config(cursor="")

    def set_command(self, command):
        self.command = command

    def set(self, value):
        if value == self.current:
            return
        self.frompos = self.width if self.current else 0
        self.current = value
        self.topos = self.width if self.current else 0
        self.redraw_background()
        self.move = 0
        self.move_slider()
        if self.command is not None:
            self.command()

    def get(self):
        return self.current

