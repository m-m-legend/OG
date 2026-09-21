from collections import deque
from math import inf
from Aula1 import GrafoDirecionado

# Aula 3: DFS

def DFS(G):
    d = {u: inf for u in G.V}
    f = {u: inf for u in G.V}
    cor = {u: 'W' for u in G.V}
    pi = {u: None for u in G.V}
    tempo = [0]
    for u in G.V:
        if cor[u] == 'W':
            DFS_VISIT(G,u,cor,d,f, pi,tempo)
    return cor, d, f, pi

def DFS_VISIT(G,u,cor,d,f, pi, tempo):
    tempo[0] = tempo[0] + 1
    cor[u] = 'C'
    d[u] = tempo[0]
    for v in G.E[u]:
        if cor[v] == 'W':
            pi[v] = u
            DFS_VISIT(G,v,cor,d,f, pi, tempo)
    tempo[0] = tempo[0] + 1
    cor[u] = 'P'
    f[u] = tempo[0]

K = GrafoDirecionado( # Grafo direcionado com semântica implícita de ciclos
    ["u", "v", "w", "s"],
    {
        "u": ["v", "w", "s"],
        "v": ["u"],
        "w": ["u", "s"],
        "s": ["w", "u"]
    }
)

print(DFS(K))






    