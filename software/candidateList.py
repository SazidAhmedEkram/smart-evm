from candidate_card_widget import CandidateCardWidget
import sqlite3
from PyQt6.QtWidgets import QGridLayout, QWidget
from candidate_card_widget import CandidateCardWidget
import sqlite3

def set(ui):
    container = ui.cardsContainer
    main_layout = container.layout()  # QVBoxLayout

    # Clear old content
    while main_layout.count():
        item = main_layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()

    candidates = load_candidates()

    columns = 2
    row = 0
    col = 0

    grid_widget = QWidget()
    grid_layout = QGridLayout(grid_widget)
    grid_layout.setSpacing(16)
    grid_layout.setContentsMargins(10, 10, 10, 10)



    for candidate in candidates:
        card = CandidateCardWidget(candidate)

        grid_layout.addWidget(card, row, col)

        col += 1
        if col >= columns:
            col = 0
            row += 1

    main_layout.addWidget(grid_widget)
def load_candidates():
    conn = sqlite3.connect("evmDatabase.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, party, constituency
        FROM candidates
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": r[0],
            "party": r[1],          # ✅ correct
            "constituency": r[2]    # ✅ correct
        }
        for r in rows
    ]
