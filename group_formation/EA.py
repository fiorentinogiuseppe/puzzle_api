import random
import copy
from .individual import Individual
import numpy as np
from operator import attrgetter
from .SetFitness import SetFitness


class EvolutionaryAlgorithm(object):
    # it's the algorithm itself
    def __init__(self, tam_grupo, tam_turma, carac, ppg, numcarac, interations):
        self.Grupos = []  # each individual represents a candidate solution to an optimization problem.
        self.tam_grupo = tam_grupo
        self.tam_turma = tam_turma
        self.carac = carac
        self.part = 0  # part of the chromossome will be divided
        self.bestC = []
        self.bestF = []
        self.tm = []
        self.im = []
        self.ppg = ppg
        self.homo = []
        self.hetero = []
        self.tamGrupos = 100  # number of possibles soluctions.
        self.numcarac = numcarac
        self.interations = interations

    # FAZER COM QUE POSSAR TER GRUPOS COM NUMEROS IMPARES
    def InitialPopulation(self):

        for i in range(self.tamGrupos):  # cread a initial population
            gene = list(range(self.tam_turma))
            random.shuffle(gene)
            personal = Individual()  # its a chromossome
            gene = np.array(gene)
            gene = gene.reshape(-1, self.ppg)
            personal.chromossome = gene[::]
            self.Grupos.append(copy.deepcopy(personal))

    # calculate the fitness. That function call a class to calculate the fitness
    def Fitness(self):
        dados = SetFitness(self.tam_grupo, self.tam_turma, self.carac, self.ppg, self.Grupos, self.numcarac,
                                      self.interations)
        dados.CharacteristicsNormalization()
        dados.InterationNormalization()

        dados.TM()
        dados.IM()
        dados.Homo()
        dados.Hetero()
        dados.numInterations()
        self.Grupos = copy.deepcopy(
            dados.returnGrupos())  # recieve the Groups modified in the function to set the Fitness

    # calculate th ranking
    def Ranking(self):

        self.carac = np.array(self.carac)
        self.Grupos.sort(key=attrgetter("fitnesshetero"), reverse=True)  # sort heterogeneity
        for i in range(len(self.Grupos)):  # give the ranking to object
            self.Grupos[i].RankHetero = self.Grupos.index(self.Grupos[i]) + 1

        self.Grupos.sort(key=attrgetter("fitnesshomo"))  # sort homogeneity

        for i in range(len(self.Grupos)):  # give the ranking to object
            self.Grupos[i].RankHomo = self.Grupos.index(self.Grupos[i]) + 1

        self.Grupos.sort(key=attrgetter("interation"), reverse=True)  # sort interation

        for i in range(len(self.Grupos)):  # give the ranking to object
            self.Grupos[i].RankIteration = self.Grupos.index(self.Grupos[i]) + 1

        for i in range(len(self.Grupos)):
            self.Grupos[i].fitness = self.Grupos[i].RankHomo + self.Grupos[i].RankHetero + self.Grupos[i].RankIteration

    # the selection chose the best of the individuals
    def Selection(self):
        if self.tamGrupos % 2 == 0:
            self.parte = int((-1 + self.tamGrupos) / 2)
        elif self.tamGrupos % 2 != 0:
            self.parte = int(-1 + self.tamGrupos / 2) + 1
        self.Grupos.sort(key=attrgetter("fitness"))

        for i in range(self.parte + 1, len(self.Grupos)):
            del self.Grupos[self.parte + 1]

        #print('Melhor fitness', self.Grupos[0].fitness)  # print in each generation the best fitness

    # Calculate the crossover. The crossover is based in the traveling salesman problem.
    def CrossOver(self):
        # this if will divided the chromossome
        if self.tam_turma % 2 == 0:
            self.parte = (self.tam_turma - 1) / 2
        elif self.tam_turma % 2 != 0:
            self.parte = int((self.tam_turma - 1) / 2)

        filho1 = []
        filho2 = []
        # self.Grupos
        for i in range(0, len(self.Grupos)):
            self.Grupos[i].chromossome = self.Grupos[i].chromossome.reshape(1, -1)

        for i in range(len(self.Grupos)):
            del filho1
            filho1 = []
            filho1 = (copy.deepcopy(self.Grupos[i].chromossome))
            for j in range(self.tam_turma):
                if j > self.parte:
                    if self.Grupos[i - 1].chromossome[0, j] in filho1[0]:
                        indx = (filho1[0]).tolist().index(copy.deepcopy(self.Grupos[i - 1].chromossome[0, j]))
                        if indx != j:
                            temp = copy.deepcopy(filho1[0, j])
                            filho1[0, j] = (copy.deepcopy(filho1[0, indx]))
                            filho1[0, indx] = copy.deepcopy(temp)
                        else:
                            filho1[0, j] = (copy.deepcopy(self.Grupos[i - 1].chromossome[0, j]))

            person = Individual()
            person.chromossome = copy.deepcopy(filho1)
            self.Grupos.append(person)

        for i in range(0, len(self.Grupos)):
            self.Grupos[i].chromossome = self.Grupos[i].chromossome.reshape(-1, self.ppg)

    # the mutation occours random and choose 2 genes to rearanges.
    def Mutation(self):
        for i in range(len(self.Grupos)):
            self.Grupos[i].chromossome = self.Grupos[i].chromossome.reshape(1, -1)

        for i in range(self.tam_grupo):
            gene1 = random.randint(0, self.tam_turma - 1)
            gene2 = random.randint(0, self.tam_turma - 1)
            cam = random.randint(0, self.tam_grupo - 1)

            salvar = self.Grupos[cam].chromossome[0][gene1]
            self.Grupos[cam].chromossome[0][gene1] = self.Grupos[cam].chromossome[0][gene2]
            self.Grupos[cam].chromossome[0][gene2] = salvar

        for i in range(len(self.Grupos)):
            self.Grupos[i].chromossome = self.Grupos[i].chromossome.reshape(-1, self.ppg)

    # sort the groups and choose the best chromosome and fitness
    def SortBest(self):
        self.Grupos.sort(key=attrgetter("fitness"))
        self.bestC.append(copy.deepcopy(self.Grupos[0].chromossome))
        self.bestF.append(copy.deepcopy(self.Grupos[0].fitness))

    def The_best(self, iteracoes, to_file=False):  # print the best of the bests and create an archive
        var = min(self.bestF)
        idt = self.bestF.index(var)
        # print("Best Class", self.bestC[idt])
        # print("Best Fitness", var)
        if to_file:
            arqv = open('dados.txt', 'a')
            texto = ["\nIteracoes:\n", str(iteracoes), "\n", "MelhorFitness:\n", str(min(self.bestF)), "\n"]
            arqv.writelines(texto)
            arqv.close()
        return var,  self.bestC[idt]
