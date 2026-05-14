import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from pathlib import Path
import os

# ─── Helpers ───────────────────────────────────────────────────────────────────
BG       = "#0e0e0e"
FG       = "#f0f0f0"
ACCENT   = "#e94560"
CARD     = "#1a1a1a"
BORDER   = "#2a2a2a"
SUCCESS  = "#4ecdc4"
WARN     = "#f5a623"
FONT     = ("Segoe UI", 11)
FONT_B   = ("Segoe UI", 11, "bold")
MONO     = ("Consolas", 10)

def get_all_items():
    p = Path('')
    return sorted(p.rglob('*'))

def refresh_tree(listbox):
    listbox.delete(0, tk.END)
    items = get_all_items()
    if not items:
        listbox.insert(tk.END, "  📭 No files or folders found")
    for item in items:
        icon = "📁" if item.is_dir() else "📄"
        listbox.insert(tk.END, f"  {icon} {item}")

# ─── Main Window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("🗂️ File Manager — CRUD")
root.geometry("950x650")
root.configure(bg=BG)
root.resizable(True, True)

# ─── Title Bar ─────────────────────────────────────────────────────────────────
title_frame = tk.Frame(root, bg="#1a1a2e", pady=14)
title_frame.pack(fill="x")
tk.Label(title_frame, text="🗂️  File Manager", font=("Segoe UI", 20, "bold"),
         bg="#1a1a2e", fg=ACCENT).pack(side="left", padx=24)
tk.Label(title_frame, text="CRUD operations · files & folders · powered by pathlib",
         font=("Consolas", 9), bg="#1a1a2e", fg="#a0a0b0").pack(side="left", padx=4)

# ─── Main Layout ───────────────────────────────────────────────────────────────
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=16, pady=12)

# Left panel — file explorer
left = tk.Frame(main, bg=CARD, bd=0, relief="flat", width=220)
left.pack(side="left", fill="y", padx=(0, 12))
left.pack_propagate(False)

tk.Label(left, text="EXPLORER", font=("Consolas", 8), bg=CARD,
         fg=ACCENT, pady=8).pack(fill="x", padx=10)

explorer = tk.Listbox(left, bg=CARD, fg="#c8c8d8", font=MONO,
                      selectbackground=ACCENT, selectforeground="white",
                      bd=0, highlightthickness=0, activestyle="none")
explorer.pack(fill="both", expand=True, padx=4, pady=(0, 4))

refresh_btn = tk.Button(left, text="⟳ Refresh", font=FONT,
                        bg=ACCENT, fg="white", bd=0, pady=6, cursor="hand2",
                        command=lambda: refresh_tree(explorer))
refresh_btn.pack(fill="x", padx=6, pady=6)

# Right panel — operations
right = tk.Frame(main, bg=BG)
right.pack(side="left", fill="both", expand=True)

# ─── Output Box ────────────────────────────────────────────────────────────────
out_frame = tk.Frame(right, bg=CARD, bd=1, relief="flat")
out_frame.pack(fill="x", pady=(0, 10))
tk.Label(out_frame, text="OUTPUT", font=("Consolas", 8),
         bg=CARD, fg=ACCENT, pady=6, padx=10).pack(anchor="w")
output = scrolledtext.ScrolledText(out_frame, height=6, bg="#111", fg=SUCCESS,
                                   font=MONO, bd=0, state="disabled",
                                   insertbackground=FG)
output.pack(fill="x", padx=8, pady=(0, 8))

def log(msg, color=SUCCESS):
    output.configure(state="normal")
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)
    output.configure(state="disabled")

def clear_log():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    output.configure(state="disabled")

# ─── Input Helpers ─────────────────────────────────────────────────────────────
def ask(prompt):
    return simpledialog.askstring("Input", prompt, parent=root)

def confirm(msg):
    return messagebox.askyesno("Confirm", msg)

# ─── CRUD Functions ─────────────────────────────────────────────────────────────
def create_file():
    clear_log()
    name = ask("Enter file name (e.g. notes.txt):")
    if not name: return
    p = Path(name)
    if p.exists():
        log("⚠️  File already exists!", WARN)
    else:
        content = ask("Enter file content:") or ""
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            log(f"✅ '{name}' created successfully!")
            refresh_tree(explorer)
        except Exception as e:
            log(f"❌ Error: {e}", ACCENT)

def read_file():
    clear_log()
    name = ask("Enter file name to read:")
    if not name: return
    p = Path(name)
    if p.exists():
        try:
            content = p.read_text()
            log(f"📄 Content of '{name}':\n{'-'*40}")
            log(content if content else "(empty file)")
        except Exception as e:
            log(f"❌ Error: {e}", ACCENT)
    else:
        log("❌ File not found!", ACCENT)

def update_file():
    clear_log()
    name = ask("Enter file name to update:")
    if not name: return
    p = Path(name)
    if not p.exists():
        log("❌ File not found!", ACCENT)
        return
    mode = messagebox.askquestion("Update Mode",
                                  "Click YES to Overwrite, NO to Append")
    content = ask("Enter new content:") or ""
    try:
        m = 'w' if mode == 'yes' else 'a'
        with open(name, m) as f:
            f.write(content)
        action = "Overwritten" if m == 'w' else "Appended"
        log(f"✅ '{name}' updated ({action})!")
    except Exception as e:
        log(f"❌ Error: {e}", ACCENT)

def delete_file():
    clear_log()
    name = ask("Enter file name to delete:")
    if not name: return
    p = Path(name)
    if p.exists():
        if confirm(f"Permanently delete '{name}'?"):
            try:
                os.remove(p)
                log(f"🗑️  '{name}' deleted.")
                refresh_tree(explorer)
            except Exception as e:
                log(f"❌ Error: {e}", ACCENT)
    else:
        log("❌ File not found!", ACCENT)

def rename_file():
    clear_log()
    name = ask("Enter current file name:")
    if not name: return
    p = Path(name)
    if p.exists():
        new_name = ask("Enter new file name:")
        if not new_name: return
        try:
            p.rename(new_name)
            log(f"✅ Renamed '{name}' → '{new_name}'!")
            refresh_tree(explorer)
        except Exception as e:
            log(f"❌ Error: {e}", ACCENT)
    else:
        log("❌ File not found!", ACCENT)

def create_folder():
    clear_log()
    name = ask("Enter folder name:")
    if not name: return
    p = Path(name)
    if p.exists():
        log("⚠️  Folder already exists!", WARN)
    else:
        try:
            p.mkdir(parents=True)
            log(f"✅ Folder '{name}' created!")
            refresh_tree(explorer)
        except Exception as e:
            log(f"❌ Error: {e}", ACCENT)

def delete_folder():
    clear_log()
    name = ask("Enter folder name to delete (must be empty):")
    if not name: return
    p = Path(name)
    if p.exists():
        if confirm(f"Permanently delete folder '{name}'?"):
            try:
                p.rmdir()
                log(f"🗑️  Folder '{name}' deleted.")
                refresh_tree(explorer)
            except Exception as e:
                log(f"❌ Error: {e}\nMake sure folder is empty!", ACCENT)
    else:
        log("❌ Folder not found!", ACCENT)

def create_file_in_folder():
    clear_log()
    folder = ask("Enter folder name:")
    if not folder: return
    fname  = ask("Enter file name:")
    if not fname: return
    p = Path(folder) / fname
    if p.exists():
        log("⚠️  File already exists!", WARN)
    else:
        content = ask("Enter file content:") or ""
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            log(f"✅ '{p}' created successfully!")
            refresh_tree(explorer)
        except Exception as e:
            log(f"❌ Error: {e}", ACCENT)

# ─── Buttons Grid ──────────────────────────────────────────────────────────────
btn_frame = tk.Frame(right, bg=BG)
btn_frame.pack(fill="both", expand=True)

buttons = [
    ("📄 Create File",         create_file),
    ("👁️ Read File",           read_file),
    ("✏️ Update File",         update_file),
    ("🗑️ Delete File",         delete_file),
    ("🔤 Rename File",         rename_file),
    ("📁 Create Folder",       create_folder),
    ("❌ Delete Folder",       delete_folder),
    ("📁➕ File in Folder",    create_file_in_folder),
]

for i, (label, cmd) in enumerate(buttons):
    row, col = divmod(i, 2)
    btn = tk.Button(btn_frame, text=label, font=FONT_B,
                    bg=ACCENT, fg="white", activebackground="#c73652",
                    activeforeground="white", bd=0, pady=14,
                    cursor="hand2", command=cmd)
    btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)
for r in range(4):
    btn_frame.rowconfigure(r, weight=1)

# ─── Init Explorer ─────────────────────────────────────────────────────────────
refresh_tree(explorer)
log("👋 Welcome! Select an operation above.")

root.mainloop()