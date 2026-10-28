# Euclid's Elements (Στοιχεῖα)

Interactive Mathematical Proof Suite & Constructive Axiomatic Engine

## Theoretical Foundation

Euclid of Alexandria formulated the axiomatic foundation of deductive mathematics around 300 BCE in the thirteen books of the Elements (Στοιχεῖα). By commencing with an explicit collection of primitive definitions, unproven constructive postulates, and self-evident common notions, Euclid demonstrated that the entirety of planar geometry and classical arithmetic could be rigorously derived through finite sequences of deductive steps.

This repository provides an interactive digital implementation of Euclid's Elements, featuring:
1. Exact constructive geometry solver (compass-and-straightedge primitives, line-line and circle-circle intersection algorithms).
2. Deductive step-by-step theorem demonstrator with geometric justifications citing specific postulates, common notions, and previously established propositions.
3. High-precision vector diagram generator with chromatic styling inspired by Oliver Byrne's 1847 visual edition.
4. Interactive web application featuring a real-time draggable geometry canvas and complete book reader.
5. Print-ready layout engine for export to standard PDF and document formats.

---

## Axiomatic Architecture

### Definitions of Book I
The system models primitive entities without circular coordinate definitions:
* Definition 1 (Point): That which has no part.
* Definition 2 (Line): Breadthless length.
* Definition 4 (Straight Line): A line which lies evenly with the points on itself.
* Definition 10 (Right Angle): Adjacent angles formed when a straight line set upon a straight line produces equal angles.
* Definition 15 (Circle): A plane figure contained by one line such that all straight lines falling upon it from one point within equal one another.
* Definition 23 (Parallel Lines): Coplanar straight lines produced indefinitely in both directions that never meet.

### The Five Postulates
1. Postulate 1: To draw a straight line from any point to any point.
2. Postulate 2: To produce a finite straight line continuously in a straight line.
3. Postulate 3: To describe a circle with any center and distance.
4. Postulate 4: That all right angles equal one another.
5. Postulate 5 (Parallel Postulate): If a straight line falling on two straight lines makes interior angles on the same side less than two right angles, the two lines meet on that side if produced indefinitely.

### The Five Common Notions
1. Things which equal the same thing also equal one another (Transitivity of equality).
2. If equals are added to equals, the wholes are equal (Additive congruence).
3. If equals are subtracted from equals, the remainders are equal (Subtractive congruence).
4. Things which coincide with one another equal one another (Superposition principle).
5. The whole is greater than the part (Order and containment property).

---

## Core Constructive Propositions

### Proposition I.1: Equilateral Triangle Construction
Given a finite straight line segment AB:
1. Draw circle with center A and radius AB (Postulate 3).
2. Draw circle with center B and radius BA (Postulate 3).
3. Locate intersection point C of the two circles.
4. Join CA and CB (Postulate 1).
5. Since AC = AB (radii of circle A) and BC = AB (radii of circle B), AC = BC by Common Notion 1.
6. Triangle ABC is equilateral (Q.E.F.).

### Proposition I.47: The Pythagorean Theorem (Windmill Proof / Bride's Chair)
In right-angled triangles, the square on the side subtending the right angle equals the sum of the squares on the sides containing the right angle:
$$\text{Area}(BDEC) = \text{Area}(BAGF) + \text{Area}(ACKH)$$
The proof uses shear invariance: parallelograms on the same base and between the same parallels are equal in area (Proposition I.41), proving that rectangle BDLM equals square BAGF and rectangle CELM equals square ACKH.

### Proposition IX.20: Infinitude of Prime Numbers
Euclid's constructive demonstration that prime numbers are more than any assigned multitude of prime numbers:
Given finite set $P = \{p_1, p_2, \dots, p_k\}$, construct $N = \left(\prod_{i=1}^k p_i\right) + 1$. Either $N$ is prime or possesses a prime factor $q$. If $q \in P$, then $q$ divides both $N$ and $\prod P$, implying $q$ divides their difference $1$, a contradiction. Thus $q \notin P$, proving the existence of an infinite succession of primes (Q.E.D.).

---

## Installation & Setup

Zero third-party dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/MATH.git
cd MATH/Euclid
```

Run test suite:
```bash
python3 -m unittest discover tests
```

---

## Command Line Usage

### Launch Interactive Reader
Starts the built-in HTTP server hosting the interactive book and dynamic geometry laboratory:
```bash
python3 -m euclid.cli serve --port 8000
```
Open `http://localhost:8000` in any modern web browser.

### Terminal Deductive Demonstrator
Print full step-by-step proofs with axiomatic citations in your console:
```bash
# Demonstrate the Pythagorean Theorem
python3 -m euclid.cli prove Prop.I.47

# Demonstrate Equilateral Triangle Construction
python3 -m euclid.cli prove Prop.I.1

# Demonstrate the Infinitude of Primes
python3 -m euclid.cli prove Prop.IX.20
```

### Export Standalone Book (HTML / PDF)
Export the publication-ready interactive document:
```bash
python3 -m euclid.cli export -o euclid_elements.html
```
To generate a PDF, open `euclid_elements.html` in Chrome or Safari and select `File > Print > Save as PDF`. The document includes specialized CSS print rules that eliminate browser chrome and format proof cards into clean page breaks.

---

## Python API Reference

```python
from euclid.geometry import Point, Circle, Line
from euclid.proofs import construct_proposition_1, construct_proposition_47
from euclid.visualizer import SVGVisualizer
from euclid.book import BookGenerator

# Construct Proposition I.1
prop1 = construct_proposition_1()
print(prop1.title)
for step in prop1.steps:
    print(f"Step {step.step_number}: {step.action} [{step.justification}]")

# Render vector diagram
visualizer = SVGVisualizer(width=600, height=500)
svg_content = visualizer.render_figure(prop1.figure)

# Generate complete HTML book
generator = BookGenerator()
html_document = generator.generate_html()
```

---

## Verification & Integrity

The test suite validates:
* Exact constructive intersection coordinates for intersecting and tangent circles.
* Triangle and polygon area calculations using the shoelace algorithm.
* Step sequence completeness and citation validity across all propositions.
* SVG markup generation and canvas DOM integration.

Run verification:
```bash
python3 -m unittest discover tests -v
```

---

## License

MIT License. Copyright (c) 2026 Jeong Hoon Kim.
