import json
from solana.keypair import Keypair
from driftpy.drift_client import DriftClient
from driftpy.drift_user import DriftUser
from driftpy.constants.numeric_constants import QUOTE_PRECISION
from anchorpy import Provider, Wallet
from solana.rpc.async_api import AsyncClient
from config import SOLANA_KEYPAIR_PATH


async def init_drift():
    """Initializes the Drift client and user from wallet and provider."""
    with open(SOLANA_KEYPAIR_PATH, 'r') as f:
        secret = json.load(f)
    kp = Keypair.from_secret_key(bytes(secret))
    wallet = Wallet(kp)
    connection = AsyncClient("https://api.mainnet-beta.solana.com")
    provider = Provider(connection, wallet)
    drift_client = DriftClient(provider)
    drift_user = DriftUser(drift_client)
    await drift_client.subscribe()
    await drift_user.subscribe()
    return drift_client, drift_user


async def get_health_ratio(drift_user):
    """Returns the current health ratio of the Drift user."""
    try:
        ratio = await drift_user.get_health_ratio()
        return float(ratio)
    except Exception as e:
        print(f"Failed to fetch health ratio: {e}")
        return None


async def withdraw_from_drift(drift_client, amount):
    """Withdraws a specified amount of USDC from Drift."""
    try:
        await drift_client.withdraw(
            amount=int(amount * QUOTE_PRECISION),
            market_index=0,  # 0 is typically USDC
            reduce_only=False
        )
        print(f"Withdrew {amount} USDC from Drift.")
    except Exception as e:
        print(f"Drift withdrawal failed: {e}")


async def deposit_to_drift(drift_client, amount):
    """Deposits a specified amount of USDC into Drift."""
    try:
        await drift_client.deposit(
            amount=int(amount * QUOTE_PRECISION),
            market_index=0  # 0 is typically USDC
        )
        print(f"Deposited {amount} USDC to Drift.")
    except Exception as e:
        print(f"Drift deposit failed: {e}")