# binance_client.py

import time
import hmac
import hashlib
from urllib.parse import urlencode

import aiohttp

import config

class BinanceClient:
    """Client to interact with Binance API for account status and fund transfers."""
    def __init__(self):
        # API credentials and endpoints
        self.api_key = config.BINANCE_API_KEY
        self.api_secret = config.BINANCE_API_SECRET
        self.futures_base_url = "https://fapi.binance.com"  # Binance Futures (USD-M Futures) base URL
        self.spot_base_url = "https://api.binance.com"      # Binance Spot API base URL (for withdrawals)
        # Initialize an HTTP session for re-use in requests
        self.session = aiohttp.ClientSession()

    async def get_margin_ratio(self):
        """Fetch the unified margin ratio (as percentage) of the Binance account (e.g. cross futures)."""
        endpoint = "/fapi/v2/account"
        # Prepare query string with timestamp and signature
        timestamp = int(time.time() * 1000)
        query_str = f"timestamp={timestamp}"
        signature = hmac.new(self.api_secret.encode(), query_str.encode(), hashlib.sha256).hexdigest()
        url = f"{self.futures_base_url}{endpoint}?{query_str}&signature={signature}"
        headers = {'X-MBX-APIKEY': self.api_key}
        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Binance API error (status {resp.status}): {text}")
            data = await resp.json()
        # Calculate margin ratio as (totalMaintMargin / totalMarginBalance) * 100
        total_margin_balance = float(data.get('totalMarginBalance', 0))
        total_maint_margin = float(data.get('totalMaintMargin', 0))
        if total_margin_balance <= 0:
            # Avoid division by zero
            return 0.0
        margin_ratio = (total_maint_margin / total_margin_balance) * 100.0
        return margin_ratio

    async def withdraw_to_address(self, amount):
        """Withdraw the specified amount of asset from Binance to the configured target address."""
        endpoint = "/sapi/v1/capital/withdraw/apply"
        # Prepare request parameters
        params = {
            "coin": config.TRANSFER_ASSET,
            "address": config.TARGET_ADDRESS,
            "amount": amount,
            "network": config.NETWORK,
            "timestamp": int(time.time() * 1000)
        }
        # Create query string and signature
        query_str = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query_str.encode(), hashlib.sha256).hexdigest()
        query_str += f"&signature={signature}"
        url = f"{self.spot_base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        # Execute the withdrawal request
        async with self.session.post(f"{url}?{query_str}", headers=headers) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"Binance withdrawal failed (status {resp.status}): {text}")
            # If successful, Binance returns an ID for the withdrawal
            # We'll log the response text for reference
            return text

    async def close(self):
        """Close the HTTP session."""
        await self.session.close()
