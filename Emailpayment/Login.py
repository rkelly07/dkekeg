from requests import session

payload = {
    'action': 'login',
    'username': "mikedelaus@gmail.com",
    'password': "quechee27"
}

with session() as c:
    c.post('https://api.venmo.com/v1/oauth/authorize?client_id=2899&scope=access_payment_history', data=payload)
    response = c.get('https://venmo.com/MikeDeLaus')
    print(response.text)