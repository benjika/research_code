#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <TimeLib.h>
#include <Adafruit_BME280.h>
const int  cs=8; //chip select

Adafruit_BME280 bme; // I2C
tmElements_t tm;

//LCD 1602 or LCD 2004 settings
LiquidCrystal_I2C lcd(0x3F,20,4);  // set the LCD address to 0x27

const char *monthName[12] = {
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};


void setup() {
  Serial.begin (9600); //init clock
  //Serial.println(__DATE__);
  //Serial.println(__TIME__);


  if (getDate(__DATE__) && getTime(__TIME__)) {
    //Serial.println("AVR Macro strings converted to tmElements.");
  }
  
  //Serial.println("System millis clock referenced to tmElements.");
  //Serial.println();
  
  while ( !Serial ) delay(100);
  setTime(makeTime(tm));//set Ardino system clock to compiled time  // wait for native usb
  //Serial.println(F("BMP280 test"));

  lcd.init();                      // initialize the lcd 
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Weather Station On");
  //Serial.println("Weather Station On");

  //Serial.println("datetime, temperature(c), pressure(mbar), altitude(m)");
  
  
  bool status;
  status = bme.begin(); 
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Could not find a valid BME280");
    while (1);
  }

  Serial.println("weather station started");
}

void loop() {
   
    //String datetime_str = get_datetime_string();
    String temp_str = String(bme.readTemperature(),2);
    String humidity_str = String(bme.readHumidity(),2);
    String prs_str = String(bme.readPressure()/100,2);
    String alt_str = String(bme.readAltitude(1013.25),2);
    
    //Serial.print(datetime_str);
    //Serial.print(",");
    Serial.print(temp_str);
    Serial.print(",");
    Serial.print(humidity_str);
    Serial.print(",");
    Serial.print(prs_str);
    Serial.print(",");
    Serial.println(alt_str);
    
    lcd.clear();
    lcd.setCursor(0,0);
    //lcd.print("abc");
    lcd.print("Temp.= " + temp_str + " C*");
    //lcd.print(datetime_str);
    //lcd.setCursor(0,1);
    //lcd.print("Temp.= " + temp_str + " C*");
    lcd.setCursor(0,1);
    lcd.print("Humidity= " + humidity_str + " %");
    lcd.setCursor(0,2);
    lcd.print("Pres.= " + prs_str + " mbar");
    lcd.setCursor(0,3);
    lcd.print("Alt.= " + alt_str + " m");
    
    delay(1000);
}

bool getTime(const char *str)
{
  int Hour, Min, Sec;

  if (sscanf(str, "%d:%d:%d", &Hour, &Min, &Sec) != 3) return false;
  tm.Hour = Hour;
  tm.Minute = Min;
  tm.Second = Sec;
  return true;
}

bool getDate(const char *str)
{
  char Month[12];
  int Day, Year;
  uint8_t monthIndex;

  if (sscanf(str, "%s %d %d", Month, &Day, &Year) != 3) return false;
  for (monthIndex = 0; monthIndex < 12; monthIndex++) {
    if (strcmp(Month, monthName[monthIndex]) == 0) break;
  }
  if (monthIndex >= 12) return false;
  tm.Day = Day;
  tm.Month = monthIndex + 1;
  tm.Year = CalendarYrToTm(Year);
  return true;
}

String get_datetime_string(){
    return get_date_string() + " " + get_time_string();
}

String get_date_string(){
  return get_digitized_string(day()) + "/" + get_digitized_string(month()) + "/" + get_digitized_string(year());  
}

String get_time_string(){
  return get_digitized_string(hour()) + ":" + get_digitized_string(minute()) + ":" + get_digitized_string(second());  
}

String get_digitized_string(int digits){
  if(digits < 10)
    return "0" + String(digits);
  else
    return String(digits);
}
