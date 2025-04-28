import hashlib

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree(transactions)

    def hash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def build_tree(self, transactions):
        nodes = [self.hash(tx) for tx in transactions]

        if not nodes:
            return None

        while len(nodes) > 1:
            temp_nodes = []
            for i in range(0, len(nodes), 2):
                left_node = nodes[i]
                right_node = nodes[i+1] if i + 1 < len(nodes) else left_node
                combined_hash = self.hash(left_node + right_node)
                temp_nodes.append(combined_hash)
            nodes = temp_nodes

        return nodes[0]

if __name__ == "__main__":
    transactions = ["tx1", "tx2", "tx3", "tx4"]
    tree = MerkleTree(transactions)
    print("Merkle Root:", tree.root)
