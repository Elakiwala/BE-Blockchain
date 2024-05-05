
#TODO @EVA

class TxInput:
    def __init__(self, hash, outIndex, montantEntree, comment): #On ne traite pas les verrouillages de transaction dans ce projet mais ça reste une partie importante de la sécurité!
        #self.previousTxHash = ""
        #self.previousTxIndex = 0 
        #self.hauteur = hauteur #je ne sais pas trop à quoi ça sert...
        self.hash = hash
        self.outIndex = outIndex
        self.montantEntree = montantEntree
        self.comment = comment

    def printTxInput(self):
        print(f"--- Input List ---")
        print("Current hash : {self.hash}")
        print("Out Index : {self.outIndex}")
        print("Montant : {self.montantEntree}")
        print("Comment : {self.comment}")

    def getMontant(self):
        return self.montantEntree