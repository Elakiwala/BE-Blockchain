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

nb_votants = 10
nb_candidats = 3
listeVotants = #mise a jour creationData
listeCandidats = #mise a jour creationData
Txfifo = [] 
difficulte = 4
index = 1
indexT = 1
rewardMinage = 50
rewardVote = 5
tempsDeVote = 3
dureeMax = nb_votants * 3
initMoney = 1

# ---------- 1) MISE EN PLACE ----------

# Création de la blockchain et du wallet
blockchain = Blockchain(difficulte, rewardMinage)

# Helicopter money sur touts les votants

blockchain.helicopterMoney(listeVotants, initMoney) # Pour tous les votants mettre 1 si le votant veut voter ou -1 si abstention (certainement à faire autrement...)


# ---------- 2) PHASE DE VOTE ----------

# Transaction des votes des votants vers les candidats
    # Possible pour une certaine durée de vote 

duree = 0
vote = 0

while vote < nb_votants and duree < dureeMax: # tous les votants ont voté ou bien le temps des élection s'est écoulé
    dodo = random.randint(0,5)
    t.sleep(dodo)
    duree += dodo
    votant = random.randint(0, nb_votants - 1)

    abstention = random.randint(0,10)
    if abstention != 10 :
        # Choix du candidat pour lequel le votant va voter
        candidat = random.randint(0, nb_candidats - 1)
        tx = Transaction(indexT, "vote")
        Txfifo.append(tx)
        indexT += 1
        # Effectuer le vote/transaction
        blockchain.utxoList = tx.voteTx(blockchain.utxoList, listeVotants[votant], listeCandidats[candidat])
    
    # Un mienur doit faire la vérification du vote
    mineur = random.randint(0, nb_votants - 1)
    newBlock = blockchain.makeBlock(index, Txfifo, rewardMinage, listeVotants[mineur])

    index += 1
    vote += 1

if vote == nb_votants: print("Fin de la phase de vote. Tous les votants ont voté!")
if dureeMax <= duree: print("Fin de la phase de vote. Le temps des élections est écoulé!")


#------------4) VERIFICATION ---------
#verification

# ---------- 3) RESULTATS ----------

# Il faut afficher le résultat de l'élection et dure qui est le vainqueur

# Affichage des votant ayant voté un candidat, blanc ou abstention

#TODO affichage json transaction votant

# Affichage des candidats et leurs voies et Affichage du gagnant

maxVote = 0
gagnant = "Candidat..."


print(f"Le gagnant des élections est ", gagnant, " avec " " voies !")



#JSON TODO @Robin