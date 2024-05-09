from blockchain import *
from main import *

class Wallet:
    def __init__(self, utxoList):
        self.utxolist = utxoList 
        self.jeton = 0
        self.credit = 0

    def getSoldeUser(self, user):
        solde = 0
        for utxo in self.utxolist:
            if utxo.getOwner() == user:
                solde += 1
        return solde
    
    def getSoldeTotal(self):
        solde = 0
        for utxo in self.utxolist:
            solde += utxo.getMontant()
        return solde

    #def totalCredit TODO @ROBIN
    
    #def totalJeton TODO @ROBIN