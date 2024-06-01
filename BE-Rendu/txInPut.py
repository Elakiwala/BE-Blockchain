from hashlib import sha256

class TxInput:
    def __init__(self, outIndex, owner, montantEntree, comment): #On ne traite pas les verrouillages de transaction dans ce projet mais ça reste une partie importante de la sécurité!
        #self.previousTxHash = ""
        #self.previousTxIndex = 0 
        #self.hauteur = hauteur #je ne sais pas trop à quoi ça sert...
        self.owner = owner
        self.outIndex = outIndex
        self.montantEntree = montantEntree
        self.comment = comment
        self.hash = self.calcul_hash()

    def calcul_hash(self):
        TxIn_string = str(self.outIndex)+str(self.montantEntree)+str(self.owner)+str(self.comment)
        return sha256(TxIn_string.encode()).hexdigest()

    def printTxInput(self):
        print(f"--- Input List ---")
        print(f"Current hash : ", self.hash)
        print(f"Out Index : ", self.outIndex)
        print(f"Owner : ", self.owner)
        print(f"Montant : ", self.montantEntree)
        print(f"Comment : ", self.comment)

    def getMontant(self):
        return self.montantEntree

    def getOwner(self):
        return self.owner