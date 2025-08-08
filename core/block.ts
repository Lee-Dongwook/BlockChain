import crypto from "crypto";
import { Transaction } from "./transaction.js";

export class Block {
  constructor(
    public index: number,
    public previousHash: string,
    public timestamp: number,
    public transactions: Transaction[],
    public nonce: number = 0
  ) {}

  getHash(): string {
    const data =
      this.index +
      this.previousHash +
      this.timestamp +
      JSON.stringify(this.transactions) +
      this.nonce;

    return crypto.createHash("sha256").update(data).digest("hex");
  }
}
