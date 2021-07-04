class Individual(object):
    def __init__(self):
        # echar of group
        self.chromossome = []
        # the fitness for heterogeneity
        self.fitnesshomo = 0
        # the fitness for heterogenty
        self.fitnesshetero = 0
        # the general fitness.( ranking)
        self.fitness = 0
        # the ranking only for heterogeneity
        self.RankHomo = 0
        # the ranking only for heterogenty
        self.RankHetero = 0
        # the number of iteration of the group. That value is the sum of the all interation fo the group
        self.interation = float(0.0)
        # he ranking only for interation
        self.RankIteration = 0
