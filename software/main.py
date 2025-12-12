from PyQt6.QtGui import QColor, QIcon, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QGraphicsBlurEffect

from software import FaceRecognition
from ui_main import Ui_AdminDashboard

import BD_Constituencies
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
        #Setupn the database for the first time
        FaceRecognition.setup_database()
        #Add shadow to the cards and buttons
        cards = [self.ui.card2, self.ui.card1, self.ui.card4, self.ui.card3, self.ui.topBar1]
        for card in cards:
            self.addShadow(card)
        buttons = [self.ui.registerBtn, self.ui.electionBtn, self.ui.voterBtn,
                 self.ui.systemBtn, self.ui.votingBtn, self.ui.candidateBtn]
        for button in buttons:
            self.addShadowButton(button)
        self.addShadowBackcard(self.ui.backCard1)
        #Load the Data to comboBox1
        # Clear previous items
        self.ui.comboBox1.clear()
        for i in BD_Constituencies.BD_Constituencies:
            self.ui.comboBox1.addItem(str(i))

        #After Pressing the save1 button
        import VoterRegistration
        self.ui.save1.clicked.connect(lambda: VoterRegistration.validate_registration(self.ui))
        #After Pressing the faceScan1 button
        self.ui.faceScan1.clicked.connect(lambda: FaceRecognition.register_voter(self.ui))
        #Validity button
        self.validButon()
        #Button Clicked Signal

        self.ui.registerBtn.clicked.connect(self.go_to_page1)
        self.ui.backBtn1.clicked.connect(self.go_to_page0)


    def go_to_page1(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def go_to_page0(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def validButon(self):
        self.ui.validNid.setVisible(False)
        self.ui.validAddress.setVisible(False)
        self.ui.validDob.setVisible(False)
        self.ui.validConstituency.setVisible(False)
        self.ui.validName.setVisible(False)
        self.ui.validPhn.setVisible(False)



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
    def addShadowBackcard(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(100)  # Larger blur for bigger card
        shadow.setXOffset(2)  # Keep horizontal centered
        shadow.setYOffset(5)  # Slightly more vertical offset
        shadow.setColor(QColor(0, 0, 0, 12))  # Darker and more visible
        widget.setGraphicsEffect(shadow)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
