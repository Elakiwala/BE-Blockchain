from hashlib import sha256
import time
import random

class TxInputs:
    def __init__(self, hash, hauteur, outIndex, montant, unlockSize, unlock_Script,comment):
        self.hauteur = hauteur
        self.hash = hash
        self.outIndex = outIndex
        self.montant = montant
        self.unlockSize = unlockSize
        self.unlock_Script = unlock_Script
        self.comment = comment

    def print(self):
        print("--- Input List ---\n")
        print("Hauteur : "+ self.hauteur)
        print(" ; hash : "+self.hash)
        print(" ; out index : "+self.outIndex)
        print(" ; unlock size : "+self.unlockSize)
        print(" ; unlock script : "+self.unlock_Script)
        print(" ; comment : "+self.comment)