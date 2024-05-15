class Wallet:
    def __init__(self, utxoList,fiatList , prenom):
        self.prenom = prenom
        self.fiatList = fiatList
        self.utxolist = utxoList 
        self.jeton = 0
        self.credit = 0

    def getSoldeUser(self):
        solde = 0
        for utxo in self.utxolist:
            if utxo.getOwner() == self.prenom:
                solde += 1
        return solde
    
    def getSoldeTotal(self):
        solde = 0
        for utxo in self.utxolist:
            solde += utxo.getMontant()
        return solde

    def updateFiat(self):
        for minage in self.fiatList:
            if minage[0] == self.prenom:
                self.credit += minage[1]