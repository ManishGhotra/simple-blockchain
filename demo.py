import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def add_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, last_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {json.dumps(block.transactions, indent=4)}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Current Hash: {block.hash}")
            print("-" * 50)

# Testing the Blockchain
blockchain = Blockchain()
blockchain.add_block([{ "sender": "A", "receiver": "B", "amount": 10 }])
blockchain.add_block([{ "sender": "C", "receiver": "D", "amount": 5 }])

print("Blockchain before tampering:")
blockchain.print_chain()
print("Is blockchain valid?", blockchain.is_chain_valid())

# Tamper with blockchain
blockchain.chain[1].transactions = [{ "sender": "A", "receiver": "B", "amount": 100 }]

print("\nBlockchain after tampering:")
blockchain.print_chain()
print("Is blockchain valid?", blockchain.is_chain_valid())
