from Aula1 import GrafoDirecionado
from collections import deque

# Aula 2: BFS
def BFS(G: GrafoDirecionado, s):
    cor = {u:'W' for u in G.V}
    d = {u: float('inf') for u in G.V}
    pi = {u: None for u in G.V}
    cor[s], d[s] = 'G', 0
    Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in (G.E[u] or []):
            if cor[v] == 'W':
                cor[v] = 'G'
                d[v] = d[u]+1
                pi[v] = u
                Q.append(v)
        cor[u] = 'B'
    return d, pi


# Árvore binária completa de 7 vértices
G = GrafoDirecionado([0,1,2,3,4,5,6], {0: [1,2], 1: [3,4], 2: [5,6], 3: None, 4: None, 5: None, 6: None})
print(G, end="\n\n")

# BFS na Figura 20.2(a) do Cormen
F = GrafoDirecionado(
    [1,2,3,4,5,6],
    {1: [2,4],
     2: [5],
     3: [5,6],
     4: [2],
     5: [4],
     6: [6]}
)

print(BFS(F, 3), end="\n")

# Tempo da BFS com matriz de adjacência: O(V²)
# Na representação por lista de adjacência, quando um vértice u é removido da fila, a BFS percorre apenas seus vizinhos. Como cada aresta é examinada uma única vez (ou duas, em grafos não direcionados), o tempo total é O(V+E).

# Já na representação por matriz de adjacência, não existe uma lista contendo apenas os vizinhos de um vértice. Para descobrir quais vértices são adjacentes a u, é necessário percorrer toda a linha correspondente a u na matriz.

# Como:

#  - existem V vértices;
#  - para cada vértice visitado percorrem-se V posições da matriz;

# o número total de operações é V×V=V² -> O(V²)

# Eliminar distinção cinza/preto na BFS
def BFS_visited(G, s):
    visited = {v: False for v in G.V}
    d = {v: float('inf') for v in G.V}
    pi = {v: None for v in G.V}
    visited[s] = True
    d[s] = 0
    Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in G.E[u]:
            if not visited[v]:
                visited[v] = True
                d[v] = d[u] + 1
                pi[v] = u
                Q.append(v)
    return d, pi

# BFS no digrafo de fonte 3 (d, pi = BFS(W, 3))

# Dividir lutadores em faces (BFS simples)

# Diâmetro de uma árvore
def BFS_dist(G, s):
    d = {v: float('inf') for v in G.V}
    d[s] = 0
    Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in G.E[u]:
            if d[v] == float('inf'):
                d[v] = d[u] + 1
                Q.append(v)
    return d


def diametro_arvore(G):
    d1 = BFS_dist(G, G.V[0])
    u = max(d1, key=d1.get)

    d2 = BFS_dist(G, u)
    v = max(d2, key=d2.get)

    return d2[v]

# Dado que para toda árvore |E| = |V| - 1
# Complexidade: O(V)

# Explicação: ao fazer a primeira BFS a partir de qualquer vértice, encontramos uma das extremidades da árvore com a maior distância d encontrada ao fim da BFS. Depois, fazemos uma outra BFS com o vértice da extremidade da árvore e,no fim desta, vemos a distância d entre este vértice de extremidade e o vértice mais distante dele, que é, factualmente, o diâmetro da árvore (maior caminho entre quaisquer 2 vértices da árvore). 
