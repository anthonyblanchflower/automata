import tkinter as tk
import os
import subprocess


def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry


def enter(seed, xaxis, yaxis, scale):
    print (seed)
    print (xaxis)
    print (yaxis)
    print (scale)
    dir_path = os.getcwd()
    automata_call = dir_path + "/automata.py -s " \
                    + seed + " -x " + str(xaxis) + " -y " + str(yaxis) + " -S " + str(scale)
    subprocess.Popen(automata_call)


root = tk.Tk()
root.geometry('300x220')
root.title('Enter automata parameters')
# frame for window margin
parent = tk.Frame(root, padx=10, pady=10)
parent.pack(fill=tk.BOTH, expand=True)
# entrys with not shown text
seed_json = make_entry(parent, "Seed JSON:", 16)
x_axis = make_entry(parent, "World Cell Width:", 16)
y_axis = make_entry(parent, "World Cell Height:", 16)
display_scale = make_entry(parent, "Pixel Scale:", 16)
# button to attempt to login
b = tk.Button(parent, borderwidth=4, text="Start Simulation", width=20, pady=8,
              command=enter(seed_json, x_axis, y_axis, display_scale))
b.pack(side=tk.BOTTOM)
display_scale.bind('<Return>', enter(seed_json, x_axis, y_axis, display_scale))
seed_json.focus_set()
parent.mainloop()
