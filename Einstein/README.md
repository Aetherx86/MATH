# Albert Einstein: Special & General Relativity

Interactive Spacetime Geodesic Engine, Lorentz Transformations, and Schwarzschild Metric Simulator

## Theoretical Foundation

In 1905 and 1915, Albert Einstein transformed the conceptual foundations of physics. Special Relativity replaced absolute Galilean space and universal time with a four-dimensional pseudo-Riemannian Minkowski manifold where the speed of light $c$ is an invariant limit and spacetime intervals $\Delta s^2 = -c^2 \Delta t^2 + \Delta x^2 + \Delta y^2 + \Delta z^2$ remain invariant under Lorentz group transformations. General Relativity generalized this to curved pseudo-Riemannian manifolds governed by the Einstein Field Equations, demonstrating that gravity is the manifestation of spacetime curvature.

This repository provides an interactive digital implementation of Einstein's relativity:
1. Special Relativistic Lorentz transformations, time dilation, length contraction, and 4-momentum conservation.
2. Invariant mass-shell relation verification: $E^2 - (pc)^2 = (m_0 c^2)^2$.
3. General Relativistic Schwarzschild geometry: exact calculation of event horizons (Schwarzschild radius $r_s = 2GM/c^2$) and light deflection.
4. Relativistic Binet geodesic orbit integrator reproducing Mercury's historic perihelion precession of $43''$ arcseconds per century.
5. Interactive Web Reader and print-ready document layout.

---

## Core Mathematical Formulations

### Minkowski Metric & Lorentz Boost
For relative motion along the $x$-axis with parameter $\beta = v/c$:
$$\gamma = \frac{1}{\sqrt{1 - \beta^2}}$$
$$\begin{pmatrix} c t' \\ x' \\ y' \\ z' \end{pmatrix} = \begin{pmatrix} \gamma & -\beta\gamma & 0 & 0 \\ -\beta\gamma & \gamma & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} c t \\ x \\ y \\ z \end{pmatrix}$$
Spacetime Interval Invariance:
$$\Delta s'^2 = -(ct')^2 + x'^2 + y'^2 + z'^2 = -(ct)^2 + x^2 + y^2 + z^2 = \Delta s^2$$

### The Einstein Field Equations
$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$
where $G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu}$ is the Einstein curvature tensor.

### Relativistic Perihelion Advance of Mercury
In Schwarzschild geometry, the orbital equation for $u(\phi) = 1/r(\phi)$ acquires a non-linear General Relativistic correction:
$$\frac{d^2 u}{d\phi^2} + u = \frac{GM}{h^2} + \frac{3GM}{c^2} u^2$$
Perturbative integration across one complete revolution yields the anomalous advance:
$$\Delta \phi = \frac{6\pi G M}{c^2 a (1 - e^2)} \quad \text{rad/revolution}$$
For Mercury ($a = 57.9 \times 10^9 \text{ m}, e = 0.2056$), this corresponds to exactly $43.0''$ arcseconds per century.

---

## Installation & Setup

Zero third-party dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/MATH.git
cd MATH/Einstein
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Command Line Usage

### Launch Interactive Reader
```bash
python3 -m einstein.cli serve --port 8083
```
Open `http://localhost:8083` in any web browser.

### Compute Lorentz Boost
```bash
python3 -m einstein.cli boost --beta 0.8 --ct 10.0 --x 6.0
```

### Calculate Mercury Perihelion Advance
```bash
python3 -m einstein.cli precession
```

### Export Standalone Book (HTML / PDF)
```bash
python3 -m einstein.cli export -o einstein_relativity.html
```

---

## Python API Reference

```python
from einstein.relativity import FourVector, LorentzBoost, GeneralRelativityEngine, M_SUN

# Lorentz Boost
v4 = FourVector(ct=10.0, x=5.0, y=0.0, z=0.0)
boosted = LorentzBoost.boost_x(v4, beta=0.6)
assert abs(v4.spacetime_interval() - boosted.spacetime_interval()) < 1e-10

# Solar Schwarzschild Radius
r_s = GeneralRelativityEngine.schwarzschild_radius(M_SUN)
print(f"Solar Schwarzschild radius: {r_s / 1000.0:.2f} km")

# Relativistic Orbit Geodesic
trajectory = GeneralRelativityEngine.integrate_relativistic_orbit(a=1.0, e=0.3, num_orbits=3)
print(f"Computed {len(trajectory)} geodesic trajectory points.")
```

---

## Verification & Integrity

The test suite validates:
* Invariance of the Minkowski metric interval under Lorentz boosts.
* Relativistic energy-momentum mass shell relation $E^2 - (pc)^2 = (m_0 c^2)^2$.
* Solar Schwarzschild radius ($r_s \approx 2.95$ km).
* General Relativistic Mercury perihelion advance ($43''$ arcseconds/century).
* Gravitational light deflection at solar limb ($1.75''$ arcseconds).

Run verification:
```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License. Copyright (c) 2026 Jeong Hoon Kim.
