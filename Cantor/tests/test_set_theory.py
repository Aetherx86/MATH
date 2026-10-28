import unittest
from cantor.set_theory import CantorPairing, CantorTernarySet, Diagonalization, PowerSetTheorem
from cantor.visualizer import CantorVisualizer
from cantor.book import CantorBookGenerator

class TestCantor(unittest.TestCase):
    def test_cantor_pairing_bijection(self):
        for x in range(15):
            for y in range(15):
                z = CantorPairing.pair(x, y)
                rx, ry = CantorPairing.unpair(z)
                self.assertEqual((rx, ry), (x, y))

    def test_diagonalization_binary(self):
        seqs = [
            "000000",
            "111111",
            "010101",
            "101010",
        ]
        witness = Diagonalization.diagonalize_binary(seqs)
        self.assertEqual(len(witness), 4)
        for i, s in enumerate(seqs):
            self.assertNotEqual(witness[i], s[i])

    def test_cantor_ternary_set_measure(self):
        stages = CantorTernarySet.generate_stages(depth=4)
        self.assertEqual(len(stages), 5)  # depth 0 to 4
        # Stage 0: 1 interval, len 1.0
        self.assertEqual(CantorTernarySet.total_measure(stages[0]), 1.0)
        # Stage 4: 2^4 = 16 intervals, measure (2/3)^4 = 16/81 = 0.19753...
        m4 = CantorTernarySet.total_measure(stages[4])
        self.assertAlmostEqual(m4, (2.0 / 3.0)**4, places=6)

    def test_power_set_theorem(self):
        domain = {"a", "b", "c"}
        # Attempted mapping f
        mapping = {
            "a": {"b", "c"},
            "b": {"b"},
            "c": set(),
        }
        witness = PowerSetTheorem.diagonal_witness(domain, lambda x: mapping[x])
        # "a" not in {"b", "c"} -> a in witness
        # "b" in {"b"} -> b not in witness
        # "c" not in set() -> c in witness
        self.assertEqual(witness, {"a", "c"})
        # Verify witness cannot equal f(x) for any x in domain
        for x in domain:
            self.assertNotEqual(witness, mapping[x])

    def test_book_and_visualizer(self):
        vis = CantorVisualizer()
        svg = vis.render_diagonal_matrix_svg(["01", "10"], "11")
        self.assertIn("<svg", svg)
        gen = CantorBookGenerator()
        html = gen.generate_html()
        self.assertIn("Georg Cantor", html)
        self.assertIn("Transfinite Set Theory", html)

if __name__ == "__main__":
    unittest.main()
