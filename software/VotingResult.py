# db_results_loader.py

import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

DB_NAME = "evmDatabase.db"

def load_candidate_results(table_widget, search_text="", sort_option="Votes (High to Low)"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Map ComboBox text to SQL ORDER BY clauses
    sort_mapping = {
        "Votes (High to Low)": "total_votes DESC",
        "Votes (Low to High)": "total_votes ASC",
        "Name (A-Z)": "c.name ASC",
        "Party": "c.party ASC"
    }
    order_by = sort_mapping.get(sort_option, "total_votes DESC")

    query = f"""
            SELECT c.name, 
                   c.party, 
                   c.constituency, 
                   COUNT(v.id) AS total_votes
            FROM candidates c
            LEFT JOIN votes v ON c.id = v.candidate_id
            WHERE c.name LIKE ?
            GROUP BY c.id
            ORDER BY {order_by};
            """

    search_param = f"%{search_text}%"
    cursor.execute(query, (search_param,))
    rows = cursor.fetchall()

    # Table Setup
    table_widget.setRowCount(len(rows))
    table_widget.setColumnCount(4)
    table_widget.setHorizontalHeaderLabels(["Name", "Party", "Constituency", "Total Votes"])

    # Header Styling
    header = table_widget.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    header_font = QFont()
    header_font.setPointSize(14)
    header_font.setBold(True)
    header.setFont(header_font)
    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    # Populate Data
    for row_index, row_data in enumerate(rows):
        for col_index, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table_widget.setItem(row_index, col_index, item)

    conn.close()