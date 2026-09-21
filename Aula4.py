from collections import deque
from math import inf
from Aula1 import GrafoDirecionado

# Aula 4: Ordenação Topológica e CFCs

def Ordenacao_Topologica(G):
    d = {u: inf for u in G.V}
    f = {u: inf for u in G.V}
    cor = {u: 'W' for u in G.V}
    pi = {u: None for u in G.V}
    l = []
    tempo = [0]
    for u in G.V:
        if cor[u] == 'W':
            DFS_VISIT(G,u,cor,d,f, pi,tempo,l)
    return l

def DFS_VISIT(G,u,cor,d,f, pi, tempo,l):
    tempo[0] = tempo[0] + 1
    cor[u] = 'C'
    d[u] = tempo[0]
    for v in G.E[u]:
        if cor[v] == 'W':
            pi[v] = u
            DFS_VISIT(G,v,cor,d,f, pi, tempo,l)
    tempo[0] = tempo[0] + 1
    cor[u] = 'P'
    f[u] = tempo[0]
    l.insert(0,u)

K = GrafoDirecionado( 
    ["u", "v", "w", "s"],
    {
        "u": ["v", "w", "s"],
        "v": ["u"],
        "w": ["u", "s"],
        "s": ["w", "u"]
    }
)

# Observação: CFCs em atualização futura 






    