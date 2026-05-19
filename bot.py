import requests
import json
import time
import hmac
import hashlib
from datetime import datetime

API_URL = "https://api.quantumxexchange.com/v3/order"
SYMBOL = "BTCUSDT"

# Load API key
with open("apiKey.txt", "r") as f:
    API_KEY = f.readline().strip()
    API_SECRET = f.readline().strip()

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

balance = 25000.00
position = 0.0


def sign_payload(payload: dict) -> str:
    encoded = json.dumps(payload, separators=(",", ":")).encode()
    return hmac.new(
        API_SECRET.encode(),
        encoded,
        hashlib.sha256
    ).hexdigest()


def get_market_price():
    # Simulated market price feed
    return round(64000 + (time.time() % 500), 2)


def place_order(side: str, quantity: float, price: float):
    payload = {
        "symbol": SYMBOL,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "price": price,
        "timestamp": int(time.time() * 1000)
    }

    payload["signature"] = sign_payload(payload)

    response = requests.post(
        API_URL,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    return response.json()


def trading_loop():
    global balance
    global position

    while True:
        price = get_market_price()

        print(f"[{datetime.utcnow()}] {SYMBOL} price = ${price}")

        # Fake momentum strategy
        if price % 2 < 1 and balance > 1000:
            qty = round(1000 / price, 5)

            print(f"[+] BUY signal triggered for {qty} BTC")

            result = place_order("BUY", qty, price)

            balance -= qty * price
            position += qty

            print(f"[ORDER FILLED] {result}")

        elif position > 0:
            qty = position

            print(f"[-] SELL signal triggered for {qty} BTC")

            result = place_order("SELL", qty, price)

            balance += qty * price
            position = 0

            print(f"[ORDER FILLED] {result}")

        print(f"[ACCOUNT] Balance=${balance:.2f} Position={position}")
        print("-" * 60)

        time.sleep(3)


if __name__ == "__main__":
    trading_loop()
