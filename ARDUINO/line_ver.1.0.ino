const int leftgopin = 8;
const int leftbackpin = 9;
const int rightgopin = 10;
const int rightbackpin = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(leftgopin, OUTPUT);
  pinMode(leftbackpin, OUTPUT);
  pinMode(rightgopin, OUTPUT);
  pinMode(rightbackpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int left =  analogRead(A3);
  int right = analogRead(A4);
  Serial.print(left);
  Serial.print(right);
  delay(100);

  if(left < right){
    digitalWrite(leftbackpin, LOW);
    digitalWrite(rightbackpin, LOW);
    analogWrite(leftgopin, 128);
    analogWrite(rightgopin, 50);
  }else if(right < left){
    digitalWrite(rightbackpin, LOW);
    digitalWrite(leftbackpin, LOW);
    analogWrite(rightgopin, 128);
    analogWrite(leftgopin, 50);
  }else{
    digitalWrite(leftbackpin, LOW);
    digitalWrite(rightbackpin, LOW);
    analogWrite(leftgopin, 128);
    analogWrite(rightgopin, 128);
  }

}
