import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

class HilbertVector:
    """Vector in an inner product space (finite-dimensional R^n or truncated l^2)."""
    def __init__(self, components: List[float]):
        self.components = [float(c) for c in components]

    def __len__(self) -> int:
        return len(self.components)

    def __add__(self, other: "HilbertVector") -> "HilbertVector":
        dim = max(len(self), len(other))
        v1 = self.components + [0.0] * (dim - len(self))
        v2 = other.components + [0.0] * (dim - len(other))
        return HilbertVector([a + b for a, b in zip(v1, v2)])

    def __sub__(self, other: "HilbertVector") -> "HilbertVector":
        dim = max(len(self), len(other))
        v1 = self.components + [0.0] * (dim - len(self))
        v2 = other.components + [0.0] * (dim - len(other))
        return HilbertVector([a - b for a, b in zip(v1, v2)])

    def scale(self, alpha: float) -> "HilbertVector":
        return HilbertVector([alpha * c for c in self.components])

    def inner_product(self, other: "HilbertVector") -> float:
        """Standard inner product <x, y> = sum(x_i * y_i)."""
        dim = min(len(self), len(other))
        return sum(self.components[i] * other.components[i] for i in range(dim))

    def norm(self) -> float:
        """Induced norm ||x|| = sqrt(<x, x>)."""
        return math.sqrt(max(0.0, self.inner_product(self)))

    def normalize(self) -> "HilbertVector":
        n = self.norm()
        if n < 1e-14:
            raise ValueError("Cannot normalize a zero vector.")
        return self.scale(1.0 / n)

class HilbertSpaceEngine:
    """Functional analysis operations in real Hilbert spaces."""
    @staticmethod
    def verify_cauchy_schwarz(x: HilbertVector, y: HilbertVector) -> Tuple[bool, float, float]:
        """Validates |<x, y>| <= ||x|| * ||y||."""
        ip = abs(x.inner_product(y))
        bound = x.norm() * y.norm()
        return ip <= bound + 1e-12, ip, bound

    @staticmethod
    def verify_parallelogram_law(x: HilbertVector, y: HilbertVector) -> Tuple[bool, float, float]:
        """Validates ||x + y||^2 + ||x - y||^2 = 2(||x||^2 + ||y||^2)."""
        lhs = (x + y).norm()**2 + (x - y).norm()**2
        rhs = 2.0 * (x.norm()**2 + y.norm()**2)
        return abs(lhs - rhs) < 1e-10, lhs, rhs

    @staticmethod
    def gram_schmidt(vectors: List[HilbertVector]) -> List[HilbertVector]:
        """Gram-Schmidt orthonormalization procedure."""
        ortho: List[HilbertVector] = []
        for v in vectors:
            w = HilbertVector(v.components)
            for u in ortho:
                proj = u.scale(w.inner_product(u))
                w = w - proj
            if w.norm() > 1e-10:
                ortho.append(w.normalize())
        return ortho

@dataclass(frozen=True)
class AxiomGroup:
    group_name: str
    german_name: str
    description: str
    axioms: List[str]

HILBERT_GEOMETRY_AXIOMS: List[AxiomGroup] = [
    AxiomGroup(
        group_name="Group I: Incidence Axioms",
        german_name="Verknüpfung",
        description="Establishes relations between points, straight lines, and planes.",
        axioms=[
            "I.1: Two distinct points A and B always completely determine a straight line a.",
            "I.2: Any two distinct points of a straight line completely determine that line.",
            "I.3: On every straight line there exist at least two points; there exist at least three points not on the same line.",
            "I.4: Three points A, B, C not situated on the same straight line determine a plane.",
        ],
    ),
    AxiomGroup(
        group_name="Group II: Order Axioms",
        german_name="Anordnung",
        description="Formalizes the betweenness relation (B is between A and C) and Pasch's axiom.",
        axioms=[
            "II.1: If a point B lies between A and C, then A, B, C are three distinct points of a straight line, and B lies also between C and A.",
            "II.2: For two points A and C, there always exists at least one point B on the line AC such that C lies between A and B.",
            "II.3: Of any three points on a line, there exists no more than one that lies between the other two.",
            "II.4 (Pasch's Axiom): Let A, B, C be three points that do not lie on a line and let a be a line in the plane ABC not containing any of the points A, B, C. If the line a passes through any point of the segment AB, it also passes through a point of the segment AC or BC.",
        ],
    ),
    AxiomGroup(
        group_name="Group III: Congruence Axioms",
        german_name="Kongruenz",
        description="Defines congruence of segments and angles independently of rigid body motion.",
        axioms=[
            "III.1: If A, B are distinct points and A' is a point on line a', there exists a unique point B' on a given ray from A' such that AB is congruent to A'B'.",
            "III.2: If segment A'B' and segment A''B'' are congruent to the same segment AB, then A'B' is congruent to A''B''.",
            "III.3: Addition of congruent segments produces congruent wholes.",
            "III.4: Given an angle and a ray, there exists a unique congruent angle on a given side of the ray.",
            "III.5 (SAS): If for two triangles ABC and A'B'C' the congruences AB = A'B', AC = A'C', and angle BAC = angle B'A'C' hold, then angle ABC = angle A'B'C'.",
        ],
    ),
    AxiomGroup(
        group_name="Group IV: Parallel Axiom",
        german_name="Parallelenaxiom",
        description="Hilbert's modern reformulation of the Euclidean parallel postulate.",
        axioms=[
            "IV: Let a be any line and A a point not on it. Then there exists in the plane determined by a and A at most one line that passes through A and does not intersect a.",
        ],
    ),
    AxiomGroup(
        group_name="Group V: Continuity Axioms",
        german_name="Stetigkeit",
        description="Archimedean axiom and line completeness axiom.",
        axioms=[
            "V.1 (Axiom of Archimedes): If AB and CD are arbitrary segments, there exists a number n such that n copies of CD laid out continuously from A exceed B.",
            "V.2 (Line Completeness): An extension of a system of points on a line with its order and congruence relations that preserves previous axioms is impossible.",
        ],
    ),
]

@dataclass(frozen=True)
class HilbertProblem:
    number: int
    title: str
    field: str
    status: str
    description: str

HILBERT_PROBLEMS_HIGHLIGHTS: List[HilbertProblem] = [
    HilbertProblem(
        number=1,
        title="Continuum Hypothesis",
        field="Set Theory",
        status="Resolved (Independence proved by Gödel 1940 and Cohen 1963)",
        description="Is there a set whose cardinality is strictly between that of the integers and the real numbers? (2^aleph_0 = aleph_1).",
    ),
    HilbertProblem(
        number=2,
        title="Consistency of the Axioms of Arithmetic",
        field="Mathematical Logic",
        status="Resolved (Gödel's Incompleteness Theorems 1931 showed unprovability from within arithmetic; Gentzen proved consistency using transfinite induction 1936)",
        description="Prove that the axioms of arithmetic are consistent.",
    ),
    HilbertProblem(
        number=8,
        title="Riemann Hypothesis and Goldbach Conjecture",
        field="Number Theory",
        status="Open (Clay Millennium Prize Problem)",
        description="All non-trivial zeros of the Riemann zeta function have real part 1/2.",
    ),
    HilbertProblem(
        number=10,
        title="Solvability of Diophantine Equations",
        field="Computability / Logic",
        status="Resolved (Matiyasevich theorem 1970 proved algorithmic insolvability)",
        description="Find an algorithm to determine whether a given polynomial Diophantine equation with integer coefficients has integer solutions.",
    ),
]
