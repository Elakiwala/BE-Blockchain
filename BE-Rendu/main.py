import random
from transactions import Transaction
from blockchain import Blockchain
from block import Block
from txInPut import TxInput
from txOutPut import TxOutPut
from institution import Institution
from wallet import Wallet
import time as t

# ---------- VARIABLES GLOBALES ----------

maxVotants = 100
maxCandidats = 10
nb_votants = 10
nb_candidats = 3
listeVotants = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
listeCandidats = ["Robin", "Souad", "Eva"]
Txfifo = [] 
difficulte = 4
index = 1
indexT = 1
frais = 5
reward = 8
duree = 2 # minutes
initMoney = 1 + frais/100

# ---------- 1) MISE EN PLACE ----------

# Création de la blockchain et du wallet
blockchain = Blockchain(difficulte, reward)
wallet = Wallet(blockchain.getUTXOList())

# Helicopter money sur touts les votants
for votant in listeVotants: 
    dernierBlock = blockchain.getLastBlock()
    previousHash = dernierBlock.getHash()
    mineur = "Institution miner"
    blockchain.addBlock(blockchain.helicopterMoney(votant, index, previousHash, initMoney, mineur)) # Pour tous les votants mettre 1 si le votant veut voter ou -1 si abstention (certainement à faire autrement...)
    index+=1

# ---------- 2) PHASE DE VOTE ----------

# Transaction des votes des votants vers les candidats
    # Possible pour une certaine durée de vote 

start = t.time()
vote = 0

while vote < nb_votants | t.time() - duree <= start: # tous les votants ont voté ou bien le temps des élection s'est écoulé
    votant = random.randint(1, nb_votants - 1)
    # Vérification si le votant peut voter (wallet = 1 | wallet = 0 (a déjà voté) | wallet = -1 (abstention)) | wallet = -2 (a déjà voté mais blanc) 
    if wallet.getSoldeUser(listeVotants[votant]) == 0 | wallet.getSoldeUser(listeVotants[votant]) == -2:
        print("Le votant a déjà voté\n")
    elif wallet.getSoldeUser(listeVotants[votant]) == -1: 
        print("Le votant ne souhaite pas voter\n")
    else:
        # Choix du candidat pour lequel le votant va voter
        candidat = random.randint(1, nb_candidats - 1)
        montant = random.randint(0, 1) # si 0 alors vote blanc sinon vote
        tx = Transaction(indexT, "vote")
        Txfifo.append(tx)
        indexT += 1
        # Effectuer le vote/transaction
        blockchain.utxoList = tx.voteTx(blockchain.utxoList, listeVotants[votant], listeCandidats[candidat], montant, frais)
    
    # Un mienur doit faire la vérification du vote
    mineur = random.randint(1, nb_votants - 1)
    newBlock = blockchain.makeBlock(index, Txfifo, reward, listeVotants[mineur])

    # Il faut que les tx de newBlock soient retirées de la liste globale des transaction (car elle sert uniquement de file d'attente de traitement)
    for i in range(len(newBlock.getTransaction())):
        k = 0
        if newBlock.getTransaction()[i] in Txfifo:
            while Txfifo[k] != newBlock.getTransaction()[i] : k += 1
            Txfifo.pop(k)

    index += 1
    vote += 1

if vote == nb_votants: print("Fin de la phase de vote. Tous les votants ont voté!")
if t.time() - duree > start : print("Fin de la phase de vote. Le temps des élections est écoulé!")


# ---------- 3) RESULTATS ----------

# Il faut afficher le résultat de l'élection et dure qui est le vainqueur

# Affichage des votant ayant voté un candidat, blanc ou abstention
for votant in listeVotants:
    if wallet.getSoldeUser(votant) == 0: # Le votant a voté un candidat
        for block in blockchain:
            for tx in block.getTransaction():
                if tx.getUser() == votant:
                    print(f"", votant, " a voté pour ", tx.getDest())
                    break
            break
    elif wallet.getSoldeUser(votant) == -1:
        print(f"", votant, " n'est pas allé voter")
    else:
        print(f"", votant, " a voté blanc")

# Affichage des candidats et leurs voies et Affichage du gagnant

maxVote = 0
gagnant = "Candidat..."

for candidat in listeCandidats:
    solde = wallet.getSoldeUser(candidat)
    print(f"", candidat, " a rempoté ", solde, " voies")
    if maxVote < solde: maxVote, gagnant = solde, candidat

print(f"Le gagnant des élections est ", gagnant, " avec ", solde, " voies !")



#JSON TODO @Robin