import tkinter as tk
from tkinter import LEFT, RIGHT, TRUE, StringVar, filedialog

window = tk.Tk()
window.geometry("500x150")

# canvas = tk.Canvas(window, width=500, height=150)
# canvas.grid(ipadx=10, ipady=15, column=4, row=3)
frame = tk.Frame(window)
frame.pack(padx=15, pady=10)

save_dir = StringVar()

def get_folder_path():
    dir = filedialog.askdirectory(parent=window,initialdir="/",title='Please select a directory')
    # path_label.config(show=dir)
    save_dir.set(dir)

# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()

path_label = tk.Entry(frame, textvariable=save_dir)
path_label.config(state='disabled')
path_label.pack(side=LEFT)
# path_label.grid(columnspan=3, rowspan=1, column=0, row=0)

# Creating a photoimage object to use image
open_folder = tk.PhotoImage(file = r"assets/open-folder.png")
  
# Resizing image to fit on button
open_folder = open_folder.subsample(1, 1)

btn_dir = tk.Button(frame, text="Open Folder", image=open_folder, command=get_folder_path)
btn_dir.pack(side=LEFT)
# btn_dir.grid(column=3, row=0)



window.mainloop()