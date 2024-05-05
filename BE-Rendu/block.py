import time as t
from hashlib import sha256


class Block:
    def __init__(self, index, previous_hash, transactions, miner):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = t.time()
        self.transactions = transactions
        self.nbTransactions = len(self.transactions)
        #self.merkleRoot(self.transactions) TODO @Souad
        self.miner = miner
        self.nonce = 0
        self.blockHash = self.calcul_hash()
        
    def getTransaction(self):
        return self.transactions
    
    def printBlock(self):
        print(f"Previous hash : {self.previous_hash}")
        print(f"Current hash : {self.blockHash}")
        print(f"Timestamp : {self.timestamp}")
        print(f"Nb transactions : {self.nbTransactions}")
        print("Liste des tx : ")
        for tx in self.transactions:
            tx.printTransaction()
        #print("Merkle tree root : "+)
        print(f"Miner : {self.miner}")
        print(f"Nonce : {self.nonce}")
        print("------------------------------------------")
        
    def getHash(self):
        return self.blockHash

    def calcul_hash(self):
        block_string = str(self.index)+str(self.timestamp)+str(self.transactions)+str(self.previous_hash)+str(self.nonce)+str(self.miner)#+str(self.merkleRoot)
        return sha256(block_string.encode()).hexdigest()
    
    def mineBlock(self, difficulte, miner):
        cible = '0' * difficulte
        self.miner = miner
        while self.blockHash[:difficulte] != cible:
            self.nonce += 1
            self.blockHash = self.calcul_hash()
        print(f"Block Miné!! : {self.blockHash}")
        print(f"Block numéro : {self.index}")
        print(f"Nonce = {self.nonce}")
    
    def verifyBlock(self):
        hashControl = self.calcul_hash()
        if(self.blockHash == hashControl):
            return True
        else :
            print("Block numero : {self.index} est un mauvais block.")
            return False
    
    #ajouter un affichafe avec un json TODO @ROBIN
    
    #ajouter verification merkle tree
    
    #MERKLE TREE TODO @SOUAD