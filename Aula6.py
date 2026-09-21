import heapq
from math import inf

from Aula1 import GrafoNaoDirecionado
# Aula 6: Prim e Kruskal

# Prim

def Decrease_Key(Q, key, vertice, nova_chave):

    if nova_chave >= key[vertice]:
        return

    key[vertice] = nova_chave
    heapq.heappush(Q, (nova_chave, vertice))


def Peso_Aresta(w, u, v):

    if (u, v) in w:
        return w[(u, v)]

    return w[(v, u)]


def Prim(G: GrafoNaoDirecionado, w: dict[tuple[int | str, int | str], int], r: int | str):
    key = {u: inf for u in G.V}
    pi = {u: None for u in G.V}
    key[r] = 0
    Q = []
    for u in G.V:
        heapq.heappush(Q, (key[u], u))
    visitados = set()
    while Q:
        chave_u, u = heapq.heappop(Q)

        # Entrada antiga da heap
        if chave_u != key[u]:
            continue
        # 
        if u in visitados:
            continue

        visitados.add(u)

        for v in G.E[u]:

            if v in visitados:
                continue

            peso = Peso_Aresta(w, u, v)

            if peso < key[v]:

                pi[v] = u

                Decrease_Key(Q, key, v, peso)

     # Construção da AGM
    E_AGM = {u: [] for u in G.V}
    w_AGM = {}

    for v in G.V:
        if pi[v] is not None:
            u = pi[v]

            E_AGM[u].append(v)
            E_AGM[v].append(u)

            w_AGM[(u, v)] = w[(u, v)] if (u, v) in w else w[(v, u)]

    return GrafoNaoDirecionado(G.V, E_AGM, w_AGM), key, pi

# Kruskal

def Make_Set(V):

    pai = {}
    rank = {}

    for v in V:
        pai[v] = v
        rank[v] = 0

    return pai, rank


def Find(pai, v):

    if pai[v] != v:
        pai[v] = Find(pai, pai[v])

    return pai[v]


def Union(pai, rank, u, v):

    raiz_u = Find(pai, u)
    raiz_v = Find(pai, v)

    if raiz_u == raiz_v:
        return False

    if rank[raiz_u] < rank[raiz_v]:
        pai[raiz_u] = raiz_v

    elif rank[raiz_u] > rank[raiz_v]:
        pai[raiz_v] = raiz_u

    else:
        pai[raiz_v] = raiz_u
        rank[raiz_u] += 1

    return True

def Kruskal(G: GrafoNaoDirecionado, w: dict[tuple[int | str, int | str], int]):

    # Cria uma lista de arestas sem duplicação
    arestas = []

    for (u, v), peso in w.items():
        arestas.append((peso, u, v))

    # Ordena as arestas pelo peso
    arestas.sort()

    # Cada vértice começa em um conjunto separado
    pai, rank = Make_Set(G.V)

    # Estrutura da AGM
    E_AGM = {u: [] for u in G.V}
    w_AGM = {}

    for peso, u, v in arestas:

        # Só adiciona a aresta se ela não criar ciclo
        if Union(pai, rank, u, v):

            E_AGM[u].append(v)
            E_AGM[v].append(u)

            w_AGM[(u, v)] = peso

    return GrafoNaoDirecionado(G.V, E_AGM, w_AGM)

G = GrafoNaoDirecionado( # Grafo não direcionado em que quando se tem (u,v), se tem também (v,u)
    ["u", "v", "w", "s"],
    {
        "u": ["v", "w", "s"],
        "v": ["u"],
        "w": ["u", "s"],
        "s": ["w", "u"]
    },
    {
        ("u", "v"): 4,
        ("u", "w"): 2,
        ("u", "s"): 5,
        ("w", "s"): 1
    }
)

AGM_Prim, key, pi = Prim(G, G.w, "u")
print(AGM_Prim)
print(key)
print(pi)

AGM_Kruskal = Kruskal(G, G.w)
print(AGM_Kruskal)