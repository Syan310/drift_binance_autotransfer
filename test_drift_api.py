import asyncio
from drift_api import init_drift, get_health_ratio, deposit_to_drift, withdraw_from_drift

async def main():
    drift_client, drift_user = await init_drift()
    ratio = await get_health_ratio(drift_user)
    print(f"当前健康度: {ratio}")

    # await deposit_to_drift(drift_client, 1.0)
    # await withdraw_from_drift(drift_client, 1.0)

if __name__ == "__main__":
    asyncio.run(main())
