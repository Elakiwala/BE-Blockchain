import time as t
#from blockchain import*
from txInPut import*
from txOutPut import*

nbInputs = 0
nbOutputs = 0
Inputlist = []
Outputlist = []

class Transaction:
    def __init__(self, index, comment, user, dest):
        self.index = index
        self.hash = ""
        self.user = user
        self.dest = dest
        self.nbJeton = 1
        self.timestamp = t.time()
        self.comment = comment
        self.nbInputs = nbInputs
        self.nbOutputs = nbOutputs
        self.Inputlist = Inputlist
        self.Outputlist = Outputlist

    def getUser(self):
        return self.user
    
    def getDest(self):
        return self.dest

    def printTransaction(self):
        print(f"--- Transaction ---")
        print("Nb Inputs :", self.nbInputs)
        print("Nb Outputs :", self.nbOutputs)
        print(f"Input list :")
        for i in range(len(self.Inputlist)):
            self.Inputlist[i].printTxInput()
        print(f"Output list : ")
        for i in range(len(self.Outputlist)):
            self.Outputlist[i].printTxOutput()
        print(f"Comment : ", self.comment)

    def InstitutionTx(self, montant, user):
        outTx = TxOutPut(0, "0", user, montant)
        self.Outputlist.append(outTx)
        self.nbInputs = len(Inputlist)
        self.nbOuputs = len(Outputlist)

    def frais(self):
        montantInput = 0
        montantOutput = 0
        for i in range(len(Outputlist)):
            montantOutput += Outputlist[i].getMontant()
        for i in range(len(Inputlist)):
            montantInput += Inputlist[i].getMontant()
        return montantInput - montantOutput
    
    def voteTx(self, UTXOlist, user, dest, montant, fraisPourcentage):
        UTXOlistIn = []
        hashSourceTx = ""
        change = 0
        montantEntree = 0
        sommeInputs = 0

        fees = montant * fraisPourcentage/100

    #On chercher toutes les utxos qui peuvent être utilisé pour justifier la source (Donc si je comprends bien, les utilisateurs ne possèdent pas réellement d'UTXO)
    #Puisque tous les votants ont le même nombre d'utxo alors la boucle va toujours s'arrêter à 1 (normalement, ou bien à 2 puisqu'il y a les frais en plus...)
    #Mais du coup je ne sais pas comment les Wallets peuvent fonctionner si on utilise la liste des UTXOs comme ça...
        for utxo in UTXOlist: 
            if utxo.getOwner() == user:
                sommeInputs += utxo.getMontant()
                UTXOlistIn.append(utxo)
                if sommeInputs >= montant + fees: break
        
        change = sommeInputs - montant - fees

        for utxo in UTXOlistIn:
                hashSourceTx = utxo.getHash()
                montantEntree = utxo.getMontant()

                Txin = TxInput(hashSourceTx, 0, user, montantEntree, "vote tx")
                self.Inputlist.append(Txin)
                for UTXO in UTXOlist:
                    if UTXO == utxo :
                        UTXOlist.pop(UTXO)
                        break

        if len(Inputlist) == 0:
            print("=======> Liste inputs vide. Problème")
        
        outChange = TxOutPut(1, "0", user, change)
        outChange.setHash(outChange.calcul_hash())
        Txout = TxOutPut(0, "0", dest, montant)
        
        self.Outputlist.append(Txout)
        self.Outputlist.append(outChange)
        self.nbInputs = len(self.Inputlist)
        self.nbOutputs = len(self.Outputlist)

        UTXOlist.append(Txout)
        UTXOlist.append(outChange)
        
# Le problème ici est qu'à aucun moment le "user" perd son UTXO, de même que le "dest" ne resoit jamais rien
# Il faut trouver un moyen de créditer et débiter les UTXO de la liste et les attribuer (d'une manière nomminative ou autre)
# Car dans le code Java les variables "user" et "dest" sont uniquement utilisé pour les vérifications (lock et unlock scripts)
        return UTXOlist
    
    def setInputList(self, Inputliste):
        self.Inputlist = Inputliste

    def setOutputList(self, Outputliste):
        self.Inputlist = Outputliste

    def setNbInput(self, nbInp):
            self.nbInputs = nbInp

    def setNbOutput(self, nbOut):
            self.nbOuputs = nbOut


    def stringify(self):
        return t.time() + self.nbInputs + self.Inputlist + self.nbOutputs + self.Outputlist + self.comment

    

testTx = Transaction(1, "Test")
testTx.printTransaction()
