import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from txOutPut import *

UTXOlist = []
test1 = TxOutPut(0, "Eva", 123)
UTXOlist.append(test1)
test2 = TxOutPut(1, "James", 456)
UTXOlist.append(test2)
test3 = TxOutPut(2, "Claire", 789)
UTXOlist.append(test3)
test4 = TxOutPut(3, "Paul", 1011)
UTXOlist.append(test4)
test5 = TxOutPut(4, "Chani", 1213)
UTXOlist.append(test5)
test1.printTxOutput()
print("\n-----------------------\n")
owner = test1.getOwner()
print("owner : ", owner)
print("\n-----------------------\n")
montant = test1.getMontant()
print("montant : ", montant)
print("\n-----------------------\n")
Hash = test1.getHash()
print("Hash : ", Hash)
print("\n-----------------------\n")
newHash = "abcdef"
test1.setHash(newHash)
print("newHash : ", newHash)
print("\n-----------------------\n")
for utxo in UTXOlist:
    utxo.printTxOutput()