# Georg Cantor: Transfinite Set Theory (Mengenlehre)

Interactive Mathematical Diagonalization Suite & Transfinite Cardinality Engine

## Theoretical Foundation

In 1874 and 1891, Georg Cantor revolutionized the foundations of mathematics by demonstrating that actual infinity is not a monolithic concept, but comprises a rich, well-ordered hierarchy of distinct transfinite cardinalities. Cantor proved that while rational numbers and integers share the same countable cardinality ($\aleph_0$), the continuum of real numbers $\mathbb{R}$ possesses a strictly higher uncountability ($2^{\aleph_0} = \mathfrak{c}$).

This repository provides an interactive mathematical engine implementing Cantor's core foundational breakthroughs:
1. Cantor's Diagonal Argument (1891): Constructs anti-diagonal witness reals proving $|\mathbb{R}| > |\mathbb{N}|$.
2. Cantor's Polynomial Pairing Function: Bijection between $\mathbb{N} \times \mathbb{N}$ and $\mathbb{N}$, demonstrating countability of products and rationals.
3. Cantor's Theorem on Power Sets: Proves that for every set $S$, $|S| < |\mathcal{P}(S)|$ by constructing the unmapped diagonal witness subset $D = \{x \in S : x \notin f(x)\}$.
4. The Cantor Ternary Set: Fractal continuum with Lebesgue measure tending to zero while retaining uncountably infinite cardinality $\mathfrak{c}$.
5. Interactive Web Reader and printable document layout.

---

## Core Mathematical Formulations

### Cantor's Pairing Bijection
Maps any pair of non-negative integers $(k_1, k_2)$ uniquely to an integer:
$$\pi(k_1, k_2) = \frac{1}{2}(k_1 + k_2)(k_1 + k_2 + 1) + k_2$$
The inverse mapping $\pi^{-1}(z) = (k_1, k_2)$ is uniquely recovered via:
$$w = \left\lfloor \frac{\sqrt{8z + 1} - 1}{2} \right\rfloor, \quad t = \frac{w(w + 1)}{2}, \quad k_2 = z - t, \quad k_1 = w - k_2$$

### The Diagonal Argument
Given an enumerable listing of infinite sequences $s_1, s_2, s_3, \dots \in \{0, 1\}^\mathbb{N}$:
Cantor defines the sequence $d$ where $d_n = 1 - s_{n, n}$. Because $d$ differs from sequence $s_k$ at the $k$-th position for every $k \in \mathbb{N}$, $d$ cannot appear anywhere in the enumerated list. Hence, the continuum cannot be placed in one-to-one correspondence with natural numbers.

### The Cantor Ternary Set $\mathcal{C}$
Starting from $C_0 = [0, 1]$, each stage removes the open middle third of every constituent interval:
* Step $k$ contains $2^k$ closed intervals of length $3^{-k}$.
* Total Lebesgue measure: $\lambda(C_k) = \left(\frac{2}{3}\right)^k \to 0$ as $k \to \infty$.
* Hausdorff dimension: $\dim_H(\mathcal{C}) = \frac{\ln 2}{\ln 3} \approx 0.6309$.
* Points in $\mathcal{C}$ correspond to ternary expansions containing only $0$ and $2$, establishing an injection to $\{0, 1\}^\mathbb{N}$ and proving $|\mathcal{C}| = \mathfrak{c}$.

---

## Installation & Setup

Zero third-party dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/MATH.git
cd MATH/Cantor
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Command Line Usage

### Launch Interactive Reader
```bash
python3 -m cantor.cli serve --port 8081
```
Open `http://localhost:8081` in any web browser.

### Diagonal Witness Construction
```bash
python3 -m cantor.cli diagonalize 10110 01001 11010 00101 10011
```

### Cantor Pairing Demonstration
```bash
python3 -m cantor.cli pairing 7 13
```

### Cantor Set Iteration Metrics
```bash
python3 -m cantor.cli cantor-set --depth 6
```

### Export Standalone Book
```bash
python3 -m cantor.cli export -o cantor_set_theory.html
```

---

## Python API Reference

```python
from cantor.set_theory import CantorPairing, Diagonalization, CantorTernarySet, PowerSetTheorem

# Pairing bijection
z = CantorPairing.pair(5, 12)
k1, k2 = CantorPairing.unpair(z)
assert (k1, k2) == (5, 12)

# Diagonalization
witness = Diagonalization.diagonalize_binary(["001", "110", "101"])
print(f"Anti-diagonal witness: {witness}")

# Cantor Set stages
stages = CantorTernarySet.generate_stages(depth=4)
print(f"Measure at depth 4: {CantorTernarySet.total_measure(stages[4])}")
```

---

## Verification & Integrity

The test suite validates:
* Exact roundtrip invertibility of Cantor's polynomial pairing bijection across integer grids.
* Anti-diagonal divergence property ($d_i \ne s_{i, i}$).
* Lebesgue measure decay of the Cantor ternary set matching $(2/3)^k$.
* Diagonal witness construction for arbitrary power set mappings.

Run verification:
```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License. Copyright (c) 2026 Jeong Hoon Kim.
