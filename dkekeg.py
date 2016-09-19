#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import DBAccessor

continue_reading = True
current_uid = "0"

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    DBAccessor.closeConnection()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

DBAccessor = DBAccessor()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
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
        
        #if user is already logged in, log them out 
        if str_uid == current_uid:
            print "Logged Out"
            current_uid="0"
            continue
        else:
            current_uid=str_uid
            # Check Venmo for new payments here
            """

            TODO MIKE

            """
            # login to the database
            currentName = DBAccessor.getName(current_uid)
            currentBalance = DBAccessor.getBalance(current_uid)
            # TODO MAISEL CODE



        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        