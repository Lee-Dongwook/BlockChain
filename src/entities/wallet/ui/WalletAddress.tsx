import React from "react";
import type { Wallet } from "../model";

interface Props {
  wallet: Wallet;
}

export const WalletAddress: React.FC<Props> = ({ wallet }) => {
  return (
    <div>
      <strong>Address:</strong> {wallet.address} <br />
      <strong>Balance:</strong> {wallet.balance}
    </div>
  );
};
