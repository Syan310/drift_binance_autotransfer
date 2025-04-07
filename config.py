# config.py

# ========= Binance 主网配置 =========
BINANCE_API_KEY = "your_binance_api_key_here"
BINANCE_API_SECRET = "your_binance_api_secret_here"

BINANCE_TESTNET = False  # 设置为 False 使用主网
BINANCE_USDC_ADDRESS = "your_binance_usdc_deposit_address"
BINANCE_USDC_NETWORK = "SOL"  # 通常是 SOL、ERC20 或 TRC20，注意和提现地址网络匹配

# ========= Solana 钱包（Drift 使用） =========
SOLANA_KEYPAIR_PATH = "your_keypair_file.json"  # Drift 主网使用你的 Solana 钱包

# ========= 自动转账设置 =========
TRANSFER_AMOUNT = 10  # 每次转账的 USDC 数量，可根据需要调整

BINANCE_MARGIN_THRESHOLD = 1.1    # Binance 联合保证金率小于此值触发资金从 Drift → Binance
DRIFT_HEALTH_THRESHOLD = 1.1      # Drift 健康度低于此值触发资金从 Binance → Drift

# ========= 运行参数 =========
CHECK_INTERVAL_SECONDS = 60  # 轮询周期（单位：秒），建议 60~300 秒之间