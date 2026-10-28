import math
import unittest
from euclid.geometry import Circle, Line, Point, Polygon, Segment

class TestGeometry(unittest.TestCase):
    def test_point_distance_and_midpoint(self):
        p1 = Point(0.0, 0.0)
        p2 = Point(3.0, 4.0)
        self.assertEqual(p1.distance_to(p2), 5.0)
        mid = p1.midpoint_to(p2)
        self.assertEqual(mid, Point(1.5, 2.0))

    def test_line_intersection(self):
        # Line 1: through (0, 0) and (2, 2) -> x - y = 0
        l1 = Line.from_points(Point(0.0, 0.0), Point(2.0, 2.0))
        # Line 2: through (0, 2) and (2, 0) -> x + y - 2 = 0
        l2 = Line.from_points(Point(0.0, 2.0), Point(2.0, 0.0))
        inter = l1.intersect_line(l2)
        self.assertIsNotNone(inter)
        self.assertAlmostEqual(inter.x, 1.0)
        self.assertAlmostEqual(inter.y, 1.0)

    def test_circle_circle_intersection_prop1(self):
        # Construct equilateral triangle base points
        pA = Point(100.0, 200.0)
        pB = Point(300.0, 200.0)
        r = 200.0
        cA = Circle(pA, r)
        cB = Circle(pB, r)
        intersections = cA.intersect_circle(cB)
        self.assertEqual(len(intersections), 2)
        # Expected intersection y: 200 - sqrt(200^2 - 100^2) = 200 - 173.205 = 26.7949
        top_pt = min(intersections, key=lambda p: p.y)
        self.assertAlmostEqual(top_pt.x, 200.0)
        self.assertAlmostEqual(top_pt.y, 200.0 - 100.0 * math.sqrt(3), places=4)
        # Verify equilateral side lengths
        self.assertAlmostEqual(pA.distance_to(top_pt), 200.0, places=4)
        self.assertAlmostEqual(pB.distance_to(top_pt), 200.0, places=4)

    def test_polygon_shoelace_area(self):
        # Right triangle with base 3, height 4, area = 6.0
        poly = Polygon([Point(0.0, 0.0), Point(3.0, 0.0), Point(0.0, 4.0)])
        self.assertAlmostEqual(poly.area, 6.0)
        self.assertAlmostEqual(poly.perimeter, 12.0)

if __name__ == "__main__":
    unittest.main()
