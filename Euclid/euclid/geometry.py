import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def midpoint_to(self, other: "Point") -> "Point":
        return Point((self.x + other.x) / 2.0, (self.y + other.y) / 2.0)

    def vector_to(self, other: "Point") -> Tuple[float, float]:
        return (other.x - self.x, other.y - self.y)

    def __add__(self, other: Tuple[float, float]) -> "Point":
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other: "Point") -> Tuple[float, float]:
        return (self.x - other.x, self.y - other.y)

@dataclass(frozen=True)
class Segment:
    p1: Point
    p2: Point

    @property
    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    @property
    def midpoint(self) -> Point:
        return self.p1.midpoint_to(self.p2)

@dataclass(frozen=True)
class Line:
    # ax + by + c = 0
    a: float
    b: float
    c: float

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> "Line":
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = p1.x * p2.y - p2.x * p1.y
        norm = math.hypot(a, b)
        if norm < 1e-12:
            raise ValueError("Distinct points required to define a straight line.")
        return cls(a / norm, b / norm, c / norm)

    def intersect_line(self, other: "Line") -> Optional[Point]:
        det = self.a * other.b - self.b * other.a
        if abs(det) < 1e-12:
            return None  # Parallel lines
        x = (self.b * other.c - self.c * other.b) / det
        y = (self.c * other.a - self.a * other.c) / det
        return Point(x, y)

@dataclass(frozen=True)
class Circle:
    center: Point
    radius: float

    def intersect_circle(self, other: "Circle") -> List[Point]:
        """
        Exact intersection of two circles (Compass-and-Straightedge operation).
        Used extensively in Euclid Book I (e.g. Proposition I.1).
        """
        d = self.center.distance_to(other.center)
        if d > self.radius + other.radius + 1e-12 or d < abs(self.radius - other.radius) - 1e-12 or d < 1e-12:
            return []  # No intersection or concentric

        # Distance along line of centers to radical axis
        a = (self.radius**2 - other.radius**2 + d**2) / (2.0 * d)
        h_sq = self.radius**2 - a**2
        h = math.sqrt(max(0.0, h_sq))

        # Midpoint on radical axis
        dx = (other.center.x - self.center.x) / d
        dy = (other.center.y - self.center.y) / d

        p_base = Point(self.center.x + a * dx, self.center.y + a * dy)

        if h < 1e-12:
            return [p_base]  # Tangent circles

        # Perpendicular offsets
        p1 = Point(p_base.x + h * (-dy), p_base.y + h * dx)
        p2 = Point(p_base.x - h * (-dy), p_base.y - h * dx)
        return [p1, p2]

    def intersect_line(self, line: Line) -> List[Point]:
        # Distance from center to line: |a*cx + b*cy + c| / sqrt(a^2 + b^2)
        dist = line.a * self.center.x + line.b * self.center.y + line.c
        if abs(dist) > self.radius + 1e-12:
            return []
        # Projection of center onto line
        proj_x = self.center.x - line.a * dist
        proj_y = self.center.y - line.b * dist
        h_sq = self.radius**2 - dist**2
        if h_sq <= 1e-12:
            return [Point(proj_x, proj_y)]
        h = math.sqrt(h_sq)
        # Tangent unit vector (-b, a)
        return [
            Point(proj_x - line.b * h, proj_y + line.a * h),
            Point(proj_x + line.b * h, proj_y - line.a * h),
        ]

@dataclass(frozen=True)
class Polygon:
    vertices: List[Point]

    @property
    def area(self) -> float:
        """Computes polygon area using the Surveyor's Shoelace formula."""
        n = len(self.vertices)
        if n < 3:
            return 0.0
        acc = 0.0
        for i in range(n):
            j = (i + 1) % n
            acc += self.vertices[i].x * self.vertices[j].y
            acc -= self.vertices[j].x * self.vertices[i].y
        return abs(acc) / 2.0

    @property
    def perimeter(self) -> float:
        n = len(self.vertices)
        return sum(self.vertices[i].distance_to(self.vertices[(i + 1) % n]) for i in range(n))
