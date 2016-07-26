import time
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.IN)
#GPIO.setup(16, GPIO.IN)

#some keg variables
kegprice = 80 #dollars
kegvolume = 960 #oz
est_flowrate = 2 #oz/second
delta_t = 0.25 #interval of iteration in seconds

#basic user directory with balances
users = {'Mitch':1, 'Ryan':2, 'Mike':3}

#system variables
sys_state = 'idle' #idle, active, admin

#class for all variables to keep things clean
class Keg(object):
    def __init__(self, kegprice, kegvolume, est_flowrate, delta_t, user, balance, sys_state, pin_input):
        self.kegprice = kegprice
        self.kegvolume = kegvolume
        self.est_flowrate = est_flowrate
        self.delta_t = delta_t
        self.user = user
        self.balance = balance
        self.sys_state = sys_state
        self.pin_input = pin_input

    #determines whether valve is open or closed
    def valve_state(self):
        if self.balance > 0 and self.sys_state == 'active':
            return 'open'
        else:
            return 'closed'

    def handle_state(self):
        if self.pin_input == 'GPIO.HIGH':
            return 'pulled'
        else:
            return 'not pulled'

    def delta_balance(self):
        costpervol = self.kegprice / self.kegvolume
        costpertime = costpervol * self.est_flowrate
        return costpertime * self.delta_t




#simulating recognized card tap
while True:
    inp = input('Enter User: ')
    if inp in users:
        sys_state = 'active'
        print('Active State')
        safety_counter = 40 #valve shouldn't be opened for more than 3 min at a time
        active_counter = 15 #timer for active state that gets reset when handle is pulled
    
        while safety_counter > 0 and active_counter > 0:
            #define Keg class instance with user info
            current = Keg(kegprice, kegvolume, est_flowrate, delta_t, inp, users[inp], sys_state, 'GPIO.HIGH')
            if current.valve_state() == 'open':
                #opens valve
                #GPIO.output(21, True)
                print('valve open')

                #now looks to handle
                if current.handle_state() == 'pulled':
                    time.sleep(delta_t)
                    users[inp] -= current.delta_balance() #subtracting from balance
                    print(users[inp])
                    active_counter = 15
                    safety_counter -= 1
                elif current.handle_state() == 'not pulled':
                    time.sleep(delta_t)
                    active_counter -= 1
                    safety_counter -= 1
            
            elif current.valve_state() == 'closed':
                #closes valve
                #GPIO.output(21, False)
                print('valve closed')
                if users[inp] <= 0: #if we do end up getting a display
                    print('Zero Balance')
                active_counter = 0 #triggers else statement below
        else:
            sys_state = 'idle'
            print('Idle State')
            
    elif inp == 'quit':
        break
    else:
        print('User not recognized')
