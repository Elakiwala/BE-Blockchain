from block import *

def testBlock():
    print("Creation du block :")
    b1 = Block(1,"0",[],"Me")
    b1.printBlock()
    print("\n")
    print("Verification du block sans minage (Doit rien afficher):")
    b1.verifyBlock()
    print("\n")
    print("Minage du block:")
    b1.mineBlock(4,"Other")
    print("\n")
    print("Verification du block avec minage (Doit rien afficher):")
    b1.verifyBlock()
    print("\n")
    print("Verificaiton du merkle tree (Doit rien afficher) :")
    b1.verifyMerkleTree()
    print("\n")
    print("Le block avec les donnes apte a rentrer dans la blockchain :")
    b1.printBlock()
    b1.to_json("./Json/testBlock.json")

testBlock()