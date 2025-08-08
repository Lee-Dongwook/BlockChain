from statistics import mean
from utils.network_graph import build_network_graph
from utils.network_status import get_network_status
from core.blockchain import Blockchain

def build_network_overview(local_url:str, peers:dict, blockchain:Blockchain):
    graph = build_network_graph(local_url, peers, blockchain)
    status = get_network_status(blockchain, list(peers.keys()))

     # 네트워크 통계
    all_block_counts = [node["block_count"] for node in graph["nodes"]]
    avg_block_count = mean(all_block_counts) if all_block_counts else 0
    max_block_count = max(all_block_counts) if all_block_counts else 0
    min_block_count = min(all_block_counts) if all_block_counts else 0

    return {
        "status": status,
        "graph": graph,
        "stats": {
            "avg_block_count": avg_block_count,
            "max_block_count": max_block_count,
            "min_block_count": min_block_count,
            "node_count": len(graph["nodes"])
        }
    }