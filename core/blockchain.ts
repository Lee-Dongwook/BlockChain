import { Block } from "./block.js";
import { mineBlock } from "./pow.js";
import { createCoinbaseTx } from "./transaction.js";
import { UTXOPool, UTXO } from "./utxo.js";

export class Blockchain {
  public chain: Block[];
  public difficulty: number;
  public reward: number;
  public utxoPool: UTXOPool;

  constructor() {
    this.chain = [];
    this.difficulty = 4;
    this.reward = 50;
    this.utxoPool = new UTXOPool();

    const genesisBlock = new Block(0, "0", Date.now(), []);
    this.chain.push(genesisBlock);
  }

  getLatestBlock(): Block | undefined {
    return this.chain[this.chain.length - 1];
  }

  updateUTXOs(block: Block) {
    for (const tx of block.transactions) {
      // 기존 UTXO 중에서 이번 트랜잭션 input이 소비한 것 제거
      for (const input of tx.inputs) {
        this.utxoPool.removeUTXO(input.txId, input.outputIndex);
      }

      // 이번 트랜잭션 output을 UTXO에 추가
      tx.outputs.forEach((out, index) => {
        const utxo: UTXO = {
          txId: tx.id || block.getHash(),
          outputIndex: index,
          address: out.address,
          amount: out.amount,
        };
        this.utxoPool.addUTXO(utxo);
      });
    }
  }

  minePendingTransactions(minerAddress: string) {
    // 보상 트랜잭션
    const rewardTx = createCoinbaseTx(minerAddress, this.reward);
    const block = new Block(
      this.chain.length,
      this.getLatestBlock()?.getHash() as string,
      Date.now(),
      [rewardTx]
    );

    mineBlock(block, this.difficulty);
    this.chain.push(block);

    // UTXO 업데이트
    this.updateUTXOs(block);
  }

  getBalance(address: string): number {
    return this.utxoPool.getBalance(address);
  }
}
