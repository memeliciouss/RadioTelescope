#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <SPI.h>

#define ADC_PIN1 34  // First wire (ADC1 channel)
#define ADC_PIN2 35  // Second wire (ADC1 channel)

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  pinMode(ADC_PIN1, INPUT);  // Set ADC pins as input
  pinMode(ADC_PIN2, INPUT);
}

void loop() {
  // Read values from both ADC channels (0-4095)
  int adcValue1 = analogRead(ADC_PIN1);
  int adcValue2 = analogRead(ADC_PIN2);
  
  // Convert ADC readings to voltage (scale it to 0-1V range)
  float voltage1 = adcValue1 * (1.0 / 4095.0);  // 0 to 1V
  float voltage2 = adcValue2 * (1.0 / 4095.0);  // 0 to 1V
  
  // Calculate the difference in voltages (0 to 1V range)
  float voltageDifference = voltage1 - voltage2;
  
  // Print the voltage difference to the Serial Monitor
  Serial.print("Voltage Difference: ");
  Serial.print(voltageDifference, 3);  // 3 decimal places for clarity
  Serial.println();

  
  delay(500);  // Delay for a smoother graph
}