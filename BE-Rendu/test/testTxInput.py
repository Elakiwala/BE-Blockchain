import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from txInPut import *
test1 = TxInput(0, "moi", 2, "test1")
test2 = TxInput(1, "autre", 5, "test2")

test1.printTxInput()
print("\n")
montantT1 = test1.getMontant()
print("montant test1 : ", montantT1)
ownerT1 = test1.getOwner()
print("owner test1 : ", ownerT1)
print("\n-------------------------------------------\n")
test2.printTxInput()
print("\n")
montantT2= test2.getMontant()
print("montant test2 : ", montantT2)
ownerT2 = test2.getOwner()
print("owner test2 : ", ownerT2)