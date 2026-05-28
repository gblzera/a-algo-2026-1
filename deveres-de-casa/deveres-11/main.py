"""
Dever 11 - O Desafio da Arvore Geradora MAXIMA

Modificacao do Prim do deveres-10: em vez do "caminho mais barato sem
ciclos" (MST minima), queremos o "caminho mais CARO sem ciclos"
(MST maxima).

Truque da modificacao:
  heapq do Python e um min-heap. Para extrair sempre a aresta de MAIOR
  peso, basta empilhar (-peso). O parametro `modo` deixa o codigo
  servir nos dois casos.

Mesmo grafo do deveres-10:
  A-B: 4   A-C: 4
  B-C: 2   B-D: 5
  C-D: 5   C-E: 6
  D-E: 3   D-F: 4
  E-F: 2

Complexidade:
  Identica ao Prim original: O(E * log V).
  A negacao do peso e O(1) por insercao, nao altera a complexidade.
"""

import heapq


def prim(vertices, adj, inicio, modo="min"):
    """
    modo:
      'min' -> Arvore Geradora MINIMA (custo total minimo)
      'max' -> Arvore Geradora MAXIMA (custo total maximo)

    Implementacao: heapq e min-heap. Para 'max', negamos o peso na
    chave do heap; o peso original continua sendo armazenado.
    """
    sinal = 1 if modo == "min" else -1

    visitados = {inicio}
    mst = []
    custo_total = 0
    heap = []

    for (v, w) in adj[inicio]:
        heapq.heappush(heap, (sinal * w, w, inicio, v))

    while heap and len(visitados) < len(vertices):
        _, peso, u, v = heapq.heappop(heap)
        if v in visitados:
            continue

        visitados.add(v)
        mst.append((u, v, peso))
        custo_total += peso

        for (viz, w) in adj[v]:
            if viz not in visitados:
                heapq.heappush(heap, (sinal * w, w, v, viz))

    return mst, custo_total


# ============================================================
# DADOS DO ENUNCIADO  (mesmo grafo do dever 10)
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

    adj = {v: [] for v in vertices}
    for u, v, w in arestas:
        adj[u].append((v, w))
        adj[v].append((u, w))

    inicio = "A"

    print("=" * 60)
    print("Dever 11 - Arvore Geradora MAXIMA")
    print("=" * 60)

    # Comparacao lado a lado
    for modo, titulo in [("min", "MST MINIMA (custo mais barato)"),
                         ("max", "MST MAXIMA (custo mais caro)")]:
        mst, custo = prim(vertices, adj, inicio, modo=modo)
        print(f"\n--- {titulo} ---")
        for i, (u, v, w) in enumerate(mst, start=1):
            print(f"  {i}. {u} <-> {v}   ({w} km)")
        print(f"  Total: {custo} km")

    # Resposta principal do dever 11:
    mst_max, custo_max = prim(vertices, adj, inicio, modo="max")
    print("\n" + "=" * 60)
    print("RESPOSTA DEVER 11")
    print("=" * 60)
    print("Arestas escolhidas para a Arvore Geradora MAXIMA:")
    for i, (u, v, w) in enumerate(mst_max, start=1):
        print(f"  {i}. {u} <-> {v}   ({w} km)")
    print(f"\nCusto total maximo (sem ciclos): {custo_max} km")
