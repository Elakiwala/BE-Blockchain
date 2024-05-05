from block import *
from transactions import *

utxoList = []

class Blockchain:
    def __init__(self,difficulte,reward):
        self.nbBlock = 1
        self.difficulte = difficulte
        self.utxolist =[]
        self.masse_monetaire = 0
        self.masse_jeton = 0
        self.bc = []
        self.bc.append(self.createGenesisBlock(reward))
        
    def createGenesisBlock(self,reward):
        genesisTransactions = []
        tx = Transaction("genesis")
        tx.InstitutionTx(reward, "Creator")
        self.masse_monetaire += reward
        genesisTransactions.append(0,tx)
        newBlock = Block(0,"0",genesisTransactions,"Creator")
        utxoList.append(Outputlist[0])
        newBlock.mineBlock(self.difficulte,"Creator")
        return newBlock
    
    def getMasseMonetaire(self):
        return self.masse_monetaire

    def majMasseMonetaire(self, montant):
        self.masse_monetaire += montant
        return self.masse_monetaire

    def helicopterMoney(self, user, index, previousHash, reward, miner): #distribution du jeton aux votants de la part de l'institution
        heliTransactions = []
        tx = Transaction("helicopter")
        tx.InstitutionTx(reward, user)
        heliTransactions.append(0, tx) #add(index:0, tx) est ce que ça correspond à insert(0, tx)?
        utxoList.append(tx.OutputList[0])
        nb = Block(index, previousHash, heliTransactions, miner)
        nb.mineBlock(self.difficulte, miner)
        self.majMasseMonetaire(reward)
        return nb

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
    
    #ajouter un affichage avec un json TODO @ROBIN
    
    