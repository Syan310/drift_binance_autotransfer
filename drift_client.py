# drift_client.py

import json
import logging

# Import driftpy modules for interacting with Drift Protocol
try:
    from solana.keypair import Keypair
    from solana.rpc.async_api import AsyncClient
    from anchorpy import Provider, Wallet
    from driftpy.constants.config import configs
    from driftpy.drift_client import DriftClient as DriftPyClient
    from driftpy.drift_user import DriftUser
except ImportError as e:
    logging.error("DriftPy library not found. Please install driftpy and dependencies.")
    raise

import config

class DriftClient:
    """Client to monitor a Drift account and perform deposits/withdrawals."""
    def __init__(self):
        # Load Solana keypair for the Drift wallet
        with open(config.DRIFT_KEY_PATH, 'r') as f:
            secret = json.load(f)
        keypair = Keypair.from_secret_key(bytes(secret))
        # Setup Solana RPC client and Anchor provider
        env = config.DRIFT_ENV
        if env not in configs:
            raise Exception(f"Unknown Drift environment: {env}")
        drift_config = configs[env]
        connection = AsyncClient(drift_config.default_http)
        wallet = Wallet(keypair)
        provider = Provider(connection, wallet)
        # Initialize Drift client and user
        self.drift = DriftPyClient.from_config(drift_config, provider)
        self.user = DriftUser(self.drift)
        # Assume USDC is the collateral asset, determine its spot market index from config or default (1)
        self.usdc_market_index = getattr(config, 'DRIFT_USDC_MARKET_INDEX', 1)

    async def get_health(self):
        """Get the current health ratio of the Drift account."""
        # DriftUser.get_health() returns a health ratio; values > 1 (or >100%) are safe, near 1 is at risk.
        try:
            # If DriftUser.get_health is implemented as async
            health = await self.user.get_health()
        except AttributeError:
            # If get_health is sync, call directly
            health = self.user.get_health()
        return float(health)

    async def withdraw_from_drift(self, amount):
        """Withdraw the specified amount of USDC from Drift into the wallet."""
        # Convert amount to smallest units (assuming USDC has 6 decimals)
        raw_amount = int(amount * (10 ** 6))
        # Determine associated token account for USDC (where to withdraw to)
        user_token_account = self.drift.get_associated_token_account_public_key(self.usdc_market_index)
        # Execute withdrawal (allowing borrowing if necessary by setting reduce_only=False)
        tx = await self.drift.withdraw(raw_amount, self.usdc_market_index, user_token_account, reduce_only=False)
        return tx

    async def deposit_to_drift(self, amount):
        """Deposit the specified amount of USDC from the wallet into Drift."""
        raw_amount = int(amount * (10 ** 6))
        # Perform deposit into the Drift account for the given spot market index
        tx = await self.drift.deposit(raw_amount, self.usdc_market_index)
        return tx
