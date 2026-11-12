from collections import deque
from math import inf

from Aula1 import GrafoDirecionado

# Aulas 9 e 10: Fluxo Máximo


def _DFS_Residual(residual, s, t):
    pi = {}
    pilha = [(None, s)]

    while pilha:
        pai, u = pilha.pop()
        if u in pi:
            continue
        pi[u] = pai
        if u == t:
            break

        # A pilha percorre primeiro o vizinho inserido primeiro no grafo residual.
        for v in reversed(residual[u]):
            if residual[u][v] > 0 and v not in pi:
                pilha.append((u, v))

    return pi


def _BFS_Residual(residual, s, t):
    pi = {s: None}
    Q = deque([s])

    while Q:
        u = Q.popleft()
        for v, capacidade in residual[u].items():
            if capacidade > 0 and v not in pi:
                pi[v] = u
                if v == t:
                    return pi
                Q.append(v)

    return pi


def _Fluxo_Maximo(G, c, s, t, busca):
    if s not in G.V or t not in G.V or s == t:
        raise ValueError("A fonte e o sorvedouro devem ser vértices distintos do grafo.")

    fluxo = {}
    residual = {u: {} for u in G.V}
    for u in G.V:
        for v in G.E[u] or []:
            capacidade = c[u, v]
            if not 0 <= capacidade < inf:
                raise ValueError(f"A capacidade de {(u, v)} deve ser finita e não negativa.")
            fluxo[u, v] = 0
            residual[u][v] = capacidade

    # Reserva a aresta reversa sem sobrescrever uma capacidade original.
    for u, v in fluxo:
        residual[v].setdefault(u, 0)

    valor = 0
    while True:
        pi = busca(residual, s, t)
        if t not in pi:
            return valor, fluxo

        # O gargalo é a menor capacidade residual no caminho de s a t.
        aumento = inf
        v = t
        while v != s:
            u = pi[v]
            aumento = min(aumento, residual[u][v])
            v = u

        v = t
        while v != s:
            u = pi[v]
            # A capacidade residual soma a folga em u -> v e o fluxo em v -> u.
            # Primeiro cancela o fluxo contrário e depois usa a folga restante.
            cancelado = min(aumento, fluxo.get((v, u), 0))
            if cancelado > 0:
                fluxo[v, u] -= cancelado
            if aumento > cancelado:
                fluxo[u, v] += aumento - cancelado

            residual[u][v] -= aumento
            residual[v][u] += aumento
            v = u

        valor += aumento


def Ford_Fulkerson(G: GrafoDirecionado, c, s, t):
    """Retorna (valor, fluxo por aresta) usando DFS. Com capacidades inteiras, O(E |f*|)."""
    return _Fluxo_Maximo(G, c, s, t, _DFS_Residual)


def Edmonds_Karp(G: GrafoDirecionado, c, s, t):
    """Retorna (valor, fluxo por aresta) usando BFS no residual. Tempo O(VE²)."""
    return _Fluxo_Maximo(G, c, s, t, _BFS_Residual)


if __name__ == "__main__":
    # No exemplo, w representa as capacidades das arestas.
    G = GrafoDirecionado(
        ["s", "a", "b", "t"],
        {"s": ["a", "b"], "a": ["b", "t"], "b": ["t"], "t": None},
        {("s", "a"): 1, ("s", "b"): 1, ("a", "b"): 1, ("a", "t"): 1, ("b", "t"): 1},
    )

    # DFS escolhe s -> a -> b -> t e depois s -> b -> a -> t, cancelando a -> b.
    print("Ford-Fulkerson", Ford_Fulkerson(G, G.w, "s", "t"))
    # BFS escolhe s -> a -> t e s -> b -> t. O valor máximo também é 2.
    print("Edmonds-Karp", Edmonds_Karp(G, G.w, "s", "t"))
