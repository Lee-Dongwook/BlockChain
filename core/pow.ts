import { Block } from "./block";

export function mineBlock(block: Block, difficulty: number): Block {
  const prefix = "0".repeat(difficulty);

  while (!block.getHash().startsWith(prefix)) {
    block.nonce++;
  }
  return block;
}
