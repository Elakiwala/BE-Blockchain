from hashlib import sha256

class TxOutPut:
    def __init__(self,outIndex, owner, montantSortie):
        self.montantSortie = montantSortie
        self.owner = owner
        self.outIndex = outIndex
        self.hash = self.calcul_hash()

    def printTxOutput(self):
        print(f"--- Output List ---")
        print(f"Out Index : ", self.outIndex)
        print(f"Hash : ", self.hash)
        print(f"Owner : ", self.owner)
        print(f"Montant : ", self.montantSortie)

    def calcul_hash(self):
        TxOut_string = str(self.outIndex)+str(self.montantSortie)+str(self.owner)
        return sha256(TxOut_string.encode()).hexdigest()
    
    def getOwner(self):
        return self.owner

    def getMontant(self):
        return self.montantSortie
    
    def getHash(self):
        return self.hash

    def setHash(self, hash):
        self.hash = hash