import { Block } from "../core/block";
import { mineBlock } from "../core/pow";
import { createCoinbaseTx } from "../core/transaction";

const MY_ADDRESS = "dongwook123"; //  지갑 주소 넣어도 됨
const REWARD = 50;

const coinbaseTx = createCoinbaseTx(MY_ADDRESS, REWARD);

const block = new Block(
  1, // index
  "0000000000", // previous hash
  Date.now(), // timestamp
  [coinbaseTx] // transactions
);

mineBlock(block, 4); // 해시가 0000으로 시작하면 성공
