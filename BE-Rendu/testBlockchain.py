from blockchain import *
from wallet import *

def testblockchain():
    bc = Blockchain(4,50)
    wCreator = Wallet(bc.getUTXOList,bc.fiatList,"Creator")
    wMe = Wallet(bc.getUTXOList,bc.fiatList,"me")
    for i in range(5):
        b = bc.makeBlock(i + 1,[],5,"me")
        bc.addBlock(b)
    bc.to_json("./Json/testBlockchain.json")
    wCreator.updateFiat()
    wMe.updateFiat()
    print("wallet creator : ",wCreator.credit)
    print("wallet me : ",wMe.credit)
    print("Conformite de la blockchain :",bc.verifyBlockchain())
        
testblockchain()