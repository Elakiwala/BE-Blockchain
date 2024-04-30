from txOutput import TxOutputs

class Wallet:
    def __init__(self, nom):
        self.utxoList = []
        self.pubKey = "pubKey"+nom
        self.privKey = "privKey"+nom
        self.totalAmount = 0
    
    def totalAmount(self):
        som = 0
        for i in range(len(self.utxoList)):
            som += self.utxoList[i].montant
        self.totalAmount = som
        return som