import { Block } from "./block";

export function mineBlock(block: Block, difficulty: number): Block {
  const target = "0".repeat(difficulty);
  console.log("⛏ 마이닝 시작...");

  while (true) {
    const hash = block.getHash();
    if (hash.startsWith(target)) {
      console.log(`✅ 마이닝 성공! Nonce: ${block.nonce}, Hash: ${hash}`);
      return block;
    }

    block.nonce++;
    if (block.nonce % 100000 === 0) {
      console.log(`...${block.nonce} 시도 중`);
    }
  }
}
