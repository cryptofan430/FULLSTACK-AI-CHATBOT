from src.redis.config import Redis
import asyncio
from src.model.gptj import GPT
from src.redis.cache import Cache

redis = Redis()

async def main():
    json_client = redis.create_rejson_connection()
    await Cache(json_client).add_message_to_cache(token="18196e23-763b-4808-ae84-064348a0daff", message_data={
        "id": "1",
        "msg": "Hello",
        "timestamp": "2022-07-16 13:20:01.092109"
    })
    data = await Cache(json_client).get_chat_history(token="18196e23-763b-4808-ae84-064348a0daff")
    print(data)

if __name__ == "__main__":
    asyncio.run(main())