int lockState = 0; // 0 for locked, 1 for unlocked
const int RELAY_PIN = A5; // Arduino pin connected to the relay's pin

void setup() {
  Serial.begin(115200); // Initialize serial communication
  pinMode(RELAY_PIN, OUTPUT); // Set Arduino pin to output mode
  digitalWrite(RELAY_PIN, LOW); // Lock the door initially
  delay(15000);
  digitalWrite(RELAY_PIN, HIGH);
}

void unlockDoor() {
  if (lockState == 0) {
    // Control the relay to unlock the door
    digitalWrite(RELAY_PIN, LOW);
    lockState = 1;
    Serial.println("Door Unlocked.");
  } else {
    Serial.println("Door Already Unlocked.");
  }
}

void lockDoor() {
  if (lockState == 1) {
    // Control the relay to lock the door
    digitalWrite(RELAY_PIN, HIGH);
    lockState = 0;
    Serial.println("Door Locked.");
  } else {
    Serial.println("Door Already Locked.");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String receivedMessage = Serial.readStringUntil('\n');
    receivedMessage.trim(); // Remove leading/trailing spaces or line breaks

    if (receivedMessage.equals("1")) {
      digitalWrite(RELAY_PIN, LOW); // Unlock the door
      delay(10000); // Maintain unlocked state for 10 seconds (adjust as needed)
      digitalWrite(RELAY_PIN, HIGH); // Lock the door
      delay(5000); // Lock for 5 seconds (adjust as needed)
    } else if (receivedMessage.equals("/unlock")) {
      unlockDoor();
    } else if (receivedMessage.equals("/lock")) {
      lockDoor();
    }
  }
}
