import unittest
from hilbert.foundations import (
    HILBERT_GEOMETRY_AXIOMS,
    HILBERT_PROBLEMS_HIGHLIGHTS,
    HilbertSpaceEngine,
    HilbertVector,
)
from hilbert.visualizer import HilbertVisualizer
from hilbert.book import HilbertBookGenerator

class TestHilbert(unittest.TestCase):
    def test_cauchy_schwarz_inequality(self):
        v1 = HilbertVector([1.0, 2.0, 3.0, 4.0])
        v2 = HilbertVector([4.0, -1.0, 2.0, 0.5])
        valid, ip, bound = HilbertSpaceEngine.verify_cauchy_schwarz(v1, v2)
        self.assertTrue(valid)
        self.assertLessEqual(ip, bound)

    def test_parallelogram_law(self):
        v1 = HilbertVector([3.0, 1.0, -2.0])
        v2 = HilbertVector([1.0, 4.0, 5.0])
        valid, lhs, rhs = HilbertSpaceEngine.verify_parallelogram_law(v1, v2)
        self.assertTrue(valid)
        self.assertAlmostEqual(lhs, rhs, places=7)

    def test_gram_schmidt_orthonormalization(self):
        v1 = HilbertVector([1.0, 1.0, 0.0])
        v2 = HilbertVector([1.0, 0.0, 1.0])
        v3 = HilbertVector([0.0, 1.0, 1.0])
        ortho = HilbertSpaceEngine.gram_schmidt([v1, v2, v3])
        self.assertEqual(len(ortho), 3)

        # Each vector must have unit norm
        for u in ortho:
            self.assertAlmostEqual(u.norm(), 1.0, places=7)

        # Mutually orthogonal
        self.assertAlmostEqual(ortho[0].inner_product(ortho[1]), 0.0, places=7)
        self.assertAlmostEqual(ortho[0].inner_product(ortho[2]), 0.0, places=7)
        self.assertAlmostEqual(ortho[1].inner_product(ortho[2]), 0.0, places=7)

    def test_axioms_and_problems_registry(self):
        self.assertEqual(len(HILBERT_GEOMETRY_AXIOMS), 5)
        self.assertTrue(len(HILBERT_PROBLEMS_HIGHLIGHTS) >= 4)

    def test_visualizer_and_book_generation(self):
        vis = HilbertVisualizer()
        pasch = vis.render_pasch_axiom_svg()
        des = vis.render_desargues_svg()
        self.assertIn("<svg", pasch)
        self.assertIn("<svg", des)

        gen = HilbertBookGenerator()
        html = gen.generate_html()
        self.assertIn("David Hilbert", html)
        self.assertIn("Grundlagen der Geometrie", html)

if __name__ == "__main__":
    unittest.main()
