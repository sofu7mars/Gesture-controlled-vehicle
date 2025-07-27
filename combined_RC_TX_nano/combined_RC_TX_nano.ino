#include <cvzone.h>
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

/*
nRF24 pin setup for Uno and Nano:
1: GND
2: VCC 3.3V
3: 9
4: 10
5: 13
6: 11
7: 12
*/
int led = 5;

SerialData serialData(8, 3);
int valsRec[8];

RF24 radio(9, 10);
byte address[][8] = {"1Node", "2Node", "3Node", "4Node", "5Node", "6Node", "7Node", "8Node"};

uint8_t dataToUno[8] = {0, 0, 0, 0, 0, 0, 0, 0};
byte counter[5] = {0, 0, 0, 0, 0};
int test = 3;

int power = 0;
int forward = 0;
int backward = 0;
int right = 0;
int left = 0;
int rightforw = 0;
int leftforw = 0;

int typePointer = 0;

int thumb = 0;
int index = 0;
int middle = 0;
int ring = 0;
int little = 0;
int br = 0;

void setup() {
  serialData.begin(9600);
  int valsRec[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  radio.begin();
  radio.setAutoAck(1);
  radio.setRetries(0, 15);
  radio.enableAckPayload();
  radio.setPayloadSize(32);

  radio.openWritingPipe(address[0]);
  radio.setChannel(0x7a);

  radio.setPALevel (RF24_PA_MAX);
  radio.setDataRate (RF24_1MBPS);

  radio.powerUp();
  radio.stopListening();
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  delay(1000);
  digitalWrite(led, LOW);
}

void loop() {

  radio.write(&dataToUno, sizeof(dataToUno));
  
  serialData.Get(valsRec);

  typePointer = valsRec[6];
  if (typePointer == 100){
    
    thumb = valsRec[0];
    index = valsRec[1];
    middle = valsRec[2];
    ring = valsRec[3];
    little = valsRec[4];
    power = valsRec[7];
    power = map(power, 10, 170, 0, 255);
    power = (power <= 10) ? 0 : power;
    power = (power >= 240) ? 255 : power;
    dataToUno[7] = power;
    dataToUno[5] = 0;
    dataToUno[6] = 1; // type pointer for 1

    if(thumb == 100){
      dataToUno[0] = 1;
    } else {
      dataToUno[0] = 0;    
    }  
    if(index == 100){
      dataToUno[1] = 1;  
    } else {
      dataToUno[1] = 0;
    }
    if(middle == 100){
      dataToUno[2] = 1;
    } else {
      dataToUno[2] = 0;
      
    }
    if(ring == 100){
      dataToUno[3] = 1;
    } else {
      dataToUno[3] = 0;
    }
    if(little == 100){
      dataToUno[4] = 1;
    } else {
      dataToUno[4] = 0;
    }
      
  } else if (typePointer == 200){
    power = valsRec[7];
    forward = valsRec[0];
    backward = valsRec[1];
    right = valsRec[2];
    left = valsRec[3];
    rightforw = valsRec[4];
    leftforw = valsRec[5];
    power = map(power, 10, 145, 0, 255);
    power = (power <= 10) ? 0 : power;
    power = (power >= 240) ? 255 : power;
    
    if (forward == 100) {
      dataToUno[0] = 1;
    } else if (forward == 200) {
      dataToUno[0] = 2;
    }
    
    if (backward == 100) {
      dataToUno[1] = 1;
    } else if (backward == 200) {
      dataToUno[1] = 2;
    }
    
    if (right == 100) {
      dataToUno[2] = 1;
    } else if (right == 200) {
      dataToUno[2] = 2;
    }
    
    if (left == 100) {
      dataToUno[3] = 1;
    } else if (left == 200) {
      dataToUno[3] = 2;
    }
    
    if (rightforw == 100) {
      dataToUno[4] = 1;
    } else if (rightforw == 200) {
      dataToUno[4] = 2;
    }
    
    if (leftforw == 100) {
      dataToUno[5] = 1;
    } else if (leftforw == 200) {
      dataToUno[5] = 2;
    }
    dataToUno[7] = power;
    dataToUno[6] = 2; // type pointer for 2
    
  }
  if (typePointer == 100){
    analogWrite(led, 0);
   
  } else if (typePointer == 200) {
    analogWrite(led, power);
  }
  


 
 
}
