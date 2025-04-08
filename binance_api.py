import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from decimal import Decimal
from config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    BINANCE_TESTNET,
    BINANCE_USDC_ADDRESS,
    BINANCE_USDC_NETWORK
)

# Initialize Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
if BINANCE_TESTNET:
    client.API_URL = 'https://testnet.binance.vision/api'


def get_account_info():
    """Fetches full account information from Binance."""
    try:
        return client.get_account()
    except BinanceAPIException as e:
        print(f"Error fetching account info: {e}")
        return None



def get_margin_ratio():
    """
    Returns a fake 'margin ratio' for non-margin users, based on USDT balance.
    You can replace this with true margin account logic if you enable it.
    """
    balance = get_asset_balance('USDT')
    if balance is None:
        return None
    if balance < 1:
        return 0.5  # 模拟危险
    elif balance < 10:
        return 1.2  # 接近阈值
    else:
        return 5.0  # 安全


# def get_margin_ratio():
#     """
#     Returns a margin ratio proxy using margin account data.
#     NOTE: This is NOT Portfolio Margin (uniMMR), which requires special activation.
#     """
#     try:
#         response = client._request_margin_api('get', '/sapi/v1/margin/account')
#         total_assets = Decimal(response['totalAssetOfBtc'])
#         total_liabilities = Decimal(response['totalLiabilityOfBtc'])
#         if total_liabilities == 0:
#             return float('inf')
#         return float(total_assets / total_liabilities)
#     except Exception as e:
#         print(f"Error fetching margin ratio: {e}")
#         return None


def get_asset_balance(asset='USDC'):
    """Gets the free balance of a specific asset."""
    info = get_account_info()
    if not info:
        return None
    for balance in info['balances']:
        if balance['asset'] == asset:
            return float(balance['free'])
    return 0.0


def withdraw_usdc_to_wallet(amount, address=None, network=None):
    """Withdraws USDC to specified wallet address via chosen network."""
    try:
        address = address or BINANCE_USDC_ADDRESS
        network = network or BINANCE_USDC_NETWORK
        result = client.withdraw(
            coin='USDC',
            amount=amount,
            address=address,
            network=network
        )
        print(f"Withdrawal initiated: {result}")
        return result
    except BinanceAPIException as e:
        print(f"Withdrawal failed: {e}")
        return None


def get_usdc_deposit_address(network=None):
    """Fetches the USDC deposit address for the account."""
    try:
        network = network or BINANCE_USDC_NETWORK
        result = client.get_deposit_address(coin='USDC', network=network)
        return result['address']
    except BinanceAPIException as e:
        print(f"Error fetching deposit address: {e}")
        return None