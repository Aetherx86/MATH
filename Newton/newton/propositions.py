import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass(frozen=True)
class AxiomItem:
    identifier: str
    latin_title: str
    english_title: str
    latin_text: str
    english_text: str
    mathematical_formulation: str
    commentary: str

LAWS_OF_MOTION: List[AxiomItem] = [
    AxiomItem(
        identifier="Lex.I",
        latin_title="Lex I: Lex Inertiae",
        english_title="Law I: The Law of Inertia",
        latin_text="Corpus omne perseverare in statu suo quiescendi vel movendi uniformiter in directum, nisi quatenus a viribus impressis cogitur statum illum mutare.",
        english_text="Every body perseveres in its state of being at rest or of moving uniformly straight forward, except insofar as it is compelled to change its state by forces impressed.",
        mathematical_formulation="\\sum \\mathbf{F} = 0 \\implies \\frac{d\\mathbf{v}}{dt} = 0",
        commentary="Establishes inertial reference frames; velocity is an invariant vector in the absence of net external force.",
    ),
    AxiomItem(
        identifier="Lex.II",
        latin_title="Lex II: Lex Motus",
        english_title="Law II: Law of Motion and Force",
        latin_text="Mutationem motus proportionalem esse vi motrici impressae, et fieri secundum lineam rectam qua vis illa imprimitur.",
        english_text="A change in motion is proportional to the motive force impressed and takes place along the straight line in which that force is impressed.",
        mathematical_formulation="\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = m \\frac{d^2\\mathbf{r}}{dt^2}",
        commentary="Force is the temporal derivative of linear momentum p = mv. For constant mass, F = ma.",
    ),
    AxiomItem(
        identifier="Lex.III",
        latin_title="Lex III: Actio et Reactio",
        english_title="Law III: Action and Reaction",
        latin_text="Actioni contrariam semper et aequalem esse reactionem: sive corporum duorum actiones in se mutuo semper esse aequales et in partes contrarias dirigi.",
        english_text="To any action there is always an opposite and equal reaction; in other words, the mutual actions of two bodies upon each other are always equal and directed to contrary parts.",
        mathematical_formulation="\\mathbf{F}_{12} = -\\mathbf{F}_{21} \\implies \\frac{d}{dt}(\\mathbf{p}_1 + \\mathbf{p}_2) = 0",
        commentary="Guarantees the global conservation of total linear momentum for any isolated multi-body physical system.",
    ),
]

@dataclass
class NewtonProofStep:
    step_number: int
    statement: str
    geometric_justification: str
    analytical_relation: str

@dataclass
class DiscreteImpulseStep:
    time: float
    point_name: str
    position: Tuple[float, float]
    inertial_projection: Optional[Tuple[float, float]] # Point c where body would go without impulse
    impulse_vector: Tuple[float, float]
    triangle_area: float

@dataclass
class NewtonProposition:
    prop_id: str
    book: int
    number: int
    latin_title: str
    english_title: str
    enunciation: str
    steps: List[NewtonProofStep]
    qed_conclusion: str

def compute_proposition_1_discrete_impulses(
    r0: float = 200.0,
    v0: float = 140.0,
    mu: float = 3000000.0,
    delta_t: float = 0.5,
    num_steps: int = 6,
    origin_s: Tuple[float, float] = (300.0, 300.0),
) -> List[DiscreteImpulseStep]:
    """
    Constructs Newton's exact polygonal impulse sequence for Proposition 1.
    Shows that each triangle SAB, SBC, SCD... has identical area.
    """
    sx, sy = origin_s
    # Point A
    x_curr = sx + r0
    y_curr = sy
    vx = 0.0
    vy = -v0

    trajectory: List[DiscreteImpulseStep] = []

    # Step 0: Point A
    trajectory.append(DiscreteImpulseStep(
        time=0.0,
        point_name="A",
        position=(x_curr, y_curr),
        inertial_projection=None,
        impulse_vector=(0.0, 0.0),
        triangle_area=0.0,
    ))

    # Point B: move with constant velocity for delta_t
    x_b = x_curr + vx * delta_t
    y_b = y_curr + vy * delta_t
    area_sab = 0.5 * abs((x_curr - sx) * (y_b - sy) - (y_curr - sy) * (x_b - sx))

    trajectory.append(DiscreteImpulseStep(
        time=delta_t,
        point_name="B",
        position=(x_b, y_b),
        inertial_projection=None,
        impulse_vector=(0.0, 0.0),
        triangle_area=area_sab,
    ))

    curr_x, curr_y = x_b, y_b
    curr_vx, curr_vy = vx, vy
    point_labels = ["C", "D", "E", "F", "G", "H", "I", "J"]

    for i in range(min(num_steps - 2, len(point_labels))):
        name = point_labels[i]
        # Inertial continuation point c: where it would have arrived in delta_t without impulse
        c_x = curr_x + curr_vx * delta_t
        c_y = curr_y + curr_vy * delta_t

        # Central impulsive force toward S: delta_v along (S - current_pos)
        dx_s = sx - curr_x
        dy_s = sy - curr_y
        dist_s = math.hypot(dx_s, dy_s)
        force_mag = (mu / (dist_s**2)) * delta_t
        dvx = (dx_s / dist_s) * force_mag
        dvy = (dy_s / dist_s) * force_mag

        # New velocity after impulse at B
        curr_vx += dvx
        curr_vy += dvy

        # Actual arrival at point C
        next_x = curr_x + curr_vx * delta_t
        next_y = curr_y + curr_vy * delta_t

        # Triangle area with center S: Area = 0.5 * |r_1 x r_2|
        area = 0.5 * abs((curr_x - sx) * (next_y - sy) - (curr_y - sy) * (next_x - sx))

        trajectory.append(DiscreteImpulseStep(
            time=(i + 2) * delta_t,
            point_name=name,
            position=(next_x, next_y),
            inertial_projection=(c_x, c_y),
            impulse_vector=(dvx, dvy),
            triangle_area=area,
        ))

        curr_x, curr_y = next_x, next_y

    return trajectory

def get_principia_propositions() -> Dict[str, NewtonProposition]:
    prop1_steps = [
        NewtonProofStep(
            step_number=1,
            statement="Let the time be divided into equal parts, and in the first part of that time let the body describe the straight line AB.",
            geometric_justification="Law I (Uniform rectilinear motion in absence of impulse)",
            analytical_relation="\\mathbf{r}_B = \\mathbf{r}_A + \\mathbf{v}_1 \\Delta t",
        ),
        NewtonProofStep(
            step_number=2,
            statement="In the second part of time, if nothing hindered, it would go on directly to c, describing Bc equal to AB.",
            geometric_justification="Law I (Bc = AB along continuation of line)",
            analytical_relation="\\mathbf{r}_c = \\mathbf{r}_B + \\mathbf{v}_1 \\Delta t",
        ),
        NewtonProofStep(
            step_number=3,
            statement="Then triangles SAB and SBc are equal, since having equal bases AB and Bc they share the common vertex S and equal altitudes.",
            geometric_justification="Euclid Elements Book I, Proposition 38",
            analytical_relation="\\text{Area}(\\triangle SAB) = \\text{Area}(\\triangle SBc) = \\frac{1}{2}|\\mathbf{r}_A \\times \\mathbf{r}_B|",
        ),
        NewtonProofStep(
            step_number=4,
            statement="When the body arrives at B, let the centripetal force act with a single instantaneous impulse and compel it to deviate from line Bc into line BC.",
            geometric_justification="Law II (Impulse directed towards center S)",
            analytical_relation="\\Delta \\mathbf{v} \\parallel (\\mathbf{r}_S - \\mathbf{r}_B)",
        ),
        NewtonProofStep(
            step_number=5,
            statement="Through c draw cC parallel to BS meeting the line of motion at C. By composition of motion, the body at the end of the second time step arrives at C.",
            geometric_justification="Corollary 1 to Laws of Motion (Parallelogram of Forces)",
            analytical_relation="\\mathbf{r}_C = \\mathbf{r}_c + \\Delta \\mathbf{v} \\Delta t",
        ),
        NewtonProofStep(
            step_number=6,
            statement="Since cC is parallel to BS, triangles SBC and SBc lie on the same base SB and between the same parallels BS and cC; therefore triangle SBC equals triangle SBc.",
            geometric_justification="Euclid Elements Book I, Proposition 37",
            analytical_relation="\\text{Area}(\\triangle SBC) = \\text{Area}(\\triangle SBc)",
        ),
        NewtonProofStep(
            step_number=7,
            statement="Therefore triangle SBC is equal to triangle SAB. By identical reasoning, all subsequent triangles SCD, SDE, SEF are equal to one another.",
            geometric_justification="Common Notion 1 (Transitivity of equality)",
            analytical_relation="\\text{Area}(\\triangle SAB) = \\text{Area}(\\triangle SBC) = \\text{Area}(\\triangle SCD) = \\text{const}",
        ),
        NewtonProofStep(
            step_number=8,
            statement="Now let the number of triangles be multiplied and their width decreased indefinitely (Delta t -> 0). Their perimeter will form a continuous curve, and the areas swept out will be precisely proportional to the times.",
            geometric_justification="Book I, Section 1, Lemma III",
            analytical_relation="\\lim_{\\Delta t \\to 0} \\frac{\\Delta A}{\\Delta t} = \\frac{1}{2} |\\mathbf{r} \\times \\mathbf{v}| = \\frac{1}{2} h = \\text{const}",
        ),
    ]

    prop1 = NewtonProposition(
        prop_id="Prop.I.1",
        book=1,
        number=1,
        latin_title="Propositio I, Theorema I",
        english_title="Proposition 1, Theorem 1: Conservation of Areal Velocity",
        enunciation="The areas which bodies made to move in orbits describe by radii drawn to an unmoving center of forces are contained in unmoving planes and are proportional to the times.",
        steps=prop1_steps,
        qed_conclusion="Q.E.D. — Demonstrating Kepler's Second Law as a necessary deduction of centripetal force.",
    )

    prop11_steps = [
        NewtonProofStep(
            step_number=1,
            statement="Let the body revolve in an ellipse; it is required to find the law of the centripetal force directed to a focus S of the ellipse.",
            geometric_justification="Specification of Keplerian Ellipse with focus S",
            analytical_relation="r(\\theta) = \\frac{p}{1 + e \\cos \\theta}",
        ),
        NewtonProofStep(
            step_number=2,
            statement="From the general measure of centripetal force (Proposition VI), the force is reciprocally as the solid (SP^2 * QT^2) / QR.",
            geometric_justification="Proposition VI, Theorem 5",
            analytical_relation="F \\propto \\lim_{\\Delta t \\to 0} \\frac{QR}{SP^2 \\cdot QT^2}",
        ),
        NewtonProofStep(
            step_number=3,
            statement="By the geometric properties of the ellipse (conjugate diameters, focal property, and latus rectum L = 2b^2/a), the ratio (QR * 2a) / QT^2 converges to 2a / L = a^2 / b^2.",
            geometric_justification="Conic Sections: Apollonius Book III",
            analytical_relation="\\frac{L \\cdot QR}{QT^2} \\to 1 \\implies \\frac{QR}{QT^2} \\to \\frac{1}{L}",
        ),
        NewtonProofStep(
            step_number=4,
            statement="Multiplying both sides by SP^2, we obtain SP^2 * QT^2 / QR -> L * SP^2. Since L is a constant parameter of the orbit, the force is inversely proportional to SP^2.",
            geometric_justification="Conclusion",
            analytical_relation="F(r) = \\frac{\\mu}{SP^2} = \\frac{\\mu}{r^2}",
        ),
    ]

    prop11 = NewtonProposition(
        prop_id="Prop.I.11",
        book=1,
        number=11,
        latin_title="Propositio XI, Problema VI",
        english_title="Proposition 11, Problem 6: Inverse-Square Law for Elliptic Orbits",
        enunciation="If a body revolves in an ellipse; it is required to find the law of the centripetal force directed to a focus of the ellipse.",
        steps=prop11_steps,
        qed_conclusion="Q.E.I. — Proving that Kepler's First Law implies Newton's Inverse-Square Gravitational Law.",
    )

    return {"Prop.I.1": prop1, "Prop.I.11": prop11}
