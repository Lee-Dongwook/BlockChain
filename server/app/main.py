import sys
import os

# app 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, WebSocket
from api.routes import blockchain, router
from api.wallet_routes import wallet_router
from api.p2p_routes import p2p_router
from api.explorer_routes import explorer_router
from api.stats_routes import stats_router
from api.multisig_routes import multisig_router
from api.contract_routes import contract_router, contracts
from p2p.manager import manager
from p2p.messages import MESSAGE_TYPE
from core.block import Block
from core.contract import SmartContract

app = FastAPI(title="Blockchain API")

# REST API
app.include_router(router)
app.include_router(wallet_router, prefix='/wallet')
app.include_router(p2p_router, prefix='/p2p')
app.include_router(explorer_router, prefix='/explorer')
app.include_router(stats_router, prefix='/stats')    
app.include_router(multisig_router, prefix='/multisig')
app.include_router(contract_router, prefix='/contract')

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
                

            await manager.broadcast(data)
    except:
        await manager.disconnect(websocket)