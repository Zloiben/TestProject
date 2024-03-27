from fast_api_core.router import Documentation

from src.api.v1.router import v1
from src.core.redis_client import redis_pool

app = Documentation(
    documentation_path='/',
    title='API Тестовый',
    version='1.0',
    summary='Хранения в redis (номер телефона - Адрес)'
)


@app.on_event("shutdown")
async def shutdown_event():
    await redis_pool.aclose()


app.include_documentation(v1)
app.push()
