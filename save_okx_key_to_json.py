import json
import os
from solders.keypair import Keypair

# ✅ 你的 OKX Web3 钱包私钥
base58_key = "3gtn4fvZFsMcToiB4bdkpchiEZV8mn1rgJc4iP79hV6t4zZkGqeoA6HUngRfuqwBKC89LXd7Sy8RLWm2v5aYdcov"

# 转换为 Keypair
kp = Keypair.from_base58_string(base58_key)
secret_bytes = list(kp.to_bytes())

# 保存为 JSON 文件
os.makedirs("wallet", exist_ok=True)
with open("wallet/drift_wallet.json", "w") as f:
    json.dump(secret_bytes, f)

print("✅ 私钥已保存为 wallet/drift_wallet.json")
print("🔑 公钥地址:", kp.pubkey())
