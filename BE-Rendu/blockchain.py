from block import *
from transactions import *

utxoList = []

class Blockchain:
    def __init__(self,difficulte,reward):
        self.nbBlock = 1
        self.difficulte = difficulte
        self.utxoList = utxoList
        self.masse_monetaire = 0
        self.masse_jeton = 0
        self.bc = []
        self.createLog()
        self.bc.append(self.createGenesisBlock(reward))
        
    def createLog(self):
        blockchainInfo = {
            "difficulte" : self.difficulte
        }
        with open("./Json/logMineur.json", 'w') as file:
            json.dump(blockchainInfo, file, indent=4)
            
    def createGenesisBlock(self,reward):
        genesisTransactions = []
        tx = Transaction(0,"genesis","Creator","Creator")
        tx.InstitutionTx(reward, "Creator")
        self.masse_monetaire += reward
        genesisTransactions.insert(0,tx)
        newBlock = Block(0,"0",genesisTransactions,"Creator")
        self.utxoList.append(tx.Outputlist[0])
        newBlock.mineBlock(self.difficulte,"Creator")
        self.ajoutLog("Creator",0,reward)
        return newBlock
    
    def getMasseMonetaire(self):
        return self.masse_monetaire

    def majMasseMonetaire(self, montant):
        self.masse_monetaire += montant
        return self.masse_monetaire

    def helicopterMoney(self, users, index, previousHash, montant, miner): #distribution du jeton aux votants de la part de l'institution
        for votant in users:
            heliTransactions = []
            tx = Transaction(1, "helicopter", "Institution", votant)
            tx.InstitutionTx(montant, votant)
            heliTransactions.append(0, tx) #add(index:0, tx) est ce que ça correspond à insert(0, tx)?
            self.utxoList.append(tx.Outputlist[0])
            nb = Block(index, previousHash, heliTransactions, miner)
            nb.mineBlock(self.difficulte, miner)
            self.majMasseMonetaire(montant)
        return nb

    def getUTXOList(self):
        return self.utxoList

    def makeBlock(self, index, txList, reward, miner): #c'est le mineur qui fait le block à partir d'une transaction entre 2 utilisateurs (votant-candidat ici) et l'ajout dans la blockchain après vérification
        blockTransactions = []
        listTransactionsFrais = []
        nbTx = 2
        for i in range(min(nbTx, len(txList))):
            blockTransactions.append(0, txList[0])
            txList.pop()
        
        previousHash = self.getLastBlock().getHash()

        if reward > 0:
            tx = Transaction("institution")
            if tx.nbOutputs != 0:
                self.utxoList.append(tx.Outputlist[0])
            
            tx.InstitutionTx(reward, miner)
            for j in range(len(blockTransactions)):
                txI = blockTransactions[j]
                fees = txI.frais()
                txFees = Transaction("frais")
                txFees.setInputList(txI.Inputlist)
                outTx = TxOutPut(0, "0", fees)
                outTx.setHash(outTx.calcul_hash())
                txFees.setOutputList(txFees.Outputlist.append(outTx))
                txFees.setNbInput(len(txFees.Inputlist))
                txFees.setNbOutput(len(txFees.Outputlist))
                self.utxoList.append(txFees.Outputlist[0])
                listTransactionsFrais.append(0, txFees)
            for txF in listTransactionsFrais:
                blockTransactions.append(txF)
            blockTransactions.append(0, tx)
            self.majMasseMonetaire(reward)
        nb = Block(index, previousHash, blockTransactions, miner)
        nb.mineBlock(self.difficulte, miner)
        self.ajoutLog(miner,index,reward)
        return nb
            
    def ajoutLog(self,miner,index,reward):
        minerInfo = {
            "Miner" : miner,
            "Index" : index,
            "Reward" : reward,
        }
        with open("./Json/logMineur.json", 'a') as file:
            json.dump(minerInfo, file, indent=4)
        
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
    
    def to_json(self,fileName):
        blockchain_json = {
            "nbBlock": self.nbBlock,
            "difficulte": self.difficulte,
            "masse_monetaire": self.masse_monetaire,
            "masse_jeton": self.masse_jeton
        }
        with open(fileName, 'w') as file:
            json.dump(blockchain_json, file, indent=4)
        for block in self.bc:
            block.to_json(fileName)
    
    
    