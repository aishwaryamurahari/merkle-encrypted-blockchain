import os
import json
from crypto_utils import CryptoUtils

def load_block(filename):
    with open(filename, "r") as file:
        return json.load(file)

def decrypt_blockchain(key, directory="blockchain_data"):
    crypto_utils = CryptoUtils(key)

    files = sorted(os.listdir(directory), key=lambda x: int(x.split("_")[1].split(".")[0]))

    for idx, filename in enumerate(files):
        filepath = os.path.join(directory, filename)
        block = load_block(filepath)

        print(f"\n--- Block {idx} ---")
        print(f"Timestamp: {block['timestamp']}")
        print(f"Previous Hash: {block['previous_hash']}")
        print(f"Merkle Root: {block['merkle_root']}")
        print(f"Block Hash: {block['hash']}")
        print("\nTransactions:")

        for encrypted_tx in block["transactions"]:
            try:
                decrypted_tx = crypto_utils.decrypt(encrypted_tx)
                parsed_tx = json.loads(decrypted_tx)
                print(json.dumps(parsed_tx, indent=4))
            except Exception as e:
                print(f"[ERROR] Failed to decrypt transaction: {e}")

if __name__ == "__main__":
    # Automatically load the encryption key
    crypto_utils = CryptoUtils(key_file="key.key")
    decrypt_blockchain(crypto_utils.key)