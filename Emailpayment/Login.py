
import gmail
import time
import datetime

from gmail import Gmail

#Filter emails that are only payment emails
def filterPayments(emails):
    i = 0
    filtered = []
    while i < len(emails):
        emails[i].fetch()
        if "paid" in emails[i].subject:
            filtered.append(emails[i])
        i+=1
    return filtered

#Check if email from venmo is for DKE Keg and not mdelaus (depending on which email we use might not need this)
def isKegEmail(email):
    value = False
    email.fetch()
    body = email.body
    if "DKE Keg" in body:
        value = True
    return value


# Main Part, use Gmail to find venmo balances
IDs = []
charges = {}

#can use this if we only want to check most recent emails
#then = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

while True:
    g = Gmail()
    g.login("mikedelaus@gmail.com", "quechee27")
    newMail = g.inbox().mail(fr="venmo@venmo.com")

    #Filter venmo emails that are payments emails from venmo
    payments = filterPayments(newMail)

    #Can use this part to implement only most recent email checking, Note: use email.sent_at to get the emails timestamp.
    #for i in pay:
        #if i.sent_at >= then:
            #payments.append(i)

    #Iterate through payment emails to find balances
    i = 0
    while i < len(payments):

        #Check if the ID number of the email has already been checked
        #as this prevents checking emails twice and incorrectly calculating balances
        if payments[i].uid not in IDs:

            #Check if email is a payment to DKE Keg  
            if isKegEmail(payments[i]): 

                #Seperate out the subject of the email to find Name and Amount that was paid 
                IDs.append(payments[i].uid) 
                payments[i].fetch()
                message =  payments[i].subject
                name = message.split(" p")[0]
                if len(message.split("$")[1]) >= 10:
                    amount = float(message.split("$")[1].split(" ")[0])
                else:
                    amount = float(message.split("$")[1])

                #Update amount if name is already in the database
                if name in charges:
                    amount = charges[name] + amount

                #This check is only for when I (Mike DeLaus) pay from the my venmo account as it is the same email we use for DKE Keg
                if name != "You":
                    charges[name] = amount
        i+=1
    print charges

    #Sleep the program so we don't constantly check, can probably find better way to do this
    time.sleep(60)

    #Logout of email so next check uses a refreshed inbox
    g.logout()