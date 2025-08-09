export interface Transaction {
  tx_id: string;
  from_address: string;
  to_address: string;
  amount: number;
  fee?: number;
  timestamp: number;
  type?: "multisig" | "standard";
  signatures?: string[];
  required_signatures?: number;
}

export interface Block {
  index: number;
  previous_hash: string;
  timestamp: number;
  transactions: Transaction[];
  nonce: number;
  hash: string;
  difficulty: number;
}

export interface NetworkStatus {
  peers: string[];
  blockHeight: number;
  pendingTxCount: number;
  difficulty: number;
}
