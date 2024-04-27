from block import *

class Blockchain:
    def __init__(self,difficulte,reward):
        self.nbBlock = 1
        self.difficulte = difficulte
        #self.utxolist TODO @EVA
        self.masse_monetaire = 0
        self.masse_jeton = 0
        self.bc = []
        self.bc.append(self.createGenesisBlock(reward))
        
    def createGenesisBlock(self,reward):
        genesisTransactions = []
        #Transactions tx = new Transactions("genesis");
        #tx.coinbaseTx(reward, "Creator"); TODO @EVA
        self.masse_monetaire += reward
        #genesisTransactions.add(0,tx);
        newBlock = Block(0,"0",genesisTransactions,"Creator")
        #utxoList.add(tx.lstOutputs.get(0)); TODO @EVA
        newBlock.mineBlock(self.difficulte,"Creator")
        return newBlock
    
    #def helicopterMoney le prof en avait parler mais je n'ai pas bien compris l'utiliter
    
    #def makeBlock pas compris aussi a quoi sa sert
    
    def getLastBlock(self):
        return self.bc[-1]
    
    def addBlock(self,blk):
        self.bc.append(blk)
        self.nbBlock += 1
    
    def is_valid_proof(self,block):
        return (block.blockHash.startswith('0' * self.difficulty))
    
    def verifyBlockchain(self):
        result = True
        previous_hash = "0"
        for block in self.bc:
            if not self.is_valid_proof(block) or not block.verifyBlock or previous_hash != block.blockHash:
                result = False
                break
        return result
    
    #ajouter un affichafe avec un json TODO @ROBIN
    
    