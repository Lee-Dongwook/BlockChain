import { useState } from "react";
import { Blockchain } from "../core/blockchain.js";

const chain = new Blockchain();
const myAddress = "dongwook123";

function getAllTransactions(chain: Blockchain) {
  const txs: any[] = [];
  chain.chain.forEach((block, blockIndex) => {
    block.transactions.forEach((tx: any) => {
      tx.outputs.forEach((out: any) => {
        txs.push({
          blockIndex,
          from:
            tx.inputs.length === 0
              ? "System"
              : tx.inputs[0]?.publicKey || "Unknown",
          to: out.address,
          amount: out.amount,
        });
      });
    });
  });
  return txs;
}

export default function App() {
  const [balance, setBalance] = useState<number>(chain.getBalance(myAddress));
  const [transactions, setTransactions] = useState<any[]>([]);

  const handleMine = () => {
    chain.minePendingTransactions(myAddress);
    setBalance(chain.getBalance(myAddress));
    setTransactions(getAllTransactions(chain));
  };

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        padding: 20,
        background: "#0d1117",
        minHeight: "100vh",
        color: "#fff",
      }}
    >
      <h1 style={{ fontSize: 24, marginBottom: 10 }}>
        💰 내 지갑 ({myAddress})
      </h1>

      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 14, color: "#aaa" }}>주소</div>
        <div style={{ fontSize: 16, wordBreak: "break-all" }}>{myAddress}</div>
        <div style={{ marginTop: 10, fontSize: 18 }}>잔액: {balance} BTC</div>
      </div>

      <button
        onClick={handleMine}
        style={{
          background: "#1abc9c",
          border: "none",
          padding: "10px 16px",
          borderRadius: 4,
          color: "#fff",
          cursor: "pointer",
          fontSize: 16,
        }}
      >
        ⛏ 마이닝
      </button>

      <h3 style={{ marginTop: 30, fontSize: 20 }}>📜 거래 내역</h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "80px 1fr 1fr 100px",
          gap: "8px",
          marginTop: 10,
          padding: "8px 0",
          borderBottom: "1px solid #333",
          fontWeight: "bold",
        }}
      >
        <div>블록</div>
        <div>보낸 사람</div>
        <div>받는 사람</div>
        <div style={{ textAlign: "right" }}>금액</div>
      </div>

      {transactions.map((tx, idx) => (
        <div
          key={idx}
          style={{
            display: "grid",
            gridTemplateColumns: "80px 1fr 1fr 100px",
            gap: "8px",
            padding: "8px 0",
            borderBottom: "1px solid #222",
            alignItems: "center",
            fontSize: 14,
          }}
        >
          <div>{tx.blockIndex}</div>
          <div style={{ wordBreak: "break-all", color: "#aaa" }}>{tx.from}</div>
          <div style={{ wordBreak: "break-all", color: "#1abc9c" }}>
            {tx.to}
          </div>
          <div style={{ textAlign: "right" }}>{tx.amount}</div>
        </div>
      ))}
    </div>
  );
}
