# Werner Heisenberg: Matrix Mechanics & The Uncertainty Principle

Interactive Non-Commutative Quantum Operator Suite, Commutation Relations, Harmonic Oscillator Spectrum, and Uncertainty Relation Engine

## Theoretical Foundation

In July 1925, Werner Heisenberg published his breakthrough paper *Über quantentheoretische Umdeutung kinematischer und mechanischer Beziehungen* ("Quantum-theoretical re-interpretation of kinematic and mechanical relations"). Discarding classical, unobservable continuous electron orbital trajectories in favor of observable transition radiation frequencies and transition dipole moments, Heisenberg laid the mathematical foundation of modern quantum theory. Max Born and Pascual Jordan soon recognized Heisenberg's novel multiplication rules as the algebra of infinite matrices, proving the canonical commutation relation:

$$[X, P] \equiv XP - PX = i \hbar I$$

Because the position operator $X$ and momentum operator $P$ do not commute, they do not share a common eigenbasis. Consequently, simultaneously sharp physical measurement of both conjugate observables is impossible. In 1927, Heisenberg formulated the Uncertainty Principle, rigorously bounded by the Robertson-Schrödinger inequality:

$$\sigma_X \cdot \sigma_P \ge \frac{\hbar}{2}$$

This repository provides an interactive digital implementation of Heisenberg's quantum mechanics:
1. Exact complex matrix operator arithmetic with Hermitian transposition, trace calculation, inner products, and commutator brackets.
2. Canonical commutation verification $[X, P] = i\hbar I$ in truncated Fock state representations.
3. Quantum Harmonic Oscillator ladder operator algebra ($a$ and $a^\dagger$) yielding quantized stationary energy levels $E_n = (n + 1/2)\hbar\omega$ and non-vanishing zero-point vacuum energy.
4. Robertson-Schrödinger uncertainty bounds for Gaussian wavepacket states.
5. Interactive Web Reader and SVG phase-space visualizations.

---

## Core Mathematical Formulations

### Canonical Commutation Relation
In the energy eigenbasis $\{|n\rangle\}$ of the Quantum Harmonic Oscillator:
$$a = \begin{pmatrix} 0 & \sqrt{1} & 0 & 0 & \dots \\ 0 & 0 & \sqrt{2} & 0 & \dots \\ 0 & 0 & 0 & \sqrt{3} & \dots \\ \vdots & \vdots & \vdots & \vdots & \ddots \end{pmatrix}, \quad a^\dagger = \begin{pmatrix} 0 & 0 & 0 & \dots \\ \sqrt{1} & 0 & 0 & \dots \\ 0 & \sqrt{2} & 0 & \dots \\ 0 & 0 & \sqrt{3} & \dots \end{pmatrix}$$

The dimensionless coordinate and momentum operators are:
$$X = \sqrt{\frac{\hbar}{2m\omega}} (a + a^\dagger), \quad P = i \sqrt{\frac{\hbar m \omega}{2}} (a^\dagger - a)$$

Evaluating the commutator on the interior subspace of dimension $N$:
$$[X, P]_{jk} = (XP - PX)_{jk} = i\hbar \delta_{jk}$$

### The Harmonic Oscillator Hamiltonian
The quantum Hamiltonian is constructed without arbitrary coordinate assumptions:
$$H = \frac{P^2}{2m} + \frac{1}{2}m\omega^2 X^2 = \hbar\omega \left(a^\dagger a + \frac{1}{2}I\right)$$
Stationary state eigenvalues:
$$H |n\rangle = E_n |n\rangle = \hbar\omega \left(n + \frac{1}{2}\right) |n\rangle, \quad n \in \{0, 1, 2, \dots\}$$
Even in the ground state $|0\rangle$, quantum fluctuations preserve the zero-point energy $E_0 = \frac{1}{2}\hbar\omega$.

### Heisenberg's Uncertainty Relation
For any pair of Hermitian observables $A$ and $B$, the variance product satisfies:
$$\sigma_A^2 \sigma_B^2 \ge \left( \frac{1}{2i} \langle [A, B] \rangle \right)^2 + \left( \frac{1}{2} \langle \{A - \langle A \rangle, B - \langle B \rangle\} \rangle \right)^2$$
For canonical conjugate variables $A = X$ and $B = P$, where $[X, P] = i\hbar I$:
$$\sigma_X \sigma_P \ge \frac{\hbar}{2}$$
Equality is achieved uniquely by minimum-uncertainty Gaussian wavepackets:
$$\psi(x) = \left( \frac{1}{2\pi \sigma_x^2} \right)^{1/4} \exp\left( -\frac{x^2}{4\sigma_x^2} \right)$$

---

## Installation & Setup

Zero external dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/MATH.git
cd MATH/Heisenberg
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Usage

### Interactive Web Server
Start the local interactive reader:
```bash
python3 -m heisenberg.cli serve --port 8080
```
Open `http://localhost:8080` in any modern web browser to view the interactive matrix heatmaps, commutator tables, and uncertainty distributions.

### Static Document Export
Export the standalone publication-ready HTML edition:
```bash
python3 -m heisenberg.cli export --out heisenberg_matrix_mechanics.html
```

### Inspecting Canonical Commutators via CLI
Evaluate the $[X, P]$ operator matrix across $N$ truncated Fock states:
```bash
python3 -m heisenberg.cli commutator --dim 8
```

### Computing Oscillator Energy Eigenvalues
Calculate the diagonal spectrum of the quantized Hamiltonian:
```bash
python3 -m heisenberg.cli oscillator --dim 6
```

---

## Project Structure

```
Heisenberg/
├── heisenberg/
│   ├── __init__.py            # Library exports
│   ├── matrix_mechanics.py    # Complex matrix operators, commutators, harmonic oscillator
│   ├── visualizer.py          # SVG rendering for commutator matrices & Gaussian wavepackets
│   ├── book.py                # Publication layout and interactive HTML generator
│   └── cli.py                 # Command-line interface and HTTP server
├── tests/
│   └── test_matrix_mechanics.py # Unit test suite verifying quantum operator algebra
├── static/                    # Generated assets and diagrams
├── pyproject.toml             # Packaging configuration
├── LICENSE                    # MIT License (Jeong Hoon Kim)
└── README.md                  # Theoretical documentation and usage guide
```

---

## Verification & Precision

All numerical operations rely strictly on exact floating-point and complex arithmetic within Python's standard library. Ladder operator actions, Hermitian matrix properties, commutator invariance, and energy eigenvalue equations are verified by automated unit tests with rigorous tolerances:

```bash
python3 -m unittest discover tests -v
```

Expected output:
```
test_canonical_commutator (tests.test_matrix_mechanics.TestMatrixMechanics.test_canonical_commutator) ... ok
test_gaussian_uncertainty (tests.test_matrix_mechanics.TestMatrixMechanics.test_gaussian_uncertainty) ... ok
test_harmonic_oscillator_hamiltonian (tests.test_matrix_mechanics.TestMatrixMechanics.test_harmonic_oscillator_hamiltonian) ... ok
test_hermitian_properties (tests.test_matrix_mechanics.TestMatrixMechanics.test_hermitian_properties) ... ok
test_matrix_algebra (tests.test_matrix_mechanics.TestMatrixMechanics.test_matrix_algebra) ... ok
test_svg_generation (tests.test_matrix_mechanics.TestMatrixMechanics.test_svg_generation) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

---

## License

This software is released under the MIT License. Copyright (c) 2026 Jeong Hoon Kim.
