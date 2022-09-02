from doctest import master
import tkinter as tk
from pickle import TRUE
from tkinter import filedialog

import customtkinter as ctk

# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("system")
# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("green")


class App(ctk.CTk):

    WIDTH = 500
    HEIGHT = 215
    PATH_LABEL = 'Select folder that contains pattern .packages to recategorize'
    TOOL_LABEL = 'Choose new pattern category and run tool'
    CATEGORIES = ['Fabric',
                  'Weave_Wicker',
                  'Plastic_Rubber',
                  'Tile_Mosaic',
                  'Abstract',
                  'Metal',
                  'Miscellaneous',
                  'Carpet_Rug',
                  'Paint',
                  'Theme',
                  'Wood',
                  'Leather_Fur',
                  'Geometric',
                  'Masonry',
                  'Rock_Stone']

    def __init__(self):
        super().__init__()

        self.title("Sims 3 Pattern Recategorizer")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.resizable(0,0)

        # ================ methods ==================

        def get_folder_path_callback() -> str:
            dir = filedialog.askdirectory(
                parent=self, initialdir="/", title='Please select a directory')
            # path_label.config(show=dir)
            self.path_dir.set(dir)
            print(dir)
            return dir

        # ============ create two rows ============
        # configure grid layout (1x2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.row_1 = ctk.CTkFrame(
            master=self, border_width=1, fg_color=self.fg_color, border_color=('gray85', 'gray25')
        )
        self.row_1.grid(row=0, sticky="nswe", pady=10, padx=15)

        self.row_2 = ctk.CTkFrame(
            master=self, border_width=1, fg_color=self.fg_color, border_color=('gray85', 'gray25')
        )
        self.row_2.grid(row=1, sticky="nswe", pady=10, padx=15)

        # # ============ row_1 ============

        self.row_1.columnconfigure(0, weight=9)
        self.row_1.columnconfigure(1, weight=1)
        self.row_1.rowconfigure(0, weight=0)
        self.row_1.rowconfigure(1, weight=1)

        # self.row_1.grid(rowspan=1, columnspan=4, row=0, column=0)
        # self.row_1.pack(pady=10, padx=15, fill=tk.X, expand=True)

        self.path_label = ctk.CTkLabel(master=self.row_1, text=self.PATH_LABEL)
        self.path_label.grid(row=0, column=0, sticky=tk.N, columnspan=2)
        # # path_label.pack(side=tk.TOP)

        # self.subrow_1 = ctk.CTkFrame(master=self.row_1, fg_color=None)
        # # self.subrow_1.pack(pady=10, padx=15, fill=tk.X, expand=True)

        self.path_dir = tk.StringVar()
        self.path_entry = ctk.CTkEntry(
            master=self.row_1,
            state='disabled', textvariable=self.path_dir, border_width=0)
        self.path_entry.grid(row=1, column=0, sticky='EW',
                             padx=(15, 5), pady=10)
        # # path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Creating a photoimage object to use image
        self.open_icon = tk.PhotoImage(file=r"assets/open-folder.png")

        self.path_btn = ctk.CTkButton(
            master=self.row_1,
            text="Browse",
            image=self.open_icon, command=get_folder_path_callback, width=100)
        self.path_btn.grid(row=1, column=1, sticky='EW', padx=(0, 15), pady=10)
        # # path_btn.pack(side=tk.LEFT, padx=(5, 0))

        # # ============ row_2 ============

        self.row_2.rowconfigure(0, weight=0)
        self.row_2.rowconfigure(1, weight=1)
        self.row_2.columnconfigure(0, weight=1)
        self.row_2.columnconfigure(9, weight=1)

        # self.row_2.rowconfigure(0, weight=1)
        # self.row_2.rowconfigure(3, weight=1)
        # self.row_2.columnconfigure((0, 1), weight=1)
        # self.row_2.columnconfigure(2, weight=1)

        # # self.row_2.pack(pady=10, padx=15, fill=tk.X, expand=True)

        self.tool_label = ctk.CTkLabel(self.row_2, text=self.TOOL_LABEL)
        self.tool_label.grid(row=0, column=0, sticky=tk.N, columnspan=10)
        # path_label.pack(side=tk.TOP)

        self.progress_bar = ctk.CTkProgressBar(self.row_2)
        self.progress_bar.grid(row=1, column=0, padx=(15, 10), sticky='nswe', pady=8)

        # Creating a photoimage object to use image
        self.run_icon = tk.PhotoImage(file=r"assets/energy.png")

        self.run_btn = ctk.CTkButton(self.row_2, text="Run",
                                     image=self.run_icon)
        self.run_btn.grid(row=1, column=9, sticky=tk.E, padx=(0, 15))

        # self.subrow_2 = ctk.CTkFrame(master=self.row_2, fg_color=self.fg_color)
        # # self.subrow_2.grid(column=4, row=2)
        # # self.subrow_2.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

        # self.subrow_column_1 = ctk.CTkFrame(
        #     master=self.subrow_2, fg_color=None)
        # # self.subrow_column_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.category_menu = ctk.CTkComboBox(
            self.row_2, values=self.CATEGORIES, border_width=1)
        self.category_menu.grid(
            row=2, column=0, columnspan=2, sticky='we', padx=(15, 10), pady=10)
        # # category_menu.pack(fill=tk.X)

        self.extract_icon_checkbox = ctk.CTkCheckBox(
            self.row_2, text="Extract icon", border_width=1.5, width=16, height=16, corner_radius=5, pady=10)
        self.extract_icon_checkbox.grid(row=2, column=8)

        self.change_category_checkbox = ctk.CTkCheckBox(
            self.row_2, text="Change category", border_width=1.5, width=16, height=16, corner_radius=5, pady=10)
        self.change_category_checkbox.grid(row=2, column=9)

        # run_btn.pack(side=tk.RIGHT)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
