export interface UTXO {
  txId: string;
  outputIndex: number;
  address: string;
  amount: number;
}

export class UTXOPool {
  private utxos: UTXO[] = [];

  addUTXO(utxo: UTXO) {
    this.utxos.push(utxo);
  }

  removeUTXO(txId: string, index: number) {
    this.utxos = this.utxos.filter(
      (u) => !(u.txId === txId && u.outputIndex === index)
    );
  }

  findUTXO(address: string): UTXO[] {
    return this.utxos.filter((u) => u.address === address);
  }

  getAll(): UTXO[] {
    return this.utxos;
  }

  getBalance(address: string): number {
    return this.findUTXO(address).reduce((sum, u) => sum + u.amount, 0);
  }
}
