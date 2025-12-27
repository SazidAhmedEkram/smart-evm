// Arduino UNO sketch
const int button1 = 2;  // Candidate 1
const int button2 = 3;  // Candidate 2


void setup() {
  Serial.begin(9600);  // open serial communication
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);

}

void loop() {
  if (digitalRead(button1) == LOW) {
    Serial.println("1");  // send candidate ID 1
    delay(500);           // debounce
  }
  if (digitalRead(button2) == LOW) {
    Serial.println("2");  // send candidate ID 2
    delay(500);
  }

}
