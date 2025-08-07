import crypto from "crypto";
import { randomBytes } from "crypto";

// 주소 생성 = SHA256 -> RIPEMD160 -> (base58은 나중)
function getAddress(publicKeyHex: string) {
  const pubKeyBuffer = Buffer.from(publicKeyHex, "hex");
  const sha256 = crypto.createHash("sha256").update(pubKeyBuffer).digest();
  const ripemd160 = crypto.createHash("ripemd160").update(sha256).digest();
  return ripemd160.toString("hex");
}

// 개인키/공개키는 ECDSA-secp256k1 기반
export function createWallet() {
  const keyPair = crypto.generateKeyPairSync("ec", {
    namedCurve: "secp256k1",
    publicKeyEncoding: { type: "spki", format: "der" },
    privateKeyEncoding: { type: "pkcs8", format: "der" },
  });

  const privateKeyHex = keyPair.privateKey.toString("hex");
  const publicKeyHex = keyPair.publicKey.toString("hex");
  const address = getAddress(publicKeyHex);

  return {
    privateKey: privateKeyHex,
    publicKey: publicKeyHex,
    address,
  };
}
