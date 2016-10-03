#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import DBAccessor
import Login 
from Login import findPayments
from lcd_i2c import lcd_string, lcd_byte, LCD_LINE_1, LCD_LINE_2, LCD_CMD

continue_reading = True
current_uid = "0"
current_name = "THOMAS LYNN"
current_balance = 0.0
login_counter = 0
VALVE_OUT = 21
BUTTON_IN = 69
DELTA_BALANCE = 69
LOGIN_COUNTER_START = 69
SAFET_COUNTER_START = 69
beer_counter = 69
# Keep beers dranken in a file
# beer_percentage = 165 - beers dranken/165 *100 
def default_display():
    lcd_string(" Natural Light ",LCD_LINE_1)
    #display beer percentage
    lcd_string("               ",LCD_LINE_2)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    lcd_byte(0x01, LCD_CMD)
    continue_reading = False
    GPIO.cleanup()
    dbaccessor.closeConnection()

def logout():
    print "Logged Out"
    current_uid="0"
    current_balance = 0.0
    current_name = "THOMAS LYNN"
    default_display()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

dbaccessor = DBAccessor.DBAccessor()
default_display()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    if login_counter == 0 or safety_counter == 0:
        logout()

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        #convert uid to standard string representation
        str_uid = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        lcd_string(str_uid,LCD_LINE_2)
        #if user is already logged in, log them out 
        if str_uid == current_uid:
            logout()
            continue
        else:
            current_uid=str_uid
            # login to the database
            current_name = dbaccessor.getName(current_uid)
            current_balance = dbaccessor.getBalance(current_uid)
            #display name and balance on screen
            lcd_string(current_name,LCD_LINE_1)
            lcd_string(str(current_balance),LCD_LINE_2)
            login_counter = LOGIN_COUNTER_START
            safety_counter = SAFET_COUNTER_START
    
    if current_balance > 0:
        GPIO.output(VALVE_OUT,True)
        while GPIO.input(BUTTON_IN):
            if current_balance <=0:
                GPIO.output(VALVE_OUT,False)
                break
            time.sleep(.5)
            current_balance -= DELTA_BALANCE
            lcd_string(str(current_balance),LCD_LINE_2)
            login_counter = LOGIN_COUNTER_START
            safety_counter -= 1
            beer_counter -= 1
        dbaccessor.updateBalance(current_uid,current_balance)
        time.sleep(.5)
        safety_counter -= 1
        login_counter -= 1
    else:
        GPIO.output(VALVE_OUT,False)
        time.sleep(.5)
        login_counter -= 1


        
