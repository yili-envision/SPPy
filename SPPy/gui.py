import tkinter
from tkinter import ttk
import os
import sys
import glob

import SPPy
from SPPy.cycler import discharge


class SPPyApp(tkinter.Tk):
    """
    This class outlines the main dashboard.
    """
    heading_style = ('Helvetica', 10, 'bold')

    def __init__(self):
        super().__init__()
        self.title('SPPy')

        # widgets
        self.UserInputFrame = UserInput(self)

        # main loop
        self.mainloop()

class UserInput(ttk.Frame):
    possible_cycler_types = [file_.split('\\')[1].split('.')[0] for file_ in glob.glob('cycler/*.py')] # based on
    # files in the cycler folder
    possible_cycler_types2 = sys.modules[discharge.__name__]

    def __init__(self, parent):
        super().__init__(parent)

        # Instance variables
        self.var_cycler_type = tkinter.StringVar()
        self.var_cycler_type2 = tkinter.StringVar()

        # widgets
        self.create_cycler_frame()

        # main loop
        self.grid(row=0, column=0)

    def create_cycler_frame(self):
        ttk.Label(self, text="Cycler", font=SPPyApp.heading_style).grid(row=0, column=0)
        combox_cycler1 = ttk.Combobox(self, textvariable=self.var_cycler_type)
        combox_cycler1['values'] = UserInput.possible_cycler_types
        combox_cycler2 = ttk.Combobox(self, textvariable=self.var_cycler_type2)
        combox_cycler2['values'] = UserInput.possible_cycler_types2

        # grid placements
        combox_cycler1.grid(row=1, column=0)
        combox_cycler2.grid(row=2, column=0)

if __name__ == '__main__':
    SPPyApp()