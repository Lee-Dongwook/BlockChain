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

from utils.network_overview import build_network_overview
from utils.event_logger import get_event_logs
from utils.redis_client import r, CHANNEL

from core.block import Block
from core.blockchain import Blockchain
from core.contract import SmartContract

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시
    async def overview_loop():
        while True:
            overview = build_network_overview(LOCAL_NODE_URL, peers, blockchain)
            await manager.broadcast({
                "type": MESSAGE_TYPE["NETWORK_OVERVIEW"],
                "data": overview
            }) # pyright: ignore[reportArgumentType]
            await asyncio.sleep(5)

    async def redis_event_bridge():
        """Redis Pub/Sub으로 실시간 이벤트 받아서 WS로 전송"""
        pubsub = r.pubsub()
        pubsub.subscribe(CHANNEL)
        loop = asyncio.get_event_loop()

        while True:
            msg = await loop.run_in_executor(None, pubsub.get_message, True, 1.0)
            if msg and msg.get('type') == "message":
                try:
                    event = json.loads(msg["data"])
                    await manager.broadcast({
                        "type": "EVENT_LOG",
                        "data": event
                    }) # pyright: ignore[reportArgumentType]

                except Exception as e:
                    print('[Error] Redis event bridge:', e)
        
    t1 = asyncio.create_task(overview_loop())
    t2 = asyncio.create_task(redis_event_bridge())
    try:
        yield
    finally:
        t1.cancel()
        t2.cancel()


app = FastAPI(title="Blockchain API", lifespan=lifespan)
blockchain = Blockchain()
LOCAL_NODE_URL = "ws://localhost:8000/ws"

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
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get('type')

            if msg_type == MESSAGE_TYPE['CHAIN']:
                incoming_chain = data.get('data')
                if(len(incoming_chain) > len(blockchain.chain)):
                    blockchain.chain = incoming_chain
            elif msg_type == MESSAGE_TYPE['TRANSACTION']:
                 tx = data.get("data")
                 blockchain.pending_transactions.append(tx)
            elif msg_type == MESSAGE_TYPE['BLOCK']:
                block_data = data.get('data')
                latest_block = blockchain.get_latest_block()

                if block_data['index'] > latest_block.index:
                    print(f"[P2P] Received new block {block_data['index']} from peer, replacing chain")
                    blockchain.chain.append(Block(**block_data))
            elif msg_type == MESSAGE_TYPE["CONTRACT_DEPLOY"]:
                data_obj = data.get('data')
                if data_obj["id"] not in contracts:
                    new_contract = SmartContract(
                        condition=data_obj["condition"],
                        action=data_obj["action"],
                        expire_block=data_obj.get("expire_block") 
                    )
                    contracts[data_obj["id"]] = new_contract
                    print(f"[P2P] Contract ${data_obj['id']} deployed from peer")

            elif msg_type == MESSAGE_TYPE["CONTRACT_EXECUTE"]:
                contract_id = data.get("data", {}).get("id")
                
                if contract_id in contracts and not contracts[contract_id].executed:
                    contracts[contract_id].execute(blockchain)
        
                print(f"[P2P] Contract {contract_id} executed from peer")

            elif msg_type == MESSAGE_TYPE["NETWORK_STATUS"]:
                status = data.get('data')
                print(f"[P2P] Network status update: ${status}")
            
            elif msg_type == MESSAGE_TYPE["NETWORK_OVERVIEW"]:
                data_obj = data.get("data")
                print(f"[P2P] Live Network Overview: {data_obj['stats']}")

            elif msg_type == MESSAGE_TYPE["EVENT_LOG"]:
                event = data.get('data')
                print(f"[LIVE EVENT] {event['type']} -> {event['details']}")

                

            await manager.broadcast(data)
    except:
        await manager.disconnect(websocket)


