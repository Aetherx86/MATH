# David Hilbert: Grundlagen der Geometrie & Functional Analysis

Interactive Axiomatic Geometry Suite, Hilbert Space Engine, and 23 Problems Explorer

## Theoretical Foundation

David Hilbert was one of the most influential mathematicians of the late 19th and early 20th centuries. In 1899, Hilbert published *Grundlagen der Geometrie* (Foundations of Geometry), providing the first fully rigorous formal axiomatization of Euclidean geometry that eliminated all unstated intuitive assumptions and demonstrated the logical independence of geometric axioms. Hilbert subsequently pioneered functional analysis, introducing infinite-dimensional complete inner product spaces (Hilbert spaces $L^2$ and $\ell^2$) that laid the mathematical foundations for quantum mechanics.

This repository provides an interactive mathematical suite implementing Hilbert's foundational contributions:
1. Grundlagen der Geometrie (1899): Complete formalization of Hilbert's 5 Axiom Groups (Incidence, Order/Betweenness, Congruence, Parallels, Continuity).
2. Projective & Synthetic Theorems: Verification of Pasch's Axiom and Desargues's Theorem.
3. Hilbert Space Engine: Vector operations in inner product spaces, verification of the Cauchy-Schwarz inequality, Parallelogram Law, and Gram-Schmidt orthonormalization.
4. The 23 Mathematical Problems (Paris 1900): Categorized database and solution tracking across modern mathematics.
5. Interactive Web Reader and print-ready document layout.

---

## The Five Axiom Groups of Geometry

1. **Group I: Axioms of Incidence (Verknüpfung):** Connects points, lines, and planes (e.g., two distinct points uniquely determine a straight line).
2. **Group II: Axioms of Order (Anordnung):** Establishes the betweenness relation and includes Pasch's Axiom (a line entering a triangle through one edge must exit through another).
3. **Group III: Axioms of Congruence (Kongruenz):** Defines congruence of segments and angles without relying on rigid body movement.
4. **Group IV: Axiom of Parallels (Parallelenaxiom):** Reformulates the Euclidean parallel postulate into a transparent uniqueness condition.
5. **Group V: Axioms of Continuity (Stetigkeit):** The Axiom of Archimedes and the Axiom of Line Completeness (Vollständigkeit).

---

## Hilbert Space & Functional Analysis

A Hilbert space $\mathcal{H}$ is an inner product space that is complete under the metric induced by its inner product:
$$\langle x, y \rangle = \sum_{i=1}^\infty x_i y_i, \quad \|x\| = \sqrt{\langle x, x \rangle}$$

### Fundamental Theorems Verified:
* **Cauchy-Schwarz Inequality:**
  $$|\langle x, y \rangle| \le \|x\| \cdot \|y\|$$
* **Parallelogram Law (Characterizing Hilbert Spaces among Banach Spaces):**
  $$\|x + y\|^2 + \|x - y\|^2 = 2(\|x\|^2 + \|y\|^2)$$
* **Gram-Schmidt Orthonormalization:**
  $$u_k = v_k - \sum_{j=1}^{k-1} \langle v_k, e_j \rangle e_j, \quad e_k = \frac{u_k}{\|u_k\|}$$

---

## Installation & Setup

Zero third-party dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/Hilbert.git
cd Hilbert
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Command Line Usage

### Launch Interactive Reader
```bash
python3 -m hilbert.cli serve --port 8082
```
Open `http://localhost:8082` in any web browser.

### Run Gram-Schmidt Orthonormalization
```bash
python3 -m hilbert.cli ortho
```

### Display 23 Mathematical Problems
```bash
python3 -m hilbert.cli problems
```

### Export Standalone Book (HTML / PDF)
```bash
python3 -m hilbert.cli export -o hilbert_grundlagen.html
```

---

## Python API Reference

```python
from hilbert.foundations import HilbertVector, HilbertSpaceEngine

v1 = HilbertVector([1.0, 1.0, 0.0])
v2 = HilbertVector([1.0, 0.0, 1.0])

# Verify Cauchy-Schwarz inequality
valid, ip, bound = HilbertSpaceEngine.verify_cauchy_schwarz(v1, v2)
print(f"Cauchy-Schwarz holds: {valid} (|{ip}| <= {bound})")

# Verify Parallelogram Law
valid_pl, lhs, rhs = HilbertSpaceEngine.verify_parallelogram_law(v1, v2)
print(f"Parallelogram law holds: {valid_pl} ({lhs} == {rhs})")

# Gram-Schmidt
ortho = HilbertSpaceEngine.gram_schmidt([v1, v2])
print(f"Orthogonal inner product: {ortho[0].inner_product(ortho[1]):.2e}")
```

---

## Verification & Integrity

The test suite validates:
* Exact satisfaction of the Cauchy-Schwarz inequality and Parallelogram Law.
* Mutual orthogonality and unit normalization in Gram-Schmidt procedures.
* Structural completeness of the 5 Axiom Groups and Hilbert Problems registry.
* Vector diagram rendering and HTML book compilation.

Run verification:
```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License. Copyright (c) 2026 Jeong Hoon Kim.
