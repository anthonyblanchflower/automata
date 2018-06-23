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

        self.menuVariable_Seed = tkinter.StringVar()
        self.seedList = []
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(sys.argv[0])) + "/data/seeds"):
            for file in files:
                if file.endswith('.json'):
                    self.seedList.append(file)
        self.menu_seed = tkinter.OptionMenu(self, self.menuVariable_Seed, *self.seedList)
        self.menu_seed.grid(column=0, row=0, sticky='EW')

        self.menuVariable_X = tkinter.StringVar()
        self.xList = ['12', '32', '64', '128', '256']
        self.menu_x = tkinter.OptionMenu(self, self.menuVariable_X, *self.xList)
        self.menu_x.grid(column=0, row=3, sticky='EW')

        self.menuVariable_Y = tkinter.StringVar()
        self.yList = ['12', '32', '64', '128', '256']
        self.menu_y = tkinter.OptionMenu(self, self.menuVariable_Y, *self.yList)
        self.menu_y.grid(column=0, row=5, sticky='EW')

        self.menuVariable_Scale = tkinter.StringVar()
        self.scaleList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.menu_scale = tkinter.OptionMenu(self, self.menuVariable_Scale, *self.scaleList)
        self.menu_scale.grid(column=0, row=7, sticky='EW')

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
        self.labelVariable_Seed.set(u" seed file name")

        self.labelVariable_X = tkinter.StringVar()
        label_x = tkinter.Label(self, textvariable=self.labelVariable_X,
                                anchor="w", fg="green", bg="black")
        label_x.grid(column=0, row=4, columnspan=2, sticky='EW')
        self.labelVariable_X.set(u" x axis")

        self.labelVariable_Y = tkinter.StringVar()
        label_y = tkinter.Label(self, textvariable=self.labelVariable_Y,
                                anchor="w", fg="green", bg="black")
        label_y.grid(column=0, row=6, columnspan=2, sticky='EW')
        self.labelVariable_Y.set(u" y axis")

        self.labelVariable_Scale = tkinter.StringVar()
        label_scale = tkinter.Label(self, textvariable=self.labelVariable_Scale,
                                    anchor="w", fg="green", bg="black")
        label_scale.grid(column=0, row=8, columnspan=2, sticky='EW')
        self.labelVariable_Scale.set(u" pixel scale")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())

    def onbuttonclick_seed(self):
        self.labelVariable_Seed.set(self.menuVariable_Seed.get())

    def onbuttonclick_x(self):
        self.labelVariable_X.set(self.menuVariable_X.get())

    def onbuttonclick_y(self):
        self.labelVariable_Y.set(self.menuVariable_Y.get())

    def onbuttonclick_scale(self):
        self.labelVariable_Scale.set(self.menuVariable_Scale.get())

    def onbuttonclick_launch(self):
        self.automataCall = sys.executable + " " + os.path.dirname(os.path.realpath(sys.argv[0])) + "/automata.py -s " \
                        + self.labelVariable_Seed.get() + \
                        " -x " + self.labelVariable_X.get() + \
                        " -y " + self.labelVariable_Y.get() + \
                        " -S " + self.labelVariable_Scale.get()
        subprocess.call(self.automataCall, shell=True)


if __name__ == "__main__":
    app = Launcher(None)
    app.title('automata launcher')
    app.mainloop()
