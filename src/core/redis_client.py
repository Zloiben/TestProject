from redis.asyncio import ConnectionPool
from src.config import config

redis_pool = ConnectionPool.from_url(f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}')