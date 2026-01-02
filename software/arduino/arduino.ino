#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>

// TFT Pins
#define TFT_CS   10
#define TFT_DC   9
#define TFT_RST  8

// Colors
#define CLR_BG       0xFFFF
#define CLR_PURPLE_D 0x4810
#define CLR_PURPLE_L 0xD6FF
#define CLR_TEXT     0x0000
#define CLR_ACCENT   0x780F
#define CLR_WHITE    0xFFFF

bool votingActive = false;

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

struct Candidate { int x, y; const char* name; };

Candidate candidates[6] = {
  {5, 32, "BNP"}, {83, 32, "Jamat"},
  {5, 62, "NCP"}, {83, 62, "GOP"},
  {5, 92, "BJP"}, {83, 92, "IMB"}
};

int selected = 0;
bool prevBtns[7] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};

void drawHeader() {
  tft.fillRect(0,0,160,28,CLR_PURPLE_D);
  tft.setTextColor(CLR_WHITE);
  tft.setTextSize(1);
  tft.setCursor(5,4); tft.print("PLEASE PRESS A BUTTON");
  tft.setCursor(5,16); tft.print("TO VOTE:");
}

void drawFooter(const char* msg,uint16_t color){
  tft.fillRect(0,118,160,10,CLR_BG);
  tft.setTextColor(color); tft.setCursor(10,119); tft.print(msg);
}

void drawCandidate(int i,bool isSelected){
  int x=candidates[i].x, y=candidates[i].y;
  if(isSelected){
    tft.fillRoundRect(x,y,72,26,4,CLR_ACCENT); tft.setTextColor(CLR_WHITE);
  } else {
    tft.fillRoundRect(x,y,72,26,4,CLR_PURPLE_L);
    tft.drawRoundRect(x,y,72,26,4,CLR_PURPLE_D);
    tft.setTextColor(CLR_TEXT);
  }
  tft.setCursor(x+6, y+9); tft.print(candidates[i].name);
}

void showScanScreen(){
  tft.fillScreen(CLR_BG);
  tft.setTextColor(CLR_PURPLE_D); tft.setTextSize(2);
  tft.setCursor(10,50); tft.print("Please scan your");
  tft.setCursor(20,80); tft.print("face to vote");
}

void showConfirmScreen(int choice){
  tft.fillScreen(CLR_BG);
  tft.fillCircle(80,35,22,CLR_PURPLE_L); tft.drawCircle(80,35,22,CLR_PURPLE_D);
  tft.drawLine(72,35,77,40,CLR_PURPLE_D); tft.drawLine(77,40,88,30,CLR_PURPLE_D);
  tft.setTextColor(CLR_PURPLE_D); tft.setTextSize(2); tft.setCursor(32,65); tft.print("VOTED!");
  tft.fillRoundRect(20,85,120,30,8,CLR_PURPLE_D);
  tft.setTextSize(1); tft.setTextColor(CLR_PURPLE_L); tft.setCursor(30,91); tft.print("SELECTION:");
  tft.setTextColor(CLR_WHITE); tft.setCursor(30,101); tft.print(candidates[choice-1].name);
  drawFooter("SECURE TRANSACTION OK",0x7BEF);

  Serial.print("VOTE_ID:"); Serial.println(choice);  // send vote id
}

void setup(){
  for(int i=2;i<=7;i++) pinMode(i,INPUT_PULLUP);
  pinMode(A0,INPUT_PULLUP);
  Serial.begin(9600);
  while(!Serial){;} // wait for serial ready
  tft.initR(INITR_BLACKTAB); tft.setRotation(1);
  showScanScreen();
  Serial.println("READY"); // handshake
}

void loop() {
    // Handle serial commands
    if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n'); 
        cmd.trim();
        if (cmd == "START_VOTING") {
            votingActive = true;
            selected = 0;
            tft.fillScreen(CLR_BG); drawHeader();
            for(int i=0; i<6; i++) drawCandidate(i, false);
            drawFooter("READY TO START", CLR_PURPLE_D);
            Serial.println("Voting started!");
        } else if (cmd == "RESET_SCREEN") {
            showScanScreen();
            votingActive = false;
        }
    }

    if (votingActive) {
        // Candidate selection
        for (int i=0; i<6; i++) {
            bool state = digitalRead(i+2);
            if (state == LOW && prevBtns[i] == HIGH) {
                if (selected > 0) drawCandidate(selected-1,false);
                selected = i+1;
                drawCandidate(i,true);
                drawFooter("HOLD TO CONFIRM", CLR_ACCENT);
                delay(50);
            }
            prevBtns[i] = state;
        }

        // Confirm button
        bool confirm = digitalRead(A0);
        if (confirm == LOW && prevBtns[6] == HIGH && selected != 0) {
            showConfirmScreen(selected);
            votingActive = false;  // voting done
            // Python will send RESET_SCREEN
        }
        prevBtns[6] = confirm;
    }
}
