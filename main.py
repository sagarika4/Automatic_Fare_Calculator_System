import pandas as pd
from fare_calculator import FareCalculator
from license_plate import recognize_license_plate
import identify_vehicle
import RPi.GPIO as GPIO   
import time
import Adafruit_CharLCD as LCD

   

def main():
    img_path='car.jpeg'
    startup(img_path)# might need to be changed to 21 for older revision Pi's.
    
def startup(img_path):
    GPIO.setmode(GPIO.BCM)
    TRIG = 23                                  
    ECHO = 24
    lcd_rs        = 20  # might need to be changed to 21 for older revision Pi's.
    lcd_en        = 21
    lcd_d4        = 6
    lcd_d5        = 13
    lcd_d6        = 19
    lcd_d7        = 26
    lcd_backlight = 4
    lcd_columns = 16
    lcd_rows    = 2
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
    
    
    lcd.clear()
    detect_object(img_path,TRIG,ECHO,lcd)
    time.sleep(15)
    lcd.clear()
    GPIO.cleanup()
    
def run_usecase(img_path,lcd):
    try:
        df=pd.read_csv('Fare Calculation.csv')
    except FileNotFoundError:
        df=pd.DataFrame(columns=['License_Plate_Number','Vehicle Type','Entry Time'])
    license_plate=(recognize_license_plate(img_path)).strChars
    v=FareCalculator(img_path,df,license_plate)
    if v.check_existence():
        '''print("Your fare amount is " + str(v.calculate_fare()))'''
        lcd.message("Fare: Rs " +str(v.calculate_fare()))
        df=v.remove_entry()
    else:
        lcd.message("Welcome Dude!")
        vehicle_type=identify_vehicle.test_type(img_path)
        df=v.insert_df(vehicle_type)
    df.to_csv('Fare Calculation.csv',index=False)
def detect_object(img_path,TRIG,ECHO,lcd):
    print ("Distance measurement in progress") 
    GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out 
    GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in 
    GPIO.output(TRIG, False)                 #Set TRIG as LOW   
    print ("Waitng For Sensor To Settle")   
    time.sleep(2)
    flag=0
    while flag==0:
        GPIO.output(TRIG, True)                  #Set TRIG as HIGH   
        time.sleep(0.00001)                      #Delay of 0.00001 seconds   
        GPIO.output(TRIG, False)                 #Set TRIG as LOW   
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
            '''print("start time " + str(pulse_start))''' #Saves the last known time of LOW pulse   
        while GPIO.input(ECHO)==1:
    
    #Check whether the ECHO is HIGH
            '''print("echo pin got 1")'''
            pulse_end = time.time()                #Saves the last known time of HIGH pulse  
            '''print("end time " +str(pulse_end))'''  
        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable 
        '''print(pulse_duration)'''
        distance = pulse_duration * 17000   #Multiply pulse duration by 17150 to get distance   
        if distance > 2 and distance <500:
            print(distance)
            run_usecase(img_path,lcd)
            flag=1
    
if __name__ == "__main__":
    main()
