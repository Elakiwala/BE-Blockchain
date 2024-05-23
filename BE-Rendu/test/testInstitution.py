import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from institution import *

nombreVotant = 30
calcul = 50 * nombreVotant * 2 + 5 * nombreVotant

def testInstitution():
    testInsti = Institution(nombreVotant)
    print("Nombres de jeton est egale au nombre de votant passer en parametre : ",nombreVotant == testInsti.totalJeton)
    print("Nombres de fiat egale au calcul qui doit etre fais : ",calcul == testInsti.totalCredit)

testInstitution()