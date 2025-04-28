# main.py

import asyncio
import logging

import config
from binance_client import BinanceClient
from drift_client import DriftClient
import logging_util
import monitor

async def main():
    # Initialize logging
    logging_util.init_logging()
    logging.info("启动Binance与Drift账户监控程序...")
    # Initialize API clients
    binance = BinanceClient()
    drift = DriftClient()
    # Begin monitoring concurrently
    try:
        await monitor.start_monitoring(binance, drift)
    finally:
        # Ensure Binance HTTP session is closed on exit
        await binance.close()

if __name__ == "__main__":
    asyncio.run(main())
