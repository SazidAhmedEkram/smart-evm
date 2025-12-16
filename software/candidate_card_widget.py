from PyQt6.QtWidgets import QWidget
from candidate import Ui_Form

class CandidateCardWidget(QWidget):
    def __init__(self, candidate_data: dict):
        super().__init__()
        self.setContentsMargins(8, 8, 8, 8)
        self.setMinimumWidth(360)  # card width
        self.setMaximumWidth(420)  # optional
        self.setMinimumHeight(200)

        # Build UI
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Fill data
        self.set_data(candidate_data)

        # Button signals
        self.ui.edit3.clicked.connect(self.edit_clicked)
        self.ui.delete3.clicked.connect(self.delete_clicked)

    def set_data(self, data: dict):
        self.ui.name3.setText(data.get("name", ""))
        self.ui.constituency3.setText(data.get("constituency", ""))
        self.ui.party3.setText(data.get("party", ""))

    def edit_clicked(self):
        print("Edit:", self.ui.name3.text())

    def delete_clicked(self):
        print("Delete:", self.ui.name3.text())
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = QMainWindow()
#     window.show()
#     app.exec()
