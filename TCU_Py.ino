
void setup(){
// Open serial connection.
Serial.begin(9600);
while(!Serial);
}

void loop(){
  int incomingByte = 0;
  char a[1200];
  for(int i = 0; i < 1200; i++){
    incomingByte = Serial.read();
    a[i] = incomingByte;
  }
  Serial.print("Arduino: ");
  Serial.println(a);
  while(1){};
}
