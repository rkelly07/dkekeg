#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import DBAccessor

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
DBAccessor = DBAccessor.DBAccessor()
# Welcome message
print "Scan the ID to be added to the database"

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        kerberos = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        name = raw_input("Enter the name associated with your venmo account: ")
        DBAccessor.addUser(name,kerberos)
        break
print "Successfully added new user"
    
        

