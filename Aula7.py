from math import inf
import heapq
from Aula1 import GrafoDirecionado
from Aula4 import Ordenacao_Topologica
# Aula 7: Caminhos Mínimos de Fonte Única

K = GrafoDirecionado( 
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
        ("w","u"):  -2,
        ("w", "s"): 1,
        ("v","u"):  6,
        ("s","w"):  -1,
        ("s","u"):  7
    }
)

A = GrafoDirecionado( 
    ["u", "v", "w", "s", "r"],
    {
        "u": ["s"],
        "v": [],
        "w": ["s"],
        "s": ["r"],
        "r": ["v"]
    },
    {
        ("u","s"): 4,
        ("w","s"): 5,
        ("s","r"): 1,
        ("r", "v"): -1
    }
)

P = GrafoDirecionado( 
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
        ("w","u"):  2,
        ("w", "s"): 1,
        ("v","u"):  6,
        ("s","w"):  1,
        ("s","u"):  7
    }
)

def Initialize_Single_Source(G, s: int | str):
    pi = {v: None for v in G.V} # Predecessores
    d = {v: inf for v in G.V} # Estimativa de caminho mínimo
    d[s] = 0
    return d, pi

def Relax(u,v,w,d,pi): # Relaxação
    if d[v] > d[u] + w[(u,v)]:
        d[v] = d[u] + w[(u,v)]
        pi[v] = u
        return True
    return False

def Bellman_Ford(G: GrafoDirecionado,w,s): # Geral, O(V² + VE) e tipicamente O(VE)
    d, pi = Initialize_Single_Source(G,s)
    for i in range(1,len(G.V)):
        for u in G.V:
            for v in G.E[u]:
                Relax(u,v,w,d,pi)
    for u in G.V:
        for v in G.E[u]:
            if d[v] > d[u] + w[(u,v)]:
                return False
    return True, d, pi

def Dag_Caminhos_Minimos(G,w,s): # Grafos Direcionados Acíclicos, O(V + E)
    l = Ordenacao_Topologica(G)
    d, pi = Initialize_Single_Source(G,s)
    for u in l:
        for v in G.E[u]:
            Relax(u,v,w,d,pi)
    return d, pi

def Decrease_Key(Q, d, v):
    heapq.heappush(Q, (d[v], v))


def Dijkstra(G, w, s):  # Pesos não negativos, O(E log V)
    d, pi = Initialize_Single_Source(G, s)
    S = set()
    Q = []
    for u in G.V:
        heapq.heappush(Q, (d[u], u))
    while Q:
        du, u = heapq.heappop(Q)
        # Ignora entrada antiga da heap, mantendo a complexidade em O(E log V)
        if du != d[u]:
            continue
        if u in S:
            continue
        S.add(u)
        for v in G.E[u]:
            if v in S:
                continue
            diminuiu = Relax(u, v, w, d, pi)
            if diminuiu:
                Decrease_Key(Q, d, v)

    return d, pi


    

if __name__ == "__main__":
    print(Bellman_Ford(K,K.w,"u"))
    print(Dag_Caminhos_Minimos(A,A.w,"u"))
    print(Dijkstra(P,P.w,"u"))







