import time as t
#from blockchain import*
from txInPut import*
from txOutPut import*

nbInputs = 0
nbOutputs = 0
Inputlist = []
Outputlist = []

class Transaction:
    def __init__(self,index, comment):
        self.index = index
        self.hash = ""
        #self.utilisateur = utilisateur
        #self.candidat = candidat
        self.nbJeton = 1
        self.timestamp = t.time()
        self.comment = comment

    def setInputlist(self, InputL):
        Inputlist = InputL
    
    def setOutputlist(self, OutputL):
        Outputlist = OutputL
    
    def getNbOutput(self):
        return nbOutputs
    
    def setNbOutput(self, nb):
        nbOutputs = nb

    def setNbInptut(self, nb):
        nbIntputs = nb
    
    def getNbInput(self):
        return nbInputs
    
    def getInputList(self):
        return Inputlist
    
    def getOutputList(self):
        return Outputlist

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
        print(f"Comment : ", self.comment)

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
            sommeInputs += utxo.getMontant()
            UTXOlistIn.append(utxo)
            if sommeInputs >= montant + fees: break
        
        change = sommeInputs - montant - fees

        for utxo in UTXOlistIn:
            hashSourceTx = utxo.getHash()
            montantEntree = utxo.getMontant()

            Txin = TxInput(hashSourceTx, 0, montantEntree, "vote tx")
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
        UTXOlist.append(outChange)
        
# Le problème ici est qu'à aucun moment le "user" perd son UTXO, de même que le "dest" ne resoit jamais rien
# Il faut trouver un moyen de créditer et débiter les UTXO de la liste et les attribuer (d'une manière nomminative ou autre)
# Car dans le code Java les variables "user" et "dest" sont uniquement utilisé pour les vérifications (lock et unlock scripts)
        return UTXOlist

    def stringify(self):
        return t.time() + nbInputs + Inputlist + nbOutputs + Outputlist + self.comment

    

testTx = Transaction("Test")
testTx.printTransaction()