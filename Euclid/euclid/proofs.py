import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from .geometry import Circle, Line, Point, Polygon, Segment

@dataclass
class ProofStep:
    step_number: int
    action: str
    justification: str
    active_elements: List[str]
    description: str

@dataclass
class GeometricFigure:
    points: Dict[str, Point]
    segments: List[Tuple[str, str, str]]  # (p1_name, p2_name, color_hex_or_name)
    circles: List[Tuple[str, str, str]]   # (center_name, radius_point_name, color)
    polygons: List[Tuple[List[str], str]] # (vertex_names, fill_color)

@dataclass
class Proposition:
    prop_id: str
    book: int
    number: int
    title: str
    statement: str
    steps: List[ProofStep]
    figure: GeometricFigure
    qed_conclusion: str

def construct_proposition_1() -> Proposition:
    """
    Proposition I.1:
    To construct an equilateral triangle on a given finite straight line.
    """
    pA = Point(100.0, 200.0)
    pB = Point(300.0, 200.0)
    r = pA.distance_to(pB)  # 200.0

    cA = Circle(pA, r)
    cB = Circle(pB, r)
    intersections = cA.intersect_circle(cB)
    pC = min(intersections, key=lambda p: p.y)  # Upper intersection point

    points = {"A": pA, "B": pB, "C": pC}
    segments = [
        ("A", "B", "#1f77b4"),  # Base line AB (Blue)
        ("A", "C", "#d62728"),  # Line AC (Red)
        ("B", "C", "#ff7f0e"),  # Line BC (Orange)
    ]
    circles = [
        ("A", "B", "rgba(31, 119, 180, 0.3)"),  # Circle with center A, radius AB
        ("B", "A", "rgba(214, 39, 40, 0.3)"),   # Circle with center B, radius BA
    ]
    polygons = [
        (["A", "B", "C"], "rgba(44, 160, 44, 0.15)"),
    ]

    steps = [
        ProofStep(
            step_number=1,
            action="Let AB be the given finite straight line.",
            justification="Hypothesis",
            active_elements=["A", "B", "segment_AB"],
            description="We begin with an arbitrary given finite segment AB.",
        ),
        ProofStep(
            step_number=2,
            action="Describe the circle BCD with center A and radius AB.",
            justification="Postulate 3",
            active_elements=["circle_A"],
            description="With center A and distance AB, describe circle with compass.",
        ),
        ProofStep(
            step_number=3,
            action="Describe the circle ACE with center B and radius BA.",
            justification="Postulate 3",
            active_elements=["circle_B"],
            description="With center B and distance BA, describe the second circle.",
        ),
        ProofStep(
            step_number=4,
            action="From point C, in which the circles cut one another, join straight lines CA and CB.",
            justification="Postulate 1",
            active_elements=["C", "segment_AC", "segment_BC"],
            description="Connect intersection C to endpoints A and B using the straightedge.",
        ),
        ProofStep(
            step_number=5,
            action="Since point A is center of circle CDB, AC equals AB. Since point B is center of circle CAE, BC equals BA.",
            justification="Definition 15",
            active_elements=["segment_AB", "segment_AC", "segment_BC"],
            description="Radii drawn from the center of the same circle are equal to one another.",
        ),
        ProofStep(
            step_number=6,
            action="Therefore, each of the straight lines CA and CB equals AB. But things which equal the same thing also equal one another; therefore CA also equals CB.",
            justification="Common Notion 1",
            active_elements=["polygon_ABC"],
            description="Since AC = AB and BC = AB, it follows transitively that AC = BC = AB.",
        ),
        ProofStep(
            step_number=7,
            action="Therefore the three straight lines CA, AB, and BC equal one another. The triangle ABC is therefore equilateral, constructed on the given straight line AB.",
            justification="Conclusion (Q.E.F.)",
            active_elements=["polygon_ABC"],
            description="Triangle ABC is equilateral, which was to be done.",
        ),
    ]

    return Proposition(
        prop_id="Prop.I.1",
        book=1,
        number=1,
        title="Proposition 1: Equilateral Triangle Construction",
        statement="To construct an equilateral triangle on a given finite straight line.",
        steps=steps,
        figure=GeometricFigure(points=points, segments=segments, circles=circles, polygons=polygons),
        qed_conclusion="ὅπερ ἔδει ποιῆσαι — Which was to be done (Q.E.F.).",
    )

def construct_proposition_47() -> Proposition:
    """
    Proposition I.47: The Pythagorean Theorem (The Bride's Chair / Windmill Proof).
    In right-angled triangles the square on the side subtending the right angle
    equals the squares on the sides containing the right angle.
    """
    # Right triangle ABC at A
    # Let A be at (200, 250), right angle at A
    # Leg AB vertical or horizontal: AB = 120, AC = 90 (hypotenuse BC = 150)
    pA = Point(200.0, 250.0)
    pB = Point(200.0, 130.0)  # AB = 120
    pC = Point(290.0, 250.0)  # AC = 90
    # BC vector = (90, 120), length = 150

    # Square on AB (left square ABGF)
    pF = Point(80.0, 250.0)
    pG = Point(80.0, 130.0)

    # Square on AC (bottom square ACKH)
    pH = Point(200.0, 340.0)
    pK = Point(290.0, 340.0)

    # Square on BC (hypotenuse square BDEC, external to triangle)
    # Vector BC = C - B = (90, 120)
    # Perpendicular outward normal = (120, -90) normalized or scaled by length
    # Here vector BC has dx=90, dy=120. Outward normal is (dy, -dx) = (120, -90)
    pD = Point(pB.x + 120.0, pB.y - 90.0)
    pE = Point(pC.x + 120.0, pC.y - 90.0)

    # Altitude from A perpendicular to BC meeting BC at L and DE at M
    # Line BC: (y - 130)/(250 - 130) = (x - 200)/(290 - 200) -> 120*(x-200) - 90*(y-130) = 0
    # 4(x-200) - 3(y-130) = 0 -> 4x - 3y - 410 = 0
    line_bc = Line.from_points(pB, pC)
    # Line through A perpendicular to line_bc: slope is -b/a = -(-3)/4 -> normal vector
    line_alt = Line(line_bc.b, -line_bc.a, -line_bc.b * pA.x + line_bc.a * pA.y)
    pL = line_bc.intersect_line(line_alt)
    line_de = Line.from_points(pD, pE)
    pM = line_de.intersect_line(line_alt)

    points = {
        "A": pA, "B": pB, "C": pC,
        "D": pD, "E": pE, "F": pF, "G": pG, "H": pH, "K": pK,
        "L": pL if pL else Point(236.0, 178.0),
        "M": pM if pM else Point(356.0, 88.0),
    }

    segments = [
        ("A", "B", "#111111"), ("B", "C", "#111111"), ("C", "A", "#111111"),
        # Square on AB
        ("B", "G", "#e41a1c"), ("G", "F", "#e41a1c"), ("F", "A", "#e41a1c"),
        # Square on AC
        ("A", "H", "#377eb8"), ("H", "K", "#377eb8"), ("K", "C", "#377eb8"),
        # Square on BC
        ("B", "D", "#4daf4a"), ("D", "E", "#4daf4a"), ("E", "C", "#4daf4a"),
        # Shear lines
        ("A", "D", "#984ea3"), ("F", "C", "#984ea3"),
        ("A", "L", "#ff7f00"), ("L", "M", "#ff7f00"),
    ]

    polygons = [
        (["A", "B", "C"], "rgba(0,0,0,0.08)"),
        (["A", "B", "G", "F"], "rgba(228, 26, 28, 0.15)"),
        (["A", "C", "K", "H"], "rgba(55, 126, 184, 0.15)"),
        (["B", "C", "E", "D"], "rgba(77, 175, 74, 0.15)"),
    ]

    steps = [
        ProofStep(
            step_number=1,
            action="Let ABC be a right-angled triangle having the angle BAC right.",
            justification="Hypothesis",
            active_elements=["A", "B", "C", "polygon_ABC"],
            description="The right angle is formed at vertex A with legs AB and AC.",
        ),
        ProofStep(
            step_number=2,
            action="Describe on BC the square BDEC, on AB the square BAGF, and on AC the square ACKH.",
            justification="Proposition I.46",
            active_elements=["square_BC", "square_AB", "square_AC"],
            description="Construct three squares on the hypotenuse and the two legs.",
        ),
        ProofStep(
            step_number=3,
            action="Through A draw AL parallel to BD and extend it to M on DE.",
            justification="Proposition I.31",
            active_elements=["line_ALM"],
            description="The line divides the hypotenuse square into two rectangles: BDLM and CELM.",
        ),
        ProofStep(
            step_number=4,
            action="Join AD and FC.",
            justification="Postulate 1",
            active_elements=["segment_AD", "segment_FC"],
            description="Construct cross segments creating test triangles ABD and FBC.",
        ),
        ProofStep(
            step_number=5,
            action="Since angle DBC equals angle FBA (each right), add angle ABC to both: whole angle DBA equals whole angle FBC.",
            justification="Common Notion 2",
            active_elements=["angle_DBA", "angle_FBC"],
            description="Angles DBA and FBC are proved congruent.",
        ),
        ProofStep(
            step_number=6,
            action="Since DB = BC and FB = BA, the two sides DB, BA equal the two sides CB, FB, and the contained angles equal; therefore triangle ABD equals triangle FBC.",
            justification="Proposition I.4 (SAS)",
            active_elements=["triangle_ABD", "triangle_FBC"],
            description="Triangles ABD and FBC are congruent in area.",
        ),
        ProofStep(
            step_number=7,
            action="Now parallelogram BDLM is double triangle ABD (same base BD, in same parallels), and square BAGF is double triangle FBC (same base FB, in same parallels).",
            justification="Proposition I.41",
            active_elements=["rectangle_BDLM", "square_BAGF"],
            description="A parallelogram is double a triangle having the same base and between the same parallels.",
        ),
        ProofStep(
            step_number=8,
            action="Therefore parallelogram BDLM equals square BAGF. Similarly, by joining AE and BK, parallelogram CELM equals square ACKH.",
            justification="Common Notion 1",
            active_elements=["rectangle_BDLM", "rectangle_CELM", "square_BAGF", "square_ACKH"],
            description="The two rectangles sum to the two leg squares.",
        ),
        ProofStep(
            step_number=9,
            action="Therefore the whole square BDEC equals the two squares BAGF and ACKH together. Q.E.D.",
            justification="Common Notion 2",
            active_elements=["square_BDEC"],
            description="BC^2 = AB^2 + AC^2. In right triangles, the square on the hypotenuse equals the sum of the squares on the sides.",
        ),
    ]

    return Proposition(
        prop_id="Prop.I.47",
        book=1,
        number=47,
        title="Proposition 47: The Pythagorean Theorem",
        statement="In right-angled triangles the square on the side subtending the right angle equals the squares on the sides containing the right angle.",
        steps=steps,
        figure=GeometricFigure(points=points, segments=segments, circles=[], polygons=polygons),
        qed_conclusion="ὅπερ ἔδει δεῖξαι — Which was to be demonstrated (Q.E.D.).",
    )

def construct_proposition_9() -> Proposition:
    """Proposition I.9: To bisect a given rectilinear angle."""
    pA = Point(200.0, 250.0)
    pB = Point(320.0, 180.0)
    pC = Point(280.0, 330.0)

    # Take point D on AB and E on AC such that AD = AE
    d_len = 80.0
    uB = (pB.x - pA.x) / pA.distance_to(pB), (pB.y - pA.y) / pA.distance_to(pB)
    uC = (pC.x - pA.x) / pA.distance_to(pC), (pC.y - pA.y) / pA.distance_to(pC)
    pD = Point(pA.x + d_len * uB[0], pA.y + d_len * uB[1])
    pE = Point(pA.x + d_len * uC[0], pA.y + d_len * uC[1])

    # Construct equilateral triangle on DE
    seg_de = Segment(pD, pE)
    circD = Circle(pD, seg_de.length)
    circE = Circle(pE, seg_de.length)
    inter = circD.intersect_circle(circE)
    pF = max(inter, key=lambda p: p.x)  # Outward intersection

    points = {"A": pA, "B": pB, "C": pC, "D": pD, "E": pE, "F": pF}
    segments = [
        ("A", "B", "#333333"), ("A", "C", "#333333"),
        ("D", "E", "#e41a1c"), ("D", "F", "#377eb8"), ("E", "F", "#377eb8"),
        ("A", "F", "#4daf4a"),  # Angle bisector (Green)
    ]
    circles = [
        ("D", "E", "rgba(55, 126, 184, 0.2)"),
        ("E", "D", "rgba(55, 126, 184, 0.2)"),
    ]

    steps = [
        ProofStep(
            step_number=1,
            action="Let the angle BAC be the given rectilinear angle.",
            justification="Hypothesis",
            active_elements=["A", "B", "C"],
            description="The given angle formed by rays AB and AC.",
        ),
        ProofStep(
            step_number=2,
            action="Take an arbitrary point D on AB, and cut off AE from AC equal to AD.",
            justification="Proposition I.3",
            active_elements=["D", "E"],
            description="Make AD = AE along the two arms.",
        ),
        ProofStep(
            step_number=3,
            action="Join DE, and construct an equilateral triangle DEF on DE.",
            justification="Proposition I.1",
            active_elements=["D", "E", "F", "segment_DF", "segment_EF"],
            description="Build equilateral triangle DEF on base DE.",
        ),
        ProofStep(
            step_number=4,
            action="Join AF.",
            justification="Postulate 1",
            active_elements=["segment_AF"],
            description="Draw ray from vertex A through F.",
        ),
        ProofStep(
            step_number=5,
            action="Since AD = AE, and AF is common, the two sides DA, AF equal the two sides EA, AF; and base DF equals base EF. Therefore angle DAF equals angle EAF.",
            justification="Proposition I.8 (SSS)",
            active_elements=["segment_AF"],
            description="Triangles DAF and EAF are congruent by SSS, so angle DAF = angle EAF.",
        ),
        ProofStep(
            step_number=6,
            action="Therefore the rectilinear angle BAC has been bisected by the straight line AF.",
            justification="Conclusion (Q.E.F.)",
            active_elements=["segment_AF"],
            description="The ray AF bisects angle BAC into two equal angles.",
        ),
    ]

    return Proposition(
        prop_id="Prop.I.9",
        book=1,
        number=9,
        title="Proposition 9: Angle Bisection",
        statement="To bisect a given rectilinear angle.",
        steps=steps,
        figure=GeometricFigure(points=points, segments=segments, circles=circles, polygons=[]),
        qed_conclusion="ὅπερ ἔδει ποιῆσαι — Which was to be done (Q.E.F.).",
    )

def construct_proposition_ix_20() -> Proposition:
    """
    Proposition IX.20:
    Prime numbers are more than any assigned multitude of prime numbers.
    (Euclid's Theorem on the Infinitude of Primes).
    """
    pA = Point(100.0, 150.0)
    pB = Point(220.0, 150.0)
    pC = Point(320.0, 150.0)
    pD = Point(440.0, 150.0)
    # Number line representations
    points = {"A": pA, "B": pB, "C": pC, "D": pD}
    segments = [
        ("A", "B", "#1f77b4"),  # P_1
        ("B", "C", "#ff7f0e"),  # P_2
        ("C", "D", "#2ca02c"),  # P_3
    ]
    steps = [
        ProofStep(
            step_number=1,
            action="Let A, B, C be the assigned prime numbers.",
            justification="Hypothesis",
            active_elements=["A", "B", "C"],
            description="Assume any finite collection of prime numbers P = {p1, p2, ..., pk}.",
        ),
        ProofStep(
            step_number=2,
            action="Take the least number measured by A, B, C, and let it be DE.",
            justification="Proposition VII.36",
            active_elements=["DE"],
            description="Compute the product M = p1 * p2 * ... * pk.",
        ),
        ProofStep(
            step_number=3,
            action="Add the unit DF to DE; then the whole EF is either prime or not.",
            justification="Definition VII.11",
            active_elements=["EF"],
            description="Construct N = M + 1.",
        ),
        ProofStep(
            step_number=4,
            action="First, let EF be prime; then prime numbers A, B, C, EF have been found which are more than A, B, C.",
            justification="Case 1",
            active_elements=["EF"],
            description="If N is prime, we have found a prime not in the original finite set P.",
        ),
        ProofStep(
            step_number=5,
            action="Next, let EF not be prime; then it must be measured by some prime number G.",
            justification="Proposition VII.31",
            active_elements=["G"],
            description="Every composite number has at least one prime divisor G.",
        ),
        ProofStep(
            step_number=6,
            action="I say that G is not the same with any of the numbers A, B, C. For if it were, since A, B, C measure DE, G would also measure DE. But it also measures EF, so it would measure the remainder, the unit DF: which is impossible.",
            justification="Proposition VII.28 & Common Notion 5",
            active_elements=["G"],
            description="If G were in P, it would divide M and (M + 1), hence divide 1, an impossibility.",
        ),
        ProofStep(
            step_number=7,
            action="Therefore G is a prime not identical with any of A, B, C. Therefore prime numbers are more than any assigned multitude of prime numbers.",
            justification="Conclusion (Q.E.D.)",
            active_elements=["G"],
            description="G is a prime outside P. Hence the set of prime numbers is infinite.",
        ),
    ]

    return Proposition(
        prop_id="Prop.IX.20",
        book=9,
        number=20,
        title="Proposition IX.20: Infinitude of Prime Numbers",
        statement="Prime numbers are more than any assigned multitude of prime numbers.",
        steps=steps,
        figure=GeometricFigure(points=points, segments=segments, circles=[], polygons=[]),
        qed_conclusion="ὅπερ ἔδει δεῖξαι — Which was to be demonstrated (Q.E.D.).",
    )

ALL_PROPOSITIONS: Dict[str, Proposition] = {
    "Prop.I.1": construct_proposition_1(),
    "Prop.I.9": construct_proposition_9(),
    "Prop.I.47": construct_proposition_47(),
    "Prop.IX.20": construct_proposition_ix_20(),
}
