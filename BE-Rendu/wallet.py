import json

class Wallet:
    def __init__(self, utxoList,fiatList , prenom):
        self.prenom = prenom
        self.fiatList = fiatList
        self.utxolist = utxoList 
        self.jeton = self.getSoldeUser()
        self.credit = 0
        self.updateFiat()

    def getSoldeUser(self):
        solde = 0
        for utxo in self.utxolist:
            if utxo.getOwner() == self.prenom:
                solde += utxo.getMontant()
        return solde
    
    def getSoldeTotal(self):
        solde = 0
        for utxo in self.utxolist:
            solde += utxo.getMontant()
        return solde


    def updateFiat(self):
        self.credit = 0
        for minage in self.fiatList:
            if minage[0] == self.prenom:
                self.credit += minage[1]
                
    def toJson(self,fileName):
        self.jeton = self.getSoldeUser()
        self.updateFiat()
        walletJson =  {
            "name" : self.prenom,
            "jeton" : self.jeton,
            "fiat" : self.credit
        }
        with open(fileName, 'a') as file:
            json.dump(walletJson, file, indent=4)