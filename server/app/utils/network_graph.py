def build_network_graph(local_url: str, peers: dict, blockchain):
    """
    네트워크 그래프 데이터 생성
    """
    nodes = [{"id": local_url, "type": "self", "block_count": len(blockchain.chain)}]
    links = []

    for peer_url, info in peers.items():
        nodes.append({
            "id": peer_url,
            "type": "peer",
            "block_count": info.get("block_count", 0)
        })
        links.append({"source": local_url, "target": peer_url})

    return {"nodes": nodes, "links": links}
