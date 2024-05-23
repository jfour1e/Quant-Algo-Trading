import time
import hashlib
import hmac
import requests
from flask import Flask, request, json

app = Flask(__name__)

BITSTAMP_API_KEY = 'Icmpyrz4cg0boWWmChNnNmV6D6wHb2xV'
BITSTAMP_SECRET_KEY = 'mQ9symgNc7s6Tvsycp9fBp3ehpRTLc7G'
BITSTAMP_CLIENT_ID = 'btqu0804'

def generate_nonce():
    return str(int(time.time() * 1000))

def generate_signature(nonce, api_key, client_id, secret_key):
    message = nonce + client_id + api_key
    signature = hmac.new(secret_key.encode(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest().upper()
    return signature

def place_order(order_type, amount):
    nonce = generate_nonce()
    signature = generate_signature(nonce, BITSTAMP_API_KEY, BITSTAMP_CLIENT_ID, BITSTAMP_SECRET_KEY)
    
    url = f'https://www.bitstamp.net/api/v2/{order_type}/'
    params = {
        'key': BITSTAMP_API_KEY,
        'signature': signature,
        'nonce': nonce,
        'amount': amount
    }
    response = requests.post(url, data=params)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    response = None
    if 'Buy' in data.get('message', ''):
        response = place_order('buy/market/btcusd', 1)  # Modify amount as needed
    elif 'Sell' in data.get('message', ''):
        response = place_order('sell/market/btcusd', 1)  # Modify amount as needed
    return json.dumps(response), 200

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')