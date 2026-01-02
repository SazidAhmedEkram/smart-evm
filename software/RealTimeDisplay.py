from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtWidgets import QLabel

def set_date_time_am_pm(label: QLabel):
    """
    Set a QLabel to show the current date, time in 12-hour format with AM/PM, and day,
    updating every second.

    :param label: QLabel instance to update
    """
    def update():
        now = QDateTime.currentDateTime()
        # Format: Day, dd MMM yyyy | hh:mm:ss AP (12-hour with AM/PM)
        label.setText(now.toString("dddd, dd MMMM yyyy | hh:mm:ss AP"))

    # Initial update
    update()

    # Timer to update every second
    timer = QTimer(label)  # parent to label so it doesn't get garbage collected
    timer.timeout.connect(update)
    timer.start(1000)


import sqlite3
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel


def set_total_voter(label: QLabel, db_path: str):
    """
    Dynamically update a QLabel with the total number of voters from the database.

    :param label: QLabel instance to update
    :param db_path: Path to your SQLite database
    """

    def update():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Assuming your voters table is named 'voters'
            cursor.execute("SELECT COUNT(*) FROM voters")
            total = cursor.fetchone()[0]

            label.setText(f"{total}")

            conn.close()
        except Exception as e:
            label.setText(f"Error: {e}")

    # Initial update
    update()

    # Timer to refresh every 5 seconds (you can adjust)
    timer = QTimer(label)
    timer.timeout.connect(update)
    timer.start(5000)  # 5000 ms = 5 seconds


import sqlite3
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel


def set_registered_face(label: QLabel, db_path: str):
    """
    Dynamically update a QLabel with the number of voters
    who have registered their face (face_encoding is not NULL).

    :param label: QLabel instance to update
    :param db_path: Path to your SQLite database
    """

    def update():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Count rows where face_encoding is not NULL
            cursor.execute("SELECT COUNT(*) FROM voters WHERE face_encoding IS NOT NULL")
            registered_count = cursor.fetchone()[0]

            label.setText(f"{registered_count}")

            conn.close()
        except Exception as e:
            label.setText(f"Error: {e}")

    # Initial update
    update()

    # Timer to refresh every 5 seconds
    timer = QTimer(label)
    timer.timeout.connect(update)
    timer.start(5000)  # update every 5 seconds

import sqlite3
from PyQt6.QtCore import QTimer, QDate
from PyQt6.QtWidgets import QLabel

def set_votes_cast_today(label: QLabel, db_path: str):

    def update():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get today's date in YYYY-MM-DD format
            today = QDate.currentDate().toString("yyyy-MM-dd")

            # Count votes where vote_timestamp starts with today's date
            cursor.execute(
                "SELECT COUNT(*) FROM votes WHERE vote_timestamp LIKE ?",
                (f"{today}%",)
            )
            votes_today = cursor.fetchone()[0]

            label.setText(f"{votes_today}")

            conn.close()
        except Exception as e:
            label.setText(f"Error: {e}")

    update()

    # Timer to refresh every 5 seconds
    timer = QTimer(label)
    timer.timeout.connect(update)
    timer.start(5000)


import sqlite3
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel

def set_active_election(label: QLabel, db_path: str):
    """
    Dynamically update a QLabel with the number of active elections
    (Status = 'Ongoing') from the active_elections table.

    :param label: QLabel instance to update
    :param db_path: Path to your SQLite database
    """
    def update():
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Count elections where Status is 'Ongoing'
            cursor.execute("SELECT COUNT(*) FROM active_elections WHERE Status = 'Ongoing'")
            active_count = cursor.fetchone()[0]

            label.setText(f"{active_count}")

            conn.close()
        except Exception as e:
            label.setText(f"Error: {e}")

    # Initial update
    update()

    # Timer to refresh every 5 seconds
    timer = QTimer(label)
    timer.timeout.connect(update)
    timer.start(5000)
