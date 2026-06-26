import os
from fastapi import APIRouter, FastAPI, WebSocket, Request, BackgroundTasks, HTTPException
import uuid
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from ..redis.config import Redis

manager = ConnectionManager()

chat = APIRouter()

redis = Redis()

@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())

    if name == "":
        raise HTTPException(status_code = 400, detail={
            "loc": "name", "msg": "Enter a valid name"
        })
    
    json_client = redis.create_rejson_connection()

    chat_session = Chat(
        token = token,
        messages = [],
        name=name
    )

    json_client.jsonset(str(token), Path.rootPath(), chat_session.dict())

    redis_client = await redis.create_connection()
    await redis_client.expire(str(token), 3600)

    return chat_session.dict()

@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket = WebSocket, token: str - Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis_create_connection()
    producer = Producer(redis_client)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data, "message_channel")
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
