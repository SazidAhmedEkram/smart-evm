# Smart EVM

![Status](https://img.shields.io/badge/status-in_progress-yellow)
![Python](https://img.shields.io/badge/python-3.10-blue)
![Arduino](https://img.shields.io/badge/arduino-UNO-green)

A secure **Arduino-based Electronic Voting Machine (EVM)** prototype featuring **webcam face recognition**, **LCD display**, **voting buttons**, **buzzer feedback**, and a **dedicated PC software** for voter authentication and vote logging.

> **Status:** 🚧 Project under development — features will be added gradually.

---

## 🔥 Features (Planned)

### PC Software (Python)
- Real-time **face recognition** using OpenCV  
- Voter **registration system** with NID input  
- Voter authentication before voting  
- Stores face encodings & voter data securely  
- Prevents multiple voting (one voter → one vote)

### Hardware (Arduino UNO)
- LCD display for instructions  
- Voting interface with push buttons (or touch buttons)  
- LED indicators  
- Buzzer feedback  
- Serial communication with PC

### Security Features
- Face verification before voting  
- NID-based unique user records  
- Local encrypted storage  
- Prevents duplicate votes

---

## 🧰 Technologies Used
- **Python 3**  
- **OpenCV**  
- **NumPy**  
- **Pickle** (data storage)  
- **pySerial**  
- **SAPI** (text-to-speech)  
- **Arduino UNO**, LCD, buttons, LEDs, buzzer

---

## 📂 Roadmap
- [ ] Face registration system  
- [ ] Face recognition for authentication  
- [ ] Arduino voting interface  
- [ ] LCD + buttons integration  
- [ ] Vote logging  
- [ ] Admin dashboard  
- [ ] Demo video & screenshots  
- [ ] Final documentation

---

## 🚀 Setup (Basic)
Install Python dependencies:

```bash
pip install opencv-python numpy pyserial
