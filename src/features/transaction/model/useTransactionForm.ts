import { useState } from "react";
import type { TransactionFormData } from "./types";

export function useTransactionForm(initial?: Partial<TransactionFormData>) {
  const [form, setForm] = useState<TransactionFormData>({
    fromAddress: "",
    toAddress: "",
    amount: 0,
    fee: 0,
    signature: "",
    publicKey: "",
    ...initial,
  });

  const updateField = <K extends keyof TransactionFormData>(
    key: K,
    value: TransactionFormData[K]
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  return { form, updateField };
}
