from faker import Faker
import random

def creationCandidats(nbCandidats):
    faker = Faker()
    prenoms_aleatoires = set()
    while len(prenoms_aleatoires) < nbCandidats:
        prenoms_aleatoires.add(faker.first_name())
    prenoms_aleatoires = list(prenoms_aleatoires)
    file_name = "./dataCandidats/candidats.txt"
    with open(file_name, 'w') as file:
        for i, prenom in enumerate(prenoms_aleatoires):
            file.write(prenom)
            if i < len(prenoms_aleatoires) - 1:
                file.write(", ")
    return prenoms_aleatoires


def creationVotant(listeCandidats,nombreVotant):
    listeVotant = []
    faker = Faker()
    while len(listeVotant) < nombreVotant:
        listeVotant = [faker.first_name() for _ in range(nombreVotant - len(listeVotant))]
        listeVotant = [prenom for prenom in listeVotant if prenom not in listeCandidats]
    votes = []
    for nomVotant in listeVotant:
        votant = nomVotant
        candidat = random.choice(listeCandidats)
        votes.append((votant, candidat))
    file_name = "./dataCandidats/votes.txt"
    with open(file_name, 'w') as file:
        for vote in votes:
            file.write(f"{vote[0]},{vote[1]}\n")

    
    
    
def creationData(nombreCandidats,nombreVotant):
    listeCandidat = creationCandidats(nombreCandidats)
    creationVotant(listeCandidat,nombreVotant)
   
creationData(10,50)