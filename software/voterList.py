from PyQt6.QtWidgets import QTableWidgetItem, QLabel, QWidget, QHBoxLayout, QPushButton, QHeaderView
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QHeaderView

from software.BD_Constituencies import BD_Constituencies


def add_voter_row(table, voter):
    row = table.rowCount()
    table.insertRow(row)

    table.setItem(row, 0, QTableWidgetItem(voter["nid"]))
    table.setItem(row, 1, QTableWidgetItem(voter["name"]))
    table.setItem(row, 2, QTableWidgetItem(voter["dob"]))
    table.setItem(row, 3, QTableWidgetItem(voter["constituency"]))

    #allignment
    for col in range(4):
        table.item(row, col).setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

    table.setCellWidget(row, 4, create_face_pill(voter["face"]))
    table.setCellWidget(row, 5, create_status_pill(voter["status"]))
    table.setCellWidget(row, 6, create_action_buttons())

def load_voters(table, voters):
    table.setRowCount(0)
    for voter in voters:
        add_voter_row(table, voter)


def create_face_pill(face_status):
    color = "#22c55e" if face_status == "Registered" else "#f59e0b"

    label = QLabel(face_status)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet(f"""
        QLabel {{
            background-color: {color};
            color: white;
            padding: 6px 16px;
            border-radius: 14px;
            border : None;
            font-weight: 600;

        }}
    """)
    return label

def create_status_pill(status):
    color = "#2563eb" if status == "Voted" else "#94a3b8"

    label = QLabel(status)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet(f"""
        QLabel {{
            background-color: {color};
            color: white;
            padding: 6px 16px;
            border-radius: 14px;
            font-weight: 600;
            border : None;
        }}
    """)
    return label

def create_action_buttons():
    w = QWidget()
    w.setStyleSheet("""
    background-color: transparent;
    border: None""")
    layout = QHBoxLayout(w)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)


    view = QPushButton("👁")
    view.setFixedSize(32, 32)
    view.setStyleSheet("background:#2563eb; color:white; border-radius:8px;")

    delete = QPushButton("🗑")
    delete.setFixedSize(32, 32)
    delete.setStyleSheet("background:#ef4444; color:white; border-radius:8px;")

    layout.addWidget(view)
    layout.addWidget(delete)
    return w

def filter_voters(voters, search_text, constituency, status, face_filter):
    search_text = search_text.lower().strip()

    filtered = []

    for voter in voters:
        # 🔍 NID or Name
        if search_text:
            if (search_text not in voter["nid"].lower() and
                search_text not in voter["name"].lower()):
                continue

        # 🗺 Constituency
        if constituency and constituency != "All":
            if voter["constituency"] != constituency:
                continue

        # 🗳 Vote Status
        if status and status != "All":
            if voter["status"] != status:
                continue

        # ✅ Face Verification
        if face_filter and face_filter != "All":
            if voter["face"] != face_filter:
                continue

        filtered.append(voter)

    return filtered
