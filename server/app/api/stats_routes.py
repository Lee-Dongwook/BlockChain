from fastapi import APIRouter
from core.blockchain import Blockchain
import statistics

stats_router = APIRouter()
blockchain = Blockchain()

@stats_router.get('/network-status')
def network_status() : 
    return {
        "block_count": len(blockchain.chain),
        "difficulty": blockchain.difficulty,
        "mining_reward": blockchain.mining_reward
    }

@stats_router.get('/block-time')
def block_time_average(last_n: int = 5):
    if len(blockchain.chain) < 2:
        return {"average_time": None}

    times = []
    for i in range(1, min(last_n + 1, len(blockchain.chain))):
        t = blockchain.chain[i].timestamp - blockchain.chain[i-1].timestamp
        times.append(t)
    
    return {"average_time": statistics.mean(times)}


@stats_router.get('/address-distribution')
def address_distribution():
    balances = {}
    for block in blockchain.chain:
        for tx in block.transactions:
            balances[tx["to_address"]] = balances.get(tx["to_address"], 0) + tx["amount"]
            if tx.get("from_address") and tx["from_address"] != "System":
                balances[tx["from_address"]] = balances.get(tx["from_address"], 0) - tx["amount"]
    return balances 