import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

#TODO @Eva
import time as t
from transactions import *
from txInPut import*
from txOutPut import*
from wallet import *

UTXOlist = []
fiatList = []

tx1 = Transaction(0, "tx1", "Eva", "James",[],[])
wJ = Wallet(UTXOlist, fiatList, "James")
wE = Wallet(UTXOlist, fiatList, "Eva")
"""print("Solde James : ", w.getSoldeUser("James"))
print("Solde Eva : ", w.getSoldeUser("Eva"))"""
tx1.printTransaction()
print("\n--------------------------\n")
tx1.InstitutionTx(1, "James")
UTXOlist.append(tx1.Outputlist[-1])
"""
for j in range(len(UTXOlist)):
    print("Owner = ", UTXOlist[j].getOwner())
    print("Montant = ", UTXOlist[j].getMontant())"""
#print("Solde James : ", w.getSoldeUser("James"))
print("\n--------------------------\n")
tx1.printTransaction()
print("\n--------------------------\n")
tx1.InstitutionTx(5, "Eva")
UTXOlist.append(tx1.Outputlist[-1])
"""for j in range(len(UTXOlist)):
    print("Owner = ", UTXOlist[j].getOwner())
    print("Montant = ", UTXOlist[j].getMontant())"""
#print("Solde Eva : ", w.getSoldeUser("Eva"))
print("\n--------------------------\n")
tx1.printTransaction()
print("\n--------------------------\n")

for utxo in UTXOlist:
    utxo.printTxOutput()
"""
print("\n\n Wallet!")
print("Solde James : ", w.getSoldeUser("James"))
print("Solde Eva : ", w.getSoldeUser("Eva"))"""

print("VOTE 1 !!!!!!")
tx1.voteTx(UTXOlist, "Eva", "James")
tx1.printTransaction()
print("\n\n Wallet!")
print("Solde James : ", wJ.getSoldeUser())
print("Solde Eva : ", wE.getSoldeUser())