# # inventory-service/src/config/redis.py
# import redis
# import os

# redis_client = redis.Redis(
#     host=os.getenv('REDIS_HOST', '110.238.74.93'),
#     port=os.getenv('REDIS_PORT', 6379),
#     db=0
# )

# def get_redis_client():
#     return redis_client



import redis
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up Redis connection
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', '110.238.74.93'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=0
    )
    # Test Redis connection
    redis_client.ping()
    logger.info("Successfully connected to Redis.")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

def get_redis_client():
    if redis_client:
        logger.info("Returning Redis client.")
    else:
        logger.warning("Redis client is not available.")
    return redis_client
