class Institution:
    def __init__(self,nbVotant):
        self.totalJeton = nbVotant
        self.totalCredit = self.calculCredit(nbVotant)
        
    def calculCredit(self,nbVotant):
        recompenseMinage = 50
        recompenseVote = 5
        return nbVotant * recompenseMinage * 2 + nbVotant * recompenseVote
    