from fastapi import APIRouter
from utils.network_graph import build_network_graph
from api.p2p_routes import peers
from core.blockchain import Blockchain
from utils.network_overview import build_network_overview

network_router = APIRouter()
blockchain = Blockchain()
LOCAL_NODE_URL = "ws://localhost:8000/ws" # 나중에 설정으롭 변경 가능

@network_router.get("/network/graph")
def network_graph():
    return build_network_graph(LOCAL_NODE_URL, peers, blockchain)

@network_router.get('/network/overview')
def network_overview():
    return build_network_overview(LOCAL_NODE_URL, peers, blockchain)