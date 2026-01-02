import threading
import serial
from PyQt6.QtCore import pyqtSignal, QObject
import time

class ArduinoListener(QObject):
    vote_signal = pyqtSignal(int)

    def __init__(self, port='/dev/cu.usbmodem141011', baud=9600):
        super().__init__()
        self.ser = None
        for i in range(5):
            try:
                self.ser = serial.Serial(port, baud, timeout=1)
                time.sleep(2)  # give Arduino time to reset
                break
            except serial.SerialException:
                print(f"Port busy, retrying... ({i+1}/5)")
                time.sleep(1)
        if not self.ser:
            raise serial.SerialException(f"Could not open port {port}")

        self.running = True
        threading.Thread(target=self.read_loop, daemon=True).start()

    def read_loop(self):
        while self.running:
            try:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode(errors="ignore").strip()
                    if line.startswith("VOTE_ID:"):
                        candidate_id = int(line.split(":")[1])
                        self.vote_signal.emit(candidate_id)
                    elif line.startswith("READY") or line.startswith("Voting started!"):
                        print("Arduino:", line)
                    elif line.startswith("VOTED_FOR:"):
                        print("Arduino:", line)
            except serial.SerialException as e:
                print("Arduino read error (ignored):", e)
                time.sleep(0.1)
            except Exception as e:
                print("Arduino general error:", e)
                time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.ser:
            try:
                self.ser.close()
            except:
                pass
