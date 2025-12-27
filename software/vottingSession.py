import FaceRecognition
import sqlite3
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy, QWidget, QMessageBox
from PyQt6.QtCore import Qt
import threading
import VoiceInstructions
import arduino

# ----------------- Voting Session Class -----------------
class VotingSession:
    def __init__(self, main_window):
        self.main_window = main_window
        self.voting_active = False
        self.cards = []

    # ----------------- Face Scan -----------------
    def faceForVoting(self):
        name, nid, status = FaceRecognition.vote()  # always returns 3-tuple
        self.main_window.current_voter_nid = nid

        # Update GUI labels
        self.main_window.ui.name7.setText(f"Name: {name if name else 'Unknown'}")
        self.main_window.ui.nid7.setText(f"Nid: {nid if nid else '------'}")
        self.main_window.ui.status7.setText(f"Status: {status}")

        # Disconnect previous clicks
        try:
            self.main_window.ui.startVotingBtn7.clicked.disconnect()
        except TypeError:
            pass

        # Verified voter
        if status == "Verified":
            self.main_window.ui.status7.setStyleSheet("color: green;")
            self.main_window.ui.startVotingBtn7.setStyleSheet("""
                QPushButton { border-radius: 10px; background: rgb(94, 194, 105); color: White; font: Bold; }
                QPushButton:hover { background: rgb(76, 162, 84); }
                QPushButton:pressed { background: rgb(21, 153, 71); }
            """)
            self.main_window.ui.startVotingBtn7.setText("Start Voting")
            try:
                self.main_window.ui.startVotingBtn7.clicked.disconnect()
            except TypeError:
                pass
            self.main_window.ui.startVotingBtn7.clicked.connect(self.voting)

        # Not verified
        else:
            self.main_window.ui.status7.setStyleSheet("color: red;")
            self.main_window.ui.startVotingBtn7.setStyleSheet("""
                QPushButton { border-radius: 10px; background: rgb(255, 0, 0); color: White; font: Bold; }
                QPushButton:hover { background: rgb(200, 0, 0); }
                QPushButton:pressed { background: rgb(150, 0, 0); }
            """)
            self.main_window.ui.startVotingBtn7.setText("Back")
            self.main_window.ui.startVotingBtn7.clicked.connect(
                lambda: self.main_window.ui.stackedWidget.setCurrentIndex(5)
            )
        self.main_window.ui.stackedWidget.setCurrentIndex(6)
    # ----------------- Voting -----------------
    def voting(self):
        if not getattr(self.main_window, "current_voter_nid", None):
            QMessageBox.warning(self.main_window, "Error", "No verified voter.")
            return

        self.startArduinoVoting()

    # ----------------- Candidate Fetch -----------------
    @staticmethod
    def get_candidates():
        conn = sqlite3.connect("evmDatabase.db")
        c = conn.cursor()
        c.execute("SELECT id, name, party FROM candidates")
        candidates = c.fetchall()
        conn.close()
        return candidates

    # ----------------- Load Candidate Cards -----------------
    def load_candidate_list(self):
        candidates = self.get_candidates()
        layout = self.main_window.ui.verticalLayout_candidates
        if isinstance(layout, QWidget):
            layout = layout.layout()

        # Clear previous cards
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.cards = []

        self.main_window.ui.scrollArea.setWidgetResizable(True)
        layout.setSpacing(15)

        for cand_id, name, party in candidates:
            card = QFrame()
            card.setStyleSheet("""
                QFrame { background-color: #ffffff; border-radius: 15px; border: None; padding: 10px; }
                QFrame:hover { background-color: rgb(120, 160, 240); }
            """)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            card.setMinimumHeight(80)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(2, 2, 2, 2)
            card_layout.setSpacing(1)

            label_id_name = QLabel(f"ID: {cand_id}  |  {name}")
            label_id_name.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333; background-color: transparent;")
            label_id_name.setWordWrap(True)
            label_id_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            label_id_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            label_party = QLabel(f"Party: {party}")
            label_party.setStyleSheet("font-size: 15px; color: #555555; background-color: transparent;")
            label_party.setWordWrap(True)
            label_party.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            label_party.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            card_layout.addWidget(label_id_name)
            card_layout.addWidget(label_party)
            card_layout.addStretch()

            layout.addWidget(card)
            self.cards.append(card)

        layout.addStretch()

        # Voice instruction after loading candidates
        # threading.Thread(target=lambda: VoiceInstructions.speak(
        #     "Candidates loaded. Please select your candidate using the buttons."
        # ), daemon=True).start()

    # ----------------- Cast Vote -----------------
    @staticmethod
    def cast_vote(main_window, voter_nid, candidate_id):
        conn = sqlite3.connect("evmDatabase.db")
        c = conn.cursor()
        c.execute("SELECT has_voted FROM voters WHERE nid=?", (voter_nid,))
        hv = c.fetchone()
        if hv and hv[0] == 1:
            QMessageBox.warning(main_window, "Already voted", "This voter has already voted.")
            conn.close()
            return
        c.execute("INSERT INTO votes (nid, candidate_id) VALUES (?, ?)", (voter_nid, candidate_id))
        c.execute("UPDATE voters SET has_voted=1 WHERE nid=?", (voter_nid,))
        conn.commit()
        conn.close()
        QMessageBox.information(main_window, "Success", "Your vote has been recorded!")
        main_window.ui.stackedWidget.setCurrentIndex(5)

    # ----------------- Arduino Voting -----------------
    def startArduinoVoting(self):
        # Stop previous listener
        if hasattr(self.main_window, "arduino") and self.main_window.arduino:
            self.main_window.arduino.stop()
            self.main_window.arduino = None

        # Load candidates and show page
        self.load_candidate_list()
        self.main_window.ui.stackedWidget.setCurrentIndex(7)
        self.voting_active = True

        # Start Arduino listener
        self.main_window.arduino = arduino.ArduinoListener('/dev/cu.usbmodem141011')
        self.main_window.arduino.vote_signal.connect(self.arduinoVoteReceived)

        threading.Thread(target=lambda: VoiceInstructions.speak(
            "Voting started. Please press the button of your chosen candidate."
        ), daemon=True).start()

    def arduinoVoteReceived(self, button_id):
        if not self.voting_active:
            return
        voter_nid = getattr(self.main_window, "current_voter_nid", None)
        if not voter_nid:
            return

        # Map Arduino button to DB candidate
        button_to_candidate = {1: 1, 2: 2}  # adjust to match with DB
        candidate_id = button_to_candidate.get(button_id)
        if not candidate_id:
            return

        # Highlight selected candidate card
        index = None
        for idx, (cand_id, name, party) in enumerate(self.get_candidates()):
            if cand_id == candidate_id:
                index = idx
                break
        if index is not None:
            for i, card in enumerate(self.cards):
                if i == index:
                    card.setStyleSheet("background-color: rgb(94, 194, 105); border-radius: 15px;")
                else:
                    card.setStyleSheet("background-color: #ffffff; border-radius: 15px;")

        # Cast vote
        self.cast_vote(self.main_window, voter_nid, candidate_id)
        self.voting_active = False

        # Voice feedback
        threading.Thread(target=lambda: VoiceInstructions.speak(
            f"Vote for candidate {candidate_id} has been recorded."
        ), daemon=True).start()
