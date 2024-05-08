from hashlib import sha256
#TODO @EVA

class TxOutPut:
    def __init__(self,outIndex, hash, montantSortie):
        self.montantSortie = montantSortie
        self.outIndex = outIndex
        self.hash = hash

    def printTxOutput(self):
        print(f"--- Output List ---")
        print(f"Out Index : ", self.outIndex)
        print(f"Hash : ", self.hash)
        print(f"Montant : ", self.montantSortie)

    def calcul_hash(self):
        TxOut_string = str(self.outIndex)+str(self.montantSortie)
        return sha256(TxOut_string.encode()).hexdigest()
    

    def getMontant(self):
        return self.montantSortie
    
    def getHash(self):
        return self.hash

    def setHash(self, hash):
        self.hash = hash