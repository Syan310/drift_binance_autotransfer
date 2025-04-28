# config.py

# Configuration for Binance and Drift monitoring program.

# Binance API credentials
BINANCE_API_KEY = "your_binance_api_key"
BINANCE_API_SECRET = "your_binance_api_secret"

# Drift configuration
# Path to Solana keypair secret file for the Drift wallet (or provide key as needed).
DRIFT_KEY_PATH = "path/to/your/solana/keypair.json"
# Drift environment: e.g. 'mainnet' for mainnet, 'devnet' for devnet. Use 'mainnet' for production.
DRIFT_ENV = "mainnet"

# Asset and network settings
TRANSFER_ASSET = "USDC"
# Amount of USDC to transfer for each operation (as a float or int of whole tokens)
USDC_TRANSFER_AMOUNT = 100.0

# Target address for transfers (the wallet address to which Binance withdraws and from which Drift deposits).
TARGET_ADDRESS = "your_wallet_address"

# Network chain name for Binance withdrawals (e.g. 'SOL' for Solana network, 'ETH' for Ethereum, etc.)
NETWORK = "SOL"

# Thresholds for triggering transfers
# If Binance margin ratio (in percentage) falls below this, it's considered under-utilized (safe).
# If margin ratio is above this, the account is at risk (close to liquidation).
MARGIN_RATIO_THRESHOLD = 150.0  # e.g. 150% (if margin ratio drops below this, funds can be safely withdrawn)
# If Drift account health (ratio or percentage) falls below this, the account is at risk.
# If health is above this, the account has excess collateral.
HEALTH_THRESHOLD = 1.2  # e.g. 1.2 (120% health ratio)

# Cooldown period (in seconds) to prevent frequent repetitive transfers
COOLDOWN = 60
