from blockchain import *
from main import *

class Wallet:
    def __init__(self, utxoList):
        self.utxolist = utxoList #est ce que on prends le utxo de la blockchain ? Normalement oui
        #self.name = name
        self.jeton = 0
        self.credit = 0

    def getSoldeUser(self, idName):
        return self.utxoList[idName]

    #def totalCredit TODO @ROBIN
    
    #def totalJeton TODO @ROBIN