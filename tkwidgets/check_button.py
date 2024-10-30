
# ©2021-2024 Ryo Fujinami.

import tkinter as tk

UNCHECKED = 0
CHECKED = 1
INDETERMINATE = 2


class CheckButton(tk.Canvas):
    """
    Custom check button widget that supports three states: unchecked, checked, and indeterminate.
    It can synchronize with parent and child check buttons, allowing for hierarchical state management.
    
    Attributes:
        color1 (str): Color used for the unchecked or indeterminate state background.
        color2 (str): Background color of the check button.
        width (int): Size of the button in pixels.
        current (int): Current state of the check button (0: unchecked, 1: checked, 2: indeterminate).
        margin (int): Margin around the button.
        binding (bool): Whether the button has key and mouse bindings enabled.
        command (callable): Command to be called when the button is clicked or pressed.
        parent_widget (CheckButton): Reference to the parent check button.
        children_widget (list of CheckButton): List of child check buttons.
        change_command (callable): Command to be executed when the button state changes.
    """

    def __init__(
            self, master=None, /,
            bg="#F0F0F0", width=40, start=False,
            margin=8, binding=True, command=None):

        self.color1 = "white"
        self.color2 = bg
        self.width = width
        self.current = int(start)
        self.margin = margin
        self.binding = binding
        self.command = command

        self.parent_widget: CheckButton = None
        self.children_widget: CheckButton = []
        self.change_command = None

        if master is not None:
            tk.Canvas.__init__(
                self, master, width=width+self.margin*2,
                height=width+self.margin*2, takefocus=self.binding,
                bg=bg, highlightbackground=bg)
        else:
            tk.Canvas.__init__(
                self, width=width+self.margin*2,
                height=width+self.margin*2, takefocus=self.binding,
                bg=bg, highlightbackground=bg)

        # Base64のDataURI
        self.image = tk.PhotoImage(
            data="""
            iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAA
            Af5JREFUeF7tmlGywiAMRXVnLK1LY2c6dMSptUASbiBQ/HnOmxpyDoFi6vNx89fz
            5vyPJWBVwM0NrCVw8wKYexP03r/CBDvnkpU+7RII8N77vcCdc0kJUwqI8Nu27QLC
            35SE6QSc4eMel5IwlYAUfE7CNAJK8CkJUwigwl9JGF4AF/68KQ4toBY+yBhWAAJ+
            WAEo+CEFIOGHE4CGH0qABvwwArTghxCgCW9egDa8aQEt4M0KaAVvUkBL+KIASk8N
            2VRtDZ8VQO2poQT0gE8K4PTUEAJ6wV8K4PbUagX0hP8TUEom112ViCiNdxUTncO3
            H0BNBpUAdbyjBNTYx5i7AG4ytYlwxyv19iXVFz8jElCTkCX4nz2gRWItxuBWw09P
            UDNBzdhc6L894PgPjUQ1YtZAZwVINsXcnmAZnnQUjk9YKcbPdwfr8KQvQ+EZu0TC
            p5JEn839oIEyEZxrig9GpLMYlwU1mdqzBXWc83VFAdI9gZNQL/jiEqi9O1Ak9IRn
            CdCohN7wbAFICRbgRQIQEqzAiwXUSLAEXyVAIsEafLUAjgSL8BABVAnhRNnyhEe5
            BcME5CRYnfkoiHQSpNps3U6n5pW7DirgWAnhfe5HyojkETHgAqKEjwCV+AhwlSWA
            TKxVLPMzpC1iCdA2bD3+qgDrM6Sd36oAbcPW49++At5aYFBfS24sggAAAABJRU5E
            rkJggg=="""
        ).zoom(self.width).subsample(72)
        self.minus = tk.PhotoImage(
            data="""
            iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAA
            AOZJREFUeF7tmEEOgzAMBM3P/DQ/LT+j4tBWFSRIveEZrlyym5k4yhbwb4PnDwuQ
            AHgDKgAHwENQBVQA3oAKwAFwCqiACsAbUAE4AE4BFVABeAMqAAfAKbBUoKr2qno0
            JMf6q2qac/qjQ/j3zq1KuCygU/i7Ek4FjDH2zHw09rPFjzEiM38ynwrouPsrCq4U
            2Ftu/zfUmoCIYBeAVwB/CB6qdKRgdhfwIrQ68TuQ8PdVuPko/MTzPYCy07OcEiAB
            8AZUAA6Aj6IqoALwBlQADoBTQAVUAN6ACsABcAqogArAG1ABOADxAn6KSEGt6UZn
            AAAAAElFTkSuQmCC"""
        ).zoom(self.width).subsample(72)

        self.redraw_check()

        self.bind("<KeyRelease-space>", self.check_press)

        if self.binding is True:
            self.bind("<KeyRelease-space>", self.check_press)
            self.tag_bind("check", "<Enter>", self.check_hand_enter)
            self.tag_bind("check", "<Leave>", self.check_hand_leave)
            self.tag_bind("check", "<ButtonPress-1>", self.check_press)

    def bind_instead_master(self, widget: tk.Widget):
        widget.bind("<KeyRelease-space>", self.check_press)
        widget.bind("<ButtonPress-1>", self.check_press)
        widget.configure(
            cursor="hand2", takefocus=True,
            highlightthickness=2,
            highlightbackground=self.color2)

    def bind_instead_child(self, widget: tk.Widget):
        widget.bind("<ButtonPress-1>", self.check_press)

    def redraw_check(self):
        self.delete("check")
        width = int(round(self.width / 12))
        if self.current == CHECKED:
            self.create_rectangle(
                self.margin, self.margin,
                self.width+self.margin, self.width+self.margin,
                width=width, fill=self.color1, tag="check")
            self.create_image(
                self.width//2+self.margin, self.width//2+self.margin,
                image=self.image, tag="check")
        elif self.current == INDETERMINATE:
            self.create_rectangle(
                self.margin, self.margin,
                self.width+self.margin, self.width+self.margin,
                width=width, fill=self.color1, tag="check")
            self.create_image(
                self.width//2+self.margin, self.width//2+self.margin,
                image=self.minus, tag="check")
        else:
            self.create_rectangle(
                self.margin, self.margin,
                self.width+self.margin, self.width+self.margin,
                width=width, fill=self.color1, tag="check")

    def check_press(self, event):
        self.current = int(not bool(self.current))
        self.redraw_check()
        self.sync_children()
        self.sync_parent()
        if self.change_command is not None:
            self.change_command()
        if self.command is not None:
            self.command()

    def check_hand_enter(self, event):
        self.config(cursor="hand2")

    def check_hand_leave(self, event):
        self.config(cursor="")

    def set_command(self, command):
        self.command = command

    def set_change_command(self, command):
        self.change_command = command

    def set_parent(self, widget):
        self.parent_widget = widget
        self.parent_widget.sync_myself()

    def set_children(self, widget):
        if widget not in self.children_widget:
            self.children_widget.append(widget)
            self.sync_myself()

    def forget_children(self, widget):
        if widget in self.children_widget:
            self.children_widget.remove(widget)
            self.sync_myself()

    def sync_children(self):
        if self.current == UNCHECKED:
            for child in self.children_widget:
                child.set(UNCHECKED)
        elif self.current == CHECKED:
            for child in self.children_widget:
                child.set(CHECKED)

    def sync_parent(self):
        if self.parent_widget is not None:
            self.parent_widget.sync_myself()

    def sync_myself(self):
        unchecked = False
        checked = False
        for child in self.children_widget:
            data = child.get_state()
            if data == UNCHECKED:
                unchecked = True
            elif (data == CHECKED) or (data == INDETERMINATE):
                checked = True
        if checked and not unchecked:
            self.set(CHECKED)
        elif checked and unchecked:
            self.set(INDETERMINATE)
        else:
            self.set(UNCHECKED)

    def set(self, value):
        if int(value) == self.current:
            return
        self.current = int(value)
        self.redraw_check()
        self.sync_children()
        self.sync_parent()
        if self.change_command is not None:
            self.change_command()

    def get(self):
        return bool(self.current)

    def get_state(self):
        return self.current

