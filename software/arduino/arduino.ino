#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>

// --- TFT PINS ---
#define TFT_CS   10
#define TFT_DC   9
#define TFT_RST  8

// --- COLOR PALETTE ---
// Dark Mode (Splash Only)
#define CLR_DARK_BG    0x10A2  
#define CLR_DARK_SURF  0x2124  

// Light Mode (General UI)
#define CLR_LIGHT_BG   0xF7FE  // Very light lilac/white
#define CLR_PURPLE_D   0x4810  // Deep Indigo/Purple
#define CLR_PURPLE_M   0x881F  // Mid Purple
#define CLR_PURPLE_L   0xE73F  // Soft Lilac
#define CLR_TEXT_MAIN  0x2104  // Near black
#define CLR_WHITE      0xFFFF
#define CLR_SUCCESS    0x2E66  // Modern Green

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// --- CANDIDATE DATA ---
struct Candidate { int x, y; const char* name; };

Candidate candidates[6] = {
  {5, 35, "BNP"},  {68, 35, "JAMAT"},
  {5, 65, "NCP"},  {68, 65, "GOP"},
  {5, 95, "BJP"},  {68, 95, "IMB"}
};

// --- STATE VARIABLES ---
bool votingActive = false;
int selected = 0;
bool prevBtns[7] = {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH};

// --- UI COMPONENTS ---

void drawHeader(const char* title) {
  tft.fillRect(0, 0, 160, 26, CLR_PURPLE_D);
  tft.setTextColor(CLR_WHITE);
  tft.setTextSize(1);
  tft.setCursor(8, 9);
  tft.print(title);
}

void drawFooter(const char* msg, uint16_t color) {
  tft.fillRect(0, 118, 160, 10, CLR_LIGHT_BG);
  tft.setTextColor(color);
  tft.setTextSize(1);
  tft.setCursor(10, 119);
  tft.print(msg);
}

void drawCandidate(int i, bool isSelected) {
  int x = candidates[i].x;
  int y = candidates[i].y;
  uint16_t boxColor = isSelected ? CLR_PURPLE_M : CLR_PURPLE_L;
  uint16_t textColor = isSelected ? CLR_WHITE : CLR_PURPLE_D;

  // Modern Border logic
  if(isSelected) {
    tft.drawRoundRect(x-1, y-1, 59, 24, 4, CLR_PURPLE_M);
  } else {
    tft.drawRoundRect(x-1, y-1, 59, 24, 4, CLR_LIGHT_BG); 
  }

  tft.fillRoundRect(x, y, 57, 22, 3, boxColor);
  tft.setTextColor(textColor);
  tft.setCursor(x + 6, y + 7);
  tft.print(candidates[i].name);
}

void showSplashScreen() {
  // STAY IN DARK MODE FOR SPLASH
  tft.fillScreen(CLR_DARK_BG);
  tft.fillTriangle(0, 0, 60, 0, 0, 60, CLR_DARK_SURF);
  
  tft.setTextSize(2); 
  tft.setCursor(15, 45);
  tft.setTextColor(CLR_WHITE);
  tft.print("Sazid's");
  
  tft.setCursor(15, 65); 
  tft.setTextColor(CLR_PURPLE_L); // Using light purple as accent in dark mode
  tft.print("VOTE");
  
  tft.setTextSize(1);
  tft.setTextColor(0xAD55); // Muted gray
  tft.setCursor(15, 90);
  tft.print("SECURE DIGITAL SYSTEM");
  tft.fillRect(15, 102, 40, 2, CLR_PURPLE_L);
}

void showScanScreen() {
  tft.fillScreen(CLR_LIGHT_BG);
  drawHeader("AUTHENTICATION");
  
  // Modern circular icon in purple
  tft.drawCircle(80, 70, 22, CLR_PURPLE_M);
  tft.drawCircle(80, 70, 18, CLR_PURPLE_L);
  tft.fillRect(70, 68, 20, 1, CLR_PURPLE_M); 
  
  tft.setTextColor(CLR_PURPLE_D);
  tft.setTextSize(1);
  tft.setCursor(38, 105);
  tft.print("SCAN YOUR FACE");
}

void showConfirmScreen(int choice) {
  tft.fillScreen(CLR_LIGHT_BG);
  
  // Success Indicator
  tft.fillCircle(80, 40, 20, CLR_SUCCESS);
  tft.drawLine(74, 40, 78, 44, CLR_WHITE);
  tft.drawLine(78, 44, 86, 36, CLR_WHITE);

  tft.setTextColor(CLR_PURPLE_D);
  tft.setTextSize(2);
  tft.setCursor(55, 70);
  tft.print("OK!");

  tft.setTextSize(1);
  tft.setTextColor(CLR_TEXT_MAIN);
  tft.setCursor(35, 95);
  tft.print("VOTED FOR:");
  tft.setTextColor(CLR_PURPLE_M);
  tft.setCursor(35, 107);
  tft.print(candidates[choice-1].name);
  
  Serial.print("VOTE_ID:"); 
  Serial.println(choice);
}

// --- CORE LOGIC ---

void setup() {
  for(int i=2; i<=7; i++) pinMode(i, INPUT_PULLUP);
  pinMode(A0, INPUT_PULLUP);

  Serial.begin(9600);
  tft.initR(INITR_BLACKTAB);
  tft.setRotation(1);

  showSplashScreen();
  delay(3000);
  showScanScreen();
  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "START_VOTING") {
      votingActive = true;
      selected = 0;
      tft.fillScreen(CLR_LIGHT_BG);
      drawHeader("SELECT CANDIDATE");
      for(int i=0; i<6; i++) drawCandidate(i, false);
      drawFooter("TAP TO CHOOSE", CLR_PURPLE_M);
    } 
    else if (cmd == "RESET_SCREEN") {
      votingActive = false;
      showSplashScreen();
      delay(3000);
      showScanScreen();
    }
  }

  if (votingActive) {
    for (int i=0; i<6; i++) {
      bool state = digitalRead(i+2);
      if (state == LOW && prevBtns[i] == HIGH) {
        if (selected > 0) drawCandidate(selected-1, false); 
        selected = i+1;
        drawCandidate(i, true); 
        drawFooter("CONFIRM SELECTION", CLR_PURPLE_D);
        delay(50);
      }
      prevBtns[i] = state;
    }

    bool confirm = digitalRead(A0);
    if (confirm == LOW && prevBtns[6] == HIGH && selected != 0) {
      showConfirmScreen(selected);
      votingActive = false; 
    }
    prevBtns[6] = confirm;
  }
}