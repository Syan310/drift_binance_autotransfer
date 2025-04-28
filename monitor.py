# monitor.py

import asyncio
import logging
import config

import binance_client
import drift_client

# Timestamps of last transfer actions to enforce cooldown
last_binance_withdraw = 0.0
last_drift_withdraw = 0.0
last_drift_deposit = 0.0

async def monitor_binance(binance: binance_client.BinanceClient, lock: asyncio.Lock):
    """Continuously monitor Binance margin ratio and trigger withdrawal if conditions are met."""
    global last_binance_withdraw
    while True:
        try:
            # Get current margin ratio (percentage)
            margin_ratio = await binance.get_margin_ratio()
            logging.info(f"Binance保证金率: {margin_ratio:.2f}%")
            # If margin ratio is below threshold (account is under-utilized), withdraw some funds
            if margin_ratio < config.MARGIN_RATIO_THRESHOLD:
                now = asyncio.get_event_loop().time()
                if now - last_binance_withdraw >= config.COOLDOWN:
                    async with lock:
                        logging.info(f"Binance保证金率{margin_ratio:.2f}%低于阈值{config.MARGIN_RATIO_THRESHOLD}%，将提取{config.USDC_TRANSFER_AMOUNT}{config.TRANSFER_ASSET}。")
                        try:
                            result = await binance.withdraw_to_address(config.USDC_TRANSFER_AMOUNT)
                            logging.info(f"Binance提现指令已发送，响应: {result}")
                        except Exception as e:
                            logging.error(f"Binance提现错误: {e}")
                        last_binance_withdraw = asyncio.get_event_loop().time()
            # If margin ratio is above threshold (risk is high)
            elif margin_ratio > config.MARGIN_RATIO_THRESHOLD:
                logging.warning(f"Binance保证金率{margin_ratio:.2f}%高于阈值{config.MARGIN_RATIO_THRESHOLD}%，账户风险提高，请尽快向Binance存入资金！")
            # Sleep briefly before next check (low latency)
            await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"Binance监控循环异常: {e}")
            await asyncio.sleep(5)

async def monitor_drift(drift: drift_client.DriftClient, binance: binance_client.BinanceClient, lock: asyncio.Lock):
    """Continuously monitor Drift account health and trigger deposits/withdrawals as needed."""
    global last_drift_withdraw, last_drift_deposit
    while True:
        try:
            health = await drift.get_health()
            logging.info(f"Drift账户健康度: {health:.2f}")
            # If health is below threshold (at risk)
            if health < config.HEALTH_THRESHOLD:
                now = asyncio.get_event_loop().time()
                if now - last_drift_deposit >= config.COOLDOWN:
                    async with lock:
                        logging.warning(f"Drift健康度{health:.2f}低于阈值{config.HEALTH_THRESHOLD}，将存入{config.USDC_TRANSFER_AMOUNT}{config.TRANSFER_ASSET}提高保证金。")
                        try:
                            # Withdraw from Binance to wallet for funding Drift deposit
                            try:
                                result = await binance.withdraw_to_address(config.USDC_TRANSFER_AMOUNT)
                                logging.info(f"已从Binance提取{config.USDC_TRANSFER_AMOUNT}{config.TRANSFER_ASSET}用于Drift存款，Binance响应: {result}")
                            except Exception as e:
                                logging.error(f"为Drift存款从Binance提取资金时出错: {e}")
                            # Deposit into Drift
                            tx = await drift.deposit_to_drift(config.USDC_TRANSFER_AMOUNT)
                            logging.info(f"Drift存入成功，交易: {tx}")
                        except Exception as e:
                            logging.error(f"Drift存入错误: {e}")
                        last_drift_deposit = asyncio.get_event_loop().time()
            # If health is above threshold (excess collateral)
            elif health > config.HEALTH_THRESHOLD:
                now = asyncio.get_event_loop().time()
                if now - last_drift_withdraw >= config.COOLDOWN:
                    async with lock:
                        logging.info(f"Drift健康度{health:.2f}高于阈值{config.HEALTH_THRESHOLD}，将提取{config.USDC_TRANSFER_AMOUNT}{config.TRANSFER_ASSET}。")
                        try:
                            tx = await drift.withdraw_from_drift(config.USDC_TRANSFER_AMOUNT)
                            logging.info(f"Drift提现成功，交易: {tx}")
                        except Exception as e:
                            logging.error(f"Drift提现错误: {e}")
                        last_drift_withdraw = asyncio.get_event_loop().time()
            # Sleep briefly before next check
            await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"Drift监控循环异常: {e}")
            await asyncio.sleep(5)

async def start_monitoring(binance: binance_client.BinanceClient, drift: drift_client.DriftClient):
    """Start concurrent monitoring of Binance and Drift accounts."""
    # Use a lock to ensure fund transfer operations don't overlap
    transfer_lock = asyncio.Lock()
    await asyncio.gather(
        monitor_binance(binance, transfer_lock),
        monitor_drift(drift, binance, transfer_lock)
    )
