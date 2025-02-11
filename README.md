# simple-blockchain
import hashlib
import time
import json

class Block:
    def __init__(self, block_id, transaction_list, prev_hash):
        self.block_id = block_id
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.transaction_list = transaction_list
        self.prev_hash = prev_hash
        self.nonce = 0
        self.block_hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_content = json.dumps({
            "block_id": self.block_id,
            "timestamp": self.timestamp,
            "transaction_list": self.transaction_list,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_content.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        while self.block_hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.block_hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.initialize_blockchain()
    
    def initialize_blockchain(self):
        # Creating the first block (genesis block) manually
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def add_new_block(self, transaction_list):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), transaction_list, last_block.block_hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def validate_chain(self):
        # Checking each block's integrity
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            if curr_block.block_hash != curr_block.calculate_hash():
                return False
            if curr_block.prev_hash != prev_block.block_hash:
                return False
        return True
    
    def display_chain(self):
        # Display all blocks with clear formatting
        for block in self.chain:
            print(f"\n🔹 Block ID: {block.block_id}")
            print(f"⏳ Timestamp: {block.timestamp}")
            print(f"🔗 Previous Hash: {block.prev_hash}")
            print(f"📜 Transactions: {json.dumps(block.transaction_list, indent=4)}")
            print(f"🔒 Current Hash: {block.block_hash}")
            print("-" * 60)

# Interactively adding transactions
my_blockchain = Blockchain()
num_transactions = int(input("Enter the number of transactions to add: "))

for _ in range(num_transactions):
    sender = input("Enter sender name: ")
    receiver = input("Enter receiver name: ")
    amount = float(input("Enter transaction amount: "))
    my_blockchain.add_new_block([{ "sender": sender, "receiver": receiver, "amount": amount }])

print("\nBlockchain before tampering:")
my_blockchain.display_chain()
print("\nIs blockchain valid?", my_blockchain.validate_chain())

# Simulating tampering
print("\nSimulating an attack... Altering a block's data!")
my_blockchain.chain[1].transaction_list = [{ "sender": "Hacker", "receiver": "X", "amount": 10000 }]

print("\nBlockchain after tampering:")
my_blockchain.display_chain()
print("\nIs blockchain valid?", my_blockchain.validate_chain())
