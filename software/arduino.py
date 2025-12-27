import threading
import serial
from PyQt6.QtCore import pyqtSignal, QObject

class ArduinoListener(QObject):
    vote_signal = pyqtSignal(int)  # emit candidate_id when button pressed

    def __init__(self, port='/dev/cu.usbmodem141011', baud=9600):
        super().__init__()
        self.ser = serial.Serial(port, baud)
        self.running = True
        threading.Thread(target=self.read_loop, daemon=True).start()

    def read_loop(self):
        while self.running:
            if self.ser.in_waiting:
                try:
                    candidate_id = int(self.ser.readline().decode().strip())
                    self.vote_signal.emit(candidate_id)
                except ValueError:
                    pass  # ignore invalid input

    def stop(self):
        self.running = False
        self.ser.close()
