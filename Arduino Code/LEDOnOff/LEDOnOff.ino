String inputString = "";      // a String to hold incoming data
bool isStringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(19200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  pinMode(13,OUTPUT);
}

void loop() {
  // print the string when a newline arrives:
  if (isStringComplete) {
    
    //TODO: Do the command!
    if(inputString.equals("LED ON")){
      digitalWrite(13, HIGH);
      Serial.println("The LED is now on!");
    }
    else if(inputString.equals("LED OFF")){
      digitalWrite(13, LOW);
      Serial.println("The LED is now off!");
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
