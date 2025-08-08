from fastapi import APIRouter, Query
from typing import List, Optional
from utils.redis_client import r, PENDING_KEY, CHAIN_KEY
import json
import time

transaction_router = APIRouter()

@transaction_router.get('/pending')
def get_pending_transactions(limit: Optional[int] = Query(50, ge=1, le=200)):
    """대기 중인 트랜잭션 조회"""
    data = r.get(PENDING_KEY)
    if not data:
        return []
    txs = json.loads(data) # pyright: ignore[reportArgumentType]
    # 최신순 정렬 후 제한
    txs.sort(key=lambda tx: tx.get("timestamp", 0), reverse=True)
    return txs[:limit]


@transaction_router.get("/by-address/{address}")
def get_transactions_by_address(address: str, limit: Optional[int] = Query(50, ge=1, le=200)):
    """주소와 관련된 모든 트랜잭션 (블록체인 + pending)"""
    results: List[dict] = []

    # Pending 트랜잭션
    pending_data = r.get(PENDING_KEY)
    if pending_data:
        pending = json.loads(pending_data) # pyright: ignore[reportArgumentType]
        results.extend(
            tx for tx in pending
            if tx.get("from_address") == address or tx.get("to_address") == address
        )

    # 블록체인 트랜잭션
    chain_data = r.get(CHAIN_KEY)
    if chain_data:
        chain = json.loads(chain_data) # pyright: ignore[reportArgumentType]
        for block in chain:
            for tx in block.get("transactions", []):
                if tx.get("from_address") == address or tx.get("to_address") == address:
                    results.append(tx)

    # 최신순 정렬 후 제한
    results.sort(key=lambda tx: tx.get("timestamp", 0), reverse=True)
    return results[:limit]

@transaction_router.get("/recent")
def get_recent_transactions(limit: Optional[int] = Query(50, ge=1, le=200)):
    """최근 N개 트랜잭션 (블록체인 전체에서)"""
    results: List[dict] = []
    chain_data = r.get(CHAIN_KEY)
    if not chain_data:
        return []
    chain = json.loads(chain_data) # pyright: ignore[reportArgumentType]
    for block in chain:
        results.extend(block.get("transactions", []))
    results.sort(key=lambda tx: tx.get("timestamp", 0), reverse=True)
    return results[:limit]