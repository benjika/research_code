#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <HX711.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

HX711 scale;
LiquidCrystal_I2C lcd(0x3F,20,4);
Adafruit_BMP280 bmp; // I2C

uint8_t dataPin = 6;
uint8_t clockPin = 7;
float w1,wt;
float zeroStream = 1734088.00, highStream = 2062800.75, highWeight = 30.0;
float temper;

void setup()
{
  Serial.begin(9600); // 115200
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  scale.begin(dataPin, clockPin);
  lcd.init();
  lcd.backlight();
  while ( !Serial ) delay(100);   // wait for native usb
  unsigned status;
  status = bmp.begin();
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(),16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}


void loop()
{
  w1 = scale.get_units(10);
  wt = ((w1-zeroStream)/(highStream-zeroStream))*highWeight;
  temper = bmp.readTemperature();
  
  Serial.print(w1);
  Serial.print("   ");
  Serial.println(wt);
  Serial.print(F("Temperature = "));
  Serial.print(temper);
  Serial.println(" *C");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Ywrobot Arduino!");
  lcd.setCursor(0,1);
  lcd.print("Temp. = ");
  lcd.print(temper);
  lcd.print(" *C");
  lcd.setCursor(0,2);
  lcd.print("Weight: ");
  lcd.print(wt);
  lcd.print(" KG");
  delay(1000);
}
