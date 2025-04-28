import hashlib
import time
import json
import os
from merkle_tree import MerkleTree
from crypto_utils import CryptoUtils


class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time.time()
        self.crypto_utils = crypto_utils
        self.transactions = [self.crypto_utils.encrypt(json.dumps(tx, sort_keys=True)) for tx in transactions]
       # self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = MerkleTree(self.transactions).root
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = (str(self.timestamp) +
                          self.previous_hash +
                          self.merkle_root)
        return hashlib.sha256(block_contents.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "hash": self.hash
        }

    def save_to_file(self, block_id, directory="blockchain_data"):
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"block_{block_id}.json")
        with open(filepath, "w") as file:
            json.dump(self.to_dict(), file, indent=4)

class Blockchain:
    def __init__(self, crypto_utils):
        self.chain = []
        if not os.path.exists("blockchain_data/block_0.json"):
            self.chain.append(self.create_genesis_block())
            self.chain[0].save_to_file(0)
        else:
            self.load_chain()

    def create_genesis_block(self):
        return Block([{"info":"Genesis Block"}], "0")

    def load_chain(self):
        self.chain = []
        files = sorted(os.listdir("blockchain_data"), key=lambda x: int(x.split("_")[1].split(".")[0]))
        for f in files:
            with open(os.path.join("blockchain_data", f), "r") as file:
                data = json.load(file)
                block = Block(data["transactions"], data["previous_hash"])
                block.timestamp = data["timestamp"]
                block.hash = data["hash"]
                block.merkle_root = data["merkle_root"]
                self.chain.append(block)

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash
        block = Block(transactions, previous_hash)
        block_id = len(self.chain)
        block.save_to_file(block_id)
        self.chain.append(block)

def load_logs_from_json(filename):
    with open(filename, "r") as file:
        logs = json.load(file)
    return logs

if __name__ == "__main__":
    if not os.path.exists("key.key"):
        crypto_utils = CryptoUtils()
        print("New encryption key generated and saved to key.key.")
    else:
        crypto_utils = CryptoUtils(key_file="key.key")
        print("Loaded existing encryption key from key.key.")

    blockchain = Blockchain(crypto_utils)

    logs = load_logs_from_json("file_update_logs.json")
    blockchain.add_block(logs)
