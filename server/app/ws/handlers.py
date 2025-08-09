from core.block import Block
from core.blockchain import Blockchain
from core.contract import SmartContract
from api.contract_routes import contracts
from p2p.manager import manager
from p2p.messages import MESSAGE_TYPE

async def handle_chain(data, blockchain:Blockchain):
    incoming_chain = data.get('data')
    if len(incoming_chain) > len(blockchain.chain):
        blockchain.chain = incoming_chain

async def handle_transaction(data, blockchain:Blockchain):
    tx = data.get('data')
    blockchain.pending_transactions.append(tx)

async def handle_block(data, blockchain:Blockchain):
    block_data = data.get('data')
    latest_block = blockchain.get_latest_block()
    if block_data['index'] > latest_block.index:
        print(f"[P2P] Received new block {block_data['index']} from peer, replacing chain")
        blockchain.chain.append(Block(**block_data))

async def handle_contract_deploy(data, blockchain:Blockchain):
    data_obj = data.get('data')
    if data_obj["id"] not in contracts:
        new_contract = SmartContract(
            condition=data_obj["condition"],
            action=data_obj["action"],
            expire_block=data_obj.get("expire_block")
        )
        contracts[data_obj["id"]] = new_contract
        print(f"[P2P] Contract {data_obj['id']} deployed from peer")

async def handle_contract_execute(data, blockchain:Blockchain):
    contract_id = data.get("data", {}).get("id")
    if contract_id in contracts and not contracts[contract_id].executed:
        contracts[contract_id].execute(blockchain)
    print(f"[P2P] Contract {contract_id} executed from peer")

async def handle_network_status(data):
    status = data.get('data')
    print(f"[P2P] Network status update: ${status}")

async def handle_network_overview(data):
    data_obj = data.get("data")
    print(f"[P2P] Live Network Overview: {data_obj['stats']}")

async def handle_event_log(data):
    event = data.get('data')
    print(f"[LIVE EVENT] {event['type']} -> {event['details']}")


# switch 역할을 하는 매핑 테이블
MESSAGE_HANDLERS = {
    MESSAGE_TYPE['CHAIN']: handle_chain,
    MESSAGE_TYPE['TRANSACTION']: handle_transaction,
    MESSAGE_TYPE['BLOCK']: handle_block,
    MESSAGE_TYPE['CONTRACT_DEPLOY']: handle_contract_deploy,
    MESSAGE_TYPE['CONTRACT_EXECUTE']: handle_contract_execute,
    MESSAGE_TYPE['NETWORK_STATUS']: handle_network_status,
    MESSAGE_TYPE['NETWORK_OVERVIEW']: handle_network_overview,
    MESSAGE_TYPE['EVENT_LOG']: handle_event_log,
}

# 진입점
async def handle_message(msg_type, data, blockchain:Blockchain):
    handler = MESSAGE_HANDLERS.get(msg_type)
    if handler:
        await handler(data, blockchain)
    
    # 모든 메시지 브로드캐스트
    await manager.broadcast(data)