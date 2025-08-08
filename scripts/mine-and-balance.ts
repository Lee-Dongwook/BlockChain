import { Blockchain } from "../core/blockchain";

const myAddress = "dongwook123";
const chain = new Blockchain();

console.log("⛏ 첫 마이닝 시작");
chain.minePendingTransactions(myAddress);
console.log(`💰 잔액: ${chain.getBalance(myAddress)}`);

console.log("⛏ 두 번째 마이닝 시작");
chain.minePendingTransactions(myAddress);
console.log(`💰 잔액: ${chain.getBalance(myAddress)}`);
