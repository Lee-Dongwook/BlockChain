import type { TransactionFormData } from "../model";

export async function createTransaction(data: TransactionFormData) {
  const res = await fetch("/transaction/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error(`Transaction creation failed: ${res.statusText}`);
  }

  return res.json();
}
