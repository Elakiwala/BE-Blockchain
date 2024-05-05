import random
from blockchain import*
from block import *
from txInPut import * 
from txOutPut import *
from institution import *
#On donne un jeton a tous les utilisateur
#On ajoute les vote (tx) et le minage des block
#Verification de l integrite du vote numerique

maxVotants = 100
maxCandidats = 10
maxMineurs = 10
nb_votants = 10
nb_candidats = 3
nb_mineurs = 2
listeVotants = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
listeCandidats = ["Robin", "Souad", "Eva"]
listeMineurs = ["min1", "min2"]
Txfifo = [] 
difficulte = 4
index = 1
frais = 5
reward = 8
nbMaxBlock = 60
#limit = 9
#tourInflation = 1

blockchain = Blockchain(difficulte, reward)

print(f"---------- Helicopter Monet ----------")

for i in range(nb_votants):
    dernier_block = blockchain.getLastBlock()
    previousHash = dernier_block.getHash()
    blockchain.addBlock(blockchain.helicopterMoney("User", i, index, previousHash, reward))
    # Est ce qu'on prend en compte l'inflation qui va faire modifier la prime des mineur en fonction d'un nombre de bloc max etc... ou pas?
    """ 
    if (index+1)%limit == 0:
        reward /= 2
        tourInflation += 1
        print("Masse monetaire 1 = ", blockchain.getMasseMonetaire())
    """
    index += 1

#2 - phase de market. Pour notre situation on ne considère pas le nombre de block avant l'arret du marché mais le temps disponible pour voter (que l'on peut éventuellement représenter en nombre de blocs)

for i in range(nbMaxBlock):
    #nbTx = random()
    nbTx = 33
    for j in range(nbTx):
        votant = random.randint(0, nb_votants)
        candidat = random.randint(0, nb_candidats)
        montant = 1
        #pas besoin de faire de conversion
        tx = Transaction("vote")
        blockchain.utxolist = tx.marketTx(blockchain.utxolist, listeVotants[votant], listeCandidats[candidat], montant, frais)
        Txfifo.append(tx)
    
    mineur = random.randint(0, nb_mineurs)
    newBlock = blockchain.makeBlock(index, Txfifo, reward, listeMineurs[mineur])

    for j in range(len(newBlock.getTransaction())):
        if newBlock.getTransaction()[j] in Txfifo:
            Txfifo.pop(j)
    """
    blockchain.addBlock(newBlock)
    if (index+1) % limit == 0 & reward > 0:
        reward /= 2
        print("Reward = ", reward)
        tourInflation += 1
        print("Masse monetaire 2 = ", blockchain.getMasseMonetaire())
    """
    #est ce qu'on doit diviser la récompense dans notre cas? Je ne pense pas...
    index += 1

#Dump de la blockchain
#JSON TODO @Robin