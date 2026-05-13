from tkinter import *
from tkinter import messagebox
from pathlib import Path

root = Tk()
root.title("CRUD File Manager")
root.geometry("400x300")

def create_file():

    folder_name = folder_entry.get()
    file_name = file_entry.get()
    content = content_entry.get("1.0", END)

    folder_path = Path(folder_name)

    if not folder_path.exists():
        folder_path.mkdir()

    file_path = folder_path / file_name

    if file_path.exists():
        messagebox.showinfo("Info", "File already exists")

    else:
        with open(file_path, 'w') as file:
            file.write(content)

        messagebox.showinfo("Success", "File created successfully")



Label(root, text="Folder Name").pack()
folder_entry = Entry(root, width=40)
folder_entry.pack()

Label(root, text="File Name").pack()
file_entry = Entry(root, width=40)
file_entry.pack()

Label(root, text="File Content").pack()
content_entry = Text(root, height=8, width=40)
content_entry.pack()

Button(root, text="Create File", command=create_file).pack(pady=10)

root.mainloop()