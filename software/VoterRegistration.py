# validation.py
import datetime
import BD_Constituencies
import FaceRecognition

def validate_nid(nid: str) -> bool:
    return nid.isdigit() and 10 <= len(nid) <= 17

def validate_name(name: str) -> bool:
    return name.replace(" ", "").isalpha() and len(name) > 0

def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) == 11


def validate_dob(date_widget) -> bool:
    return date_widget.date().isValid()

def validate_address(address: str) -> bool:
    return len(address.strip()) > 0

def validate_constituency(constituency: str, valid_list: list) -> bool:
    return constituency in valid_list

def validate_registration(ui):
    nid = ui.nid1.text()
    name = ui.name1.text()
    phone = ui.number1.text()
    address = ui.address1.text()
    constituency = ui.comboBox1.currentText()
    # Show/hide warnings
    ui.validNid.setVisible(not validate_nid(nid))
    ui.validName.setVisible(not validate_name(name))
    ui.validPhn.setVisible(not validate_phone(phone))
    ui.validDob.setVisible(not validate_dob(ui.dob1))  # FIXED
    ui.validAddress.setVisible(not validate_address(address))
    ui.validConstituency.setVisible(not validate_constituency(constituency, BD_Constituencies.BD_Constituencies))

    return (
            validate_nid(nid) and
            validate_name(name) and
            validate_phone(phone) and
            validate_dob(ui.dob1) and
            validate_address(address) and
            validate_constituency(constituency, BD_Constituencies.BD_Constituencies)
    )

