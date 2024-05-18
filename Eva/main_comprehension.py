import random
from transactions import *
from blockchain import*
from block import *
from txInPut import * 
from txOutPut import *
from institution import *
from wallet import *
#On donne un jeton a tous les utilisateur
#On ajoute les vote (tx) et le minage des block
#Verification de l integrite du vote numerique

maxVotants = 100
maxCandidats = 10
maxMineurs = 10
nb_votants = 10
nb_candidats = 3
nb_mineurs = 2
nb_utilisateurs = nb_mineurs + nb_candidats + nb_votants
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
#creation d'un wallet pour tous les utilisateurs
"""for i in range(nb_utilisateurs):
    Wallet(i) # pas certaine que ça fonctionne comme ça
"""

wal = Wallet()

print(f"---------- Helicopter Monet ----------")

for i in range(nb_votants):
    dernier_block = blockchain.getLastBlock()
    previousHash = dernier_block.getHash()
    mineur = random.randint(1, nb_votants-1) #car les votants peuvent miner des blocks
    blockchain.addBlock(blockchain.helicopterMoney(listeVotants[i], i, index, previousHash, reward, listeVotants[mineur]))
    # Est ce qu'on prend en compte l'inflation qui va faire modifier la prime des mineur en fonction d'un nombre de bloc max etc... ou pas?
    """ 
    if (index+1)%limit == 0:
        reward /= 2
        tourInflation += 1
        print("Masse monetaire 1 = ", blockchain.getMasseMonetaire())
    """
    index += 1

#2 - phase de vote. Pour notre situation on ne considère pas le nombre de block avant l'arret du marché mais le temps disponible pour voter (que l'on peut éventuellement représenter en nombre de blocs)
# On peut choisir un nombre aléatoire de votant pourrait représenter ceux qui refusent d'aller voter (Sera indiqué dans les résultats des votes pour la transparence(?))
# On doit boucler pour tous les utilisateurs (les votants dans ce cas)
for i in range(nb_votants):
    #nbTx = random().randint(1, nb_votants) #au moins 1 vote et votes blancs inclus
    #for j in range(nbTx): pas besoin car les candidats peuvent voter qu'une seule fois
    votant = random.randint(0, nb_votants-1) #il faut gérer si le votant à déjà voté ou pas
    
    # si votant n'a plus de token dans son wallet alors 
        # alors il a déjà voté donc on passe au votant suivant 
    # sinon alors on continue
    if wal.getSoldeUser(votant) == 1:
        candidat = random.randint(0, nb_candidats-1)
        montant = random.randint(0, 1)
        #pas besoin de faire de conversion
        tx = Transaction("vote")
        blockchain.utxolist = tx.voteTx(blockchain.utxolist, listeVotants[votant], listeCandidats[candidat], montant, frais)
        Txfifo.append(tx)

    mineur = random.randint(1, nb_mineurs) # mineur = random.randint(1, nb_votants)
    newBlock = blockchain.makeBlock(index, Txfifo, reward, listeMineurs[mineur]) # (..., listeVotants[mineur])

    for j in range(len(newBlock.getTransaction())):
        if newBlock.getTransaction()[j] in Txfifo:
            Txfifo.pop(j)
    
    blockchain.addBlock(newBlock)
    """
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