# drift_api.py

import json
from solders.keypair import Keypair
from anchorpy import Wallet, Provider
from solana.rpc.async_api import AsyncClient
from driftpy.drift_client import DriftClient
from driftpy.drift_user import DriftUser
from driftpy.constants.numeric_constants import QUOTE_PRECISION
from config import SOLANA_KEYPAIR_PATH

async def init_drift():
    """Initializes the Drift client and user from wallet and provider."""
    with open(SOLANA_KEYPAIR_PATH, "r") as f:
        secret = json.load(f)
    kp = Keypair.from_bytes(bytes(secret))
    wallet = Wallet(kp)
    connection = AsyncClient("https://rpc.helius.xyz/?api-key=c048307b-bd32-463a-a253-4649745a1304")
    drift_client = DriftClient(connection, wallet)
    drift_user = DriftUser(drift_client, wallet.public_key)
    
    await drift_client.subscribe()
    await drift_user.subscribe()
    return drift_client, drift_user

async def assess_account_health(drift_user: DriftUser):
    """Assesses the health of the user's Drift account."""
    try:
        # Check if the account can be liquidated
        liquidation_status = await drift_user.can_be_liquidated()
        if liquidation_status:
            print("⚠️ The account is at risk of liquidation.")

        # Get the current health of the account
        health = await drift_user.get_health()
        print(f"Current health: {health}")

        # Get the free collateral available
        free_collateral = await drift_user.get_free_collateral()
        print(f"Free collateral: {free_collateral}")

    except Exception as e:
        print(f"❌ Failed to assess account health: {e}")


async def deposit_to_drift(drift_client: DriftClient, amount: float):
    """Deposits a specified amount of USDC into Drift."""
    try:
        await drift_client.deposit(
            amount=int(amount * QUOTE_PRECISION),
            market_index=0  # USDC index
        )
        print(f"✅ Deposited {amount} USDC to Drift.")
    except Exception as e:
        print(f"❌ Drift deposit failed: {e}")

async def withdraw_from_drift(drift_client: DriftClient, amount: float):
    """Withdraws a specified amount of USDC from Drift."""
    try:
        await drift_client.withdraw(
            amount=int(amount * QUOTE_PRECISION),
            market_index=0,
            reduce_only=False
        )
        print(f"✅ Withdrew {amount} USDC from Drift.")
    except Exception as e:
        print(f"❌ Drift withdrawal failed: {e}")
