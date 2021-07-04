import copy
import numpy as np
from math import sqrt


class SetFitness(object):
    def __init__(self, tamGrupo, tamTurma, carac, ppg, Grupo, numcarac, interations):
        self.Grupos = copy.deepcopy(Grupo)
        self.tamGrupo = tamGrupo
        self.tamTurma = tamTurma
        self.carac = carac
        self.tm = []
        self.im = []
        self.ppg = ppg
        self.numcarac = numcarac
        self.interations = interations

    def CharacteristicsNormalization(
            self):  # this function is used to calculate the normalization of the characteristics
        less = []
        more = []
        self.carac = np.array(self.carac)
        self.carac = self.carac.reshape(-1, self.numcarac)
        for i in range(self.numcarac):  # this looping find the min and max of the column
            less.append(np.amin(self.carac[:, i]))
            more.append(np.amax(self.carac[:, i]))

        for i in range(len(self.carac)):  # this loop calculate the normalization -> (number-min)/max-min
            for j in range(len(self.carac[1])):
                self.carac[i][j] = float((self.carac[i][j] - less[j]) / float(more[j] - less[j]))

    def InterationNormalization(self):  # this function is used to calculate the normalization of the interation
        self.interations = np.array(self.interations)
        self.interations = self.interations.reshape(-1, self.tamTurma)
        self.interations = self.interations.astype(float)
        less = (np.amin(self.interations))
        more = (np.amax(self.interations))

        for i in range(len(self.interations)):
            if (more - less) > 0:
                self.interations[i] = (((self.interations[i]) - less) / (more - less))
            else:
                self.interations[i] = 0

    def TM(self):  # this function is used to calculate the mean of the each characteristics
        self.tm = []
        for i in range((self.carac.shape[1])):
            cmprmt = self.carac.shape[0]
            m = sum(self.carac[:, i]) / cmprmt
            self.tm.append(m)
        self.tm = np.array(self.tm)
        self.tm = self.tm.reshape(-1, len(self.carac[1]))

    def IM(self):  # this function is used to calculate the mean of the characteristics of each studenty of the group
        lista = []
        media = []
        soma = 0
        somatorio = []
        meio = 0
        vm = 0
        self.im = []
        for i in range(len(self.Grupos)):  # acess each individual
            for j in range(len(self.Grupos[i].chromossome)):  # acess each chromossome of the individual
                for crc in range(self.carac.shape[1]):  # acess each caracteristics
                    soma = 0
                    for k in self.Grupos[i].chromossome[j]:  # acess each gene of chromossome
                        soma += self.carac[k, crc]
                    meio = soma / self.ppg  # characteristics of each studenty
                    media.append(meio)
        media = np.array(media)
        media = media.reshape(-1, self.numcarac)

        lista = []
        k = 0  # contador
        for i in range(0, len(media), self.tamGrupo):  # organization of the list
            lista.append([])

            for j in range(self.tamGrupo):
                lista[k].append(media[i + j])
            k = k + 1
        lista = np.array(lista)
        self.im = copy.deepcopy(lista)

    def Homo(self):  # calculate th homogenity
        self.homo = []
        for i in self.im:  # pick each of Individual mean
            for j in self.tm:  # piack the Team mean
                subt = np.subtract(i, j)
                quadrado = np.square(subt)
                somatorio = sum(sum(quadrado))
            self.homo.append(copy.copy(somatorio))
        for i in range(len(self.Grupos)):  # put it in each individual
            self.Grupos[i].fitnesshomo = self.homo[i]

    def Hetero(self):  ##Calculate the Heterogeneity based in euclidian distance
        cara = []
        subt = []  # subtracao e potenciacao do calculo da distancia euclidiana
        dist = 0
        for i in range(len(self.Grupos)):  # acess each individual
            for j in self.Grupos[i].chromossome:  # acess each group
                for k in range(self.ppg):  # combine the elements of i with j
                    for l in range(k + 1, self.ppg):
                        dist = 0
                        del subt
                        subt = []  # iniciar a lista de distancia de cada grupo

                        for c in range(self.carac.shape[1]):  # acessar cada caracteristica

                            idx1 = j[k]  # index of 1st element of subtraction
                            idx2 = j[l]  # index of 2nd element of subtraction
                            subt.append(
                                (abs(self.carac[idx1, c] - self.carac[idx2, c])) ** 2)  # subtraction e exponetiation
                        somatorio = sum(subt)  # summation
                        raiz = sqrt(somatorio)  # roots
                dist = dist + raiz  # summation of each distance of group
            self.Grupos[i].fitnesshetero = dist  # fitness da heterogeneiradade

    def numInterations(self):  # calculate the interation of each individual
        subt = []
        somatorio1 = []
        somatorio2 = []

        for i in range(len(self.Grupos)):  # acess each individual

            for j in self.Grupos[i].chromossome:  # acess each group
                del subt
                subt = []
                for k in range(self.ppg):  # combine elements of i with j
                    for l in range(self.ppg):
                        idx1 = j[k]  # index of 1st element of subtraction
                        idx2 = j[l]  # index of 2nd element of subtraction
                        subt.append((abs(self.interations[0, idx1] + self.interations[0, idx2])))
                somatorio1.append(sum(subt) / self.ppg)

            self.Grupos[i].interation = sum(somatorio1) / 2  # diveded by 2 beacause the matrix is simetric
            del somatorio1
            somatorio1 = []

    def returnGrupos(self):  # return the group modified
        return self.Grupos
