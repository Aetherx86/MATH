# Philosophiae Naturalis Principia Mathematica

Interactive Mechanics, Central Forces, and Geometric Fluxions

## Theoretical Foundation

In 1687, Sir Isaac Newton published the Philosophiae Naturalis Principia Mathematica, establishing classical rational mechanics, the universal law of gravitation, and the mathematical framework of differential fluxions through the geometric method of prime and ultimate ratios. Rather than relying purely on algebraic calculus notation, Newton developed rigorous synthetic geometric proofs demonstrating that Kepler's empirical laws of planetary motion were necessary consequences of an inverse-square centripetal force directed toward a center of mass.

This repository provides an interactive digital edition and numerical verification engine for the core mathematical physics of the Principia:
1. Symplectic numerical integration (Velocity-Verlet) conserving energy, angular momentum, and the Laplace-Runge-Lenz vector over long integration horizons.
2. Exact algorithmic reconstruction of Proposition 1 (Theorem 1): Kepler's Second Law derived via discrete impulse polygonal trajectories converging to continuous curves as time interval delta_t -> 0.
3. Deduction of the Inverse-Square Law (Proposition 11) from Keplerian elliptical orbits.
4. Publication-grade interactive web reader featuring real-time orbit controls, hodograph representations, and dynamic areal sweeps.
5. Print-ready layout engine for export to standard PDF and document formats.

---

## Axiomatic Architecture

### Axiomata sive Leges Motus (The Three Laws of Motion)
* Lex I (Law of Inertia): Every body continues in its state of rest or of uniform motion in a right line, unless it is compelled to change that state by forces impressed upon it.
  $$\sum \mathbf{F} = 0 \implies \frac{d\mathbf{v}}{dt} = 0$$
* Lex II (Law of Motion and Force): The change of motion is proportional to the motive force impressed, and takes place along the right line in which that force is impressed.
  $$\mathbf{F} = \frac{d\mathbf{p}}{dt} = m \frac{d^2\mathbf{r}}{dt^2}$$
* Lex III (Action and Reaction): To every action there is always opposed an equal reaction; the mutual actions of two bodies upon each other are always equal and directed to contrary parts.
  $$\mathbf{F}_{12} = -\mathbf{F}_{21} \implies \frac{d}{dt}(\mathbf{p}_1 + \mathbf{p}_2) = 0$$

---

## Core Mathematical Propositions

### Book I, Proposition 1 (Theorem 1): Conservation of Areal Velocity
"The areas which bodies made to move in orbits describe by radii drawn to an unmoving center of forces are contained in unmoving planes and are proportional to the times."

Newton's deductive constructive steps:
1. Divide time into equal intervals $\Delta t$. During the first interval, the body moves uniformly along $AB$ (Law I).
2. During the second interval, if unimpeded, it would continue straight to $c$, where $Bc = AB$.
3. Triangles $\triangle SAB$ and $\triangle SBc$ share the same base $SB$ and have equal altitudes, thus $\text{Area}(\triangle SAB) = \text{Area}(\triangle SBc)$ (Euclid I.38).
4. At $B$, an instantaneous centripetal impulse acts toward center $S$, producing deflection vector $cC \parallel BS$ (Law II and Corollary 1).
5. By parallel lines $cC \parallel BS$, triangles $\triangle SBC$ and $\triangle SBc$ share common base $SB$ and lie between the same parallels, therefore $\text{Area}(\triangle SBC) = \text{Area}(\triangle SBc)$ (Euclid I.37).
6. Transitively, $\text{Area}(\triangle SBC) = \text{Area}(\triangle SAB)$.
7. Taking the limit $\Delta t \to 0$ (Lemma III), the polygonal path converges to a smooth curve with constant areal velocity:
   $$\frac{dA}{dt} = \frac{1}{2} |\mathbf{r} \times \mathbf{v}| = \frac{1}{2} h = \text{constant}$$

### Book I, Proposition 11 (Problem 6): Inverse-Square Gravitational Law
Given a body moving along an ellipse $r(\theta) = \frac{p}{1 + e \cos \theta}$ under a force directed toward focus $S$:
Using Newton's geometric centripetal force measure (Proposition VI):
$$F \propto \lim_{\Delta t \to 0} \frac{QR}{SP^2 \cdot QT^2}$$
where $QR$ is the subtense parallel to radius $SP$ and $QT$ is perpendicular to tangent $PR$. Through the conic properties of conjugate diameters and latus rectum $L = \frac{2b^2}{a}$, Newton demonstrates that $\frac{QR}{QT^2} \to \frac{1}{L}$, proving that:
$$F(r) = \frac{\mu}{SP^2} = \frac{\mu}{r^2}$$

---

## Installation & Setup

Zero third-party dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/Newton.git
cd Newton
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Command Line Usage

### Launch Interactive Principia Book
Starts the built-in HTTP server hosting the readable edition and real-time symplectic Keplerian laboratory:
```bash
python3 -m newton.cli serve --port 8080
```
Open `http://localhost:8080` in your web browser.

### Terminal Symplectic Orbit Integrator
Run the Velocity-Verlet simulation directly in the terminal, monitoring energy and angular momentum conservation across thousands of integration steps:
```bash
python3 -m newton.cli orbit --eccentricity 0.6 --steps 2000 --dt 0.005
```

### Terminal Deductive Demonstrator
Print full step-by-step mathematical proofs of Principia propositions:
```bash
# Demonstrate Proposition 1 (Kepler's Second Law)
python3 -m newton.cli prove Prop.I.1

# Demonstrate Proposition 11 (Inverse-Square Gravitation)
python3 -m newton.cli prove Prop.I.11
```

### Export Standalone Book (HTML / PDF)
Export the interactive document:
```bash
python3 -m newton.cli export -o principia_mathematica.html
```
Open `principia_mathematica.html` in your browser and select `Print > Save as PDF` for a publication-ready document with automated page breaks.

---

## Python API Reference

```python
from newton.mechanics import CentralForceIntegrator, OrbitalState
from newton.propositions import compute_proposition_1_discrete_impulses, get_principia_propositions
from newton.visualizer import PrincipiaVisualizer
from newton.book import PrincipiaBookGenerator

# Symplectic integration of eccentric orbit
integrator = CentralForceIntegrator(mu=1.0, power_n=2.0)
trajectory = integrator.integrate_verlet(x0=0.5, y0=0.0, vx0=0.0, vy0=1.732, dt=0.002, steps=1000)

initial_energy = trajectory[0].specific_energy()
final_energy = trajectory[-1].specific_energy()
print(f"Energy conservation error: {abs(final_energy - initial_energy):.2e}")

# Compute discrete impulses for Proposition 1
impulses = compute_proposition_1_discrete_impulses(r0=200.0, v0=140.0, delta_t=0.5)
visualizer = PrincipiaVisualizer()
svg_content = visualizer.render_proposition_1_svg(impulses)

# Generate HTML book
book_gen = PrincipiaBookGenerator()
html_text = book_gen.generate_html()
```

---

## Verification & Integrity

The test suite validates:
* Symplectic Velocity-Verlet conservation of specific energy ($\Delta E / |E| < 10^{-4}$) and specific angular momentum ($\Delta h / h < 10^{-12}$).
* Constant Laplace-Runge-Lenz vector orientation for closed orbits under inverse-square forces.
* Machine-precision equality of discrete triangle areas ($\triangle SAB = \triangle SBC = \triangle SCD$) in Proposition 1.
* Vector diagram and HTML book generator integrity.

Run verification:
```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License. Copyright (c) 2026 Jeong Hoon Kim.
