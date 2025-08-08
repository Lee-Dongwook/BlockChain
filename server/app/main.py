import sys
import os

# app 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, WebSocket
from api.routes import router
from p2p.manager import manager

app = FastAPI(title="Blockchain API")

# REST API
app.include_router(router)

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except:
        await manager.disconnect(websocket)