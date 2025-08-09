import React from "react";
import type { Block } from "../model";

interface Props {
  chain: Block[];
}

export const BlockchainView: React.FC<Props> = ({ chain }) => {
  return (
    <div>
      <h2>Blockchain</h2>
      {chain.map((block) => (
        <div
          key={block.index}
          style={{ border: "1px solid #ccc", margin: "8px", padding: "8px" }}
        >
          <div>Index: {block.index}</div>
          <div>Hash: {block.hash}</div>
          <div>Prev Hash: {block.previous_hash}</div>
          <div>Tx Count: {block.transactions.length}</div>
        </div>
      ))}
    </div>
  );
};
