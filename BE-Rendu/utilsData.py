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
                file.write(",")
    return prenoms_aleatoires


def creationVotant(listeCandidats,nombreVotant):
    listeVotant = set()
    faker = Faker()
    while len(listeVotant) < nombreVotant:
        prenom = faker.first_name()
        if prenom not in listeVotant and prenom not in listeCandidats :
            listeVotant.add(prenom)
        else :
            index = 1
            while f"{prenom}{index}" in listeVotant or f"{prenom}{index}" in listeVotant :
                index += 1
            listeVotant.add(f"{prenom}{index}")
        file_name = "./dataCandidats/votants.txt"
        with open(file_name, 'w') as file:
            for i, prenom in enumerate(listeVotant):
                file.write(prenom)
                if i < len(listeVotant) - 1:
                    file.write(",")

def lire_mots(file_name, nb_mots):
    mots = []
    with open(file_name, 'r') as file:
        data = file.read().strip()
        mots = data.split(',')[:nb_mots]
    return mots

def creationData(nbVotants,nbCandidats):
    listeCandidats = creationCandidats(nbCandidats)
    creationVotant(listeCandidats,nbVotants)