from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class AxiomaticItem:
    identifier: str
    title: str
    greek_text: str
    english_text: str
    commentary: str

DEFINITIONS_BOOK_I: List[AxiomaticItem] = [
    AxiomaticItem(
        identifier="Def.I.1",
        title="Definition 1: Point",
        greek_text="Σημεῖόν ἐστιν, οὗ μέρος οὐθέν.",
        english_text="A point is that which has no part.",
        commentary="An indivisible, zero-dimensional location in space having position without magnitude.",
    ),
    AxiomaticItem(
        identifier="Def.I.2",
        title="Definition 2: Line",
        greek_text="Γραμμὴ δὲ μῆκος ἀπλατές.",
        english_text="A line is breadthless length.",
        commentary="A one-dimensional continuum possessing length but neither breadth nor thickness.",
    ),
    AxiomaticItem(
        identifier="Def.I.4",
        title="Definition 4: Straight Line",
        greek_text="Εὐθεῖα γραμμή ἐστιν, ἥτις ἐξ ἴσου τοῖς ἐφ' ἑαυτῆς σημείοις κεῖται.",
        english_text="A straight line is a line which lies evenly with the points on itself.",
        commentary="The shortest geodesic path connecting any two points in planar space.",
    ),
    AxiomaticItem(
        identifier="Def.I.10",
        title="Definition 10: Right Angle",
        greek_text="Ὅταν δὲ εὐθεῖα ἐπ' εὐθεῖαν σταθεῖσα τὰς ἐφεξῆς γωνίας ἴσας ἀλλήλαις ποιῇ...",
        english_text="When a straight line set up on a straight line makes the adjacent angles equal to one another, each of the equal angles is right.",
        commentary="An angle subtending exactly one quarter of a full planar revolution (pi/2 radians or 90 degrees).",
    ),
    AxiomaticItem(
        identifier="Def.I.15",
        title="Definition 15: Circle",
        greek_text="Κύκλος ἐστὶ σχῆμα ἐπίπεδον ὑπὸ μιᾶς γραμμῆς περιεχόμενον...",
        english_text="A circle is a plane figure contained by one line such that all straight lines falling upon it from one point among those lying within the figure equal one another.",
        commentary="The locus of all planar points equidistant from a central point.",
    ),
    AxiomaticItem(
        identifier="Def.I.23",
        title="Definition 23: Parallel Lines",
        greek_text="Παράλληλοί εἰσιν εὐθεῖαι, αἵτινες ἐν τῷ αὐτῷ ἐπιπέδῳ οὖσαι...",
        english_text="Parallel straight lines are straight lines which, being in the same plane and being produced indefinitely in both directions, do not meet one another in either direction.",
        commentary="Coplanar lines maintaining constant separation that never intersect even when extended to infinity.",
    ),
]

POSTULATES: List[AxiomaticItem] = [
    AxiomaticItem(
        identifier="Post.1",
        title="Postulate 1: Straight Line between Two Points",
        greek_text="Ἠιτήσθω ἀπὸ παντὸς σημείου ἐπὶ πᾶν σημεῖον εὐθεῖαν γραμμὴν ἀγαγεῖν.",
        english_text="To draw a straight line from any point to any point.",
        commentary="Given any two points, a straight line segment can be constructed connecting them (Ruler postulate).",
    ),
    AxiomaticItem(
        identifier="Post.2",
        title="Postulate 2: Continuous Extension",
        greek_text="Καὶ πεπερασμένην εὐθεῖαν κατὰ τὸ συνεχὲς ἐπ' εὐθείας ἐκβαλεῖν.",
        english_text="To produce a finite straight line continuously in a straight line.",
        commentary="Any finite segment can be extended continuously in either direction indefinitely.",
    ),
    AxiomaticItem(
        identifier="Post.3",
        title="Postulate 3: Circle Construction",
        greek_text="Καὶ παντὶ κέντρῳ καὶ διαστήματι κύκλον γράφεσθαι.",
        english_text="To describe a circle with any center and distance.",
        commentary="Given a center point and a radius segment, a circle can be described (Compass postulate).",
    ),
    AxiomaticItem(
        identifier="Post.4",
        title="Postulate 4: Equality of Right Angles",
        greek_text="Καὶ πάσας τὰς ὀρθὰς γωνίας ἴσας ἀλλήλαις εἶναι.",
        english_text="That all right angles equal one another.",
        commentary="Establishes the uniformity and isotropy of Euclidean planar space.",
    ),
    AxiomaticItem(
        identifier="Post.5",
        title="Postulate 5: The Parallel Postulate",
        greek_text="Καὶ ἐὰν εἰς δύο εὐθείας εὐθεῖα ἐμπίπτουσα τὰς ἐντὸς καὶ ἐπὶ τὰ αὐτὰ μέρη γωνίας δύο ὀρθῶν ἐλάσσονας ποιῇ...",
        english_text="That, if a straight line falling on two straight lines makes the interior angles on the same side less than two right angles, the two straight lines, if produced indefinitely, meet on that side on which the angles are less than two right angles.",
        commentary="The cornerstone of Euclidean geometry, distinguishing it from spherical and hyperbolic non-Euclidean geometries.",
    ),
]

COMMON_NOTIONS: List[AxiomaticItem] = [
    AxiomaticItem(
        identifier="CN.1",
        title="Common Notion 1: Transitivity of Equality",
        greek_text="Τὰ τῷ αὐτῷ ἴσα καὶ ἀλλήλοις ἐστὶν ἴσα.",
        english_text="Things which equal the same thing also equal one another.",
        commentary="Transitivity: if A = B and B = C, then A = C.",
    ),
    AxiomaticItem(
        identifier="CN.2",
        title="Common Notion 2: Addition of Equals",
        greek_text="Καὶ ἐὰν ἴσοις ἴσα προστεθῇ, τὰ ὅλα ἐστὶν ἴσα.",
        english_text="If equals are added to equals, then the wholes are equal.",
        commentary="Additive congruence: if A = B and C = D, then A + C = B + D.",
    ),
    AxiomaticItem(
        identifier="CN.3",
        title="Common Notion 3: Subtraction of Equals",
        greek_text="Καὶ ἐὰν ἀπὸ ἴσων ἴσα ἀφαιρεθῇ, τὰ καταλειπόμενά ἐστιν ἴσα.",
        english_text="If equals are subtracted from equals, then the remainders are equal.",
        commentary="Subtractive congruence: if A = B and C = D, then A - C = B - D.",
    ),
    AxiomaticItem(
        identifier="CN.4",
        title="Common Notion 4: Superposition and Coincidence",
        greek_text="Καὶ τὰ ἐφαρμόζοντα ἐπ' ἄλληλα ἴσα ἀλλήλοις ἐστίν.",
        english_text="Things which coincide with one another equal one another.",
        commentary="Rigid motion / isometry invariance: figures that can be superposed onto each other are congruent.",
    ),
    AxiomaticItem(
        identifier="CN.5",
        title="Common Notion 5: Whole and Part",
        greek_text="Καὶ τὸ ὅλον τοῦ μέρους μεῖζον.",
        english_text="The whole is greater than the part.",
        commentary="Order property: if B is a proper part of A, then A > B.",
    ),
]
