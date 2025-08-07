import { createWallet } from "../core/wallet";

const myWallet = createWallet();

console.log("📥 Private Key:", myWallet.privateKey);
console.log("🔓 Public Key:", myWallet.publicKey);
console.log("🏠 Address:", myWallet.address);
