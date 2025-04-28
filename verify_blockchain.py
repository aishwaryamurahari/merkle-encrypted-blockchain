import os
import json
import hashlib
from crypto_utils import CryptoUtils
from merkle_tree import MerkleTree

def hash_block(block):
    contents = (str(block["timestamp"]) +
                block["previous_hash"] +
                block["merkle_root"])
    return hashlib.sha256(contents.encode('utf-8')).hexdigest()

def load_block(filename):
    with open(filename, "r") as file:
        return json.load(file)

def verify_blockchain(directory="blockchain_data"):
    crypto_utils = CryptoUtils(key_file="key.key")  # Load key, but don't decrypt for Merkle root

    files = sorted(os.listdir(directory), key=lambda x: int(x.split("_")[1].split(".")[0]))

    previous_hash = "0"

    for idx, filename in enumerate(files):
        filepath = os.path.join(directory, filename)
        block = load_block(filepath)

        # ⚡ Do NOT decrypt here!
        encrypted_transactions = block["transactions"]

        merkle_root_actual = MerkleTree(encrypted_transactions).root

        if merkle_root_actual != block["merkle_root"]:
            print(f"❌ Merkle root mismatch at block {idx} ({filename})")
            return False

        calculated_hash = hash_block(block)
        if calculated_hash != block["hash"]:
            print(f"❌ Block hash mismatch at block {idx} ({filename})")
            return False

        if block["previous_hash"] != previous_hash:
            print(f"❌ Previous hash mismatch at block {idx} ({filename})")
            return False

        previous_hash = block["hash"]

    print("✅ Blockchain is VALID!")
    return True

if __name__ == "__main__":
    verify_blockchain()
