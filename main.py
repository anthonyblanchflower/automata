import tkinter
import os
import subprocess
import sys


class Launcher(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.configure(bg='black')
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable_Seed = tkinter.StringVar()
        self.entry_seed = tkinter.Entry(self, textvariable=self.entryVariable_Seed, fg="green", bg="black")
        self.entry_seed.grid(column=0, row=0, sticky='EW')
        self.entryVariable_Seed.set(u"Enter seed file name")

        self.entryVariable_X = tkinter.StringVar()
        self.entry_x = tkinter.Entry(self, textvariable=self.entryVariable_X, fg="green", bg="black")
        self.entry_x.grid(column=0, row=3, sticky='EW')
        self.entryVariable_X.set(u"Enter x axis for world")

        self.entryVariable_Y = tkinter.StringVar()
        self.entry_y = tkinter.Entry(self, textvariable=self.entryVariable_Y, fg="green", bg="black")
        self.entry_y.grid(column=0, row=5, sticky='EW')
        self.entryVariable_Y.set(u"Enter y axis for world")

        self.entryVariable_Scale = tkinter.StringVar()
        self.entry_scale = tkinter.Entry(self, textvariable=self.entryVariable_Scale, fg="green", bg="black")
        self.entry_scale.grid(column=0, row=7, sticky='EW')
        self.entryVariable_Scale.set(u"Enter pixel scale for cells")

        button_seed = tkinter.Button(self, text=u"Set Seed  ", fg="black", bg="green",
                                     command=self.onbuttonclick_seed)
        button_seed.grid(column=1, row=0)
        button_x = tkinter.Button(self, text=u"Set X Axis ", fg="black", bg="green",
                                  command=self.onbuttonclick_x)
        button_x.grid(column=1, row=3)
        button_y = tkinter.Button(self, text=u"Set Y Axis ", fg="black", bg="green",
                                  command=self.onbuttonclick_y)
        button_y.grid(column=1, row=5)
        button_scale = tkinter.Button(self, text=u"Set Scale ", fg="black", bg="green",
                                      command=self.onbuttonclick_scale)
        button_scale.grid(column=1, row=7)
        button_launch = tkinter.Button(self, text=u"Start Simulation", fg="black", bg="green",
                                       command=self.onbuttonclick_launch)
        button_launch.grid(column=0, row=9, sticky='EW')

        self.labelVariable_Seed = tkinter.StringVar()
        label_seed = tkinter.Label(self, textvariable=self.labelVariable_Seed,
                                   anchor="w", fg="green", bg="black")
        label_seed.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable_Seed.set(u" seed file name e.g. r_pentomino.json")
        self.labelVariable_X = tkinter.StringVar()
        label_x = tkinter.Label(self, textvariable=self.labelVariable_X,
                                anchor="w", fg="green", bg="black")
        label_x.grid(column=0, row=4, columnspan=2, sticky='EW')
        self.labelVariable_X.set(u" x axis e.g. 64")
        self.labelVariable_Y = tkinter.StringVar()
        label_y = tkinter.Label(self, textvariable=self.labelVariable_Y,
                                anchor="w", fg="green", bg="black")
        label_y.grid(column=0, row=6, columnspan=2, sticky='EW')
        self.labelVariable_Y.set(u" y axis e.g. 64")
        self.labelVariable_Scale = tkinter.StringVar()
        label_scale = tkinter.Label(self, textvariable=self.labelVariable_Scale,
                                    anchor="w", fg="green", bg="black")
        label_scale.grid(column=0, row=8, columnspan=2, sticky='EW')
        self.labelVariable_Scale.set(u" pixel scale e.g. 10")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())

    def onbuttonclick_seed(self):
        self.labelVariable_Seed.set(self.entryVariable_Seed.get())

    def onbuttonclick_x(self):
        self.labelVariable_X.set(self.entryVariable_X.get())

    def onbuttonclick_y(self):
        self.labelVariable_Y.set(self.entryVariable_Y.get())

    def onbuttonclick_scale(self):
        self.labelVariable_Scale.set(self.entryVariable_Scale.get())

    def onbuttonclick_launch(self):
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        automata_call = "python3 " + dir_path + "/automata.py -s " \
                        + self.labelVariable_Seed.get() + \
                        " -x " + self.labelVariable_X.get() + \
                        " -y " + self.labelVariable_Y.get() + \
                        " -S " + self.labelVariable_Scale.get()
        print(automata_call)
        subprocess.call(automata_call, shell=True)


if __name__ == "__main__":
    app = Launcher(None)
    app.title('automata launcher')
    app.mainloop()
