import math
import unittest
from newton.mechanics import CentralForceIntegrator, OrbitalState

class TestMechanics(unittest.TestCase):
    def test_orbital_state_energy_and_momentum(self):
        # Circular orbit at r = 1.0, v = 1.0, mu = 1.0
        st = OrbitalState(t=0.0, x=1.0, y=0.0, vx=0.0, vy=1.0)
        self.assertEqual(st.r, 1.0)
        self.assertEqual(st.v, 1.0)
        # E = 0.5 * 1^2 - 1/1 = -0.5
        self.assertAlmostEqual(st.specific_energy(mu=1.0), -0.5)
        # h = 1.0 * 1.0 - 0 = 1.0
        self.assertAlmostEqual(st.specific_angular_momentum(), 1.0)
        # Eccentricity should be 0 for circular orbit
        ex, ey = st.eccentricity_vector(mu=1.0)
        self.assertAlmostEqual(math.hypot(ex, ey), 0.0)

    def test_symplectic_verlet_conservation_laws(self):
        integrator = CentralForceIntegrator(mu=1.0, power_n=2.0)
        # Eccentric Keplerian orbit (e = 0.5, a = 1.0)
        e = 0.5
        r0 = 1.0 * (1.0 - e)  # 0.5
        v0 = math.sqrt(1.0 * (1.0 + e) / r0)  # sqrt(3.0) = 1.73205

        traj = integrator.integrate_verlet(x0=r0, y0=0.0, vx0=0.0, vy0=v0, dt=0.002, steps=3000)
        self.assertEqual(len(traj), 3001)

        e0 = traj[0].specific_energy()
        h0 = traj[0].specific_angular_momentum()

        for st in traj[::100]:
            # Angular momentum must be strictly conserved to machine precision
            self.assertAlmostEqual(st.specific_angular_momentum(), h0, places=9)
            # Energy must remain tightly bounded in symplectic Verlet
            rel_e_error = abs(st.specific_energy() - e0) / abs(e0)
            self.assertLess(rel_e_error, 1e-3)

    def test_rk4_integrator(self):
        integrator = CentralForceIntegrator(mu=1.0, power_n=2.0)
        traj = integrator.integrate_rk4(x0=1.0, y0=0.0, vx0=0.0, vy0=1.0, dt=0.01, steps=200)
        self.assertEqual(len(traj), 201)
        # Radius of circular orbit should stay near 1.0
        for st in traj:
            self.assertAlmostEqual(st.r, 1.0, delta=0.01)

if __name__ == "__main__":
    unittest.main()
