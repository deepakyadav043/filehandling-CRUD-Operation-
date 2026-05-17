### project -->> CRUD OPERATION using Exception handling (Streamlit UI)
import streamlit as st
from pathlib import Path
import os

st.set_page_config(
    page_title="File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0f0f0f !important;
    color: #d4d4d4;
}

/* ── Grid background ── */
.stApp {
    background-image:
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px) !important;
    background-size: 32px 32px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    border-right: 1px solid #1e1e1e !important;
}
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #555 !important;
    padding: 0.3rem 0.2rem !important;
    cursor: pointer !important;
    transition: color 0.15s !important;
    display: block !important;
}
[data-testid="stSidebar"] .stRadio label:hover { color: #aaa !important; }
[data-testid="stSidebar"] .stRadio label:has(input:checked) { color: #e2c97e !important; }

/* ── Header ── */
.header {
    border: 1px solid #1e1e1e;
    border-top: 3px solid #e2c97e;
    border-radius: 0 0 12px 12px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.8rem;
    background: #111;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}
.header-icon {
    font-size: 2rem;
    line-height: 1;
}
.header-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e2c97e;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.header-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #444;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 3px;
}
.header-badge {
    margin-left: auto;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 0.35rem 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #e2c97e;
    letter-spacing: 0.5px;
}

/* ── Section label ── */
.sec {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2.5px;
    color: #333;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── File tree ── */
.tree-row {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 0.35rem 0.5rem;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    margin: 1px 0;
}
.tree-row:hover { background: #161616; }
.tree-folder { color: #e2c97e; }
.tree-file   { color: #7eb8e2; }
.tree-dot    { width: 4px; height: 4px; border-radius: 50%; background: currentColor; flex-shrink: 0; }
.tree-size   { margin-left: auto; color: #2a2a2a; font-size: 0.6rem; }

/* ── Sidebar brand ── */
.brand {
    padding: 1.2rem 1rem 1rem;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 0.6rem;
}
.brand-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2c97e;
    letter-spacing: -0.3px;
}
.brand-ver {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #2d2d2d;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Feedback messages ── */
.fb {
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    margin: 0.5rem 0;
}
.fb-ok   { background: #0d1f13; border: 1px solid #1a4228; color: #4ade80; }
.fb-err  { background: #1f0d0d; border: 1px solid #421a1a; color: #f87171; }
.fb-warn { background: #1f190d; border: 1px solid #423310; color: #fbbf24; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: #111 !important;
    color: #d4d4d4 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #e2c97e !important;
    box-shadow: 0 0 0 2px rgba(226,201,126,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    color: #444 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── Select box ── */
.stSelectbox [data-baseweb="select"] > div {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #d4d4d4 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #e2c97e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.18s !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #222 !important;
    border-color: #e2c97e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(226,201,126,0.1) !important;
}
.stButton > button[kind="primary"] {
    background: #1f0d0d !important;
    color: #f87171 !important;
    border-color: #3a1515 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2a1010 !important;
    border-color: #f87171 !important;
    box-shadow: 0 4px 16px rgba(248,113,113,0.1) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
    padding: 3px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #444 !important;
    border-radius: 6px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #1e1e1e !important;
    color: #e2c97e !important;
}

/* ── Radio (main area) ── */
.stRadio label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #888 !important;
}

/* ── Subheader ── */
h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: #aaa !important;
    font-size: 1rem !important;
    margin-bottom: 0.8rem !important;
    letter-spacing: -0.2px !important;
}

/* ── Code ── */
.stCodeBlock { border: 1px solid #1e1e1e !important; border-radius: 8px !important; }

/* ── Alert ── */
.stAlert { border-radius: 8px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }

/* ── Divider ── */
hr { border-color: #1a1a1a !important; margin: 0.6rem 0 !important; }

/* ── Caption ── */
.stCaption, [data-testid="stCaptionContainer"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #333 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers (same logic as your CLI) ────────────────────────────────────────────
def readfileandfolder():
    """Same as your CLI readfileandfolder — lists current dir"""
    try:
        p = Path.cwd()
        return list(p.iterdir())
    except Exception as e:
        st.error(str(e))
        return []

def fmt_size(n):
    if n < 1024: return f"{n}B"
    if n < 1024**2: return f"{n/1024:.1f}KB"
    return f"{n/1024**2:.2f}MB"

def msg(text, kind="ok"):
    cls = {"ok": "fb-ok", "err": "fb-err", "warn": "fb-warn"}
    st.markdown(f'<div class="fb {cls.get(kind,"fb-ok")}">{text}</div>', unsafe_allow_html=True)

def render_tree():
    items = readfileandfolder()
    if not items:
        st.markdown('<div class="tree-row tree-file"><span class="tree-dot"></span>empty</div>', unsafe_allow_html=True)
        return
    for item in sorted(items):
        if item.is_dir():
            st.markdown(f'<div class="tree-row tree-folder"><span class="tree-dot"></span>📁 {item.name}</div>', unsafe_allow_html=True)
        else:
            sz = fmt_size(item.stat().st_size)
            st.markdown(f'<div class="tree-row tree-file"><span class="tree-dot"></span>📄 {item.name}<span class="tree-size">{sz}</span></div>', unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-name">📁 File Manager</div>
        <div class="brand-ver">CRUD · Exception Handling · pathlib</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec" style="padding:0 0.4rem">Operations</div>', unsafe_allow_html=True)

    operation = st.radio("menu", [
        "1 · Create File",
        "2 · Read File",
        "3 · Update File",
        "4 · Delete File",
        "5 · Rename File",
        "──────────",
        "6 · Create Folder",
        "7 · Rename Folder",
        "8 · Delete Folder",
        "──────────",
        "9 · Create File in Folder",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sec" style="padding:0 0.4rem">Current Directory</div>', unsafe_allow_html=True)
    render_tree()


# ── Header ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header">
    <div class="header-icon">📁</div>
    <div>
        <div class="header-title">File Manager</div>
        <div class="header-sub">CRUD · Exception Handling · pathlib engine</div>
    </div>
    <div class="header-badge">{operation[:25]}</div>
</div>
""", unsafe_allow_html=True)

# skip dividers
if "──" in operation:
    st.markdown('<p style="font-family:\'JetBrains Mono\',monospace;font-size:0.8rem;color:#2a2a2a;text-align:center;padding:2rem">← select an operation</p>', unsafe_allow_html=True)
    st.stop()


# ── 1. Create File ── (same as your create_file())  ─────────────────────────────
elif operation == "1 · Create File":
    st.subheader("Create File")
    file_name = st.text_input("Enter name of your file", placeholder="e.g. hello.txt")
    content   = st.text_area("Enter your file content", height=140, placeholder="type content here...")

    if st.button("Create File"):
        try:
            p = Path(file_name)
            if not file_name:
                msg("⚠ Enter a file name", "warn")
            elif p.exists():
                msg("FILE ALREADY EXISTS", "warn")
            else:
                with open(file_name, 'w') as file:
                    file.write(content)
                msg("FILE ADDED !")
                st.rerun()
        except Exception as e:
            msg(f"✗ {e}", "err")


# ── 2. Read File ── (same as your read_file()) ───────────────────────────────────
elif operation == "2 · Read File":
    st.subheader("Read File")
    items = [str(i) for i in readfileandfolder() if Path(i).is_file()]
    if not items:
        msg("No files found", "warn")
    else:
        file_name = st.selectbox("Select file to read", items)
        if st.button("Read File"):
            try:
                p = Path(file_name)
                if p.exists():
                    content = p.read_text()
                    sz = fmt_size(p.stat().st_size)
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Size", sz)
                    c2.metric("Lines", len(content.splitlines()))
                    c3.metric("Chars", len(content))
                    st.code(content if content else "(empty file)", language="text")
                else:
                    msg("FILE NOT FOUND!", "err")
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 3. Update File ── (same as your update_file()) ───────────────────────────────
elif operation == "3 · Update File":
    st.subheader("Update File")
    items = [str(i) for i in readfileandfolder() if Path(i).is_file()]
    if not items:
        msg("No files found", "warn")
    else:
        file_name   = st.selectbox("Select file to update", items)
        update_mode = st.radio("press 1 = Overwrite  |  press 2 = Append",
                               ["1 · Overwrite the content", "2 · Append the content"],
                               horizontal=True)
        content = st.text_area("Enter content to update", height=140)

        if st.button("Update File"):
            try:
                p = Path(file_name)
                if p.exists():
                    mode = 'w' if update_mode.startswith("1") else 'a'
                    with open(file_name, mode) as file:
                        file.write(content)
                    if update_mode.startswith("1"):
                        msg("CONTENT CHANGED")
                    else:
                        msg("FILE UPDATED SUCCESSFULLY")
                    st.rerun()
                else:
                    # your original creates the file if not found
                    with open(file_name, 'w') as file:
                        file.write(content)
                    msg("FILE ADDED !")
                    st.rerun()
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 4. Delete File ── (same as your delete_file()) ───────────────────────────────
elif operation == "4 · Delete File":
    st.subheader("Delete File")
    items = [str(i) for i in readfileandfolder() if Path(i).is_file()]
    if not items:
        msg("No files found", "warn")
    else:
        file_name = st.selectbox("Select file to delete", items)
        st.warning(f"⚠ This will permanently delete **{file_name}**")
        if st.button("Delete File", type="primary"):
            try:
                p = Path(file_name)
                if p.exists():
                    os.remove(p)
                    msg("FILE DELETED")
                    st.rerun()
                else:
                    msg("FILE DOES NOT EXIST", "err")
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 5. Rename File ── (same as your rename_file()) ───────────────────────────────
elif operation == "5 · Rename File":
    st.subheader("Rename File")
    items = [str(i) for i in readfileandfolder() if Path(i).is_file()]
    if not items:
        msg("No files found", "warn")
    else:
        file_name = st.selectbox("Select file to rename", items)
        new_name  = st.text_input("Enter the new name of your file", placeholder="e.g. renamed.txt")
        if st.button("Rename File"):
            try:
                p = Path(file_name)
                if not new_name:
                    msg("⚠ Enter a new name", "warn")
                elif p.exists():
                    p.rename(new_name)
                    msg("FILE RENAMED!")
                    st.rerun()
                else:
                    msg("FILE NOT FOUND!", "err")
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 6. Create Folder ── (same as your create_folder()) ───────────────────────────
elif operation == "6 · Create Folder":
    st.subheader("Create Folder")
    folder_name = st.text_input("Enter name of your folder", placeholder="e.g. my_folder")
    if st.button("Create Folder"):
        try:
            p = Path(folder_name)
            if not folder_name:
                msg("⚠ Enter a folder name", "warn")
            elif p.exists():
                msg("FOLDER ALREADY EXIST", "warn")
            else:
                p.mkdir(parents=True)
                msg("FOLDER CREATED!")
                st.rerun()
        except Exception as e:
            msg(f"✗ {e}", "err")


# ── 7. Rename Folder ── (same as your rename_folder()) ───────────────────────────
elif operation == "7 · Rename Folder":
    st.subheader("Rename Folder")
    folders = [str(i) for i in readfileandfolder() if Path(i).is_dir()]
    if not folders:
        msg("No folders found", "warn")
    else:
        folder_name = st.selectbox("Select folder to rename", folders)
        new_name    = st.text_input("Enter the new name of your folder", placeholder="e.g. new_folder")
        if st.button("Rename Folder"):
            try:
                p = Path(folder_name)
                if not new_name:
                    msg("⚠ Enter a new name", "warn")
                elif not p.exists():
                    msg("FOLDER NOT FOUND!", "err")
                else:
                    new_path = p.parent / new_name
                    if new_path.exists():
                        msg("FOLDER WITH THAT NAME ALREADY EXISTS", "warn")
                    else:
                        p.rename(new_path)
                        msg("FOLDER RENAMED!")
                        st.rerun()
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 8. Delete Folder ── (same as your delete_folder()) ───────────────────────────
elif operation == "8 · Delete Folder":
    st.subheader("Delete Folder")
    folders = [str(i) for i in readfileandfolder() if Path(i).is_dir()]
    if not folders:
        msg("No folders found", "warn")
    else:
        folder_name = st.selectbox("Select folder to delete", folders)
        st.warning(f"⚠ Folder must be **empty** to delete · permanently removes **{folder_name}**")
        if st.button("Delete Folder", type="primary"):
            try:
                p = Path(folder_name)
                if p.exists():
                    p.rmdir()
                    msg("FOLDER DELETED!")
                    st.rerun()
                else:
                    msg("FOLDER NOT FOUND!", "err")
            except Exception as e:
                msg(f"✗ {e}", "err")


# ── 9. Create File in Folder ── (same as your create_file_in_folder()) ───────────
elif operation == "9 · Create File in Folder":
    st.subheader("Create File in Folder")
    folders = [str(i) for i in readfileandfolder() if Path(i).is_dir()]

    tab1, tab2 = st.tabs(["Use Existing Folder", "Create New Folder"])

    with tab1:
        if not folders:
            msg("No folders found — create one first or use the other tab", "warn")
        else:
            folder_name = st.selectbox("Select folder", folders, key="ef_folder")
            file_name   = st.text_input("Enter the name of your file", key="ef_file", placeholder="e.g. notes.txt")
            content     = st.text_area("Enter your file content", height=110, key="ef_content")
            if st.button("Create File", key="ef_btn"):
                try:
                    p = Path(folder_name) / file_name
                    if not file_name:
                        msg("⚠ Enter a file name", "warn")
                    elif p.exists():
                        msg("FILE ALREADY EXISTS", "warn")
                    else:
                        with open(p, 'w') as file:
                            file.write(content)
                        msg("CREATED SUCCESSFULLY")
                        st.rerun()
                except Exception as e:
                    msg(f"✗ {e}", "err")

    with tab2:
        folder_name = st.text_input("Enter name of your folder", key="nf_folder", placeholder="e.g. my_folder")
        file_name   = st.text_input("Enter the name of your file", key="nf_file", placeholder="e.g. notes.txt")
        content     = st.text_area("Enter your file content", height=110, key="nf_content")
        if st.button("Create Folder + File", key="nf_btn"):
            try:
                if not folder_name or not file_name:
                    msg("⚠ Enter both folder and file names", "warn")
                else:
                    p = Path(folder_name) / file_name
                    if p.exists():
                        msg("FILE ALREADY EXISTS", "warn")
                    else:
                        Path(folder_name).mkdir(parents=True, exist_ok=True)
                        with open(p, 'w') as file:
                            file.write(content)
                        msg("CREATED SUCCESSFULLY")
                        st.rerun()
            except Exception as e:
                msg(f"✗ {e}", "err")
