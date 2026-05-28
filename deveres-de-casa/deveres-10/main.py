"""
Dever 10 - Rede de Fibra Optica  (Algoritmo de Prim - MST)

6 polos tecnologicos (A, B, C, D, E, F) precisam ser interligados.
O cabo e cobrado por km e o objetivo e conectar todos com o MENOR
custo possivel - problema classico de Arvore Geradora Minima (MST).

Grafo nao-direcionado:
  A-B: 4   A-C: 4
  B-C: 2   B-D: 5
  C-D: 5   C-E: 6
  D-E: 3   D-F: 4
  E-F: 2

Saida esperada:
  - ordem de instalacao dos cabos (arestas escolhidas)
  - quilometragem minima total

Complexidade:
  Prim com heap binario: O(E * log V)
  Espaco:                O(V + E)
"""

import heapq


def prim(vertices, adj, inicio):
    """
    vertices: lista de rotulos (ex: ['A','B','C','D','E','F'])
    adj:      dict { u: [(v, peso), ...] }  (cada aresta nos DOIS sentidos)
    inicio:   vertice de partida

    Retorna:
      mst         -> lista [(u, v, peso)] na ordem em que foram escolhidas
      custo_total -> soma dos pesos
    """
    visitados = {inicio}
    mst = []
    custo_total = 0

    # Heap de candidatas: (peso, origem_na_arvore, destino_fora)
    heap = []
    for (v, w) in adj[inicio]:
        heapq.heappush(heap, (w, inicio, v))

    while heap and len(visitados) < len(vertices):
        peso, u, v = heapq.heappop(heap)
        if v in visitados:
            continue  # ja entrou pela arvore por outro caminho

        visitados.add(v)
        mst.append((u, v, peso))
        custo_total += peso

        # Adiciona arestas do recem-incluido `v` que vao para fora da arvore
        for (viz, w) in adj[v]:
            if viz not in visitados:
                heapq.heappush(heap, (w, v, viz))

    return mst, custo_total


# ============================================================
# DADOS DO ENUNCIADO
# ============================================================
if __name__ == "__main__":
    vertices = ["A", "B", "C", "D", "E", "F"]
    arestas = [
        ("A", "B", 4),
        ("A", "C", 4),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 5),
        ("C", "E", 6),
        ("D", "E", 3),
        ("D", "F", 4),
        ("E", "F", 2),
    ]

    # Adjacencia nao-direcionada
    adj = {v: [] for v in vertices}
    for u, v, w in arestas:
        adj[u].append((v, w))
        adj[v].append((u, w))

    inicio = "A"
    mst, custo = prim(vertices, adj, inicio)

    print("=" * 60)
    print("Dever 10 - Rede de Fibra Optica  (Prim - MST)")
    print("=" * 60)

    print(f"\nIniciando em: {inicio}")
    print(f"Cabos instalados (ordem da escolha pelo algoritmo):\n")
    for i, (u, v, w) in enumerate(mst, start=1):
        print(f"  {i}. {u} <-> {v}   ({w} km)")

    print(f"\nQuilometragem total minima: {custo} km")
    print(f"Numero de cabos instalados: {len(mst)}   (esperado: |V|-1 = {len(vertices)-1})")
