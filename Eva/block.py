from hashlib import sha256
import time
import random

class Block:
    def __init__(self, index, previous_hash, transactions, miner):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.nbTransactions = len(self.transactions)
        #self.merkleRoot(self.transactions) TODO @Souad
        self.blockHash = self.calcul_hash()
        self.miner = miner
        self.nonce = 0

    def printBlock(self):
        print("Block numéro (Index) : "+ self.index)
        print("Previous hash : "+ self.previous_hash)
        print("Current hash : "+self.blockHash)
        print("Timestamp : "+self.timestamp)
        print("Nb transactions : "+ self.nbTransactions)
        print("Liste des tx : ")
        for tx in self.transactions:
            tx.printTrans()
        #print("Merkle tree root : "+)
        print("Miner : "+ self.miner)
        print("Nonce : "+ self.nonce)
        print("------------------------------------------")

    def calcul_hash(self):
        block_string = str(self.index)+str(self.timestamp)+str(self.transactions)+str(self.previous_hash)+str(self.nonce)+str(self.miner)#+str(self.merkleRoot)
        return sha256(block_string.encode()).hexdigest()
    
    def mineBlock(self, difficulte, miner):
        cible = '0' * difficulte
        while self.block_hash[:difficulte] != cible:
            self.nonce += 1
            self.block_hash = self.calculate_hash()
        print("Block Miné!! : "+self.blockHash)
        print("Block numéro : "+self.index)
        print("Nonce = "+self.nonce)

    #Verification block TODO

    #Merkle Tree TODO