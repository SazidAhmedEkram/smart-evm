from PyQt6.QtWidgets import QTableWidgetItem, QLabel, QWidget, QHBoxLayout, QPushButton, QHeaderView
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QHeaderView

def setup_voter_table(table):
    header = table.horizontalHeader()

    # 🔥 VERY IMPORTANT
    header.setStretchLastSection(False)

    # Use Interactive initially
    header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    # Set safe minimum widths
    table.setColumnWidth(0, 140)  # NID
    table.setColumnWidth(1, 200)  # Name
    table.setColumnWidth(2, 120)  # DOB
    table.setColumnWidth(3, 160)  # Constituency
    table.setColumnWidth(4, 140)  # Face
    table.setColumnWidth(5, 140)  # Status
    table.setColumnWidth(6, 120)  # Actions

    table.setWordWrap(False)
    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

def finalize_voter_table(table):
    header = table.horizontalHeader()

    # Now Qt knows actual content size
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

    # Flexible columns
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    # 🔥 Force recalculation
    table.resizeColumnsToContents()


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
    color = "#22c55e" if face_status == "OK" else "#f59e0b"

    label = QLabel(face_status)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet(f"""
        QLabel {{
            background-color: {color};
            color: white;
            padding: 6px 16px;
            border-radius: 14px;
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
        }}
    """)
    return label

def create_action_buttons():
    w = QWidget()
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
