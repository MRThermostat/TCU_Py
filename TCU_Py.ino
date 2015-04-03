
void setup(){
// Open serial connection.
Serial.begin(9600);
while(!Serial);
}

void loop(){
  int incomingByte = 0;
  byte i;
  char a[100];
  if (Serial.available() > 0) {
    for(i = 0; i < 100; i++){
      incomingByte = Serial.read();
      a[i] = incomingByte;
    }
    Serial.print("I got: "); // ASCII printable characters
    Serial.println(a);
  }
}
