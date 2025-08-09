import type { Block, Transaction } from "./types";

export const selectLatestBlock = (chain: Block[]) => chain[chain.length - 1];

export const selectPendingTransactions = (blocks: Block[]) =>
  blocks.flatMap((block) => block.transactions);

export const selectTransactionsByAddress = (
  blocks: Block[],
  address: string
): Transaction[] =>
  blocks.flatMap((block) =>
    block.transactions.filter(
      (tx) => tx.from_address === address || tx.to_address === address
    )
  );
