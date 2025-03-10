import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from PatternRecategorizer import PatternRecategorizer
from Package import PackageRecategorizer

import customtkinter as ctk

# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("system")
# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):

    WIDTH = 600
    HEIGHT = 245
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
        self.resizable(0, 0)
        self.iconbitmap(r'assets/icon.ico')

        self.path_dir = tk.StringVar()
        self.extract_icon = tk.BooleanVar(value=True)
        self.change_category = tk.BooleanVar(value=True)
        self.overwrite = tk.BooleanVar(value=False)
        self.status_update = tk.StringVar()
        self.progress = 0

        # ================ methods ==================

        def recategorize_dir(path: str, new_category: str,
                             overwrite: bool, extract_icon: bool,
                             change_category: bool):
            self.progress_bar.set(0)
            skipped_files = 0
            completed_files = 0
            files = list(filter(lambda x: os.path.isfile(
                os.path.join(path, x)), os.listdir(path)))
            num_files = len(files)
            recategorizer = PatternRecategorizer(
                new_category, extract_icon, overwrite, change_category)
            start_time = time.perf_counter()
            for file_count, filename in enumerate(files, 1):
                f = os.path.join(path, filename)
                name, extension = os.path.splitext(f)
                # print(f)
                try:
                    if extension.lower() != '.package':
                        print('Skipped file that is not .package')
                        skipped_files += 1
                        continue
                    self.status_update.set(f"Working on {filename}")
                    self.update()
                    # recategorizer.recategorize(f)
                    PackageRecategorizer.recategorize(f, name, recategorizer)
                    completed_files += 1
                    # time.sleep(0.1)
                except Exception as e:
                    print(repr(e))
                    skipped_files += 1
                    continue
                finally:
                    self.progress_bar.set(file_count / num_files)
                    self.update()

            end_time = time.perf_counter()
            time_taken = end_time - start_time
            if completed_files == 0:
                self.status_update.set(
                    f"No pattern .package files found in folder.")
            else:
                if change_category:
                    self.status_update.set(
                        f"Recategorized {completed_files} files in {time_taken:.2f} seconds. "
                        f"Skipped {skipped_files} non-pattern/non-.package files.")
                if extract_icon and not change_category:
                    self.status_update.set(
                        f"Completed extracting ICONs from {completed_files} files in {time_taken:.2f} seconds.")

        def change_category_callback():
            if self.change_category.get():
                self.category_menu.configure(state=tk.NORMAL)
            else:
                self.category_menu.configure(state=tk.DISABLED)

        def extract_icon_callback():
            if self.extract_icon.get():
                self.overwrite_checkbox.configure(state=tk.NORMAL)
            else:
                self.overwrite_checkbox.configure(state=tk.DISABLED)

        def get_folder_path_callback():
            dir = filedialog.askdirectory(
                parent=self, title='Please select a directory')
            self.path_dir.set(dir)

        def run_program():
            path = self.path_dir.get()
            extract_icon = self.extract_icon.get()
            overwrite = self.overwrite.get()
            change_category = self.change_category.get()
            new_category = self.category_menu.get()
            print(
                f"dir:{path}, extract_icon: {extract_icon}, overwrite: {overwrite}, change_category:{change_category}, new_category={new_category}")
            if path == "":
                messagebox.showerror(
                    'Empty Directory', 'Error: You need to choose a directory!')
            elif not os.path.isdir(path):
                messagebox.showerror(
                    'Not a Valid Directory', 'Error: The path is not a valid directory!')
            elif extract_icon == False and change_category == False:
                messagebox.showerror(
                    'Program Error', 'Nothing for me to do: All program options are turned off!\n¯\_(ツ)_/¯')
            else:
                # pass
                recategorize_dir(path, new_category, overwrite,
                                 extract_icon, change_category)

        # ============ create two rows ============
        # configure grid layout (1x2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure((1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        self.row_1 = ctk.CTkFrame(master=self)
        self.row_1.grid(row=0, sticky="nswe", pady=10, padx=15)

        self.row_2 = ctk.CTkFrame(master=self)
        self.row_2.grid(row=1, sticky="nswe", pady=10, padx=15)

        self.row_3 = ctk.CTkFrame(
            master=self, corner_radius=0, width=App.WIDTH)
        self.row_3.grid(row=2)

        # ============ row_1 ============

        self.row_1.columnconfigure(0, weight=9)
        self.row_1.columnconfigure(1, weight=1)
        self.row_1.rowconfigure(0, weight=0)
        self.row_1.rowconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(master=self.row_1, text=self.PATH_LABEL)
        self.path_label.grid(row=0, column=0, sticky=tk.N, columnspan=2)

        self.path_entry = ctk.CTkEntry(
            master=self.row_1,
            state='disabled', textvariable=self.path_dir, border_width=0)
        self.path_entry.grid(row=1, column=0, sticky='EW',
                             padx=(15, 5), pady=10)

        # Creating a photoimage object to use image
        self.open_icon = tk.PhotoImage(file=r"assets/open-folder.png")

        self.path_btn = ctk.CTkButton(
            master=self.row_1,
            text="Browse", text_color="white",
            image=self.open_icon, command=get_folder_path_callback, width=100)
        self.path_btn.grid(row=1, column=1, sticky='EW', padx=(0, 15), pady=10)

        # ============ row_2 ============

        self.row_2.rowconfigure(0, weight=1)
        self.row_2.rowconfigure(1, weight=1)
        self.row_2.columnconfigure((0, 1, 2), weight=3)
        self.row_2.columnconfigure(3, weight=1)

        self.tool_label = ctk.CTkLabel(self.row_2, text=self.TOOL_LABEL)
        self.tool_label.grid(row=0, column=0, sticky=tk.N, columnspan=4)

        self.progress_bar = ctk.CTkProgressBar(self.row_2, height=15)
        self.progress_bar.grid(row=1, column=0, padx=(
            15, 10), sticky='we', columnspan=3, pady=(10, 0))
        self.progress_bar.set(0)

        # Creating a photoimage object to use image
        self.run_icon = tk.PhotoImage(file=r"assets/energy.png")

        self.run_btn = ctk.CTkButton(self.row_2, text="Run", text_color="white",
                                     image=self.run_icon, command=run_program)
        self.run_btn.grid(row=1, column=3, sticky=tk.E,
                          padx=(0, 15), pady=(10, 0))

        self.category_menu = ctk.CTkOptionMenu(
            self.row_2, values=self.CATEGORIES, 
            fg_color=("white", "gray24"), button_color=("gray70", "gray32"),
            button_hover_color=("#6E7174", "#7A848D"))
        self.category_menu.grid(
            row=2, column=0, sticky='we', padx=(15, 10), pady=10)

        self.change_category_checkbox = ctk.CTkCheckBox(
            self.row_2, text="Change category", 
            border_width=1.5, width=16, height=16, corner_radius=5, pady=10, 
            variable=self.change_category, onvalue=True, offvalue=False,
            command=change_category_callback)
        self.change_category_checkbox.grid(row=2, column=1, padx=(0, 20))

        self.extract_icon_checkbox = ctk.CTkCheckBox(
            self.row_2, text="Extract icon",
            border_width=1.5, width=16, height=16, corner_radius=5, pady=10, 
            variable=self.extract_icon, onvalue=True, offvalue=False, 
            command=extract_icon_callback)
        self.extract_icon_checkbox.grid(row=2, column=2)

        self.overwrite_checkbox = ctk.CTkCheckBox(
            self.row_2, text="Overwrite icon with\nsame filename", 
            border_width=1.5, width=16, height=16, corner_radius=5, pady=10, 
            variable=self.overwrite, onvalue=True, offvalue=False)
        self.overwrite_checkbox.grid(row=2, column=3)

        # ============ row_3 ============

        status = ctk.CTkLabel(
            self.row_3, textvariable=self.status_update, width=App.WIDTH, height=20)
        status.grid(row=0, column=0)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
