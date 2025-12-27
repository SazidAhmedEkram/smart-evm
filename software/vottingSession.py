import FaceRecognition

def faceForVoting(self):
    # Run face scan
    name, nid, status = FaceRecognition.vote()  # always returns a 3-tuple

    # store current voter NID
    self.current_voter_nid = nid

    # Update GUI labels safely
    self.name7.setText(f"Name: {name if name else 'Unknown'}")
    self.nid7.setText(f"Nid: {nid if nid else '------'}")
    self.status7.setText(f"Status: {status}")


    try:
        self.startVotingBtn7.clicked.disconnect()
    except TypeError:
        pass  # nothing was connected yet

    # Update button based on status
    if status == "Verified":
        self.status7.setStyleSheet("color: green;")
        self.startVotingBtn7.setStyleSheet(
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
        self.startVotingBtn7.setText("Start Voting")
        #self.startVotingBtn7.clicked.connect(self.voting)

    else:
        self.status7.setStyleSheet("color: red;")
        self.startVotingBtn7.setStyleSheet(
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
        self.startVotingBtn7.setText("Back")



def voting(self):
    import sqlite3
    import FaceRecognition

    # Check if a voter NID exists
    if not self.current_voter_nid:
        # Safety check
        self.status7.setText("Cannot vote: No verified voter")
        self.status7.setStyleSheet("color: red;")
        return

    # Fetch candidates
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()
    c.execute("SELECT id, name, party FROM candidates")
    candidates = c.fetchall()
    conn.close()

    # Call FaceRecognition function to vote
    selected_name, selected_party = FaceRecognition.show_candidates_and_vote(
        candidates, self.current_voter_nid
    )

    # Optional: update status label after voting
    self.status7.setText(f"Vote recorded for {selected_name} ({selected_party})")
    self.status7.setStyleSheet("color: blue;")  # or any color
