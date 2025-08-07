import crypto from "crypto";

export interface TxInput {
  txId: string; // 참조할 이전 트랜잭션 ID
  outputIndex: number; // 해당 트랜잭션의 어떤 output인지
  signature: string; // 서명 (base64)
  publicKey: string; // 보내는 사람 공개키
}

export interface TxOutput {
  amount: number;
  address: string; // 받는 사람 주소
}

export interface Transaction {
  id: string;
  inputs: TxInput[];
  outputs: TxOutput[];
}

// 트랜잭션 해시 생성용 (ID 역할)
function hashTransaction(tx: Omit<Transaction, "id">): string {
  const data = JSON.stringify(tx);
  return crypto.createHash("sha256").update(data).digest("hex");
}

export function createTransaction(
  inputs: TxInput[],
  outputs: TxOutput[]
): Transaction {
  const tx = {
    id: "", // 나중에 해시로 채움
    inputs,
    outputs,
  };

  const txHash = hashTransaction(tx);
  tx.id = txHash;
  return tx;
}

// 서명 생성
export function signInput(
  input: TxInput,
  privateKey: string,
  txData: string
): string {
  const key = crypto.createPrivateKey({
    key: Buffer.from(privateKey, "hex"),
    format: "der",
    type: "pkcs8",
  });
  const sign = crypto.createSign("SHA256");
  sign.update(txData);
  sign.end();
  return sign.sign(key).toString("base64");
}

// 서명 검증
export function verifySignature(input: TxInput, txData: string): boolean {
  const key = crypto.createPublicKey({
    key: Buffer.from(input.publicKey, "hex"),
    format: "der",
    type: "spki",
  });
  const verify = crypto.createVerify("SHA256");
  verify.update(txData);
  verify.end();
  return verify.verify(key, Buffer.from(input.signature, "base64"));
}
