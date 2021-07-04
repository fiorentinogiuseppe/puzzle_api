from .EA import EvolutionaryAlgorithm


class GaConfig(object):
    # its a manager of the genetic algorithm
    def __init__(self, tam_pop, tam_genes, iteracoes, carac, tam_indiv, numcarac, interations, to_file, verbose):
        self.tam_pop = tam_pop
        self.carac = carac
        self.tam_genes = tam_genes
        self.iteracoes = iteracoes
        self.tam_indiv = tam_indiv
        self.numcarac = numcarac
        self.interations = interations
        self.to_file=to_file
        self.best_fit = None
        self.best_class = None
        self.verbose = verbose

    # will call each metod of the genetic algorithm
    def setGa(self):
        pplc = EvolutionaryAlgorithm(self.tam_pop, self.tam_genes, self.carac, self.tam_indiv, self.numcarac,
                                        self.interations)
        pplc.InitialPopulation()
        for i in range(self.iteracoes):
            if self.verbose:
                print(">> Geracao: ", i)
            pplc.Fitness()
            pplc.Ranking()
            pplc.SortBest()
            pplc.Selection()
            pplc.CrossOver()
            pplc.Mutation()

        self.best_fit, self.best_class = pplc.The_best(self.iteracoes, to_file=self.to_file)
