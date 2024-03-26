from fast_api_core.router import Documentation
from redis.asyncio import Redis

app = Documentation(
    documentation_path='/',
    title='API Тестовый',
    version='1.0',
    summary='Хранения в redis (номер телефона - Адрес)'
)
redis = Redis(host='localhost', port=6379, decode_responses=True, retry_on_timeout=True)


@app.on_event("shutdown")
async def shutdown_event():
    global redis
    await redis.aclose()
