from blockchain import*
from block import *
from txInPut import * 
from txOutPut import *
from institution import *
#On donne un jeton a tous les utilisateur
#On ajoute les vote (tx) et le minage des block
#Verification de l integrite du vote numerique


#Creation d'un blockchain
#phase d'inflation
    #1 - création de monnaie : helicopter money, openbar, c'est coinBase qui régale

"""
Création d'une blockchain:
    - Block Genesis + ...etc
    - 
"""
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
