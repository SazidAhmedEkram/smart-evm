from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from ui_main import Ui_AdminDashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminDashboard()
        self.ui.setupUi(self)
        # After loading the UI
        self.ui.centralwidget.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout.setContentsMargins(0, 0, 0, 0)  # the top-level VBoxLayout
        self.ui.verticalLayout.setSpacing(32)  # or whatever you use between sections

        self.setWindowTitle("Electronic Voting Machine")
        self.setWindowIcon(QIcon("resources/logo.jpg"))

        #Add shadow to the cards and buttons
        cards = [self.ui.card2, self.ui.card1, self.ui.card4, self.ui.card3]
        for card in cards:
            self.addShadow(card)
        buttons = [self.ui.registerBtn, self.ui.electionBtn, self.ui.voterBtn,
                 self.ui.systemBtn, self.ui.votingBtn, self.ui.candidateBtn]
        for button in buttons:
            self.addShadowButton(button)

    def addShadow(self, widget):
        # ---------- Modern Card Shadow ----------
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)  # Softer blur
        shadow.setXOffset(2)  # Horizontal offset
        shadow.setYOffset(5)  # Vertical offset
        shadow.setColor(QColor(0, 0, 0, 50))  # Soft black with transparency
        widget.setGraphicsEffect(shadow)
    def addShadowButton(self, widget):
        # ---------- Buuton Shadow ----------
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)  # Softer blur
        shadow.setXOffset(0)  # Horizontal offset
        shadow.setYOffset(3)  # Vertical offset
        shadow.setColor(QColor(0, 0, 0, 33))  # Soft black with transparency
        widget.setGraphicsEffect(shadow)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
