import unittest
from euclid.book import BookGenerator
from euclid.visualizer import SVGVisualizer
from euclid.proofs import construct_proposition_1

class TestBook(unittest.TestCase):
    def test_svg_visualizer(self):
        vis = SVGVisualizer(width=400, height=300)
        prop = construct_proposition_1()
        svg = vis.render_figure(prop.figure)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("polygon", svg)
        self.assertIn("circle", svg)
        self.assertIn("line", svg)

    def test_book_html_generation(self):
        gen = BookGenerator()
        html_out = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html_out)
        self.assertIn("Euclid's Elements", html_out)
        self.assertIn("The Five Postulates", html_out)
        self.assertIn("Common Notions", html_out)
        self.assertIn("Prop.I.47", html_out)
        self.assertIn("euclidCanvas", html_out)

if __name__ == "__main__":
    unittest.main()
