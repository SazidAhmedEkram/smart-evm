from PyQt6.QtWidgets import (
    QGridLayout, QWidget, QVBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from candidate_card_widget import CandidateCardWidget
import sqlite3


# --- UI Setup Function ---
def set(ui):
    # 1. Get the container's layout. This must be a QVBoxLayout for addStretch.
    container_layout = ui.cardsContainer.layout()

    # Safety check: ensure we have a layout and it's the correct type for vertical stacking
    if not isinstance(container_layout, QVBoxLayout):
        # If it's a QGridLayout or None, the UI setup is wrong.
        # This message helps diagnose the issue if the error persists.
        print("Error: ui.cardsContainer layout is not a QVBoxLayout. Please fix the UI structure.")
        return

    # 2. Clear all existing items (widgets and spacers) from the container layout
    # This prepares the container for new content.
    while container_layout.count() > 0:
        item = container_layout.takeAt(0)

        widget = item.widget()
        if widget:
            widget.deleteLater()

        spacer = item.spacerItem()
        if spacer:
            # Explicitly remove the spacer item (the old stretch)
            container_layout.removeItem(item)

    candidates = load_candidates()

    if not candidates:
        # Add stretch to push the empty space to the top
        container_layout.addStretch()
        return

    # 3. Create the dedicated widget to hold the grid
    grid_widget = QWidget()
    grid_layout = QGridLayout(grid_widget)

    # Set appearance and margins
    grid_layout.setSpacing(10)
    grid_layout.setContentsMargins(10, 10, 10, 10)

    # Set Size Policy: Expands horizontally, but only takes the minimum vertical space
    # required for the cards. This is crucial for correct QScrollArea behavior.
    grid_widget.setSizePolicy(
        QSizePolicy.Policy.MinimumExpanding,
        QSizePolicy.Policy.Minimum
    )

    # 4. Populate the Grid
    columns = 3
    row = 0
    col = 0
    for candidate in candidates:
        card = CandidateCardWidget(candidate)
        grid_layout.addWidget(card, row, col)

        col += 1
        if col >= columns:
            col = 0
            row += 1

    # 5. Make columns equal width and stretchable within the grid
    for c in range(columns):
        grid_layout.setColumnStretch(c, 1)

    # 6. Add the completed grid widget to the main container layout (the QVBoxLayout)
    container_layout.addWidget(grid_widget)

    # 7. Add a stretch to the QVBoxLayout.
    # This correctly pushes the content (grid_widget) to the top of the scrollable area.
    # THIS is the fixed line that resolves the original Attribute Error (it's called on QVBoxLayout).
    container_layout.addStretch()


# --- Database Loading Function ---
def load_candidates():
    """Loads candidate data from the SQLite database."""
    conn = sqlite3.connect("evmDatabase.db")
    cursor = conn.cursor()

    # NOTE: Ensure the number of columns selected matches the fields expected by the card
    cursor.execute("""
                   SELECT name, party, constituency
                   FROM candidates
                   """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": r[0],
            "party": r[1],
            "constituency": r[2]
        }
        for r in rows
    ]