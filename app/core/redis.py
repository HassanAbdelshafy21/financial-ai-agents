import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

async def get_redis():
    return redis_client
async def test_redis_connection():
    try:
        pong = await redis_client.ping()
        if pong:
            print("Connected to Redis!")
        else:
            print("Failed to connect to Redis.")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_redis_connection())
