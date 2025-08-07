import crypto from "crypto";

export class Block {
  constructor(
    public index: number,
    public previousHash: string,
    public timestamp: number,
    public data: any,
    public nonce: number = 0
  ) {}

  getHash(): string {
    return crypto
      .createHash("sha256")
      .update(
        this.index +
          this.previousHash +
          this.timestamp +
          JSON.stringify(this.data) +
          this.nonce
      )
      .digest("hex");
  }
}
