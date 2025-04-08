# test_binance_api.py

import binance_api

def test_get_account_info():
    print("▶ 测试 get_account_info()")
    info = binance_api.get_account_info()
    if info:
        print("✅ 账户信息获取成功，现有资产如下：")
        for b in info["balances"]:
            if float(b["free"]) > 0:
                print(f"{b['asset']}: {b['free']}")
    else:
        print("❌ 获取账户信息失败")

def test_get_margin_ratio():
    print("\n▶ 测试 get_margin_ratio()")
    ratio = binance_api.get_margin_ratio()
    if ratio is not None:
        print(f"✅ 保证金资产/负债比：{ratio:.4f}")
    else:
        print("❌ 获取保证金比率失败")


def test_get_asset_balance():
    print("\n▶ 测试 get_asset_balance('USDC')")
    balance = binance_api.get_asset_balance('USDC')
    if balance is not None:
        print(f"✅ 可用 USDC 余额：{balance}")
    else:
        print("❌ 获取 USDC 余额失败")

def test_get_usdc_deposit_address():
    print("\n▶ 测试 get_usdc_deposit_address()")
    address = binance_api.get_usdc_deposit_address()
    if address:
        print(f"✅ 当前账户 USDC 充值地址：{address}")
    else:
        print("❌ 获取充值地址失败")

# ⚠️ 提现测试请确保你账户里有 USDC 且地址和网络设置正确，否则先不跑
# def test_withdraw_usdc_to_wallet():
#     print("\n▶ 测试 withdraw_usdc_to_wallet()")
#     result = binance_api.withdraw_usdc_to_wallet(amount=5)  # 示例提现 5 USDC
#     if result:
#         print("✅ 提现指令已发送")
#     else:
#         print("❌ 提现失败")

if __name__ == "__main__":
    test_get_account_info()
    test_get_margin_ratio()
    test_get_asset_balance()
    test_get_usdc_deposit_address()
    # test_withdraw_usdc_to_wallet()  # 如需测试提现，请取消注释
