import React from "react";
import { Contract } from "../model";

interface Props {
  contract: Contract;
}

export const ContractStatus: React.FC<Props> = ({ contract }) => {
  return (
    <div>
      <strong>Contract ID:</strong> {contract.id} <br />
      <strong>Status:</strong> {contract.executed ? "Executed" : "Pending"}
    </div>
  );
};
