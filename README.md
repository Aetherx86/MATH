# MATH: Unified Mathematical Foundations & Visual Computing Suite

A unified monorepo bringing together the monumental works of mathematical giants—Euclid, Newton, Cantor, Hilbert, Einstein, and Heisenberg—alongside an advanced computational mathematical animation engine.

Every sub-directory contains an interactive readable digital edition, rigorous formal proof engines, vector visualizations, unit test suites, and publication-ready PDF exports.

## Repository Directory

| Sub-Directory | Theoretical Focus & Foundations | Interactive Book & Proof CLI | Key Test Suite |
| :--- | :--- | :--- | :--- |
| **[`Euclid/`](./Euclid)** | Axiomatic planar geometry, Euclidean algorithm, infinite primes proof, Pythagorean theorem | `python3 -m Euclid.euclid.cli serve` | `tests/test_proofs.py` |
| **[`Newton/`](./Newton)** | Foundations of differential calculus, fluxions, gravitational mechanics, Kepler orbits | `python3 -m Newton.newton.cli serve` | `tests/test_mechanics.py` |
| **[`Cantor/`](./Cantor)** | Transfinite set theory, Cantor diagonal argument, cardinality hierarchy ($\aleph_0 < 2^{\aleph_0}$) | `python3 -m Cantor.cantor.cli serve` | `tests/test_set_theory.py` |
| **[`Hilbert/`](./Hilbert)** | Axiomatic geometry, infinite-dimensional Hilbert space, spectral decomposition | `python3 -m Hilbert.hilbert.cli serve` | `tests/test_foundations.py` |
| **[`Einstein/`](./Einstein)** | Differential geometry, Riemannian curvature tensors, geodesic variation | `python3 -m Einstein.einstein.cli serve` | `tests/test_relativity.py` |
| **[`Heisenberg/`](./Heisenberg)** | Non-commutative operator algebras, matrix mechanics, commutator brackets $[X, P] = i\hbar$ | `python3 -m Heisenberg.heisenberg.cli serve` | `tests/test_matrix_mechanics.py` |
| **[`math-video-engine/`](./math-video-engine)**| Standalone mathematical animation and video synthesis engine (Fourier, linear algebra, Goldbach) | `python3 -m math_video_engine.cli --help` | `tests/test_scenes.py` |

## Quick Start & Verification

### Cloning the Repository

```bash
git clone https://gitlab.com/jk9576/MATH.git
cd MATH
```

### Running All Unit Test Suites

Each mathematical proof module can be tested directly:

```bash
# Euclid
cd Euclid && python3 -W error -m unittest discover tests && cd ..

# Newton
cd Newton && python3 -W error -m unittest discover tests && cd ..

# Cantor
cd Cantor && python3 -W error -m unittest discover tests && cd ..

# Hilbert
cd Hilbert && python3 -W error -m unittest discover tests && cd ..

# Einstein
cd Einstein && python3 -W error -m unittest discover tests && cd ..

# Heisenberg
cd Heisenberg && python3 -W error -m unittest discover tests && cd ..

# Math Video Engine
cd math-video-engine && python3 -m unittest discover tests && cd ..
```

### Launching Interactive Books Locally

Each interactive digital edition features embedded KaTeX rendering, responsive vector graphics, and live parameter sliders:

```bash
# Euclid's Elements
python3 -m Euclid.euclid.cli serve --port 8080

# Newton's Principia Mathematica
python3 -m Newton.newton.cli serve --port 8081

# Cantor's Transfinite Set Theory
python3 -m Cantor.cantor.cli serve --port 8082

# Hilbert's Foundations of Geometry & Analysis
python3 -m Hilbert.hilbert.cli serve --port 8083

# Einstein's Differential Geometry of Relativity
python3 -m Einstein.einstein.cli serve --port 8084

# Heisenberg's Matrix Mechanics & Commutation Relations
python3 -m Heisenberg.heisenberg.cli serve --port 8085
```

### Exporting Standalone Books (HTML & PDF)

```bash
# Export Euclid's Elements to publication PDF
python3 -m Euclid.euclid.cli export --out Euclid_Elements.pdf

# Export Newton's Principia to publication PDF
python3 -m Newton.newton.cli export --out Newton_Principia.pdf

# Export Cantor's Set Theory to publication PDF
python3 -m Cantor.cantor.cli export --out Cantor_Set_Theory.pdf
```

## Structure & Architecture

```
MATH/
├── LICENSE
├── README.md
├── Euclid/
│   ├── euclid/
│   │   ├── axioms.py
│   │   ├── geometry.py
│   │   ├── proofs.py
│   │   ├── visualizer.py
│   │   ├── book.py
│   │   └── cli.py
│   └── tests/
├── Newton/
│   ├── newton/
│   │   ├── mechanics.py
│   │   ├── propositions.py
│   │   ├── visualizer.py
│   │   ├── book.py
│   │   └── cli.py
│   └── tests/
├── Cantor/
│   ├── cantor/
│   └── tests/
├── Hilbert/
│   ├── hilbert/
│   └── tests/
├── Einstein/
│   ├── einstein/
│   └── tests/
├── Heisenberg/
│   ├── heisenberg/
│   └── tests/
└── math-video-engine/
    ├── src/math_video_engine/
    └── tests/
```

## License

MIT License - Copyright (c) 2026 Jeong Hoon Kim. See `LICENSE` for details.
