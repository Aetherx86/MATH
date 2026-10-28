import unittest
from newton.propositions import (
    LAWS_OF_MOTION,
    compute_proposition_1_discrete_impulses,
    get_principia_propositions,
)

class TestPropositions(unittest.TestCase):
    def test_proposition_1_equal_areas_in_equal_times(self):
        # Compute discrete impulse steps of Proposition 1
        steps = compute_proposition_1_discrete_impulses(
            r0=200.0,
            v0=120.0,
            mu=2000000.0,
            delta_t=0.4,
            num_steps=6,
        )
        self.assertGreaterEqual(len(steps), 4)

        # In Proposition 1, every triangle area S-A-B, S-B-C, S-C-D... must be equal!
        # Step 1 is triangle SAB
        area_sab = steps[1].triangle_area
        self.assertGreater(area_sab, 0.0)

        for step in steps[2:]:
            # Area of triangle formed by each discrete impulse interval
            self.assertAlmostEqual(step.triangle_area, area_sab, places=5)

    def test_laws_of_motion_registry(self):
        self.assertEqual(len(LAWS_OF_MOTION), 3)
        identifiers = [l.identifier for l in LAWS_OF_MOTION]
        self.assertEqual(identifiers, ["Lex.I", "Lex.II", "Lex.III"])

    def test_principia_propositions_structure(self):
        props = get_principia_propositions()
        self.assertIn("Prop.I.1", props)
        self.assertIn("Prop.I.11", props)
        self.assertTrue(len(props["Prop.I.1"].steps) >= 5)
        self.assertTrue(len(props["Prop.I.11"].steps) >= 4)

if __name__ == "__main__":
    unittest.main()
