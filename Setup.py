import numpy as np
from Carro import Carro
from Cliente import Cliente


class Setup:

    def __init__(self, n_carros, ruas):
        self.ruas = ruas
        self.mapa = self.gerar_mapa()
        self.carros = [Carro(random_pos(self.mapa)) for i in range(n_carros)]
        self.comunicador = None


    def gerar_clientes(self, max_clientes):
        n_clientes = max_clientes
        # clientes = [Cliente(random_pos(self.mapa), random_pos(self.mapa)) for i in range(n_clientes)]
        self.clientes = [Cliente(random_pos(self.mapa), random_pos(self.mapa)) for i in range(n_clientes)]
        return self.clientes

    def gerar_mapa(self):
        mapa = np.ones((self.ruas[-1]+1, self.ruas[-1]+1))
        for i in self.ruas:
            mapa[i, :] = 0
            mapa[:, i] = 0
        return mapa

    def new_goal(self):
        for i in self.clientes:
            if i.need_ride == True:
                i.goal = random_pos(self.mapa)

def random_pos(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])

    while True:
        linha_aleatoria = np.random.randint(0, linhas - 1)
        coluna_aleatoria = np.random.randint(0, colunas - 1)

        if matriz[linha_aleatoria][coluna_aleatoria] == 0:
            return [linha_aleatoria, coluna_aleatoria]