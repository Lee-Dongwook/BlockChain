import React from "react";
import { useTransactionForm } from "../model";
import { createTransaction } from "../api/createTransaction";

export const TransactionForm: React.FC = () => {
  const { form, updateField } = useTransactionForm();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await createTransaction(form);
      alert(`Transaction successful! TX ID: ${result.tx_id}`);
    } catch (err) {
      alert((err as Error).message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-sm">
      <input
        placeholder="From Address"
        value={form.fromAddress}
        onChange={(e) => updateField("fromAddress", e.target.value)}
      />
      <input
        placeholder="To Address"
        value={form.toAddress}
        onChange={(e) => updateField("toAddress", e.target.value)}
      />
      <input
        type="number"
        placeholder="Amount"
        value={form.amount}
        onChange={(e) => updateField("amount", Number(e.target.value))}
      />
      <input
        type="number"
        placeholder="Fee (optional)"
        value={form.fee}
        onChange={(e) => updateField("fee", Number(e.target.value))}
      />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">
        Send Transaction
      </button>
    </form>
  );
};
