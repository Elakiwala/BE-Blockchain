from hashlib import sha256
import time
import random


class Blockchain:
    def __init__(self, difficulte, reward):
        self.nbBlock = 1
        self.difficulte = difficulte
        self.utxoList = []
        self.masse_monetaire = 0
        self.BC = []
        self.BC.append(0, self.createGenesisBlock(reward))

    def MaJmasseMonetaire(self, montant):
        self.masse_monetaire += montant
        return self.masse_monetaire

    def printUtxoList(self):
        for i in range(len(self.utxoList)):
            print(self.utxoList[i])