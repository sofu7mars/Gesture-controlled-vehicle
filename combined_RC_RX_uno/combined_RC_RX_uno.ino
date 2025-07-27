#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

RF24 radio(8,10);
uint8_t address[][8] = {"1Node", "2Node", "3Node", "4Node", "5Node", "6Node", "7Node", "8Node"};

int forward = 0;
int backward = 0;
int right = 0;
int left = 0;
int rightforw = 0;
int leftforw = 0;
int power = 0;

int typePointer = 0;

int thumb = 0;
int index = 0;
int middle = 0;
int ring = 0;
int little = 0;


int IN1 = 2;
int IN2 = 4;
int IN3 = 5;
int IN4 = 7;
int ENA = 3;
int ENB = 6;

int extraByte = 0;

int state = 0;

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.setAutoAck(1);
  radio.setRetries(0, 15);
  radio.enableAckPayload();
  radio.setPayloadSize(32);
  radio.openReadingPipe(1, address[0]);
  radio.setChannel(0x7a);

  radio.setPALevel (RF24_PA_MAX);
  radio.setDataRate (RF24_1MBPS);

  radio.powerUp();
  radio.startListening();
  for(int i = 2; i <= 7; i++){
    pinMode(i, OUTPUT);
  }
}

void stopFunc(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

int forwardFunc(int power) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, power);
  analogWrite(ENB, power);  
}

int backwardFunc(int power) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, power);
  analogWrite(ENB, power);  
}


int turnLeftFunc(int power) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, power);
  analogWrite(ENB, power); 
}

int softTurnLeftFunc(int power){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  int velENB = 0;
  power = constrain(power, 0, 255);
  if (power > 150){
    velENB = power - 100; 
  } else if (100 <= power && power <= 150){
    velENB = power - 70; 
  } else {
    velENB = power - 40;
  }
  analogWrite(ENA, power);
  analogWrite(ENB, velENB);
}

int turnRightFunc(int power) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, power);
  analogWrite(ENB, power); 
}

int softTurnRightFunc(int power) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  int velENA = 0;
  
  power = constrain(power, 0, 255);
  if (power > 150) {
    velENA = power - 100;
    
  } else if (100 <= power && power <= 150) {
    velENA = power - 70;
  } else {
    velENA = power - 30;
  }
  
  //Serial.print(vel);
  //Serial.print("   ");
  //Serial.println(velENA);
  
  analogWrite(ENA, velENA);
  analogWrite(ENB, power); 
}

void loop() {
  byte pipeNo, gotByte[8];
  while(radio.available(&pipeNo)){
    radio.read(&gotByte, sizeof(gotByte));
    typePointer = gotByte[6];
    if (typePointer == 1){
      power = gotByte[7];
      thumb = gotByte[0];
      index = gotByte[1];
      middle = gotByte[2];
      ring = gotByte[3];
      little = gotByte[4];
      extraByte = gotByte[5];
      /*
      Serial.print("Type: ");
      Serial.print(typePointer);
      Serial.print("\t Thumb: ");
      Serial.print(thumb);
      Serial.print("\t Index: ");
      Serial.print(index);
      Serial.print("\t middle: ");
      Serial.print(middle);
      Serial.print("\t ring: ");
      Serial.print(ring);
      Serial.print("\t little: ");
      Serial.print(little);
      Serial.print("\t ExtraByte: ");
      Serial.print(extraByte);
      Serial.print("\t Power: ");
      Serial.println(power);
      */
      
    } else if (typePointer == 2){
      forward = gotByte[0];
      backward = gotByte[1];
      right = gotByte[2];
      left = gotByte[3];
      rightforw = gotByte[4];
      leftforw = gotByte[5];
      power = gotByte[7];
      /*
      Serial.print("Type: ");
      Serial.print(typePointer);
      Serial.print("\t Forw: ");
      Serial.print(forward);
      Serial.print("\t Backw: ");
      Serial.print(backward);
      Serial.print("\t Right: ");
      Serial.print(right);
      Serial.print("\t Left: ");
      Serial.print(left);
      Serial.print("\t Rightforw: ");
      Serial.print(rightforw);
      Serial.print("\t Leftforw: ");
      Serial.print(leftforw);
      Serial.print("\t Power: ");
      Serial.println(power);
      */
    }
  }

  if (typePointer == 1){
    if(thumb == 1 && index != 1 && middle != 1 && ring != 1 && little != 1){
      state = 1;
    } else if(thumb != 1 && index == 1 && middle != 1 && ring != 1 && little == 1){
      state = 2;
    } else if( thumb != 1 && index != 1 && middle != 1 && ring != 1 && little == 1){
      state = 3;
    } else if( thumb != 1 && index == 1 && middle != 1 && ring != 1 && little != 1){
      state = 4;
    } else if( thumb == 1 && index != 1 && middle != 1 && ring != 1 && little == 1){
      state = 5;
    } else if( thumb == 1 && index == 1 && middle != 1 && ring != 1 && little != 1){
      state = 6;
    } else if((thumb == 1 && index == 1 && middle == 1 && ring == 1 && little == 11) || (thumb != 1 && index != 1 && middle != 1 && ring != 1 && little != 1)) {
      state = 0;
    }
    Serial.print("Type: ");
    Serial.print(typePointer);
    Serial.print("\t Thumb: ");
    Serial.print(thumb);
    Serial.print("\t Index: ");
    Serial.print(index);
    Serial.print("\t middle: ");
    Serial.print(middle);
    Serial.print("\t ring: ");
    Serial.print(ring);
    Serial.print("\t little: ");
    Serial.print(little);
    Serial.print("\t ExtraByte: ");
    Serial.print(extraByte);
    Serial.print("\t Power: ");
    Serial.print(power);
    Serial.print("\t Direction: ");

  } else if (typePointer == 2){
    if (forward == 1 && backward != 1 && right != 1 && left != 1 && rightforw != 1 && leftforw != 1){
      state = 1;
    } else if (forward != 1 && backward == 1 && right != 1 && left != 1 && rightforw != 1 && leftforw != 1){
      state = 2;
    } else if (forward != 1 && backward != 1 && right == 1 && left != 1 && rightforw != 1 && leftforw != 1){
      state = 3;
    } else if (forward != 1 && backward != 1 && right != 1 && left == 1 && rightforw != 1 && leftforw != 1){
      state = 4;
    } else if (forward != 1 && backward != 1 && right != 1 && left != 1 && rightforw == 1 && leftforw != 1){
      state = 5;
    } else if (forward != 1 && backward != 1 && right != 1 && left != 1 && rightforw != 1 && leftforw == 1){
      state = 6;
    } else if (forward != 1 && backward != 1 && right != 1 && left != 1 && rightforw != 1 && leftforw != 1){
      state = 0;
    } 
    Serial.print("Type: ");
    Serial.print(typePointer);
    Serial.print("\t Forw: ");
    Serial.print(forward);
    Serial.print("\t Backw: ");
    Serial.print(backward);
    Serial.print("\t Right: ");
    Serial.print(right);
    Serial.print("\t Left: ");
    Serial.print(left);
    Serial.print("\t Rightforw: ");
    Serial.print(rightforw);
    Serial.print("\t Leftforw: ");
    Serial.print(leftforw);
    Serial.print("\t Power: ");
    Serial.print(power);
    Serial.print("\t");
  }
  if (typePointer == 1){
    if (state == 0){
      stopFunc();
      Serial.print("Nothing happening");
    } else if (state == 1){
      backwardFunc(power);
      Serial.print("Backward");
    } else if (state == 2) {
      forwardFunc(power);
      Serial.print("Forward");
    } else if (state == 3) {
      turnLeftFunc(power);
       Serial.print("Left");
    } else if (state == 4) {
      turnRightFunc(power);
      Serial.print("Right");
    } else if (state == 5){
      softTurnLeftFunc(power);
      Serial.print("Soft left");
    } else if (state == 6) {
      softTurnRightFunc(power);
      Serial.print("Soft right");
    }
    Serial.println(); 
  } else if (typePointer == 2) {
    if (state == 0){
      stopFunc();
      Serial.print("Nothing happening");
    } else if (state == 1) {
      forwardFunc(power);
      Serial.print("Forward\t");    
    } else if (state == 2) {
      backwardFunc(power);
      Serial.print("Backward");     
    }else if (state == 3) {
      turnRightFunc(power);
      Serial.print("Right");     
    }else if (state == 4) {
      turnLeftFunc(power);
      Serial.print("Left");   
    }else if (state == 5) {
      softTurnRightFunc(power);
      Serial.print("Soft Right");      
    }else if (state == 6) {
      softTurnLeftFunc(power);
      Serial.print("Soft Left");     
    }
    Serial.println(); 
  }
  
  
}
