import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import os

router = APIRouter()

# Get Redis URL from env or fallback to localhost
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """
    WebSocket endpoint that subscribes to the 'worker_logs' Redis channel
    and pushes messages in real-time to the connected React client.
    """
    await websocket.accept()
    
    try:
        redis_client = redis.from_url(REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("worker_logs")
        
        # We also want to push a connection success message
        await websocket.send_text("[System] WebSocket connected to backend. Awaiting worker activity...")
        
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message['type'] == 'message':
                    log_text = message['data'].decode('utf-8')
                    await websocket.send_text(log_text)
                
                # Tiny sleep to yield control to the event loop
                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                break
                
    except redis.ConnectionError:
        await websocket.send_text("[!] Error: Could not connect to Redis Pub/Sub broker. Start docker-compose or redis-server.")
    except WebSocketDisconnect:
        print("Client disconnected from log stream")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        try:
            await pubsub.unsubscribe("worker_logs")
            await redis_client.aclose()
        except:
            pass
