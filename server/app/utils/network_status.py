from core.blockchain import Blockchain

def get_network_status(blockchain: Blockchain, peers: list[str]):
    return {
        "block_count": len(blockchain.chain),
        "difficulty": blockchain.difficulty,
        "pending_transactions": len(blockchain.pending_transactions),
        "peers": peers
    }