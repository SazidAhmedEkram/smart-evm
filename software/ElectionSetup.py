from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QPushButton
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtCore import QDateTime
import sqlite3


def save_election(ui, parent=None):
    # ---------- EXTRACT DATA FROM UI ----------
    name = ui.electionName10.text().strip()
    date_val = ui.electionDate10.date()
    start_time = ui.startTime10.time()
    end_time = ui.endTime10.time()

    # ---------- VALIDATION ----------
    if not name:
        QMessageBox.warning(parent, "Validation Error", "Election name cannot be empty.")
        return False

    if len(name) < 3:
        QMessageBox.warning(parent, "Validation Error", "Election name must be at least 3 characters long.")
        return False

    if date_val < QDate.currentDate():
        QMessageBox.warning(parent, "Validation Error", "Election date cannot be in the past.")
        return False

    if start_time == end_time:
        QMessageBox.warning(parent, "Validation Error", "Start time and end time cannot be the same.")
        return False

    if start_time > end_time:
        QMessageBox.warning(parent, "Validation Error", "Start time cannot be later than end time.")
        return False

    # ---------- CONVERT TO STRING ----------
    date_str = date_val.toString("yyyy-MM-dd")
    start_str = start_time.toString("HH:mm")
    end_str = end_time.toString("HH:mm")

    # ---------- CHECK FOR OVERLAPPING ELECTIONS ----------
    try:
        conn = sqlite3.connect('evmDatabase.db')
        cursor = conn.cursor()

        # Fetch all elections on the same date
        cursor.execute("SELECT start_time, end_time FROM active_elections WHERE election_date=?", (date_str,))
        elections = cursor.fetchall()

        new_start = QDateTime.fromString(f"{date_str} {start_str}", "yyyy-MM-dd HH:mm")
        new_end = QDateTime.fromString(f"{date_str} {end_str}", "yyyy-MM-dd HH:mm")

        for existing in elections:
            existing_start = QDateTime.fromString(f"{date_str} {existing[0]}", "yyyy-MM-dd HH:mm")
            existing_end = QDateTime.fromString(f"{date_str} {existing[1]}", "yyyy-MM-dd HH:mm")

            # Check for overlap
            if not (new_end <= existing_start or new_start >= existing_end):
                QMessageBox.warning(parent, "Validation Error", "This election overlaps with an existing election.")
                return False

        # ---------- INSERT INTO DB ----------
        cursor.execute("""
            INSERT INTO active_elections (election_name, election_date, start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, date_str, start_str, end_str, 'Upcoming'))

        conn.commit()
        QMessageBox.information(parent, "Success", "Election saved successfully!")
        return True

    except sqlite3.Error as e:
        QMessageBox.critical(parent, "Database Error", f"Error saving election: {e}")
        return False

    finally:
        if conn:
            conn.close()


def update_election_status():
    now = QDateTime.currentDateTime()

    try:
        conn = sqlite3.connect('evmDatabase.db')
        cursor = conn.cursor()

        # Fetch all elections ordered by start time
        cursor.execute("SELECT id, election_date, start_time, end_time, status FROM active_elections ORDER BY election_date, start_time")
        elections = cursor.fetchall()

        ongoing_set = False  # Flag to ensure only one election is Ongoing

        for election in elections:
            election_id, date_str, start_str, end_str, old_status = election
            start_dt = QDateTime.fromString(f"{date_str} {start_str}", "yyyy-MM-dd HH:mm")
            end_dt = QDateTime.fromString(f"{date_str} {end_str}", "yyyy-MM-dd HH:mm")

            # Determine new status
            if now < start_dt:
                status = "Upcoming"
            elif start_dt <= now <= end_dt:
                if not ongoing_set:
                    status = "Ongoing"
                    ongoing_set = True  # Only the first overlapping election becomes Ongoing
                else:
                    status = "Upcoming"  # All others stay Upcoming
            else:
                status = "Completed"

            # Update in DB if status changed
            if status != old_status:
                cursor.execute("UPDATE active_elections SET status=? WHERE id=?", (status, election_id))

        conn.commit()
    except sqlite3.Error as e:
        print("Database error while updating status:", e)
    finally:
        if conn:
            conn.close()


import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton
from PyQt6.QtCore import Qt

def load_elections_into_table(window):
    """
    Populate tableWidget103 with elections and a modern Delete button.
    """
    try:
        conn = sqlite3.connect('evmDatabase.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, election_name, election_date, start_time, end_time, status 
            FROM active_elections 
            ORDER BY election_date, start_time
        """)
        elections = cursor.fetchall()

        table = window.ui.tableWidget103
        table.setRowCount(0)

        # 5 columns + delete button = 6
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["Election Name", "Election Date", "Start Time", "End Time", "Status", "Delete"]
        )

        for row_index, election in enumerate(elections):
            election_id = election[0]
            row_data = election[1:]

            table.insertRow(row_index)

            # normal columns
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_index, col_index, item)

            # ----- MODERN DELETE BUTTON -----
            delete_button = QPushButton("🗑️")
            delete_button.setCursor(Qt.CursorShape.PointingHandCursor)

            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff4d4d;
                    color: white;
                    border-radius: 12px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #cc0000;
                }
            """)

            delete_button.clicked.connect(
                lambda checked, eid=election_id: delete_election(window, eid)
            )

            table.setCellWidget(row_index, 5, delete_button)

        # stretch columns
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # -------- increase header font size --------
        font = QFont()
        font.setPointSize(12)  # choose size you like: 11–14 is good
        font.setBold(True)  # optional
        header.setFont(font)

    except sqlite3.Error as e:
        print("Database error while fetching elections:", e)

    finally:
        if conn:
            conn.close()



# ---------- Button Functionalities ----------

def delete_election(window, election_id):
    reply = QMessageBox.question(
        window,
        "Confirm Delete",
        "Are you sure you want to delete this election?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        try:
            conn = sqlite3.connect('evmDatabase.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM active_elections WHERE id=?", (election_id,))
            conn.commit()

            QMessageBox.information(window, "Deleted", "Election deleted successfully!")
            load_elections_into_table(window)

        except sqlite3.Error as e:
            QMessageBox.critical(window, "Database Error", f"Error deleting election: {e}")

        finally:
            if conn:
                conn.close()

def refresh_ongoing_election_ui(window):
    try:
        conn = sqlite3.connect("evmDatabase.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, election_name, election_date, start_time, end_time
            FROM active_elections
            WHERE status = 'Ongoing'
            ORDER BY election_date, start_time
            LIMIT 1
        """)

        row = cursor.fetchone()

    except sqlite3.Error as e:
        print("Database error:", e)
        return

    finally:
        if conn:
            conn.close()

    # ---------- Always show the card ----------
    window.ui.backCard10.setVisible(True)

    # ---------- No ongoing election ----------
    if not row:
        window.ongoing_election_id = None

        # change only activeElection101 background
        window.ui.activeElection101.setStyleSheet("""
            QWidget {
                background-color: #ff4d4d;  /* red */
                border-radius: 15px;
            }
        """)

        # text
        window.ui.name10.setText("No Active Election")
        window.ui.date10.setText("")
        window.ui.time10.setText("")

        return

    # ---------- There IS ongoing election ----------
    election_id, name, date, start, end = row
    window.ongoing_election_id = election_id

    # change only activeElection101 background
    window.ui.activeElection101.setStyleSheet("""
        QWidget {
            background-color: #2ecc71;  /* green */
            border-radius: 15px;
        }
    """)

    window.ui.name10.setText(name)
    window.ui.date10.setText(date)
    window.ui.time10.setText(f"{start} - {end}")

