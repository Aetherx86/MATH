# MATH: Unified Mathematical Foundations & Visual Computing Suite

A unified monorepo bringing together the monumental works of mathematical giants—Euclid, Newton, Cantor, Hilbert, Einstein, and Heisenberg—alongside an advanced computational mathematical animation engine.

Every sub-repository contains an interactive readable digital edition, rigorous formal proof engines, vector visualizations, unit test suites, and publication-ready PDF exports.

## Repository Directory

| Sub-Repository | Focus & Mathematical Foundations | Standalone Repository |
| :--- | :--- | :--- |
| **`Euclid/`** | Axiomatic planar geometry, Euclidean algorithm, infinite primes proof, Pythagorean theorem | [gitlab.com/jk9576/Euclid](https://gitlab.com/jk9576/Euclid) |
| **`Newton/`** | Foundations of differential calculus, fluxions, gravitational mechanics, Kepler orbits | [gitlab.com/jk9576/Newton](https://gitlab.com/jk9576/Newton) |
| **`Cantor/`** | Transfinite set theory, Cantor diagonal argument, cardinality hierarchy | [gitlab.com/jk9576/Cantor](https://gitlab.com/jk9576/Cantor) |
| **`Hilbert/`** | Axiomatic geometry, infinite-dimensional Hilbert space, spectral decomposition | [gitlab.com/jk9576/Hilbert](https://gitlab.com/jk9576/Hilbert) |
| **`Einstein/`** | Differential geometry, Riemannian curvature tensors, geodesic variation | [gitlab.com/jk9576/Einstein](https://gitlab.com/jk9576/Einstein) |
| **`Heisenberg/`** | Non-commutative operator algebras, matrix mechanics, commutator brackets | [gitlab.com/jk9576/Heisenberg](https://gitlab.com/jk9576/Heisenberg) |
| **`math-video-engine/`**| Standalone mathematical animation and video synthesis engine (Fourier, linear algebra, Goldbach) | [gitlab.com/jk9576/math-video-engine](https://gitlab.com/jk9576/math-video-engine) |

## Quick Start & Verification

### Running All Unit Test Suites

Each sub-repository can be tested independently:

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
cd math-video-engine && python3 -W error -m unittest discover tests && cd ..
```

### Exporting Interactive Books to HTML and PDF

Each interactive edition can be served locally or exported directly:

```bash
# Serve Euclid's Elements
python3 -m Euclid.euclid.cli serve --port 8080

# Export Newton's Principia to PDF
python3 -m Newton.newton.cli export --out Newton_Principia.pdf

# Export Cantor's Transfinite Set Theory to PDF
python3 -m Cantor.cantor.cli export --out Cantor_Set_Theory.pdf
```

## Structure & Architecture

```
MATH/
├── LICENSE
├── README.md
├── Euclid/
│   ├── euclid/
│   └── tests/
├── Newton/
│   ├── newton/
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
