# test_binance_connection.py
from binance.client import Client
import config

def test_binance_connection():
    client = Client(
        api_key=config.BINANCE_API_KEY,
        api_secret=config.BINANCE_API_SECRET
    )

    # 获取账户信息
    account = client.get_account()
    print("✅ 成功连接 Binance API，资产如下：")
    for asset in account["balances"]:
        free = float(asset["free"])
        locked = float(asset["locked"])
        if free > 0 or locked > 0:
            print(f"{asset['asset']}: Free={free}, Locked={locked}")

if __name__ == "__main__":
    test_binance_connection()
