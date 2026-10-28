import unittest
from newton.book import PrincipiaBookGenerator
from newton.propositions import compute_proposition_1_discrete_impulses
from newton.visualizer import PrincipiaVisualizer

class TestBook(unittest.TestCase):
    def test_visualizer_svg_rendering(self):
        vis = PrincipiaVisualizer(width=500, height=400)
        steps = compute_proposition_1_discrete_impulses(num_steps=5)
        svg = vis.render_proposition_1_svg(steps)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Center of Force", svg)
        self.assertIn("polygon", svg)

    def test_book_html_generation(self):
        gen = PrincipiaBookGenerator()
        html_out = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html_out)
        self.assertIn("Philosophiae Naturalis Principia Mathematica", html_out)
        self.assertIn("Axiomata sive Leges Motus", html_out)
        self.assertIn("orbitCanvas", html_out)
        self.assertIn("Symplectic", html_out)

if __name__ == "__main__":
    unittest.main()
