class Institution:
    def __init__(self,nbVotant):
        totalJeton = nbVotant
        totalCredit = self.calculCredit(nbVotant)
        
        def calculCredit(self,nbVotant):
            recompenseMinage = 50
            recompenseVote = 5
            return nbVotant * recompenseMinage + nbVotant * recompenseVote
    