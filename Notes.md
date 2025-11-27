### **1. Create a Virtual Environment**

D:

cd "D:\\Electro Voting Machine (EVM)"

python -m venv .venv

.venv\\Scripts\\activate.bat   // in windows cmd

source .venv/bin/activate    //in macOS



### **2. Install Required Packages**

pip install PyQt6 numpy opencv-python pyserial pywin32



### **3. Convert Qt Designer .ui file into Python**

pyuic6 -x software\main.ui -o software\ui_main.py

// for icon
pyrcc6 resources.qrc -o resources_rc.py





### **4. Run the app with virtual Environment**

.venv\\Scripts\\activate.bat

cd software

python main.py



