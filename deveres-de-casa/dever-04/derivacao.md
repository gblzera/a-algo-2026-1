# Derivação da Fórmula Fechada

## Recorrência

$$F(n) = 2F(n-1) + n^2, \quad F(1) = 2$$

---

## Passo 1: Solução Homogênea

Resolvemos a equação homogênea associada (ignorando o termo $n^2$):

$$F(n) = 2F(n-1)$$

Expandindo:

$$F(n) = 2F(n-1) = 2 \cdot 2F(n-2) = 2^2 F(n-2) = \ldots = 2^k F(n-k)$$

**Solução homogênea:**

$$F_h(n) = C \cdot 2^n$$

onde $C$ é uma constante a ser determinada.

---

## Passo 2: Solução Particular

Para o termo não-homogêneo $n^2$, chutamos uma solução particular polinomial de grau 2:

$$F_p(n) = an^2 + bn + c$$

Substituindo na recorrência original:

$$an^2 + bn + c = 2[a(n-1)^2 + b(n-1) + c] + n^2$$

Expandindo o lado direito:

$$= 2[a(n^2 - 2n + 1) + bn - b + c] + n^2$$

$$= 2an^2 - 4an + 2a + 2bn - 2b + 2c + n^2$$

$$= (2a + 1)n^2 + (-4a + 2b)n + (2a - 2b + 2c)$$

Igualando coeficientes dos dois lados:

| Termo | Esquerda | Direita | Equação |
|:-----:|:--------:|:-------:|:--------|
| $n^2$ | $a$ | $2a + 1$ | $a = 2a + 1 \Rightarrow a = -1$ |
| $n$ | $b$ | $-4a + 2b$ | $b = -4(-1) + 2b \Rightarrow b = -4$ |
| const | $c$ | $2a - 2b + 2c$ | $c = 2(-1) - 2(-4) + 2c \Rightarrow c = -6$ |

**Solução particular:**

$$F_p(n) = -n^2 - 4n - 6$$

---

## Passo 3: Solução Geral

A solução geral é a soma da homogênea com a particular:

$$F(n) = F_h(n) + F_p(n) = C \cdot 2^n - n^2 - 4n - 6$$

---

## Passo 4: Determinação da Constante

Aplicando a condição inicial $F(1) = 2$:

$$C \cdot 2^1 - 1^2 - 4(1) - 6 = 2$$

$$2C - 1 - 4 - 6 = 2$$

$$2C - 11 = 2$$

$$2C = 13$$

$$C = \frac{13}{2}$$

---

## Fórmula Fechada Final

$$\boxed{F(n) = \frac{13}{2} \cdot 2^n - n^2 - 4n - 6}$$

Simplificando:

$$F(n) = 13 \cdot 2^{n-1} - n^2 - 4n - 6$$

---

## Verificação

| $n$ | Recursão | Fórmula Fechada |
|:---:|:--------:|:---------------:|
| 1 | $2$ | $13 \cdot 1 - 1 - 4 - 6 = 2$ ✓ |
| 2 | $2(2) + 4 = 8$ | $13 \cdot 2 - 4 - 8 - 6 = 8$ ✓ |
| 3 | $2(8) + 9 = 25$ | $13 \cdot 4 - 9 - 12 - 6 = 25$ ✓ |
| 4 | $2(25) + 16 = 66$ | $13 \cdot 8 - 16 - 16 - 6 = 66$ ✓ |
| 5 | $2(66) + 25 = 157$ | $13 \cdot 16 - 25 - 20 - 6 = 157$ ✓ |

---

## Implementação em Python

```python
def F_recursive(n):
    """Versão recursiva - O(2^n)"""
    if n == 1:
        return 2
    return 2 * F_recursive(n - 1) + n * n


def F_closed(n):
    """Fórmula fechada - O(1)"""
    return 13 * (1 << (n - 1)) - n*n - 4*n - 6


n = int(input("Enter a value for n: "))
print(f"F({n}) via recursão = {F_recursive(n)}")
print(f"F({n}) via fórmula  = {F_closed(n)}")
```

---

## Complexidade

| Método | Tempo | Espaço |
|:------:|:-----:|:------:|
| Recursivo | $O(2^n)$ | $O(n)$ stack |
| Fórmula Fechada | $O(1)$ | $O(1)$ |