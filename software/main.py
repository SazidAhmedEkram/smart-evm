from PyQt6.QtGui import QColor, QIcon, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QMessageBox

from software import FaceRecognition, VoterRegistration, VoiceInstructions
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

        self.face_encoding = None  # Store captured face

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

        self.ui.save1.clicked.connect(self.save1)
        #After Pressing the faceScan1 button
        self.ui.faceScan1.clicked.connect(self.capture_face)
        #Validity button
        self.validButon()

        #Button Clicked Signal
        self.ui.registerBtn.clicked.connect(self.go_to_page1)
        self.ui.backBtn1.clicked.connect(self.go_to_page0)

    def capture_face(self):
        # This function captures the face and stores encoding in self.face_encoding
        self.face_encoding = FaceRecognition.register_voter(self.ui)
        if self.face_encoding is not None:
            print("Face captured successfully")
        else:
            print("Face capture failed")

    #Pressing the Save1 Button
    def save1(self):
        if not VoterRegistration.is_registration_valid(self.ui):
            VoterRegistration.show_validation_feedback(self.ui)
            VoiceInstructions.speak("Please fill all required fields before saving.")
            return

        if self.face_encoding is None:
            VoiceInstructions.speak("Please scan your face before saving.")
            return
        reply = QMessageBox.question(self, "Confirm Save",
                                     "Are you sure you want to save the face?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        # Insert into DB
        nid = self.ui.nid1.text()
        name = self.ui.name1.text()
        phone = self.ui.number1.text()
        dob = self.ui.dob1.text()
        constituency = self.ui.comboBox1.currentText()
        address = self.ui.address1.text()

        success, message = FaceRecognition.insert_voter_to_db(
            nid, name, dob, phone, constituency, address, self.face_encoding
        )

        print(message)
        if success:
            self.validButon()
            VoiceInstructions.speak("Congratulations! Your voter has been registered.")
            self.clear1()
            self.face_encoding = None  # Reset for next registration
            self.go_to_page0()
        else:
            VoiceInstructions.speak(message)

    def clear1(self):
        self.ui.nid1.clear()
        self.ui.name1.clear()
        self.ui.dob1.clear()
        self.ui.address1.clear()
        self.ui.comboBox1.clear()
        self.ui.number1.clear()
        self.validButon()


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
        self.ui.validRegister.setVisible(False)
        self.ui.notRegisteredCard.setStyleSheet("""background-color: rgb(232, 162, 59);
                                            border-radius: 20px;
                                            border: 1px solid rgb(200, 210, 240);""")
        self.ui.notRegistered.setText("⚠ Not Registered")


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
