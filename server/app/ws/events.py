import asyncio
import json
from utils.network_overview import build_network_overview
from utils.redis_client import r, CHANNEL
from p2p.manager import manager
from p2p.messages import MESSAGE_TYPE

async def overview_loop(local_node_url, peers, blockchain):
    while True:
        overview = build_network_overview(local_node_url, peers, blockchain)
        await manager.broadcast({
            "type": MESSAGE_TYPE["NETWORK_OVERVIEW"],
            "data": overview
        })  # pyright: ignore[reportArgumentType]
        await asyncio.sleep(5)

async def redis_event_bridge():
    """Redis Pub/Sub → WebSocket 전송"""
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)
    loop = asyncio.get_event_loop()

    while True:
        msg = await loop.run_in_executor(None, pubsub.get_message, True, 1.0)
        if msg and msg.get('type') == 'message':
            try:
              event = json.load(msg['data'])
              await manager.broadcast({
                   "type": "EVENT_LOG",
                   "data": event
              }) # pyright: ignore[reportArgumentType]
            except Exception as e:
               print('[Error] Redis event bridge:', e)