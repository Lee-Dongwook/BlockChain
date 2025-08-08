from fastapi import APIRouter
import websockets
import asyncio

p2p_router = APIRouter()
peers = {} # peer_url -> {"url": str, "last_seen": float, "block_count": int}

@p2p_router.post('/connect-peer')
async def connect_peer(peer_url: str):
    try:
        ws = await websockets.connect(peer_url)
        peers[peer_url] = {"url": peer_url, "last_seen": asyncio.get_event_loop().time(), "block_count": 0}
        return {"message": f"Connected to {peer_url}"}
    except Exception as e:
        return {"error": str(e)}

@p2p_router.get('/peers')
def get_peers():
    return list(peers.values())