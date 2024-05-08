import time as t
from hashlib import sha256

class UTXO:
    def __init__(self, owner, index):
        self.owner = owner
        self.timestamp = t.time()
        self.index = index
    
    def calcul_hash(self):
        utxo_string = str(self.index)+str(self.timestamp)+str(self.owner)
        return sha256(utxo_string.encode()).hexdigest()
    
    def getHash(self):
        return self.calcul_hash()

    def getOwner(self):
        return self.owner
    
    def getIndex(self):
        return self.index
    
    def getTime(self):
        return self.timestamp