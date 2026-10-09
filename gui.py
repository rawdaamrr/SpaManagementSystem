import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import datetime
import db_connection

# Database Helper Functions
def db_fetch(query, params=()):
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = [tuple(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def db_exec(query, params=()):
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def next_id(table, id_col):
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
    last_id = cursor.fetchone()[0]
    conn.close()
    return 1 if last_id is None else last_id + 1

BG_DARK    = "#0d1b2a"
BG_PANEL   = "#112240"
BG_TABLE   = "#0d1b2a"
BG_FORM    = "#0f2133"
GOLD       = "#c9a13b"
RED_ACTIVE = "#e8365d"
BTN_GREEN  = "#28a745";  BTN_GREEN_H = "#34c85a"
BTN_RED    = "#dc3545";  BTN_RED_H   = "#f04455"
BTN_BLUE   = "#1a6fc4";  BTN_BLUE_H  = "#2480db"
BTN_GREY   = "#4a5568";  BTN_GREY_H  = "#5a6578"
WHITE      = "#ffffff"
DIM        = "#8899aa"
GOLD_TEXT  = "#c9a13b"

# window
root = tk.Tk()
root.title("Spa Management System")
root.geometry("1360x720")
root.configure(bg=BG_DARK)
root.resizable(True, True)

F_TITLE   = tkfont.Font(family="Georgia",      size=20, weight="bold")
F_SECTION = tkfont.Font(family="Georgia",      size=13, weight="bold")
F_NAV     = tkfont.Font(family="Trebuchet MS", size=11, weight="bold")
F_BTN     = tkfont.Font(family="Trebuchet MS", size=10, weight="bold")
F_TABLE   = tkfont.Font(family="Consolas",     size=10)
F_LABEL   = tkfont.Font(family="Trebuchet MS", size=9)
F_INPUT   = tkfont.Font(family="Trebuchet MS", size=10)
F_LOGO    = tkfont.Font(family="Georgia",      size=9,  weight="bold")

def hover(btn, normal, over):
    btn.bind("<Enter>", lambda e: btn.config(bg=over))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))

def action_btn(parent, text, cmd, bg, hbg, width=15):
    b = tk.Button(parent, text=text, command=cmd,
                  font=F_BTN, fg=WHITE, bg=bg,
                  activebackground=hbg, activeforeground=WHITE,
                  relief="flat", bd=0, padx=10, pady=8,
                  width=width, cursor="hand2")
    hover(b, bg, hbg)
    return b

def entry_field(parent, label, row, col, width=22):
    tk.Label(parent, text=label, font=F_LABEL, fg=DIM, bg=BG_FORM
             ).grid(row=row, column=col, sticky="w", padx=8, pady=(6,1))
    e = tk.Entry(parent, font=F_INPUT, bg="#1a3a55", fg=WHITE,
                 insertbackground=WHITE, relief="flat", bd=4, width=width)
    e.grid(row=row+1, column=col, sticky="ew", padx=8, pady=(0,6))
    return e

def combo_field(parent, label, values, row, col, width=18):
    tk.Label(parent, text=label, font=F_LABEL, fg=DIM, bg=BG_FORM
             ).grid(row=row, column=col, sticky="w", padx=8, pady=(6,1))
    v = tk.StringVar()
    c = ttk.Combobox(parent, textvariable=v, values=values,
                     font=F_INPUT, width=width, state="readonly")
    c.grid(row=row+1, column=col, sticky="ew", padx=8, pady=(0,6))
    return v, c

def section_hdr(parent, text):
    f = tk.Frame(parent, bg=BG_DARK, pady=10)
    f.pack(fill="x", padx=20)
    tk.Label(f, text=text, font=F_SECTION, fg=GOLD, bg=BG_DARK).pack(side="left")
    tk.Frame(f, bg=RED_ACTIVE, height=2).pack(fill="x", pady=(4,0))

# FIX 2: anchor="w" on heading + column to align everything left
def make_tree(parent, cols, widths):
    tf = tk.Frame(parent, bg=BG_DARK, padx=20)
    tf.pack(fill="both", expand=True)
    tree = ttk.Treeview(tf, columns=cols, show="headings", style="Spa.Treeview")
    for c, w in zip(cols, widths):
        tree.heading(c, text=c, anchor="w")      # heading text left-aligned
        tree.column(c, width=w, anchor="w", stretch=False)  # cell text left-aligned
    vsb = ttk.Scrollbar(tf, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tf, orient="horizontal",  command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tf.rowconfigure(0, weight=1)
    tf.columnconfigure(0, weight=1)
    return tree

def btn_row(parent):
    f = tk.Frame(parent, bg=BG_DARK, pady=8)
    f.pack()
    return f

# TTK style
style = ttk.Style()
style.theme_use("clam")
style.configure("Spa.Treeview",
                background=BG_TABLE, foreground=WHITE, rowheight=26,
                fieldbackground=BG_TABLE, font=F_TABLE, borderwidth=0)
style.configure("Spa.Treeview.Heading",
                background=BG_PANEL, foreground=GOLD_TEXT,
                font=F_BTN, relief="flat")
style.map("Spa.Treeview",
          background=[("selected", "#1a4a70")],
          foreground=[("selected", WHITE)])

# sidebar
sidebar = tk.Frame(root, bg=BG_DARK, width=180)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo_f = tk.Frame(sidebar, bg="#0a1520", pady=16)
logo_f.pack(fill="x")
tk.Label(logo_f, text="🌸", font=tkfont.Font(size=28), bg="#0a1520", fg=RED_ACTIVE).pack()
tk.Label(logo_f, text="SPA SYSTEM", font=F_LOGO, bg="#0a1520", fg=WHITE).pack()

nav_btns = {}

def nav_click(page):
    for p, b in nav_btns.items():
        b.config(bg=RED_ACTIVE if p == page else BG_DARK,
                 fg=WHITE      if p == page else DIM)
    show_page(page)

for lbl, key in [
    ("👤  Clients",         "Clients"),
    ("📅  Sessions",        "Sessions"),
    ("🧖  Therapists",      "Therapists"),
    ("💆  Services",        "Services"),
    ("📄  Session Details", "SessionDetails"),
]:
    b = tk.Button(sidebar, text=lbl, font=F_NAV,
                  fg=DIM, bg=BG_DARK,
                  activebackground=RED_ACTIVE, activeforeground=WHITE,
                  relief="flat", bd=0, padx=16, pady=12,
                  anchor="w", width=18, cursor="hand2",
                  command=lambda k=key: nav_click(k))
    b.pack(fill="x")
    nav_btns[key] = b


# main area
main_area = tk.Frame(root, bg=BG_DARK)
main_area.pack(side="left", fill="both", expand=True)

hbar = tk.Frame(main_area, bg=BG_PANEL, height=60)
hbar.pack(fill="x")
hbar.pack_propagate(False)

page_title = tk.StringVar(value="Client Management")
tk.Label(hbar, textvariable=page_title,
         font=F_TITLE, fg=WHITE, bg=BG_PANEL).pack(side="left", padx=24, pady=12)
tk.Label(hbar, text="Beauty & Wellness Network",
         font=F_LABEL, fg=DIM, bg=BG_PANEL).pack(side="right", padx=24)

content = tk.Frame(main_area, bg=BG_DARK)
content.pack(fill="both", expand=True)

# clients
def build_clients(parent):
    frame = tk.Frame(parent, bg=BG_DARK)
    section_hdr(frame, "👤  Client Management")

    cols   = ("ID", "Name", "Gender", "Phone", "Email", "Member Since")
    widths = [45, 190, 85, 125, 210, 125]
    tree   = make_tree(frame, cols, widths)

    def refresh():
        tree.delete(*tree.get_children())
        try:
            for r in db_fetch("SELECT ClientID, ClientName, Gender, Phone, Email, MembershipDate FROM Client"):
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    # form
    form = tk.LabelFrame(frame, text=" Add New Client ",
                         font=F_LABEL, fg=GOLD, bg=BG_FORM,
                         labelanchor="nw", bd=1, relief="groove", padx=4, pady=4)
    form.pack(fill="x", padx=20, pady=(6,2))
    for i in range(5): form.columnconfigure(i, weight=1)

    e_name   = entry_field(form, "Name",                        0, 0)
    e_gender = entry_field(form, "Gender (Male/Female)",         0, 1)
    e_phone  = entry_field(form, "Phone (11 digits)",            0, 2)
    e_email  = entry_field(form, "Email",                        0, 3)
    e_date   = entry_field(form, "Membership Date (YYYY-MM-DD)", 0, 4)

    # update
    upd_form = tk.LabelFrame(frame, text=" Update Selected Client's Contact ",
                              font=F_LABEL, fg=GOLD, bg=BG_FORM,
                              labelanchor="nw", bd=1, relief="groove", padx=4, pady=4)
    upd_form.pack(fill="x", padx=20, pady=(2,4))
    for i in range(5): upd_form.columnconfigure(i, weight=1)

    e_upd_phone = entry_field(upd_form, "New Phone (leave blank to keep)", 0, 0)
    e_upd_email = entry_field(upd_form, "New Email (leave blank to keep)",  0, 1)

    # actions
    def do_add():
        name, gender, phone, email, date = (
            e_name.get().strip(), e_gender.get().strip(),
            e_phone.get().strip(), e_email.get().strip(), e_date.get().strip()
        )
        if not all([name, gender, phone, email, date]):
            messagebox.showwarning("Missing", "Please fill in all Add Client fields.")
            return
        try:
            cid = next_id("Client", "ClientID")
            db_exec(
                "INSERT INTO Client (ClientID, ClientName, Gender, Phone, Email, MembershipDate) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (cid, name, gender, phone, email, date)
            )
            for e in [e_name, e_gender, e_phone, e_email, e_date]:
                e.delete(0, tk.END)
            refresh()
            messagebox.showinfo("Success", f"Client '{name}' added with ID {cid}.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    # FIX 1: Smart delete with proper checks and messages
    def do_delete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a client row in the table first.")
            return

        cid  = tree.item(sel[0])["values"][0]
        name = tree.item(sel[0])["values"][1]

        try:
            conn = db_connection.get_connection()
            cursor = conn.cursor()

            # Check completed or scheduled sessions
            cursor.execute("""
                SELECT COUNT(*) FROM Session
                WHERE ClientID = ? AND Status IN ('Completed', 'Scheduled')
            """, (cid,))
            active_count = cursor.fetchone()[0]

            # Check cancelled sessions
            cursor.execute("""
                SELECT COUNT(*) FROM Session
                WHERE ClientID = ? AND Status = 'Cancelled'
            """, (cid,))
            cancelled_count = cursor.fetchone()[0]

            conn.close()

            # CASE A: Has completed or scheduled sessions — block
            if active_count > 0:
                messagebox.showwarning(
                    "Cannot Delete",
                    f"Cannot delete '{name}'.\n"
                    f"They have {active_count} Completed/Scheduled session(s) on record.\n"
                    f"Cannot delete a client with active history."
                )
                return

            # CASE B: Has only cancelled sessions — warn then delete
            if cancelled_count > 0:
                confirm = messagebox.askyesno(
                    "Warning",
                    f"Client '{name}' has {cancelled_count} cancelled session(s).\n"
                    f"Deleting this client will also delete those cancelled sessions.\n\n"
                    f"Are you sure you want to proceed?"
                )
                if not confirm:
                    return
                conn2 = db_connection.get_connection()
                cur2  = conn2.cursor()
                cur2.execute("""
                    DELETE FROM Session_Product_Usage WHERE SessionID IN
                    (SELECT SessionID FROM Session WHERE ClientID = ? AND Status = 'Cancelled')
                """, (cid,))
                cur2.execute("DELETE FROM Session WHERE ClientID = ? AND Status = 'Cancelled'", (cid,))
                cur2.execute("DELETE FROM Client WHERE ClientID = ?", (cid,))
                conn2.commit()
                conn2.close()
                refresh()
                messagebox.showinfo("Deleted", f"Client '{name}' and their cancelled sessions deleted.")
                return

            # CASE C: No sessions at all — delete directly
            if messagebox.askyesno("Confirm", f"Delete client '{name}' (ID {cid})?"):
                db_exec("DELETE FROM Client WHERE ClientID = ?", (cid,))
                refresh()
                messagebox.showinfo("Deleted", f"Client '{name}' deleted successfully.")

        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def do_update():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a client row in the table first.")
            return
        cid       = tree.item(sel[0])["values"][0]
        new_phone = e_upd_phone.get().strip()
        new_email = e_upd_email.get().strip()
        if not new_phone and not new_email:
            messagebox.showwarning("Empty", "Enter at least a new phone or email.")
            return
        try:
            if new_phone and new_email:
                db_exec("UPDATE Client SET Phone=?, Email=? WHERE ClientID=?",
                        (new_phone, new_email, cid))
            elif new_phone:
                db_exec("UPDATE Client SET Phone=? WHERE ClientID=?", (new_phone, cid))
            else:
                db_exec("UPDATE Client SET Email=? WHERE ClientID=?", (new_email, cid))
            e_upd_phone.delete(0, tk.END)
            e_upd_email.delete(0, tk.END)
            refresh()
            messagebox.showinfo("Updated", f"Client ID {cid} contact updated.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    br = btn_row(frame)
    action_btn(br, "➕  Add Client",     do_add,    BTN_GREEN, BTN_GREEN_H).pack(side="left", padx=6)
    action_btn(br, "🗑  Delete Client",  do_delete, BTN_RED,   BTN_RED_H  ).pack(side="left", padx=6)
    action_btn(br, "✏️  Update Contact",  do_update, BTN_BLUE,  BTN_BLUE_H ).pack(side="left", padx=6)


    refresh()
    return frame

# session
def build_sessions(parent):
    frame = tk.Frame(parent, bg=BG_DARK)
    section_hdr(frame, "📅  Session Management")

    cols   = ("ID", "Client", "Therapist", "Service", "Spa", "Date", "Status")
    widths = [40, 150, 150, 160, 120, 160, 95]
    tree   = make_tree(frame, cols, widths)

    def refresh():
        tree.delete(*tree.get_children())
        try:
            rows = db_fetch("""
                SELECT s.SessionID, c.ClientName, t.TherapistName,
                       sv.ServiceName, sp.SpaName, s.Date, s.Status
                FROM Session s
                JOIN Client    c  ON s.ClientID    = c.ClientID
                JOIN Therapist t  ON s.TherapistID = t.TherapistID
                JOIN Service   sv ON s.ServiceID   = sv.ServiceID
                JOIN Spa       sp ON s.SpaID       = sp.SpaID
                ORDER BY s.SessionID
            """)
            for r in rows:
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def load_options():
        try:
            clients    = [f"{r[0]} – {r[1]}" for r in db_fetch("SELECT ClientID, ClientName FROM Client")]
            therapists = [f"{r[0]} – {r[1]}" for r in db_fetch("SELECT TherapistID, TherapistName FROM Therapist")]
            services   = [f"{r[0]} – {r[1]}" for r in db_fetch("SELECT ServiceID, ServiceName FROM Service")]
            spas       = [f"{r[0]} – {r[1]}" for r in db_fetch("SELECT SpaID, SpaName FROM Spa")]
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))
            clients = therapists = services = spas = []
        return clients, therapists, services, spas

    clients, therapists, services, spas = load_options()

    form = tk.LabelFrame(frame, text=" Book New Session ",
                         font=F_LABEL, fg=GOLD, bg=BG_FORM,
                         labelanchor="nw", bd=1, relief="groove", padx=4, pady=4)
    form.pack(fill="x", padx=20, pady=(6,2))
    for i in range(4): form.columnconfigure(i, weight=1)

    v_client,    cb_client    = combo_field(form, "Client",    clients,    0, 0)
    v_therapist, cb_therapist = combo_field(form, "Therapist", therapists, 0, 1)
    v_service,   cb_service   = combo_field(form, "Service",   services,   0, 2)
    v_spa,       cb_spa       = combo_field(form, "Spa",       spas,       0, 3)

    tk.Label(form, text="Date & Time (YYYY-MM-DD HH:MM:SS)",
             font=F_LABEL, fg=DIM, bg=BG_FORM
             ).grid(row=2, column=0, sticky="w", padx=8, pady=(6,1))
    e_date = tk.Entry(form, font=F_INPUT, bg="#1a3a55", fg=WHITE,
                      insertbackground=WHITE, relief="flat", bd=4, width=22)
    e_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    e_date.grid(row=3, column=0, sticky="ew", padx=8, pady=(0,6))

    v_status, cb_status = combo_field(
        form, "Status", ["Scheduled", "Completed", "Cancelled"], 2, 3)
    cb_status.set("Scheduled")

    def _parse_id(combo_val):
        return int(combo_val.split("–")[0].strip())

    def do_book():
        if not all([v_client.get(), v_therapist.get(), v_service.get(),
                    v_spa.get(), e_date.get(), v_status.get()]):
            messagebox.showwarning("Missing", "Please fill in all booking fields.")
            return
        try:
            sid = next_id("Session", "SessionID")
            db_exec(
                "INSERT INTO Session (SessionID, ClientID, TherapistID, ServiceID, SpaID, Date, Status) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (sid,
                 _parse_id(v_client.get()),
                 _parse_id(v_therapist.get()),
                 _parse_id(v_service.get()),
                 _parse_id(v_spa.get()),
                 e_date.get().strip(),
                 v_status.get())
            )
            refresh()
            messagebox.showinfo("Booked", f"Session ID {sid} booked successfully.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def do_delete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a session row first.")
            return
        sid    = tree.item(sel[0])["values"][0]
        status = tree.item(sel[0])["values"][6]
        if status != "Cancelled":
            messagebox.showwarning("Not Cancelled",
                                   "Only Cancelled sessions can be deleted.\n"
                                   f"Session {sid} is '{status}'.")
            return
        if not messagebox.askyesno("Confirm", f"Delete cancelled session ID {sid}?"):
            return
        try:
            db_exec("DELETE FROM Session_Product_Usage WHERE SessionID = ?", (sid,))
            db_exec("DELETE FROM Session WHERE SessionID = ? AND Status = 'Cancelled'", (sid,))
            refresh()
            messagebox.showinfo("Deleted", f"Session ID {sid} deleted.")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def do_update_status():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a session row first.")
            return
        if not v_status.get():
            messagebox.showwarning("Missing", "Choose a new status from the dropdown.")
            return
        sid = tree.item(sel[0])["values"][0]
        try:
            db_exec("UPDATE Session SET Status = ? WHERE SessionID = ?",
                    (v_status.get(), sid))
            refresh()
            messagebox.showinfo("Updated", f"Session {sid} status → {v_status.get()}")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    br = btn_row(frame)
    action_btn(br, "➕  Book Session",   do_book,          BTN_GREEN, BTN_GREEN_H).pack(side="left", padx=6)
    action_btn(br, "🗑  Delete Session", do_delete,        BTN_RED,   BTN_RED_H  ).pack(side="left", padx=6)
    action_btn(br, "🔄  Update Status",  do_update_status, BTN_BLUE,  BTN_BLUE_H ).pack(side="left", padx=6)


    refresh()
    return frame

# therapists
def build_therapists(parent):
    frame = tk.Frame(parent, bg=BG_DARK)
    section_hdr(frame, "🧖  Therapist Skills & Spa")

    cols   = ("ID", "Therapist", "Phone", "Skill", "Spa", "Location")
    widths = [40, 160, 120, 200, 160, 180]
    tree   = make_tree(frame, cols, widths)

    def refresh():
        tree.delete(*tree.get_children())
        try:
            rows = db_fetch("""
                SELECT t.TherapistID, t.TherapistName, t.Phone,
                       ts.Skill, sp.SpaName, sp.SpaLocation
                FROM Therapist t
                JOIN Therapist_Skill ts ON t.TherapistID = ts.TherapistID
                JOIN Spa             sp ON t.SpaID        = sp.SpaID
                ORDER BY t.TherapistName
            """)
            for r in rows:
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    br = btn_row(frame)


    refresh()
    return frame

# services and products
def build_services(parent):
    frame = tk.Frame(parent, bg=BG_DARK)
    section_hdr(frame, "💆  Services & Wellness Products")

    cols   = ("ID", "Name", "Category / Stock", "Duration / Price", "Price (EGP)")
    widths = [45, 240, 160, 140, 110]
    tree   = make_tree(frame, cols, widths)

    def load_services():
        tree.delete(*tree.get_children())
        try:
            for r in db_fetch("SELECT ServiceID, ServiceName, Category, Duration, ServicePrice FROM Service"):
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def load_products():
        tree.delete(*tree.get_children())
        try:
            for r in db_fetch("SELECT ProductID, ProductName, 'Stock: ' + CAST(StockQuantity AS VARCHAR), '', Price FROM WellnessProduct"):
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    br = btn_row(frame)
    action_btn(br, "💆  Load Services",  load_services, BTN_BLUE,  BTN_BLUE_H ).pack(side="left", padx=6)
    action_btn(br, "🌿  Load Products",  load_products, BTN_GREEN, BTN_GREEN_H).pack(side="left", padx=6)

    load_services()
    return frame

# session details
def build_session_details(parent):
    frame = tk.Frame(parent, bg=BG_DARK)
    section_hdr(frame, "📄  Session Details")

    cols   = ("ID", "Client", "Phone", "Therapist", "Service",
              "Category", "Price", "Spa", "Location", "Date", "Status")
    widths = [40, 120, 110, 120, 140, 90, 60, 120, 140, 145, 90]
    tree   = make_tree(frame, cols, widths)

    def refresh():
        tree.delete(*tree.get_children())
        try:
            rows = db_fetch("""
                SELECT s.SessionID, c.ClientName, c.Phone,
                       t.TherapistName, sv.ServiceName, sv.Category,
                       sv.ServicePrice, sp.SpaName, sp.SpaLocation,
                       s.Date, s.Status
                FROM Session s
                JOIN Client    c  ON s.ClientID    = c.ClientID
                JOIN Therapist t  ON s.TherapistID = t.TherapistID
                JOIN Service   sv ON s.ServiceID   = sv.ServiceID
                JOIN Spa       sp ON s.SpaID       = sp.SpaID
                ORDER BY s.Date DESC
            """)
            for r in rows:
                tree.insert("", "end", values=r)
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    br = btn_row(frame)


    refresh()
    return frame

# router
pages = {}

TITLES = {
    "Clients":        "Client Management",
    "Sessions":       "Session Management",
    "Therapists":     "Therapist Skills & Spa",
    "Services":       "Services & Products",
    "SessionDetails": "Session Details",
}
BUILDERS = {
    "Clients":        build_clients,
    "Sessions":       build_sessions,
    "Therapists":     build_therapists,
    "Services":       build_services,
    "SessionDetails": build_session_details,
}

def show_page(name):
    page_title.set(TITLES.get(name, name))
    for p in pages.values():
        p.pack_forget()
    if name not in pages:
        pages[name] = BUILDERS[name](content)
    pages[name].pack(fill="both", expand=True)

# launch
nav_click("Clients")
root.mainloop()