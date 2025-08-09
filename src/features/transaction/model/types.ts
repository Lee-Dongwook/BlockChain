export interface TransactionFormData {
  fromAddress: string;
  toAddress: string;
  amount: number;
  fee?: number;
  signature?: string;
  publicKey?: string;
}
