#define YELLOW_LED 3
#define RED_LED 10
#define GREEN_LED 5
#define BLUE_LED 6
#define WHITE_LED 11

int yBright = 0;
int rBright = 0;
int gBright = 0;
int bBright = 0;
int wBright = 0;

void setup() {
  Serial.begin(115200);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);
}

void loop() {

//Serial.println("Turning on Yellow");
//analogWrite(YELLOW_LED, 100);
//delay(5000);
//analogWrite(YELLOW_LED, 200);
//delay(5000);
for (int i=0; i<=255; i++) {
  analogWrite(GREEN_LED, i);
  delay(100);
}
Serial.println("Turning on Red");
analogWrite(RED_LED, 255);
delay(5000);
analogWrite(RED_LED, 10);
delay(5000);

//Serial.println("Turning on Green");
//analogWrite(GREEN_LED, 100);
//delay(1000);
//analogWrite(GREEN_LED, 0);

//Serial.println("Turning on Blue");
//analogWrite(BLUE_LED, 100);
//delay(1000);
//analogWrite(BLUE_LED, 0);

//Serial.println("Turning on White");
//analogWrite(WHITE_LED, 200);
//delay(5000);
//analogWrite(WHITE_LED, 100);
//delay(5000);

}
