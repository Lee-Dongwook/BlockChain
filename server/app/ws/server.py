from fastapi import WebSocket
from core.blockchain import Blockchain
from p2p.manager import manager
from ws.handlers import handle_message

async def websocket_endpoint(websocket:WebSocket, blockchain:Blockchain):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get('type')
            await handle_message(msg_type, data, blockchain)
    
    except:
        await manager.disconnect(websocket)