
import gmail
import time

from gmail import Gmail


# play with your gmail...
while True:
	charges = {}
	g = Gmail()
	g.login("mikedelaus@gmail.com", "quechee27")
	payments = g.inbox().mail(fr="kegdke@gmail.com")

	i = 0
	while i < len(payments):

		payments[i].fetch()
		message =  payments[i].subject
		name = message.split(" p")[0]
		amount = float(message.split("$")[1])
		if name in charges:
			amount = charges[name] + amount
		charges[name] = amount
		i+=1
	print charges
	time.sleep(60)



g.logout()