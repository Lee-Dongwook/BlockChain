from fastapi import APIRouter
import websockets

p2p_router = APIRouter()
peers = set()

@p2p_router.post('/connect-peer')
async def connect_peer(peer_url: str):
    try:
        ws = await websockets.connect(peer_url)
        peers.add(peer_url)
        return {"message": f"Connected to {peer_url}"}
    except Exception as e:
        return {"error": str(e)}

@p2p_router.get('/peers')
def get_peers():
    return list(peers)