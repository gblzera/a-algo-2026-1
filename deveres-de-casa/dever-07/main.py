"""
Dever 07 - O Desafio do Pronto-Socorro

Tarefa: simular um sistema de triagem hospitalar.

1. Receber N pacientes com niveis de dor (1-10).
2. Usar um Max-Heap para processar os pacientes.
3. Implementar uma funcao que ajusta a prioridade de um paciente
   ja na fila (Decrease/Increase Key) e analisar o impacto na
   complexidade.
"""

# ============================================================
# ANALISE DE COMPLEXIDADE
# ============================================================
#
# Max-Heap implementado como array (indexacao 0):
#   parent(i) = (i - 1) // 2
#   left(i)   = 2 * i + 1
#   right(i)  = 2 * i + 2
#
# A propriedade do max-heap: pai >= filhos. A raiz e sempre o
# paciente com maior nivel de dor -> proximo a ser atendido.
#
# Operacoes basicas:
#   inserir(p)        -> O(log n)   (sift up apos append)
#   extrair_max()     -> O(log n)   (sift down apos trocar raiz)
#   topo()            -> O(1)
#   build_heap        -> O(n)       (heapify de baixo p/ cima)
#
# ---- Ajuste de prioridade (Increase/Decrease Key) ----
#
# Quando alteramos a "chave" (nivel de dor) de um paciente que ja
# esta na fila, a propriedade do heap pode ser violada:
#
#   - Se a dor AUMENTOU  -> pode ser maior que o pai   -> SIFT UP
#   - Se a dor DIMINUIU  -> pode ser menor que filhos  -> SIFT DOWN
#
# Ambas as operacoes percorrem no maximo a altura da arvore,
# portanto custam O(log n).
#
# Porem, para ajustar a chave, primeiro precisamos LOCALIZAR o
# paciente dentro do heap. Duas alternativas:
#
#   (a) Busca linear no array:  O(n) para localizar
#       -> Custo total da operacao: O(n) + O(log n) = O(n)
#
#   (b) Tabela hash auxiliar `pos` (id -> indice):  O(1) para localizar
#       -> Custo total da operacao: O(1) + O(log n) = O(log n)
#
# A escolha (b) e o padrao em livros como o CLRS. Mantemos `pos`
# atualizada em TODA troca (_swap), o que custa O(1) por troca e
# nao altera a complexidade assintotica das demais operacoes.
#
# CONCLUSAO: com a tabela `pos`, Increase/Decrease Key custam
# O(log n) - otimo para heaps binarios. Sem ela, degradamos para
# O(n), perdendo a principal vantagem do heap.
# ============================================================


class Paciente:
    """Paciente da triagem com id, nome e nivel de dor (1-10)."""

    def __init__(self, id, nome, dor):
        if not 1 <= dor <= 10:
            raise ValueError("Nivel de dor deve estar entre 1 e 10")
        self.id = id
        self.nome = nome
        self.dor = dor

    def __repr__(self):
        return f"Paciente(id={self.id}, nome='{self.nome}', dor={self.dor})"


class MaxHeapTriagem:
    """Max-Heap para triagem hospitalar baseada no nivel de dor."""

    def __init__(self):
        self.heap = []
        self.pos = {}  # id do paciente -> indice atual no heap

    # ---- Helpers de indice ----
    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        # Mantem a tabela `pos` consistente: O(1) por troca
        self.pos[self.heap[i].id] = j
        self.pos[self.heap[j].id] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # ---- Operacoes do heap ----
    def _sift_up(self, i):
        # Sobe enquanto o no for maior que o pai - O(log n)
        while i > 0 and self.heap[i].dor > self.heap[self._parent(i)].dor:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i):
        # Desce trocando com o maior filho - O(log n)
        n = len(self.heap)
        while True:
            l, r = self._left(i), self._right(i)
            maior = i
            if l < n and self.heap[l].dor > self.heap[maior].dor:
                maior = l
            if r < n and self.heap[r].dor > self.heap[maior].dor:
                maior = r
            if maior == i:
                break
            self._swap(i, maior)
            i = maior

    def inserir(self, paciente):
        """Insere paciente na fila - O(log n)"""
        self.heap.append(paciente)
        i = len(self.heap) - 1
        self.pos[paciente.id] = i
        self._sift_up(i)

    def extrair_max(self):
        """Remove e devolve o paciente com maior dor - O(log n)"""
        if not self.heap:
            return None
        topo = self.heap[0]
        ultimo = self.heap.pop()
        del self.pos[topo.id]
        if self.heap:
            self.heap[0] = ultimo
            self.pos[ultimo.id] = 0
            self._sift_down(0)
        return topo

    def topo(self):
        """Espia o paciente prioritario - O(1)"""
        return self.heap[0] if self.heap else None

    def atualizar_prioridade(self, id_paciente, nova_dor):
        """
        Ajusta a prioridade (chave) de um paciente ja na fila.
        Funciona como Increase Key OU Decrease Key conforme o sinal
        da variacao.

        Complexidade:
          - Localizar o paciente: O(1)   (via tabela `pos`)
          - Sift up ou sift down: O(log n)
          - Total:                O(log n)
        """
        if not 1 <= nova_dor <= 10:
            raise ValueError("Nivel de dor deve estar entre 1 e 10")
        if id_paciente not in self.pos:
            raise KeyError(f"Paciente {id_paciente} nao esta na fila")

        i = self.pos[id_paciente]
        dor_antiga = self.heap[i].dor
        self.heap[i].dor = nova_dor

        if nova_dor > dor_antiga:
            # Increase Key: pode violar a propriedade com o pai -> sobe
            self._sift_up(i)
        elif nova_dor < dor_antiga:
            # Decrease Key: pode violar a propriedade com filhos -> desce
            self._sift_down(i)
        # Se igual, nao precisa mexer

    def __len__(self):
        return len(self.heap)

    def snapshot(self):
        """Retorna a fila em ordem de array (nivel a nivel)."""
        return [(p.nome, p.dor) for p in self.heap]


# ============================================================
# DEMONSTRACAO
# ============================================================
if __name__ == "__main__":
    triagem = MaxHeapTriagem()

    pacientes = [
        Paciente(1, "Ana",     dor=3),
        Paciente(2, "Bruno",   dor=8),
        Paciente(3, "Carla",   dor=5),
        Paciente(4, "Daniel",  dor=10),
        Paciente(5, "Eduarda", dor=6),
        Paciente(6, "Fabio",   dor=2),
        Paciente(7, "Gabriel", dor=7),
    ]

    print("=" * 60)
    print("Pronto-Socorro - Sistema de Triagem (Max-Heap)")
    print("=" * 60)

    print("\nInserindo pacientes:")
    for p in pacientes:
        triagem.inserir(p)
        print(f"  + {p}")

    print(f"\nHeap (array):     {triagem.snapshot()}")
    print(f"Prioritario:      {triagem.topo()}")

    # ---- Cenario 1: Ana piorou (3 -> 9) -> Increase Key ----
    print("\n" + "-" * 60)
    print("CENARIO 1: Ana piorou. Dor 3 -> 9  (Increase Key)")
    print("-" * 60)
    triagem.atualizar_prioridade(1, 9)
    print(f"Heap apos update: {triagem.snapshot()}")
    print(f"Prioritario:      {triagem.topo()}")

    # ---- Cenario 2: Daniel melhorou (10 -> 4) -> Decrease Key ----
    print("\n" + "-" * 60)
    print("CENARIO 2: Daniel melhorou. Dor 10 -> 4  (Decrease Key)")
    print("-" * 60)
    triagem.atualizar_prioridade(4, 4)
    print(f"Heap apos update: {triagem.snapshot()}")
    print(f"Prioritario:      {triagem.topo()}")

    # ---- Atendimento por ordem de prioridade ----
    print("\n" + "-" * 60)
    print("Atendendo pacientes em ordem de dor:")
    print("-" * 60)
    ordem = 1
    while len(triagem) > 0:
        p = triagem.extrair_max()
        print(f"  {ordem}. {p}")
        ordem += 1

    # ---- Modo interativo opcional ----
    print("\n" + "=" * 60)
    resp = input("Deseja rodar o modo interativo? (s/N): ").strip().lower()
    if resp == "s":
        fila = MaxHeapTriagem()
        try:
            n = int(input("Quantos pacientes? "))
        except ValueError:
            print("Numero invalido. Encerrando.")
            raise SystemExit(0)

        for k in range(1, n + 1):
            nome = input(f"  Nome do paciente {k}: ").strip() or f"Paciente{k}"
            dor = int(input(f"  Dor de {nome} (1-10): "))
            fila.inserir(Paciente(k, nome, dor))

        print("\nComandos:")
        print("  a         -> atender (extrair max)")
        print("  u id dor  -> atualizar prioridade (id, nova dor)")
        print("  t         -> ver topo")
        print("  s         -> ver snapshot")
        print("  q         -> sair\n")

        while True:
            cmd = input("> ").strip().split()
            if not cmd:
                continue
            op = cmd[0].lower()
            if op == "q":
                break
            elif op == "a":
                p = fila.extrair_max()
                print(f"  atendido: {p}")
                if len(fila) == 0:
                    print("  fila vazia."); break
            elif op == "t":
                print(f"  topo: {fila.topo()}")
            elif op == "s":
                print(f"  snapshot: {fila.snapshot()}")
            elif op == "u" and len(cmd) == 3:
                try:
                    fila.atualizar_prioridade(int(cmd[1]), int(cmd[2]))
                    print(f"  ok. topo agora: {fila.topo()}")
                except (KeyError, ValueError) as e:
                    print(f"  erro: {e}")
            else:
                print("  comando invalido")
