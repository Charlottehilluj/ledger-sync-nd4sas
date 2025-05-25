import requests
import time

ETHERSCAN_API_KEY = "YourEtherscanApiKey"
MIN_VALUE_ETH = 1000  # Порог в ETH для "кита"
ADDRESS_LIST = ["0x742d35Cc6634C0532925a3b844Bc454e4438f44e"]  # Пример: адрес Bitfinex

def eth_price_in_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url).json()
    return response["ethereum"]["usd"]

def check_large_transactions(address):
    print(f"Проверка адреса {address}...")
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    txs = response.json().get("result", [])

    eth_price = eth_price_in_usd()
    for tx in txs[:10]:  # Проверяем только последние 10 транзакций
        value_eth = int(tx["value"]) / 10**18
        usd_value = value_eth * eth_price
        if usd_value > MIN_VALUE_ETH * eth_price:
            print(f"🐋 Обнаружен кит: {value_eth:.2f} ETH (~${usd_value:,.2f})")
            print(f"  От: {tx['from']} ➡️ Кому: {tx['to']}")
            print(f"  Хеш: {tx['hash']}")
            print("-" * 60)

if __name__ == "__main__":
    for addr in ADDRESS_LIST:
        check_large_transactions(addr)
