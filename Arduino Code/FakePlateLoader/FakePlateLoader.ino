String inputString = "";      // a String to hold incoming data
bool isStringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(19200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  // print the string when a newline arrives:
  if (isStringComplete) {
    
    //TODO: Do the command!
    if(inputString.equals("RESET")){
      delay(500);
      Serial.println("READY, SAIGAIN PE Loader, ROM Ver. 1.1.6, 12APR2001");
    }
    else if(inputString.startsWith("MOVE")){
      delay(1000);
      Serial.println("READY");
    }
    else if(inputString.startsWith("GRIPPER OPEN")){
      delay(1000);
      Serial.println("READY, OPEN");
    }
    else if(inputString.startsWith("GRIPPER CLOSE")){
      delay(1000);
      Serial.println("READY, CLOSED, NOPLATE");
    }
    else if(inputString.startsWith("Z-AXIS EXTEND")){
      delay(1000);
      Serial.println("READY, EXTENDED");
    }
    else if(inputString.startsWith("Z-AXIS RETRACT")){
      delay(1000);
      Serial.println("READY, RETRACTED");
    }
    else if(inputString.startsWith("X-AXIS")){
      delay(1000);
      Serial.println("READY");
    }
    else{
      Serial.print("Unkown command -->");
      Serial.println(inputString);
    }
    // clear the string:
    inputString = "";
    isStringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); //Char=unsigned



   
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      isStringComplete = true;
    } else {
      // add it to the inputString:
      inputString += inChar;
    }
  }
}
