from PyQt6.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_AdminDashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminDashboard()
        self.ui.setupUi(self)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
