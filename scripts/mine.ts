import { Block } from "../core/block";
import { mineBlock } from "../core/pow";

const dummyTransactions = [
  {
    id: "tx1",
    inputs: [],
    outputs: [{ amount: 50, address: "address123" }],
  },
];

const block = new Block(
  1, // index
  "0000000000", // previous hash
  Date.now(), // timestamp
  dummyTransactions // transactions
);

mineBlock(block, 4); // 해시가 0000으로 시작하면 성공
