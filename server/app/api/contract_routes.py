from fastapi import APIRouter
from typing import Dict
from core.contract import SmartContract
from core.blockchain import Blockchain
from p2p.manager import manager
from p2p.messages import MESSAGE_TYPE

contract_router = APIRouter()
blockchain = Blockchain()
contracts: Dict[str, SmartContract]= {} 

@contract_router.get("/contract/list")
def list_contracts():
    return {cid: vars(c) for cid, c in contracts.items()}

@contract_router.post("/contract/execute-pending")
def execute_pending_contracts():
    executed = []
    for cid, contract in contracts.items():
        if contract.should_execute(blockchain):
            contract.execute(blockchain)
            executed.append(cid)
    return {"executed_contracts": executed}

@contract_router.post('/contract/deploy')
async def deploy_contract(condition:dict, action:dict, expire_block: int|None = None):
    contract = SmartContract(condition, action, expire_block)
    contracts[contract.id] = contract

    # P2P 브로드 캐스트
    await manager.broadcast({
        "type": MESSAGE_TYPE["CONTRACT_DEPLOY"],
        "data": { 
            "id": contract.id,
            "condition": contract.condition,
            "action": contract.action,
            "expire_block": contract.expire_block
        }
    }) # pyright: ignore[reportArgumentType]

    return {"contract_id": contract.id}
