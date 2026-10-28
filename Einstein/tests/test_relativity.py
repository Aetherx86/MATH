import math
import unittest
from einstein.relativity import (
    C_LIGHT,
    G_GRAV,
    M_SUN,
    FourVector,
    GeneralRelativityEngine,
    LorentzBoost,
    RelativisticDynamics,
)
from einstein.visualizer import RelativityVisualizer
from einstein.book import EinsteinBookGenerator

class TestEinstein(unittest.TestCase):
    def test_lorentz_interval_invariance(self):
        v4 = FourVector(ct=10.0, x=6.0, y=3.0, z=-1.0)
        orig_interval = v4.spacetime_interval()

        # Boost along x with beta = 0.8
        boosted = LorentzBoost.boost_x(v4, beta=0.8)
        boosted_interval = boosted.spacetime_interval()

        # Spacetime interval must be identical
        self.assertAlmostEqual(orig_interval, boosted_interval, places=7)

    def test_mass_shell_invariance(self):
        m0 = 1.6726e-27  # Proton mass in kg
        v = 0.9 * C_LIGHT
        p, energy = RelativisticDynamics.momentum_energy(m0, v)
        diff = RelativisticDynamics.verify_mass_shell(m0, p, energy)
        # Difference relative to (m0 c^2)^2 should be near 0
        rel_diff = diff / ((m0 * (C_LIGHT**2))**2)
        self.assertLess(rel_diff, 1e-12)

    def test_schwarzschild_radius_sun(self):
        rs = GeneralRelativityEngine.schwarzschild_radius(M_SUN)
        # Solar Schwarzschild radius is ~2953 meters (2.95 km)
        self.assertAlmostEqual(rs / 1000.0, 2.953, places=2)

    def test_mercury_perihelion_precession(self):
        a_merc = 57.909e9
        e_merc = 0.20563
        dphi_rad = GeneralRelativityEngine.perihelion_precession_per_revolution(M_SUN, a_merc, e_merc)
        arcsec_rev = dphi_rad * (180.0 * 3600.0 / math.pi)
        arcsec_century = arcsec_rev * 415.20
        # Historical prediction of General Relativity for Mercury is ~43.0 arcsec / century
        self.assertAlmostEqual(arcsec_century, 43.0, delta=0.5)

    def test_gravitational_light_deflection(self):
        # Deflection at Sun's limb: R_sun = 6.9634e8 m
        r_sun = 6.9634e8
        deflection_rad = GeneralRelativityEngine.gravitational_light_deflection(M_SUN, r_sun)
        deflection_arcsec = deflection_rad * (180.0 * 3600.0 / math.pi)
        # Historic 1919 Eddington eclipse observation: ~1.75 arcseconds
        self.assertAlmostEqual(deflection_arcsec, 1.75, delta=0.05)

    def test_book_and_visualizer(self):
        vis = RelativityVisualizer()
        svg = vis.render_minkowski_diagram_svg(beta=0.5)
        self.assertIn("<svg", svg)
        gen = EinsteinBookGenerator()
        html = gen.generate_html()
        self.assertIn("Albert Einstein", html)
        self.assertIn("Schwarzschild Radius", html)

if __name__ == "__main__":
    unittest.main()
