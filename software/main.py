from PyQt6.QtWidgets import QApplication, QMainWindow
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



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
