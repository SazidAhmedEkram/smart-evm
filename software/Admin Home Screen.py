"""
SmartEVM Admin Panel — Polished GovTech White+Blue Theme (PyQt5)
Target: 800x480 (touch-friendly). Modern, professional look.

Run:
    python smart_evm_admin_polished.py

Requires:
    PyQt5
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QLineEdit, QTextEdit, QComboBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QSpacerItem, QSizePolicy, QMessageBox,
    QDateEdit, QGridLayout, QScrollArea, QDialog, QFormLayout, QStyleOption, QStyle
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QDate

# ---------------------------
# Demo data (in-memory)
# ---------------------------
voters = [
    {"nid": "1001001001", "name": "Rahim Uddin", "dob": "1990-05-12", "constituency": "North", "face": True, "voted": False},
    {"nid": "1001001002", "name": "Karim Ahmed", "dob": "1988-03-03", "constituency": "South", "face": False, "voted": True},
]
candidates = [
    {"name": "Alice", "party": "Blue Party", "constituency": "North"},
    {"name": "Bob",   "party": "Green Party", "constituency": "North"},
    {"name": "Charlie", "party": "Red Party", "constituency": "South"},
]

# ---------------------------
# Polished QSS (GovTech style)
# ---------------------------
APP_QSS = """
/* Global */
QWidget {
    background-color: #F8FAFF;
    color: #10243A;
    font-family: "Inter", "Segoe UI", "Roboto", Arial;
    font-size: 13px;
}

/* Topbar */
#topbar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E6EEF8;
}

/* Side nav */
#sidenav {
    background-color: #FFFFFF;
    border-right: 1px solid #E6EEF8;
}

/* Cards */
.card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid rgba(16,36,58,0.04);
}
.feature-card {
    min-width: 190px;
    min-height: 130px;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 8px 20px rgba(16,36,58,0.04);
}

/* Buttons */
QPushButton.primary {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
QPushButton.primary:hover { background-color: #1f53d6; }
QPushButton.positive {
    background-color: #10B981;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
QPushButton.ghost {
    background-color: transparent;
    color: #2563EB;
    border: 1px solid #E6EEF8;
    border-radius: 8px;
    padding: 8px 12px;
}

/* Inputs */
QLineEdit, QComboBox, QTextEdit, QDateEdit {
    background: white;
    border: 1px solid #EAF1FB;
    border-radius: 8px;
    padding: 8px;
}

/* Table */
QTableWidget {
    background: white;
    border-radius: 8px;
    gridline-color: #F1F5F9;
    selection-background-color: rgba(37,99,235,0.08);
}
QHeaderView::section {
    background-color: #FAFBFF;
    padding: 8px;
    border: none;
    font-weight: 700;
}

/* Small text */
.small-muted { color: #6B7280; font-size: 12px; }

/* Hover effect for cards */
QFrame.card:hover {
    transform: translateY(-2px);
}
"""

# ---------------------------
# Helpers
# ---------------------------
def title_label(text, size=18, bold=True):
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(size)
    f.setBold(bold)
    lbl.setFont(f)
    return lbl

def tiny(text):
    l = QLabel(text)
    l.setStyleSheet("color: #64748B; font-size:12px;")
    return l

# Utility to paint rounded background when needed (for consistent visuals)
class RoundFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
    def paintEvent(self, e):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

# ---------------------------
# Top bar
# ---------------------------
class TopBar(RoundFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.build()

    def build(self):
        self.setFixedHeight(64)
        layout = QHBoxLayout()
        layout.setContentsMargins(18, 8, 18, 8)
        layout.setSpacing(12)

        # Left: logo + title
        left = QHBoxLayout()
        logo = QLabel()
        logo.setText("🔷")  # simple emoji logo — replace with QPixmap logo if needed
        logo.setFixedSize(36, 36)
        logo.setAlignment(Qt.AlignCenter)
        title = QLabel("Smart EVM • Admin")
        title.setFont(QFont("Inter", 16, QFont.DemiBold))
        left.addWidget(logo, alignment=Qt.AlignVCenter)
        left.addSpacing(6)
        left.addWidget(title)
        left.addStretch()

        # Right: last sync + profile + logout
        right = QHBoxLayout()
        self.sync = QLabel("Last sync: now")
        self.sync.setStyleSheet("color:#667085;")
        profile = QPushButton("Admin")
        profile.setStyleSheet("padding:8px; border-radius:8px;")
        logout = QPushButton("Logout")
        logout.setProperty("class", "ghost")
        logout.clicked.connect(lambda: QApplication.quit())
        right.addWidget(self.sync)
        right.addSpacing(12)
        right.addWidget(profile)
        right.addWidget(logout)

        layout.addLayout(left)
        layout.addLayout(right)
        self.setLayout(layout)

# ---------------------------
# Pages
# ---------------------------
class HomePage(QWidget):
    def __init__(self, appwin):
        super().__init__()
        self.appwin = appwin
        self.build()

    def build(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        # Header
        header_row = QHBoxLayout()
        header_row.addWidget(title_label("Admin Dashboard", 20))
        header_row.addStretch()
        header_row.addWidget(tiny("Manage voters • candidates • elections"))
        root.addLayout(header_row)

        # Stat cards
        stat_row = QHBoxLayout()
        stat_row.setSpacing(12)
        stat_row.addWidget(self.stat_card("Total Voters", str(len(voters))))
        stat_row.addWidget(self.stat_card("Registered Faces", str(sum(1 for v in voters if v["face"]))))
        stat_row.addWidget(self.stat_card("Votes Cast", str(sum(1 for v in voters if v["voted"]))))
        stat_row.addStretch()
        root.addLayout(stat_row)

        # Feature grid (2x2)
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        features = [
            ("Register Voter", "Add and register a new voter", self.go_register),
            ("Voter List", "Search and manage voters", self.go_voters),
            ("Candidate Management", "Manage candidates & parties", self.go_candidates),
            ("Election Setup", "Create and manage elections", self.go_dashboard),
        ]
        pos = [(0,0),(0,1),(1,0),(1,1)]
        for (title, desc, cb), p in zip(features, pos):
            c = RoundFrame()
            c.setProperty("class", "feature-card card")
            cl = QVBoxLayout()
            cl.setContentsMargins(12,12,12,12)
            cl.addWidget(QLabel(f"<b>{title}</b>"))
            d = QLabel(desc)
            d.setStyleSheet("color:#64748B;")
            d.setWordWrap(True)
            cl.addWidget(d)
            cl.addStretch()
            btn = QPushButton("Open")
            btn.setProperty("class", "primary")
            btn.setFixedWidth(110)
            btn.clicked.connect(cb)
            cl.addWidget(btn, alignment=Qt.AlignRight)
            c.setLayout(cl)
            grid.addWidget(c, *p)
        root.addLayout(grid)
        root.addStretch()
        self.setLayout(root)

    def stat_card(self, title, value):
        w = RoundFrame()
        w.setProperty("class", "card")
        l = QVBoxLayout()
        l.addWidget(QLabel(title))
        val = QLabel(value)
        val.setFont(QFont("", 20, QFont.Bold))
        l.addWidget(val)
        w.setLayout(l)
        return w

    # navigation callbacks
    def go_register(self):
        self.appwin.switch_page("register")
    def go_voters(self):
        self.appwin.switch_page("voter_list")
    def go_candidates(self):
        self.appwin.switch_page("candidates")
    def go_dashboard(self):
        self.appwin.switch_page("dashboard")

class DashboardPage(QWidget):
    def __init__(self, appwin):
        super().__init__()
        self.appwin = appwin
        self.build()

    def build(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)
        root.addWidget(title_label("Election Dashboard", 20))
        root.addSpacing(6)

        # top stats
        top = QHBoxLayout()
        top.addWidget(self.stat("Total Voters", str(len(voters))))
        top.addWidget(self.stat("Votes Cast", str(sum(1 for v in voters if v["voted"]))))
        top.addWidget(self.stat("Remaining", str(len(voters) - sum(1 for v in voters if v["voted"]))))
        top.addStretch()
        root.addLayout(top)
        root.addSpacing(12)

        # placeholder for chart & logs
        bottom = QHBoxLayout()
        chart = RoundFrame()
        chart.setProperty("class", "card")
        chv = QVBoxLayout()
        chv.addWidget(QLabel("<b>Candidate Vote Distribution</b>"))
        for c in candidates:
            chv.addWidget(QLabel(f"{c['name']} — 0 votes"))
        chart.setLayout(chv)

        logs = RoundFrame()
        logs.setProperty("class", "card")
        lv = QVBoxLayout()
        lv.addWidget(QLabel("<b>Recent Activity</b>"))
        lv.addWidget(QLabel("• System started"))
        lv.addWidget(QLabel("• Face verification: 1001001001 — success"))
        lv.addStretch()
        logs.setLayout(lv)

        bottom.addWidget(chart, 1)
        bottom.addWidget(logs, 0)
        root.addLayout(bottom)
        root.addStretch()
        self.setLayout(root)

    def stat(self, t, v):
        w = RoundFrame()
        w.setProperty("class", "card")
        l = QVBoxLayout()
        l.addWidget(QLabel(t))
        val = QLabel(v)
        val.setFont(QFont("", 18, QFont.Bold))
        l.addWidget(val)
        w.setLayout(l)
        return w

class RegisterVoterPage(QWidget):
    def __init__(self, appwin):
        super().__init__()
        self.appwin = appwin
        self.photo_path = None
        self.build()

    def build(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16,12,16,12)
        layout.setSpacing(12)

        # left: form card
        form_card = RoundFrame()
        form_card.setProperty("class", "card")
        fl = QVBoxLayout()
        fl.setContentsMargins(12,12,12,12)
        fl.addWidget(title_label("Register New Voter", 18))
        fl.addSpacing(6)

        form = QFormLayout()
        self.nid = QLineEdit()
        self.name = QLineEdit()
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate(1995,1,1))
        self.const = QComboBox()
        self.const.addItems(["North","South","East","West"])
        self.addr = QTextEdit()
        self.addr.setFixedHeight(80)

        form.addRow("NID", self.nid)
        form.addRow("Full name", self.name)
        form.addRow("Date of birth", self.dob)
        form.addRow("Constituency", self.const)
        form.addRow("Address", self.addr)
        fl.addLayout(form)

        btn_row = QHBoxLayout()
        reg_face = QPushButton("Register Face")
        reg_face.setProperty("class", "primary")
        reg_face.clicked.connect(self.register_face)
        save = QPushButton("Save Voter")
        save.setProperty("class", "positive")
        save.clicked.connect(self.save_voter)
        btn_row.addWidget(reg_face)
        btn_row.addWidget(save)
        fl.addLayout(btn_row)

        form_card.setLayout(fl)

        # right: photo card
        photo_card = RoundFrame()
        photo_card.setProperty("class", "card")
        phl = QVBoxLayout()
        phl.addWidget(QLabel("<b>Photo / Face Preview</b>"))
        self.photo_preview = QLabel()
        self.photo_preview.setFixedSize(220, 180)
        self.photo_preview.setStyleSheet("background:#F1F5F9; border-radius:10px;")
        self.photo_preview.setAlignment(Qt.AlignCenter)
        phl.addWidget(self.photo_preview, alignment=Qt.AlignCenter)
        up = QPushButton("Upload Photo")
        up.setProperty("class", "ghost")
        up.clicked.connect(self.upload_photo)
        phl.addWidget(up, alignment=Qt.AlignCenter)
        photo_card.setLayout(phl)

        layout.addWidget(form_card, 1)
        layout.addWidget(photo_card, 0)
        self.setLayout(layout)

    def upload_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose photo", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.photo_path = path
            pix = QPixmap(path).scaled(self.photo_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_preview.setPixmap(pix)

    def register_face(self):
        if not self.nid.text().strip():
            QMessageBox.warning(self, "Missing NID", "Please enter NID before registering face.")
            return
        # TODO: integrate OpenCV capture for real registration
        QMessageBox.information(self, "Face registration", f"(Demo) Face registered for NID {self.nid.text().strip()}")

    def save_voter(self):
        nid = self.nid.text().strip()
        name = self.name.text().strip()
        if not nid or not name:
            QMessageBox.warning(self, "Missing fields", "NID and Full name are required.")
            return
        voters.append({
            "nid": nid, "name": name,
            "dob": self.dob.date().toString("yyyy-MM-dd"),
            "constituency": self.const.currentText(),
            "face": bool(self.photo_path),
            "voted": False
        })
        QMessageBox.information(self, "Saved", f"Voter '{name}' saved.")
        self.nid.clear(); self.name.clear(); self.addr.clear(); self.photo_preview.clear()

class VoterListPage(QWidget):
    def __init__(self, appwin):
        super().__init__()
        self.appwin = appwin
        self.build()

    def build(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)
        root.addWidget(title_label("Voter List", 18))

        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by NID or name")
        sbtn = QPushButton("Search")
        sbtn.setProperty("class", "primary")
        sbtn.clicked.connect(self.populate)
        search_row.addWidget(self.search)
        search_row.addWidget(sbtn)
        root.addLayout(search_row)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["NID","Name","DOB","Constituency","Face","Voted"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table)
        self.setLayout(root)
        self.populate()

    def populate(self):
        q = self.search.text().lower().strip()
        filtered = [v for v in voters if q in v["nid"].lower() or q in v["name"].lower()]
        self.table.setRowCount(len(filtered))
        for r, v in enumerate(filtered):
            self.table.setItem(r, 0, QTableWidgetItem(v["nid"]))
            self.table.setItem(r, 1, QTableWidgetItem(v["name"]))
            self.table.setItem(r, 2, QTableWidgetItem(v["dob"]))
            self.table.setItem(r, 3, QTableWidgetItem(v["constituency"]))
            self.table.setItem(r, 4, QTableWidgetItem("✔" if v["face"] else "✖"))
            self.table.setItem(r, 5, QTableWidgetItem("Yes" if v["voted"] else "No"))

class CandidatePage(QWidget):
    def __init__(self, appwin):
        super().__init__()
        self.appwin = appwin
        self.build()
    def build(self):
        root = QVBoxLayout()
        root.setContentsMargins(16,12,16,12)
        root.addWidget(title_label("Candidates", 18))
        add = QPushButton("Add Candidate")
        add.setProperty("class", "primary")
        add.setFixedWidth(140)
        add.clicked.connect(self.open_add_dialog)
        root.addWidget(add, alignment=Qt.AlignLeft)
        root.addSpacing(8)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.cards = QVBoxLayout()
        self.cards.setSpacing(10)
        content.setLayout(self.cards)
        scroll.setWidget(content)
        root.addWidget(scroll)
        self.setLayout(root)
        self.refresh()

    def refresh(self):
        # clear
        for i in reversed(range(self.cards.count())):
            w = self.cards.itemAt(i).widget()
            if w:
                w.setParent(None)
        for c in candidates:
            card = RoundFrame()
            card.setProperty("class", "card")
            h = QHBoxLayout()
            info = QVBoxLayout()
            info.addWidget(QLabel(f"<b>{c['name']}</b>"))
            info.addWidget(QLabel(f"{c['party']} — {c['constituency']}"))
            h.addLayout(info)
            h.addStretch()
            e = QPushButton("Edit"); e.setFixedWidth(70)
            d = QPushButton("Delete"); d.setFixedWidth(70)
            d.clicked.connect(lambda checked, name=c["name"]: self.delete(name))
            h.addWidget(e); h.addWidget(d)
            card.setLayout(h)
            self.cards.addWidget(card)

    def open_add_dialog(self):
        dlg = AddCandidateDialog()
        if dlg.exec_():
            data = dlg.get_data()
            candidates.append(data)
            QMessageBox.information(self, "Added", f"Candidate '{data['name']}' added.")
            self.refresh()

    def delete(self, name):
        r = QMessageBox.question(self, "Delete", f"Delete candidate {name}?", QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            global candidates
            candidates = [c for c in candidates if c["name"] != name]
            self.refresh()

class AddCandidateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Candidate")
        self.build()
    def build(self):
        v = QVBoxLayout()
        f = QFormLayout()
        self.name = QLineEdit(); self.party = QLineEdit()
        self.const = QComboBox(); self.const.addItems(["North","South","East","West"])
        f.addRow("Name", self.name); f.addRow("Party", self.party); f.addRow("Constituency", self.const)
        v.addLayout(f)
        br = QHBoxLayout()
        save = QPushButton("Save"); save.setProperty("class", "primary"); save.clicked.connect(self.accept)
        cancel = QPushButton("Cancel"); cancel.clicked.connect(self.reject)
        br.addStretch(); br.addWidget(save); br.addWidget(cancel)
        v.addLayout(br)
        self.setLayout(v)
        self.setFixedWidth(380)
    def get_data(self):
        return {"name": self.name.text().strip(), "party": self.party.text().strip(), "constituency": self.const.currentText()}

# ---------------------------
# Main App Window
# ---------------------------
class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartEVM • Admin")
        self.setMinimumSize(800, 480)
        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # TopBar
        self.top = TopBar(self)
        root.addWidget(self.top)

        # Main content (side nav + pages)
        main = QHBoxLayout()
        main.setContentsMargins(12,12,12,12)
        main.setSpacing(12)

        # Side nav
        sidenav = RoundFrame()
        sidenav.setObjectName("sidenav")
        sidenav.setFixedWidth(160)
        navlayout = QVBoxLayout()
        navlayout.setContentsMargins(12,12,12,12)
        navlayout.setSpacing(8)
        navlayout.addWidget(QLabel("Navigation"))
        btns = [
            ("Home", lambda: self.switch_page("home")),
            ("Dashboard", lambda: self.switch_page("dashboard")),
            ("Register Voter", lambda: self.switch_page("register")),
            ("Voter List", lambda: self.switch_page("voter_list")),
            ("Candidates", lambda: self.switch_page("candidates")),
        ]
        for text, cb in btns:
            b = QPushButton(text)
            b.clicked.connect(cb)
            b.setFixedHeight(40)
            navlayout.addWidget(b)
        navlayout.addStretch()
        sidenav.setLayout(navlayout)

        # Pages stack
        self.stack = QStackedWidget()
        self.pages = {
            "home": HomePage(self),
            "dashboard": DashboardPage(self),
            "register": RegisterVoterPage(self),
            "voter_list": VoterListPage(self),
            "candidates": CandidatePage(self),
        }
        for p in self.pages.values():
            self.stack.addWidget(p)
        self.stack.setCurrentWidget(self.pages["home"])

        main.addWidget(sidenav)
        main.addWidget(self.stack, 1)
        root.addLayout(main)
        self.setLayout(root)

    def switch_page(self, name):
        if name in self.pages:
            self.stack.setCurrentWidget(self.pages[name])
            self.top.sync.setText("Last sync: now")

# ---------------------------
# Run
# ---------------------------
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_QSS)
    win = AdminWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
