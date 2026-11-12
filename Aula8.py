from math import inf
from pprint import pprint

from Aula1 import GrafoDirecionado
from Aula7 import Bellman_Ford, Dijkstra

# Aula 8: Caminhos Mínimos entre Todos os Pares


def Floyd_Warshall(G: GrafoDirecionado, w):
    """Retorna d[u][v] e pi[u][v] para todos os pares. Tempo O(V³)."""
    d = {u: {v: inf for v in G.V} for u in G.V}
    pi = {u: {v: None for v in G.V} for u in G.V}

    for u in G.V:
        d[u][u] = 0
        for v in G.E[u] or []:
            if w[u, v] < d[u][v]:
                d[u][v] = w[u, v]
                pi[u][v] = u

    # A cada rodada, k passa a ser permitido como vértice intermediário.
    for k in G.V:
        for u in G.V:
            if d[u][k] == inf:
                continue
            for v in G.V:
                if d[k][v] == inf:
                    continue
                via_k = d[u][k] + d[k][v]
                if via_k < d[u][v]:
                    d[u][v] = via_k
                    pi[u][v] = pi[k][v]

    if any(d[u][u] < 0 for u in G.V):
        raise ValueError("O grafo contém um ciclo de peso negativo.")

    return d, pi


def Fecho_Transitivo(G: GrafoDirecionado):
    """Retorna alcanca[u][v], incluindo o caminho de comprimento zero. O(V³)."""
    A = G.matriz_adjacencia()
    alcanca = {
        u: {v: u == v or bool(A[i][j]) for j, v in enumerate(G.V)}
        for i, u in enumerate(G.V)
    }

    # Warshall usa a mesma ordem de intermediários de Floyd-Warshall.
    for k in G.V:
        for u in G.V:
            if alcanca[u][k]:
                for v in G.V:
                    alcanca[u][v] = alcanca[u][v] or alcanca[k][v]

    return alcanca


def Johnson(G: GrafoDirecionado, w):
    """Retorna d e pi como Floyd-Warshall, usando Bellman-Ford e Dijkstra."""
    # Índices permitem reservar uma superfonte e desempatar na heap da Aula 7.
    V = list(range(len(G.V)))
    indice = {u: i for i, u in enumerate(G.V)}
    E = {i: [indice[v] for v in G.E[u] or []] for i, u in enumerate(G.V)}
    pesos = {(i, j): w[G.V[i], G.V[j]] for i in V for j in E[i]}

    # A superfonte alcança todos os vértices por arestas de peso zero.
    s = len(V)
    pesos_aumentados = {**pesos, **{(s, i): 0 for i in V}}
    G_aumentado = GrafoDirecionado(V + [s], {**E, s: V}, pesos_aumentados)
    resultado = Bellman_Ford(G_aumentado, G_aumentado.w, s)
    if resultado is False:
        raise ValueError("O grafo contém um ciclo de peso negativo.")
    _, h, _ = resultado

    # Os potenciais h tornam os pesos não negativos e preservam os caminhos mínimos.
    w_novo = {(i, j): peso + h[i] - h[j] for (i, j), peso in pesos.items()}
    G_reponderado = GrafoDirecionado(V, E, w_novo)

    d = {}
    pi = {}
    for i, u in enumerate(G.V):
        d_novo, pi_novo = Dijkstra(G_reponderado, G_reponderado.w, i)
        d[u] = {}
        pi[u] = {}
        for j, v in enumerate(G.V):
            # Desfaz a reponderação nas distâncias e recupera os rótulos originais.
            d[u][v] = inf if d_novo[j] == inf else d_novo[j] - h[i] + h[j]
            pai = pi_novo[j]
            pi[u][v] = None if pai is None else G.V[pai]

    return d, pi


if __name__ == "__main__":
    # Exemplo com pesos negativos, um vértice isolado e nenhum ciclo negativo.
    G = GrafoDirecionado(
        [1, 2, 3, 4, 5, 6],
        {1: [2, 3, 5], 2: [4, 5], 3: [2], 4: [1, 3], 5: [4], 6: None},
        {
            (1, 2): 3,
            (1, 3): 8,
            (1, 5): -4,
            (2, 4): 1,
            (2, 5): 7,
            (3, 2): 4,
            (4, 1): 2,
            (4, 3): -5,
            (5, 4): 6,
        },
    )

    d_floyd, pi_floyd = Floyd_Warshall(G, G.w)
    d_johnson, _ = Johnson(G, G.w)

    print("Distâncias por Floyd-Warshall")
    pprint(d_floyd)
    print("Predecessores dos caminhos que partem do vértice 1")
    pprint(pi_floyd[1])
    print("Distâncias por Johnson")
    pprint(d_johnson)
    print("Fecho transitivo")
    pprint(Fecho_Transitivo(G))
