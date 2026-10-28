import unittest
from euclid.proofs import (
    ALL_PROPOSITIONS,
    construct_proposition_1,
    construct_proposition_9,
    construct_proposition_47,
    construct_proposition_ix_20,
)

class TestProofs(unittest.TestCase):
    def test_proposition_1_equilateral(self):
        prop = construct_proposition_1()
        self.assertEqual(prop.prop_id, "Prop.I.1")
        self.assertEqual(len(prop.steps), 7)
        # Verify equilateral side lengths
        pts = prop.figure.points
        ab = pts["A"].distance_to(pts["B"])
        ac = pts["A"].distance_to(pts["C"])
        bc = pts["B"].distance_to(pts["C"])
        self.assertAlmostEqual(ab, ac, places=4)
        self.assertAlmostEqual(ac, bc, places=4)

    def test_proposition_47_pythagorean(self):
        prop = construct_proposition_47()
        self.assertEqual(prop.prop_id, "Prop.I.47")
        pts = prop.figure.points
        ab = pts["A"].distance_to(pts["B"])
        ac = pts["A"].distance_to(pts["C"])
        bc = pts["B"].distance_to(pts["C"])
        # In right triangle ABC: AB^2 + AC^2 = BC^2
        self.assertAlmostEqual(ab**2 + ac**2, bc**2, places=4)

    def test_proposition_ix_20_prime_infinitude(self):
        prop = construct_proposition_ix_20()
        self.assertEqual(prop.prop_id, "Prop.IX.20")
        self.assertEqual(prop.book, 9)
        self.assertTrue(len(prop.steps) >= 5)

    def test_all_propositions_registry(self):
        self.assertIn("Prop.I.1", ALL_PROPOSITIONS)
        self.assertIn("Prop.I.47", ALL_PROPOSITIONS)
        self.assertIn("Prop.IX.20", ALL_PROPOSITIONS)

if __name__ == "__main__":
    unittest.main()
