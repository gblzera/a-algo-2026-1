"""
Dever 09 - Algoritmo de Dijkstra

Grafo direcionado com pesos positivos:
  (0,1) = 4
  (0,2) = 1
  (2,1) = 2
  (1,3) = 1
  (2,4) = 5
  (3,4) = 1

Tarefa: rodar Dijkstra a partir do no 0 e encontrar o caminho minimo
ate o no 4. Entregar:
  - tabela com a evolucao das distancias a cada no visitado
  - caminho final percorrido
  - custo minimo total

Complexidade:
  Com heap binario: O((V + E) * log V)
  Espaco:           O(V)
"""

import heapq

INF = float("inf")


def dijkstra(vertices, adj, origem):
    """
    vertices: lista de vertices
    adj:      dict { u: [(v, peso), ...] }  (lista de adjacencia)
    origem:   vertice de partida

    Retorna:
      dist, pred -> estados finais
      historico -> lista de snapshots apos cada extracao (no visitado)
                   cada snapshot: (no_extraido, dict {v: (dist, pred)})
    """
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[origem] = 0

    visitados = set()
    heap = [(0, origem)]
    historico = []

    while heap:
        d, u = heapq.heappop(heap)
        if u in visitados:
            continue
        visitados.add(u)

        # Relaxa arestas de u
        for (v, w) in adj.get(u, []):
            if v in visitados:
                continue
            if d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(heap, (dist[v], v))

        # Foto do estado apos visitar `u`
        snapshot = {v: (dist[v], pred[v]) for v in vertices}
        historico.append((u, snapshot))

    return dist, pred, historico


def reconstruir_caminho(pred, origem, destino):
    """Retrocede pelos predecessores para montar o caminho."""
    if pred[destino] is None and destino != origem:
        return None
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pred[atual]
    caminho.reverse()
    return caminho


def _fmt(valor, predecessor):
    d = "INF" if valor == INF else str(valor)
    p = str(predecessor) if predecessor is not None else "-"
    return f"{d}/{p}"


def imprimir_tabela(vertices, historico, origem):
    largura = max(10, max(len(str(v)) for v in vertices) + 6)

    print(f"\nTabela Dijkstra  (origem = {origem})")
    print("Formato de celula: distancia/predecessor   (INF = infinito, - = sem pred)\n")

    header = "Passo".ljust(8) + "Visita".ljust(10) + \
             "".join(str(v).center(largura) for v in vertices)
    print(header)
    print("-" * len(header))

    # Estado inicial (passo 0)
    inicial = {v: (0 if v == origem else INF, None) for v in vertices}
    linha0 = "0".ljust(8) + "-".ljust(10) + \
             "".join(_fmt(*inicial[v]).center(largura) for v in vertices)
    print(linha0)

    for i, (no, snap) in enumerate(historico, start=1):
        linha = str(i).ljust(8) + str(no).ljust(10) + \
                "".join(_fmt(*snap[v]).center(largura) for v in vertices)
        print(linha)


# ============================================================
# DADOS DO ENUNCIADO
# ============================================================
if __name__ == "__main__":
    vertices = [0, 1, 2, 3, 4]
    arestas = [
        (0, 1, 4),
        (0, 2, 1),
        (2, 1, 2),
        (1, 3, 1),
        (2, 4, 5),
        (3, 4, 1),
    ]

    # Monta lista de adjacencia (grafo direcionado)
    adj = {v: [] for v in vertices}
    for u, v, w in arestas:
        adj[u].append((v, w))

    origem, destino = 0, 4

    dist, pred, historico = dijkstra(vertices, adj, origem)

    print("=" * 60)
    print("Dever 09 - Dijkstra")
    print("=" * 60)

    imprimir_tabela(vertices, historico, origem)

    print("\nResultado final:")
    for v in vertices:
        d = "INF" if dist[v] == INF else dist[v]
        print(f"  dist[{v}] = {d}   pred[{v}] = {pred[v]}")

    caminho = reconstruir_caminho(pred, origem, destino)
    if caminho is None:
        print(f"\nNao existe caminho de {origem} ate {destino}.")
    else:
        rota = " -> ".join(str(x) for x in caminho)
        print(f"\nCaminho minimo {origem} -> {destino}: {rota}")
        print(f"Custo minimo total: {dist[destino]}")
