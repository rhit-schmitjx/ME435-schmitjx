String inputString = "";
bool isStringComplete = false;

// Simulated loader state
int xPosition = 0;
bool zExtended = false;
bool gripperClosed = true;
bool hasPlate = true;  // fake loader always reports a plate present when gripper closes

void setup() {
  Serial.begin(19200);
  inputString.reserve(200);
}

void loop() {
  if (isStringComplete) {
    if (inputString.equals("RESET") || inputString.equals("INITIALIZE")) {
      delay(500);
      zExtended = false;
      gripperClosed = true;
      xPosition = 5;
      xPosition = 3;
      Serial.println("READY, SAGIAN PE Loader, ROM Ver. 1.1.6, 12APR2001");
    } else if (inputString.startsWith("MOVE")) {
      handleMove(inputString.substring(4));
    } else if (inputString.startsWith("X-AXIS")) {
      handleXAxis(inputString.substring(6));
    } else if (inputString.equals("GRIPPER OPEN")) {
      gripperClosed = false;
      Serial.println("READY, OPEN");
    } else if (inputString.equals("GRIPPER CLOSE")) {
      gripperClosed = true;
      if (hasPlate) {
        Serial.println("READY, CLOSED, PLATE");
      } else {
        Serial.println("READY, CLOSED, NO PLATE");
      }
    } else if (inputString.equals("Z-AXIS EXTEND")) {
      zExtended = true;
      Serial.println("READY, EXTENDED");
    } else if (inputString.equals("Z-AXIS RETRACT")) {
      zExtended = false;
      Serial.println("READY, RETRACTED");
    } else if (inputString.equals("LOADER_STATUS")) {
      handleLoaderStatus();
    } else if (inputString.startsWith("SET_DELAY")) {
      handleSetDelay(inputString.substring(9));
    } else {
      Serial.print("Unknown command --> ");
      Serial.println(inputString);
    }

    inputString = "";
    isStringComplete = false;
  }
}

void handleXAxis(String params) {
  params.trim();
  int position = params.toInt();
  zExtended = false;
  xPosition = position;
  Serial.println("READY");
}

void handleMove(String params) {
  params.trim();
  int spaceIndex = params.indexOf(' ');
  if (spaceIndex == -1) {
    Serial.print("Unknown command --> ");
    Serial.println(inputString);
    return;
  }
  String loadParam = params.substring(spaceIndex + 1);
  loadParam.trim();
  int loadPosition = loadParam.toInt();

  delay(3000);
  zExtended = false;
  xPosition = loadPosition;
  Serial.println("READY");
}

void handleLoaderStatus() {
  Serial.print("READY, POSITION ");
  Serial.print(xPosition);
  Serial.print(", ZAXIS ");
  Serial.print(zExtended ? "EXTENDED" : "RETRACTED");
  Serial.print(", GRIPPER ");
  Serial.print(gripperClosed ? "CLOSED" : "OPEN");
  Serial.print(", PLATE_STATUS ");
  Serial.println(hasPlate ? "PLATE" : "NO PLATE");
}

void handleSetDelay(String params) {
  params.trim();
  int firstSpace = params.indexOf(' ');
  int secondSpace = params.indexOf(' ', firstSpace + 1);
  if (firstSpace == -1 || secondSpace == -1) {
    Serial.print("Unknown command --> ");
    Serial.println(inputString);
    return;
  }

  String fromParam = params.substring(0, firstSpace);
  String toParam = params.substring(firstSpace + 1, secondSpace);
  String delayParam = params.substring(secondSpace + 1);
  fromParam.trim();
  toParam.trim();
  delayParam.trim();

  Serial.print("READY, TO ");
  Serial.print(toParam);
  Serial.print(", FROM ");
  Serial.print(fromParam);
  Serial.print(", DELAY ");
  Serial.println(delayParam);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      isStringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}