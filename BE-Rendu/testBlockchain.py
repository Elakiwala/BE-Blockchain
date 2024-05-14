from blockchain import *

def testblockchain():
    bc = Blockchain(4,50)
    for i in range(5):
        b = bc.makeBlock(i + 1,[],0,"me")
        bc.addBlock(b)
    bc.to_json("./Json/testBlockchain.json")
        
testblockchain()