import os
import filecmp
import tkinter as tk
from tkinter import ttk, filedialog
import gettext

class FolderComparator:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Folder Comparator"))

        self.folder1_path = tk.StringVar()
        self.folder2_path = tk.StringVar()

        style = ttk.Style()
        style.configure("TButton", padding=5, relief="flat")

        self.selected_language = tk.StringVar(value="English")

        self.folder1_entry = ttk.Entry(root, textvariable=self.folder1_path, font=('Arial', 11))
        self.folder2_entry = ttk.Entry(root, textvariable=self.folder2_path, font=('Arial', 11))

        self.folder1_button = ttk.Button(root, text=_("Select Folder 1"), command=self.select_folder1)
        self.folder2_button = ttk.Button(root, text=_("Select Folder 2"), command=self.select_folder2)

        # Language dropdown
        self.language_label = ttk.Label(root, text=_("Language:"))
        self.language_dropdown = ttk.Combobox(root, textvariable=self.selected_language, values=["English", "Português"])
        self.language_dropdown.bind("<<ComboboxSelected>>", self.change_language)

        self.compare_button = ttk.Button(root, text=_("Compare Folders"), command=self.compare_folders)

        self.result_label = ttk.Label(root, text="", font=('Arial', 12))

        self.language_label.grid(row=0, column=0, padx=10, pady=10)
        self.language_dropdown.grid(row=0, column=1, padx=10, pady=10)
        
        self.folder1_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
        self.folder1_button.grid(row=1, column=2, padx=10, pady=10)

        self.folder2_entry.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
        self.folder2_button.grid(row=2, column=2, padx=10, pady=10)


        self.compare_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.result_label.grid(row=5, column=0, columnspan=3, pady=10)

    def select_folder1(self):
        folder_path = filedialog.askdirectory()
        self.folder1_path.set(folder_path)

    def select_folder2(self):
        folder_path = filedialog.askdirectory()
        self.folder2_path.set(folder_path)

    def show_differences(self, differences):
        new_window = tk.Toplevel(self.root)
        new_window.title(_("Differences"))

        listbox = tk.Listbox(new_window, selectmode=tk.SINGLE, font=('Arial', 11), width=80, height=20)
        listbox.pack(padx=10, pady=10)

        for diff in differences:
            listbox.insert(tk.END, diff)

    def compare_folders(self):
        folder1 = self.folder1_path.get()
        folder2 = self.folder2_path.get()

        if not (folder1 and folder2):
            self.result_label.config(text=_("Please select both folders."))
            return

        # Compare folders
        comparison = filecmp.dircmp(folder1, folder2)
        differences = []

        for file in comparison.diff_files:
            differences.append(_("Different file: {file}").format(file=file))

        for file in comparison.left_only:
            differences.append(_("File only in {folder}: {file}").format(folder=folder1, file=file))

        for file in comparison.right_only:
            differences.append(_("File only in {folder}: {file}").format(folder=folder2, file=file))

        if differences:
            self.show_differences(differences)
        else:
            self.result_label.config(text=_("Folders are identical."))

    def change_language(self, event):
        lang = self.selected_language.get()
        os.environ['LANG'] = lang.lower().replace(" ", "_")
        self.refresh_ui(lang)

    def refresh_ui(self, lang):
        match lang:
            case "Português":
                selected_language = 'pt_BR'
            case "English":
                selected_language = 'en_US'

        translation = gettext.translation("app", localedir="locale", languages=[selected_language])
        translation.install()
        _ = translation.gettext

        # Refresh UI elements
        self.root.title(_("Folder Comparator"))
        self.folder1_button.config(text=_("Select Folder 1"))
        self.folder2_button.config(text=_("Select Folder 2"))
        self.language_label.config(text=_("Language:"))
        self.compare_button.config(text=_("Compare Folders"))
        self.result_label.config(text="")
        

if __name__ == "__main__":
    translation = gettext.translation("app", localedir="locale", languages=['en_US', 'pt_BR'])
    translation.install()
    _ = translation.gettext
    
    root = tk.Tk()
    app = FolderComparator(root)

    root.mainloop()
