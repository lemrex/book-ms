# inventory-service/src/config/redis.py
import redis
import os

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', '110.238.74.93'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0
)

def get_redis_client():
    return redis_client