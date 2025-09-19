  #include <SoftwareSerial.h>

  SoftwareSerial Slaves(4, 8); 

  void setup() {
    Serial.begin(9600); 
    Slaves.begin(9600);   
  }

  void loop() {
    if (Serial.available() >= 2) {
      char cmd = Serial.read();   
      Serial.println(cmd);
      if (cmd == 'A') {
        Slaves.write('A');
      }
      if (cmd == 'B') {
        Slaves.write('B');
      }
      if (cmd == 'C') {
        Slaves.write('C');
      }
    }
    if (Slaves.available() >= 2) {
      char out1 = Slaves.read();
      char out2 = Slaves.read();
      if (out1 == 'A') {
        Serial.write('A');
        if (out2 == '1') {
          Serial.write('1');
        }
        if (out2 == '0') {
          Serial.write('0');
        }
      }
      
      if (out1 == 'B') {
        Serial.write('B');
        if (out2 == '1') {
          Serial.write('1');
        }
        if (out2 == '0') {
          Serial.write('0');
        }
      }
      
      if (out1 == 'C') {
        Serial.write('C');
        if (out2 == '1') {
          Serial.write('1');
        }
        if (out2 == '0') {
          Serial.write('0');
        }
      }
      
    }
  }