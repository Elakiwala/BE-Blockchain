import random
from transactions import Transaction
from blockchain import Blockchain
from txOutPut import TxOutPut
from institution import *
from wallet import Wallet
import time as t
from utilsData import *
from utils import *
from datetime import datetime

#Reste a faire le wallet institution 

# ---------- VARIABLES GLOBALES ----------

fileVotantName = "./dataCandidats/votants.txt"
fileCandidatsName = "./dataCandidats/candidats.txt"
fileVotantHelicopter = "./Json/soldeVotantApresHelicopter.json"
fileCandidatsHelicopter = "./Json/soldeCandidatApresHelicopter.json"
fileVotantVote = "./Json/soldeVotantApresVote.json"
fileCandidatsVote = "./Json/soldeCandidatApresVote.json"
fileBlockchain = "./Json/blockchainApresVote.json"
fileInstitution = "./Json/institution.json"
tauxDabstention = 10
nb_votants = 10
nb_candidats = 3
tempsVoteBool = False
listeVotants = lire_mots(fileVotantName,nb_votants)
listeCandidats = lire_mots(fileCandidatsName,nb_candidats)
listeCandidats.append("blanc")
Txfifo = [] 
difficulte = 4
indexT = 1
rewardMinage = 50
rewardVote = 5
tempsDeVote = 3
dureeMax = nb_votants * 3
initMoney = 1
txConforme = True

# ---------- 1) MISE EN PLACE ----------
clear_json_file(fileInstitution)

# Création de la blockchain et du wallet
blockchain = Blockchain(difficulte, rewardMinage)
institution = Institution(nb_votants)
instiInit = TxOutPut(0, "Institution", institution.totalJeton)
blockchain.utxoList.append(instiInit)
blockchain.fiatList.append(("Institution", institution.totalCredit))
walletInstitution = Wallet(blockchain.utxoList,blockchain.fiatList,"Institution")
walletInstitution.toJson(fileInstitution)

# Helicopter money sur touts les votants

blockchain.helicopterMoney(listeVotants, initMoney,institution.totalCredit) # Pour tous les votants mettre 1 si le votant veut voter ou -1 si abstention (certainement à faire autrement...)

clear_json_file(fileVotantHelicopter)
clear_json_file(fileCandidatsHelicopter)

for votant in listeVotants : #fichier json pour voir si tous les candidats on leur jetons et voir si les mineurs on etati recompenser
    wallet = Wallet(blockchain.utxoList,blockchain.fiatList,votant)
    wallet.toJson(fileVotantHelicopter)
for candidats in listeCandidats : #fichier json pour voir si tous les candidats on leur jetons et voir si les mineurs on etati recompenser
    wallet = Wallet(blockchain.utxoList,blockchain.fiatList,candidats)
    wallet.toJson(fileCandidatsHelicopter)
walletInstitution.toJson(fileInstitution)

# ---------- 2) PHASE DE VOTE ----------

# Transaction des votes des votants vers les candidats
    # Possible pour une certaine durée de vote 

idVotant = 0
vote = 0
startTime = datetime.now()

while idVotant < nb_votants: # tous les votants ont voté ou bien le temps des élection s'est écoulé
    if tempsVoteBool :
        dodo = random.randint(0,5)
        t.sleep(dodo)
    currentTime = datetime.now()
    passedTime = (currentTime - startTime).total_seconds()
    if passedTime >= dureeMax :
        print("Le temps est finis")
        break
    
    votant = listeVotants[idVotant] # pour simplifier au debut on les fait voter dans l'ordre

    abstention = random.randint(0,tauxDabstention)
    if abstention !=  0:
        # Choix du candidat pour lequel le votant va voter
        idCandidat = random.randint(0, len(listeCandidats) - 1)
        candidat = listeCandidats[idCandidat]
        tx = Transaction(indexT, "vote", votant, candidat,listeVotants, listeCandidats)
        if not tx.validity :
            print("Une transactions est illegale on arrete le vote.")
            txConforme = False
            break
        Txfifo.append(tx)
        indexT += 1
        blockchain.utxoList = tx.voteTx(blockchain.utxoList, votant, candidat)
        # Un mineur doit faire la vérification du vote
        mineur = random.randint(0, nb_votants - 1)
        newBlock = blockchain.makeBlock(blockchain.nbBlock, Txfifo, rewardMinage, listeVotants[mineur])
        blockchain.fiatList.append((votant,rewardVote))
        blockchain.fiatList.append(("Institution",-rewardVote))
        blockchain.addBlock(newBlock)
        vote += 1
    idVotant+= 1

clear_json_file(fileVotantVote)
clear_json_file(fileCandidatsVote)

for votant in listeVotants : 
    wallet = Wallet(blockchain.utxoList,blockchain.fiatList,votant)
    wallet.toJson(fileVotantVote)
for candidats in listeCandidats :
    wallet = Wallet(blockchain.utxoList,blockchain.fiatList,candidats)
    wallet.toJson(fileCandidatsVote)
walletInstitution.toJson(fileInstitution)
    
blockchain.to_json(fileBlockchain)

if vote == nb_votants: print("Fin de la phase de vote. Tous les votants ont voté!")
else: print("Fin de la phase de vote. Pas tous les votant ont vote!")


#------------3) VERIFICATION ---------
voteConforme = True and txConforme
blockBon = True
if not blockchain.verifyBlockchain():
    print("La blockchain n'est pas conforme et le vote n'est donc pas pris en compte.")
    voteConforme = False
for bloc in blockchain.bc :
    if not bloc.verifyBlock():
        blockBon = False
        voteConforme = False
if not blockBon:
    print("Il y a des problemes avec au moins un block le vote n'est dont pas pris en compte")

# ---------- 4) RESULTATS ----------

if voteConforme:
    resultat = []
    idGagnant1 = -1
    idGagnant2 = -1 
    voteGagnant = 0
    voteMax = 0
    nomGagnant = ""
    for candidats in listeCandidats:
        wallet = Wallet(blockchain.utxoList,blockchain.fiatList,candidats)
        resultat.append((candidats,wallet.getSoldeUser()))
    resultat.sort(key=lambda x: (-x[1], x[0]))
    if len(resultat) > 0:
        if resultat[0][0].lower() == "blanc":
            if len(resultat) > 1:
                voteGagnant = resultat[1][1]
                nomGagnant = resultat[1][0]
            else:
                nomGagnant = None
        else:
            voteGagnant = resultat[0][1]
            nomGagnant = resultat[0][0]
    else:
        nomGagnant = None
    if nomGagnant == None or vote == 0:
        print("Il n y a aucun vote pour les candidats")
    else :
        print(f"Le gagnant est {nomGagnant} avec {round(voteGagnant/vote*100,2)} % des votes.")
