import time as t
from blockchain import*
from txInPut import*
from txOutPut import*

nbInputs = 0
nbOutputs = 0
Inputlist = []
Outputlist = []

class Transaction:
    def __init__(self, comment):
        #self.index = index
        self.hash = ""
        #self.utilisateur = utilisateur
        #self.candidat = candidat
        self.nbJeton = 1
        self.timestamp = t.time()
        self.comment = comment
    
    def getComment(self):
        print(self.comment)

    def printTransaction(self):
        print(f"--- Transaction ---")
        print("Nb Inputs :", nbInputs)
        print("Nb Outputs :", nbOutputs)
        print(f"Input list :")
        for i in range(len(Inputlist)):
            Inputlist[i].printInputList()
        print(f"Output list : ")
        for i in range(len(Outputlist)):
            Outputlist[i].printOutputList()
        print("Comment : ", end="")
        self.getComment()

    def InstitutionTx(self, reward, user):
        outTx = TxOutPut(0, "0", reward)
        Outputlist.append(outTx)
        nbInputs = len(Inputlist)
        nbOuputs = len(Outputlist)

    def frais(self):
        montantInput = 0
        montantOutput = 0
        for i in range(len(Outputlist)):
            montantOutput += Outputlist[i].getMontant()
        for i in range(len(Inputlist)):
            montantInput += Inputlist[i].getMontant()
        return montantInput - montantOutput
    
    def marketTx(self, UTXOlist, user, dest, montant, fraisPourcentage):
        UTXOlistIn = []
        hashSourceTx = ""
        change = 0
        montantEntree = 0
        sommeInputs = 0

        fees = montant * fraisPourcentage/100
        for utxo in UTXOlist:
            sommeInputs += utxo.getMontant()
            UTXOlistIn.append(utxo)
            if sommeInputs >= montant + fees: break
        
        change = sommeInputs - montant - fees

        for utxo in UTXOlistIn:
            hashSourceTx = utxo.setHash()
            montantEntree = utxo.getMontant()

            Txin = TxInput(hashSourceTx, 0, montantEntree, "market tx")
            Inputlist.append(Txin)
            UTXOlist.pop()

        if len(Inputlist) == 0:
            print("=======> Liste inputs vide. Problème")
        
        outChange = TxOutPut(1, "0", change)
        outChange.setHash(outChange.calcul_hash())
        Txout = TxOutPut(0, "0", montant)
        
        Outputlist.append(Txout)
        Outputlist.append(outChange)
        nbInputs = len(Inputlist)
        nbOutputs = len(Outputlist)

        UTXOlist.append(Txout)
        UTXOlist.append(Txout)
        return UTXOlist

    def stringify(self):
        return t.time() + nbInputs + Inputlist + nbOutputs + Outputlist + self.comment

    

#testTx = Transaction(1, "Test")
#testTx.printTransaction()