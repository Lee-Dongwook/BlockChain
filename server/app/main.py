import sys
import os
import json

# app 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, WebSocket
import asyncio
from contextlib import asynccontextmanager

from api.routes import blockchain, router
from api.wallet_routes import wallet_router
from api.p2p_routes import p2p_router, peers
from api.explorer_routes import explorer_router
from api.stats_routes import stats_router
from api.multisig_routes import multisig_router
from api.contract_routes import contract_router, contracts
from api.network_routes import network_router
from api.transaction_routes import transaction_router

from p2p.manager import manager
from p2p.messages import MESSAGE_TYPE

from ws.events import overview_loop, redis_event_bridge
from ws.server import websocket_endpoint

from core.block import Block
from core.blockchain import Blockchain
from core.contract import SmartContract

LOCAL_NODE_URL = "ws://localhost:8000/ws"

@asynccontextmanager
async def lifespan(app: FastAPI):
    t1 = asyncio.create_task(overview_loop(LOCAL_NODE_URL, peers, blockchain))
    t2 = asyncio.create_task(redis_event_bridge())
    try:
        yield
    finally:
        t1.cancel()
        t2.cancel()


app = FastAPI(title="Blockchain API", lifespan=lifespan)
blockchain = Blockchain()


# REST API
app.include_router(router)
app.include_router(wallet_router, prefix='/wallet', tags=["Wallet"])
app.include_router(p2p_router, prefix='/p2p', tags=["P2P"])
app.include_router(explorer_router, prefix='/explorer', tags=["Explorer"])
app.include_router(stats_router, prefix='/stats', tags=["Stats"])    
app.include_router(multisig_router, prefix='/multisig', tags=["Multisig"])
app.include_router(contract_router, prefix='/contract', tags=["Contract"])
app.include_router(network_router, prefix="/network", tags=["Network"])
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])



# WebSocket
@app.websocket("/ws")
async def ws_route(websocket: WebSocket):
   await websocket_endpoint(websocket, blockchain)