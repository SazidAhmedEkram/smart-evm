import FaceRecognition
import sqlite3
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QWidget, QMessageBox
)
from PyQt6.QtCore import Qt

# ----------------- Face Scan & Voting Flow -----------------

def faceForVoting(self):
    # Run face scan
    name, nid, status = FaceRecognition.vote()  # always returns a 3-tuple

    # store current voter NID
    self.current_voter_nid = nid

    # Update GUI labels safely
    self.ui.name7.setText(f"Name: {name if name else 'Unknown'}")
    self.ui.nid7.setText(f"Nid: {nid if nid else '------'}")
    self.ui.status7.setText(f"Status: {status}")

    # Disconnect previous clicks
    try:
        self.ui.startVotingBtn7.clicked.disconnect()
    except TypeError:
        pass

    # Update button based on status
    if status == "Verified":
        self.ui.status7.setStyleSheet("color: green;")
        self.ui.startVotingBtn7.setStyleSheet(
            """
            QPushButton {
                border-radius: 10px;
                background: rgb(94, 194, 105);
                color: White;
                font: Bold;
            }
            QPushButton:hover {
                background: rgb(76, 162, 84);
            }
            QPushButton:pressed {
                background: rgb(21, 153, 71);
            }
            """
        )
        self.ui.startVotingBtn7.setText("Start Voting")
        # connect to voting()
        self.ui.startVotingBtn7.clicked.connect(self.votingBtn7)

    else:
        self.ui.status7.setStyleSheet("color: red;")
        self.ui.startVotingBtn7.setStyleSheet(
            """
            QPushButton {
                border-radius: 10px;
                background: rgb(255, 0, 0);
                color: White;
                font: Bold;
            }
            QPushButton:hover {
                background: rgb(200, 0, 0);
            }
            QPushButton:pressed {
                background: rgb(150, 0, 0);
            }
            """
        )
        self.ui.startVotingBtn7.setText("Back")
        # go back to previous page
        self.ui.startVotingBtn7.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(5)
        )

# ----------------- Voting Page -----------------

def voting(self):
    if not hasattr(self, "current_voter_nid") or not self.current_voter_nid:
        QMessageBox.warning(self, "Error", "No verified voter.")
        return

    load_candidate_list(self, self.current_voter_nid)

    # go to candidate vote page
    self.ui.stackedWidget.setCurrentIndex(7)

# ----------------- Candidate Fetch -----------------

def get_candidates():
    conn = sqlite3.connect("evmDatabase.db")
    c = conn.cursor()
    # column is id, not candidate_id
    c.execute("SELECT id, name, party FROM candidates")
    candidates = c.fetchall()
    conn.close()
    return candidates

# ----------------- Load Candidate Cards -----------------
def load_candidate_list(self, voter_nid):
    candidates = get_candidates()

    # get layout
    layout = self.ui.verticalLayout_candidates  # QVBoxLayout inside scroll area
    if isinstance(layout, QWidget):
        layout = layout.layout()

    # clear previous widgets
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()

    self.cards = []  # store cards for Arduino selection

    # Ensure scroll area resizes with content
    self.ui.scrollArea.setWidgetResizable(True)
    layout.setSpacing(15)  # space between cards

    for cand_id, name, party in candidates:
        # --- Card Frame ---
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: None;
                padding: 10px;
            }
            QFrame:hover {
                background-color: rgb(120, 160, 240);
            }
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setMinimumHeight(80)  # minimum height for content

        # --- Card Layout ---
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(2, 2, 2, 2)
        card_layout.setSpacing(1)

        # Candidate ID + Name
        label_id_name = QLabel(f"ID: {cand_id}  |  {name}")
        label_id_name.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;"
                                    "background-color: transparent;")
        label_id_name.setWordWrap(True)
        label_id_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label_id_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Candidate Party
        label_party = QLabel(f"Party: {party}")
        label_party.setStyleSheet("font-size: 15px; color: #555555;"
                                  "background-color: transparent;")
        label_party.setWordWrap(True)
        label_party.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label_party.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Add widgets
        card_layout.addWidget(label_id_name)
        card_layout.addWidget(label_party)
        card_layout.addStretch()  # ensures proper spacing inside card

        # Add to main layout
        layout.addWidget(card)
        self.cards.append(card)

    # Add stretch at the end so cards align nicely at the top
    layout.addStretch()

# ----------------- Cast Vote -----------------

def cast_vote(self, voter_nid, candidate_id):
    conn = sqlite3.connect("evmDatabase.db")
    c = conn.cursor()

    # prevent double vote
    c.execute("SELECT has_voted FROM voters WHERE nid=?", (voter_nid,))
    hv = c.fetchone()
    if hv and hv[0] == 1:
        QMessageBox.warning(self, "Already voted", "This voter has already voted.")
        conn.close()
        return

    # save vote
    c.execute("INSERT INTO votes (nid, candidate_id) VALUES (?, ?)", (voter_nid, candidate_id))
    c.execute("UPDATE voters SET has_voted=1 WHERE nid=?", (voter_nid,))
    conn.commit()
    conn.close()

    QMessageBox.information(self, "Success", "Your vote has been recorded!")

    # return to home page
    self.ui.stackedWidget.setCurrentIndex(0)
