import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from blockchain import *

def testblockchain():
    bc = Blockchain(4,50)
    for i in range(5):
        b = bc.makeBlock(i + 1,[],5,"me")
        bc.addBlock(b)
    bc.to_json("./testJson/testBlockchain.json")
    print("Conformite de la blockchain :",bc.verifyBlockchain())
        
testblockchain()