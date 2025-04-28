# Blockchain with Encrypted Transactions

## 🌟 Project Overview

This project is a **private blockchain prototype** built in Python. It uses:
- **Merkle Trees** to efficiently verify transaction integrity.
- **Encrypted Transactions** to ensure data privacy inside each block.
- **Symmetric Key Encryption** (using Fernet) for protecting transaction data.
- **Verification System** to detect any tampering of the blockchain.

The blockchain design mimics real-world private ledger systems like **Hyperledger Fabric** and **Quorum**.

---

## 🔎 Key Features

- **Encryption**: Every transaction is encrypted before being stored inside blocks.
- **Key Management**: Encryption keys are auto-generated and saved securely in a `key.key` file.
- **Merkle Root Integrity**: Merkle Trees are built over encrypted transactions for verifying block content integrity.
- **Blockchain Verification**: A separate verifier script recomputes hashes and Merkle roots to validate the blockchain.
- **Transaction Decryption**: A tool to decrypt and view all transactions if you own the secret key.

---

## 📅 Step-by-Step Setup Instructions

1. **Install Dependencies**

```bash
pip install cryptography
```

2. **Prepare Input Data**

Create a `file_update_logs.json` with file update transactions.

Example:
```json
[
  {"timestamp": "2025-04-26T10:15:30", "file_id": "file_001", "operation": "create", "user": "Alice"},
  {"timestamp": "2025-04-26T10:20:10", "file_id": "file_001", "operation": "update", "user": "Bob"}
]
```

3. **Create Blockchain**

```bash
python3 log_blockchain.py
```
- This generates a new encryption key (`key.key`) if not already present.
- It creates `blockchain_data/` folder with encrypted blocks.

4. **Verify Blockchain**

```bash
python3 verify_blockchain.py
```
- This recomputes Merkle roots and hashes to verify chain integrity.

5. **Decrypt Blockchain**

```bash
python3 decrypt_blockchain.py
```
- This decrypts and prints human-readable transactions.

---

## 🚨 Challenges encountered and how it was solved

While building this blockchain, faced several tricky issues. Here's a more human version of the hurdles we ran into and how we tackled them:

- **Problem:** Kept seeing "❌ Merkle root mismatch at block 0" during verification.
  - **Why it happened:** The Genesis Block was created before we introduced encryption, so its structure didn't match the new encrypted format.
  - **How we fixed it:** Fully deleted the `blockchain_data/` folder **and** the `key.key` file, then regenerated everything fresh using the new encryption logic.

- **Problem:** Even after modifying transactions, the blockchain still showed "✅ Blockchain is VALID!" (which was suspicious).
  - **Why it happened:** Forgot to use `sort_keys=True` when serializing transactions into JSON, leading to inconsistent hashing.
  - **How we fixed it:** Made sure that every `json.dumps()` used `sort_keys=True` both during block creation and verification.

- **Problem:** Still got Merkle root mismatch errors even after using encryption.
  - **Why it happened:** During verification, mistakenly decrypted transactions before building the Merkle Tree, while the original blocks were built over encrypted transactions.
  - **How we fixed it:** Corrected the verifier to compute the Merkle Tree over the **encrypted** data exactly as it was stored.

- **Problem:** Python threw `TypeError: Blockchain.__init__() takes 1 positional argument but 2 were given`.
  - **Why it happened:** After introducing encryption, we needed to pass the `crypto_utils` object to the Blockchain class, but the constructor wasn't updated.
  - **How we fixed it:** We updated the `Blockchain` class to accept `crypto_utils` as an argument and refactored all related code accordingly.

These issues helped deeply understand the importance of handling encryption consistently, especially when it comes to verifiable structures like Merkle Trees.

---

## 🛡️ Important Reminders

- **Never lose the `key.key` file**! Without it, you cannot decrypt any transactions.
- **Always verify** the blockchain after adding new blocks.
- **Encrypted transactions** must be hashed exactly as they are stored.
- **Merkle Roots are computed over encrypted data**, not plaintext.

---

## 🚀 Possible Future Enhancements

- Add **key rotation** every N blocks for even stronger security.
- Add **`--show-decrypted` flag** to verifier for optional transaction viewing.
- Implement **smart self-healing**: automatically recreate Genesis block if mismatch detected.
- Add **Proof-of-Work** to blocks for mining simulation.

---

## 🌟 Conclusion

This project successfully demonstrates building a private, tamper-evident, and encrypted blockchain ledger with Merkle Tree integrity checking, encrypted transaction privacy, and full chain verification.



