#!/usr/bin/python
import time
import RPi.GPIO as GPIO

print("Car Parking System : Setup Started")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

'''
Define pin for sensors
'''
slot1_Sensor = 29
slot2_Sensor = 31
GPIO.setup(slot1_Sensor, GPIO.IN)
GPIO.setup(slot2_Sensor, GPIO.IN)

print("Car Parking System : Setup Complete")


# Define delay between readings
delay = 5

print("Car Parking System : System Begins")
while 1:
    slot1_status = GPIO.input(slot1_Sensor)
    time.sleep(0.2)
    slot2_status = GPIO.input(slot2_Sensor)
    time.sleep(0.2)

    if slot1_status == False:
        # Do something when Slot 1 is occupied
        print("Slot 1 is occupied")
        time.sleep(0.2)
    else:
        # Do something when Slot 1 is free
        print("Slot 1 is free")
        time.sleep(0.2)

    if slot2_status == False:
        # Do something when Slot 2 is occupied
        print("Slot 2 is occupied")
        time.sleep(0.2)
    else:
        # Do something when Slot 2 is free
        print("Slot 2 is free")
        time.sleep(0.2)

print("Car Parking System : System Ends")


'''
Pin connections of Ir Module & rpi


# ir sensor 1 :
- out = pin 29
- Vcc = pin 2 (5v Power)
- Gnd = pin 6 (GND)

# ir sensor 2 :
- out = pin 31
- Vcc = pin 4 (5v Power)
- Gnd = pin 9 (GND)


https://6a79193f-6605-44e3-90fd-90cf4c111036-00-1hcnyifnrpkd8.riker.replit.dev/update?slot=slot2&status=on

'''