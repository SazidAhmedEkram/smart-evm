from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(0, 0, 1200, 750)
        self.setStyleSheet("background-color: #f9fafb;")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        main_layout = QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # ----------------- Header -----------------
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        self.label_title = QLabel("Admin Dashboard")
        self.label_title.setStyleSheet("color: #1f2937;")
        self.label_title.setFont(self.font())
        self.label_title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #1f2937;")
        header_layout.addWidget(self.label_title)

        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.btnSettings = QPushButton("⚙️")
        self.btnSettings.setMinimumSize(45, 45)
        self.btnSettings.setStyleSheet("border: none; font-size: 20px; background: transparent;")
        header_layout.addWidget(self.btnSettings)

        # ----------------- Stats Grid -----------------
        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(25)
        stats_grid.setVerticalSpacing(20)
        main_layout.addLayout(stats_grid)

        # Card templates
        def create_card(icon, number, text, color="#ffffff"):
            card = QFrame()
            card.setMinimumHeight(150)
            card.setStyleSheet(f"background: {color}; border-radius: 16px; border: 1px solid #e5e7eb;")
            layout = QVBoxLayout(card)
            layout.setContentsMargins(25, 25, 25, 25)

            lbl_icon = QLabel(icon)
            lbl_icon.setFont(self.font())
            lbl_icon.setStyleSheet(f"color: {color}; font-size: 48pt;")
            layout.addWidget(lbl_icon)

            lbl_number = QLabel(number)
            lbl_number.setFont(self.font())
            lbl_number.setStyleSheet("font-size: 32pt; font-weight: bold;")
            layout.addWidget(lbl_number)

            lbl_text = QLabel(text)
            lbl_text.setStyleSheet("color: #6b7280;")
            layout.addWidget(lbl_text)

            return card

        # Total Voters
        card_voters = QFrame()
        card_voters.setMinimumHeight(150)
        card_voters.setStyleSheet("background: white; border-radius: 16px; border: 1px solid #e5e7eb;")
        layout_voters = QVBoxLayout(card_voters)
        layout_voters.setContentsMargins(25, 25, 25, 25)
        icon_voters = QLabel("👥")
        icon_voters.setStyleSheet("color: #2563eb; font-size: 48pt;")
        layout_voters.addWidget(icon_voters)
        lbl_total_voters = QLabel("12,543")
        lbl_total_voters.setStyleSheet("font-size: 32pt; font-weight: bold;")
        layout_voters.addWidget(lbl_total_voters)
        lbl_text_voters = QLabel("Total Voters")
        lbl_text_voters.setStyleSheet("color: #6b7280;")
        layout_voters.addWidget(lbl_text_voters)
        stats_grid.addWidget(card_voters, 0, 0)

        # Registered Faces
        card_faces = QFrame()
        card_faces.setMinimumHeight(150)
        card_faces.setStyleSheet("background: white; border-radius: 16px; border: 1px solid #e5e7eb;")
        layout_faces = QVBoxLayout(card_faces)
        layout_faces.setContentsMargins(25, 25, 25, 25)
        icon_faces = QLabel("✅")
        icon_faces.setStyleSheet("color: #16a34a; font-size: 48pt;")
        layout_faces.addWidget(icon_faces)
        lbl_registered_faces = QLabel("11,892")
        lbl_registered_faces.setStyleSheet("font-size: 32pt; font-weight: bold;")
        layout_faces.addWidget(lbl_registered_faces)
        lbl_text_faces = QLabel("Registered Faces")
        lbl_text_faces.setStyleSheet("color: #6b7280;")
        layout_faces.addWidget(lbl_text_faces)
        stats_grid.addWidget(card_faces, 0, 1)

        # Votes Today
        card_votes_today = QFrame()
        card_votes_today.setMinimumHeight(150)
        card_votes_today.setStyleSheet("background: white; border-radius: 16px; border: 1px solid #e5e7eb;")
        layout_votes = QVBoxLayout(card_votes_today)
        layout_votes.setContentsMargins(25, 25, 25, 25)
        icon_votes = QLabel("📩")
        icon_votes.setStyleSheet("color: #ea580c; font-size: 48pt;")
        layout_votes.addWidget(icon_votes)
        lbl_votes_today = QLabel("8,234")
        lbl_votes_today.setStyleSheet("font-size: 32pt; font-weight: bold;")
        layout_votes.addWidget(lbl_votes_today)
        lbl_text_votes = QLabel("Votes Cast Today")
        lbl_text_votes.setStyleSheet("color: #6b7280;")
        layout_votes.addWidget(lbl_text_votes)
        stats_grid.addWidget(card_votes_today, 0, 2)

        # Active Elections
        card_elections = QFrame()
        card_elections.setMinimumHeight(150)
        card_elections.setStyleSheet("background: white; border-radius: 16px; border: 1px solid #e5e7eb;")
        layout_elections = QVBoxLayout(card_elections)
        layout_elections.setContentsMargins(25, 25, 25, 25)
        icon_elections = QLabel("📅")
        icon_elections.setStyleSheet("color: #ec4899; font-size: 48pt;")
        layout_elections.addWidget(icon_elections)
        lbl_active_elections = QLabel("3")
        lbl_active_elections.setStyleSheet("font-size: 32pt; font-weight: bold;")
        layout_elections.addWidget(lbl_active_elections)
        lbl_text_elections = QLabel("Active Elections")
        lbl_text_elections.setStyleSheet("color: #6b7280;")
        layout_elections.addWidget(lbl_text_elections)
        stats_grid.addWidget(card_elections, 0, 3)

        # ----------------- Line -----------------
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #e5e7eb;")
        main_layout.addWidget(line)

        # ----------------- Menu Grid -----------------
        menu_grid = QGridLayout()
        menu_grid.setHorizontalSpacing(30)
        menu_grid.setVerticalSpacing(25)
        main_layout.addLayout(menu_grid)

        def create_menu_button(text):
            btn = QPushButton(text)
            btn.setMinimumSize(180, 110)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #e5e7eb;
                    border-radius: 16px;
                    background: white;
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    border-color: #3b82f6;
                    background: #eff6ff;
                }
            """)
            return btn

        menu_grid.addWidget(create_menu_button("➕ Register Voter"), 0, 0)
        menu_grid.addWidget(create_menu_button("📋 Voter List"), 0, 1)
        menu_grid.addWidget(create_menu_button("⚙️ Election Setup"), 0, 2)
        menu_grid.addWidget(create_menu_button("👥 Candidate List"), 1, 0)
        menu_grid.addWidget(create_menu_button("📈 Voting Reports"), 1, 1)
        menu_grid.addWidget(create_menu_button("📊 System Logs"), 1, 2)

        # Vertical spacer
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

# ----------------- Run Application -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
