
#TODO @EVA

class TxInput:
    def __init__(self, hash, outIndex, owner, montantEntree, comment): #On ne traite pas les verrouillages de transaction dans ce projet mais ça reste une partie importante de la sécurité!
        #self.previousTxHash = ""
        #self.previousTxIndex = 0 
        #self.hauteur = hauteur #je ne sais pas trop à quoi ça sert...
        self.hash = hash
        self.owner = owner
        self.outIndex = outIndex
        self.montantEntree = montantEntree
        self.comment = comment

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