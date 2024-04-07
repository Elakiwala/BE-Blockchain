from hashlib import sha256
import time
import random

class TxOutputs:
    def __init__(self, outIndex, hash, lock_Script, montant):
        self.outIndex = outIndex
        self.hash = hash
        self.lock_Script = lock_Script
        self.montant = montant
    
    def print(self):
        print("--- Output List ---\n")
        print("out index : " + self.outIndex)
        print(" ; lock : " + self.lock_Script)
        print(" ; montant : " + self.montant)

    def calcul_hash(self):
        block_string = str(self.outIndex) + str(self.lock_Script) + str(self.montant)
        return sha256(block_string.encode()).hexdigest()
    
    #TODO vérification verrouillage/déverrouillage (moi?)