"""
Dever 08 - Bellman-Ford com tabela de iteracoes

Dado um grafo direcionado com pesos positivos e negativos:
  1. Rodar Bellman-Ford a partir de um vertice de origem.
  2. Mostrar uma tabela onde:
       - colunas = vertices
       - linhas  = iteracoes (1 .. |V|-1)
       - celula  = (distancia atual, predecessor)
  3. Detectar ciclo negativo (1 iteracao extra).

Complexidade:
  Bellman-Ford: O(V * E)
  Espaco:       O(V) para dist/pred  +  O(V*(V-1)) para a tabela
"""

INF = float("inf")


def bellman_ford(vertices, arestas, origem):
    """
    vertices: lista de rotulos (ex: ['A','B','C','D','E'])
    arestas:  lista de tuplas (u, v, peso)
    origem:   rotulo do vertice de partida

    Retorna:
      historico -> lista com |V|-1 dicionarios { v: (dist, pred) }
      ciclo_negativo -> bool
      dist_final, pred_final -> estados finais
    """
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[origem] = 0

    historico = []
    n = len(vertices)

    # |V|-1 iteracoes "oficiais"
    for _ in range(n - 1):
        atualizou = False
        for (u, v, w) in arestas:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                atualizou = True
        # Tira foto do estado APOS a iteracao
        historico.append({v: (dist[v], pred[v]) for v in vertices})
        if not atualizou:
            # Convergiu cedo - replica o snapshot ate completar |V|-1 linhas
            while len(historico) < n - 1:
                historico.append({v: (dist[v], pred[v]) for v in vertices})
            break

    # Passada extra: se ainda relaxa, existe ciclo negativo
    ciclo_negativo = False
    for (u, v, w) in arestas:
        if dist[u] != INF and dist[u] + w < dist[v]:
            ciclo_negativo = True
            break

    return historico, ciclo_negativo, dist, pred


def _fmt(valor, predecessor):
    d = "INF" if valor == INF else str(valor)
    p = str(predecessor) if predecessor is not None else "-"
    return f"{d}/{p}"


def imprimir_tabela(vertices, historico, origem):
    largura = max(10, max(len(str(v)) for v in vertices) + 6)

    print(f"\nTabela Bellman-Ford  (origem = {origem})")
    print("Formato de celula: distancia/predecessor   (INF = infinito, - = sem pred)\n")

    # Cabecalho
    header = "Iteracao".ljust(10) + "".join(str(v).center(largura) for v in vertices)
    print(header)
    print("-" * len(header))

    # Linha 0 (estado inicial)
    inicial = {v: (0 if v == origem else INF, None) for v in vertices}
    linha0 = "0".ljust(10) + "".join(
        _fmt(*inicial[v]).center(largura) for v in vertices
    )
    print(linha0)

    # Linhas 1 .. |V|-1
    for i, snap in enumerate(historico, start=1):
        linha = str(i).ljust(10) + "".join(
            _fmt(*snap[v]).center(largura) for v in vertices
        )
        print(linha)


# ============================================================
# DADOS DO GRAFO  (edite aqui quando tiver os valores reais)
# ============================================================
# Exemplo placeholder com 5 vertices e pesos +/-. Substitua pelas
# arestas do enunciado.

if __name__ == "__main__":
    # Grafo do enunciado: 5 vertices {0,1,2,3,4}
    vertices = [0, 1, 2, 3, 4]
    arestas = [
        (0, 1,  5),
        (1, 2,  1),
        (1, 3,  2),
        (3, 4, -1),
        (2, 4,  1),
    ]
    origem = 0

    historico, ciclo_neg, dist, pred = bellman_ford(vertices, arestas, origem)

    imprimir_tabela(vertices, historico, origem)

    print("\nResultado final:")
    for v in vertices:
        d = "INF" if dist[v] == INF else dist[v]
        print(f"  dist[{v}] = {d:>4}   pred[{v}] = {pred[v]}")

    print("\nCiclo negativo alcancavel a partir da origem? ", end="")
    print("SIM" if ciclo_neg else "NAO")
