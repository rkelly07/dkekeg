
import gmail
import time
import datetime
import DBAccessor

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
    if "thomaslynn" in body:
        value = True
    return value


def findPayments(username, password):
    
    # Main Part, use Gmail to find venmo balances
    file = open('recent.txt', 'r')
    most_recent = file.read()
    file.close()
    IDs = [0,most_recent]
    charges = {}

    #can use this if we only want to check most recent emails
    #then = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    '''


    Make benefits_on true to provide benefits to DKEggertor founders


    '''
    benefits_on = False
    g = Gmail()
    g.login(username, password)
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
            if isKegEmail(payments[i]) and int(payments[i].uid) >= int(most_recent)+1:

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

                #Provides benefits for the founding members of DKEggerator
                founders = ["Michael DeLaus", "Ryan Kelly", "Mitch Maisel"]
                for name in founders:
                    if benefits_on == True:
                        charges[name] = 999999999999
                file = open('recent.txt', 'w')
                most_recent = payments[i].uid
                file.write(str(most_recent))
                file.close()
        i+=1
    return charges

    #Sleep the program so we don't constantly check, can probably find better way to do this
    #time.sleep(60)

    #Logout of email so next check uses a refreshed inbox
    g.logout()
#Implement Main file to run this funciton

def main():
    dbaccessor = DBAccessor.DBAccessor()

    while True:
        payments = findPayments("kegdke@gmail.com","phiyale1844")
        for name in payments:
            dbaccessor.getKerberos()



if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
