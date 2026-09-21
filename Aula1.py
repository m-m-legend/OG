from collections import deque
# Aula 1: Representação de Grafos
class GrafoDirecionado:
    def __init__(self, V: list[int] | list[str], E: dict[int | str, list[int] | list[str] | None], w : dict[tuple[int | str, int | str], int]=None):
        self.V = V
        self.E = E
        self.w = w if w is not None else {}
    def soma_graus_vertices(self) -> int:
        return sum(len(self.E[v]) for v in self.V if self.E[v] is not None)
    def matriz_adjacencia(self) -> list[list[int]]:
        n = len(self.V)
        index = {v: i for i, v in enumerate(self.V)}

        matriz = [[0]*n for _ in range(n)]

        for u in self.V:
            if self.E[u] is not None:
                for v in self.E[u]:
                    matriz[index[u]][index[v]] = 1

        return matriz
    # Calcular grau de saída e entrada
    def grau_saida(self) -> dict[int, int]:
        return {
            v: len(self.E[v]) if self.E[v] is not None else 0
            for v in self.V
        }
    def grafo_quadrado(self) -> dict[int, set[int]]:
        G2 = {v: set() for v in self.V}

        for u in self.V:
            if self.E[u] is not None:
                for v in self.E[u]:
                    G2[u].add(v)          # caminho de 1 aresta

                    if self.E[v] is not None:
                        for w in self.E[v]:
                            G2[u].add(w)  # caminho de 2 arestas

        return G2
    def grau_entrada(self) -> dict[int, int]:
        entrada = {v: 0 for v in self.V}

        for u in self.V:
            if self.E[u] is not None:
                for v in self.E[u]:
                    entrada[v] += 1

        return entrada
    
    def __str__(self):
        return f"Vértices: {self.V} --- Arestas: {self.E}"

            
# Um grafo transposto é uma matriz de adjacencia transposta
def grafo_transposto(G: GrafoDirecionado) -> GrafoDirecionado:
    V = G.V
    E_t = {v: [] for v in V}

    for u in V:
        if G.E[u] is not None:
            for v in G.E[u]:
                E_t[v].append(u)

    return GrafoDirecionado(V, E_t)

class GrafoNaoDirecionado:
    def __init__(self, V: list[int] | list[str], E: dict[int | str, list[int] | list[str] | None], w : dict[tuple[int | str, int | str], int]=None):
        self.V = V
        self.E = E
        self.w = w if w is not None else {}
    def soma_graus_vertices(self) -> int:
        return sum(len(self.E[v]) for v in self.V if self.E[v] is not None)
    def matriz_adjacencia(self) -> list[list[int]]:
        n = len(self.V)
        index = {v: i for i, v in enumerate(self.V)}

        matriz = [[0]*n for _ in range(n)]

        for u in self.V:
            if self.E[u] is not None:
                for v in self.E[u]:
                    matriz[index[u]][index[v]] = 1

        return matriz
    def __str__(self):

        arestas = []

        for (u, v), peso in self.w.items():
            arestas.append(f"{u} --{peso}-- {v}")

        return f"Vértices: {self.V}\nAGM:\n" + "\n".join(arestas)







            
            



           



    
    

    
    
        