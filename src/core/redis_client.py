from redis.asyncio import Redis
from src.config import config

redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True, retry_on_timeout=True)