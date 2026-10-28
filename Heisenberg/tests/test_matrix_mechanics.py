import math
import unittest
from heisenberg.matrix_mechanics import (
    ComplexMatrix,
    QuantumHarmonicOscillator,
    UncertaintyPrinciple,
)
from heisenberg.visualizer import HeisenbergVisualizer
from heisenberg.book import HeisenbergBookGenerator

class TestHeisenberg(unittest.TestCase):
    def test_matrix_operations_and_hermiticity(self):
        qho = QuantumHarmonicOscillator(n_states=6, hbar=1.0, omega=1.0)
        # Position X, Momentum P, and Hamiltonian H must be Hermitian operators
        self.assertTrue(qho.X.is_hermitian())
        self.assertTrue(qho.P.is_hermitian())
        self.assertTrue(qho.H.is_hermitian())

    def test_canonical_commutation_relation(self):
        # [X, P] = i * hbar * I for truncated interior states
        qho = QuantumHarmonicOscillator(n_states=8, hbar=1.0)
        comm = qho.X.commutator(qho.P)
        # Interior diagonal elements [i, i] (i < n - 1) must equal 1.0j
        for i in range(qho.n - 1):
            val = comm.data[i][i]
            self.assertAlmostEqual(val.real, 0.0, places=7)
            self.assertAlmostEqual(val.imag, 1.0, places=7)

    def test_harmonic_oscillator_eigenvalues(self):
        omega = 2.5
        hbar = 1.0
        qho = QuantumHarmonicOscillator(n_states=6, omega=omega, hbar=hbar)
        # H is diagonal in the number basis, H[n][n] = (n + 0.5) * hbar * omega
        for n in range(qho.n):
            expected_e = (n + 0.5) * hbar * omega
            actual_e = qho.H.data[n][n].real
            self.assertAlmostEqual(actual_e, expected_e, places=7)

    def test_uncertainty_principle_ground_state(self):
        qho = QuantumHarmonicOscillator(n_states=8, hbar=1.0, omega=1.0)
        # Ground state |0> = [1, 0, 0, ...]
        ground_state = [1.0 + 0j] + [0j] * (qho.n - 1)

        valid, prod, bound = UncertaintyPrinciple.verify_uncertainty(qho.X, qho.P, ground_state, hbar=1.0)
        self.assertTrue(valid)
        # Ground state is minimum uncertainty wavepacket: sigma_X * sigma_P = hbar / 2 = 0.5
        self.assertAlmostEqual(prod, 0.5, places=7)
        self.assertEqual(bound, 0.5)

    def test_uncertainty_first_excited_state(self):
        qho = QuantumHarmonicOscillator(n_states=8, hbar=1.0, omega=1.0)
        # First excited state |1> = [0, 1, 0, ...]
        excited_state = [0j, 1.0 + 0j] + [0j] * (qho.n - 2)

        valid, prod, bound = UncertaintyPrinciple.verify_uncertainty(qho.X, qho.P, excited_state, hbar=1.0)
        self.assertTrue(valid)
        # For n=1, sigma_X * sigma_P = (n + 0.5) * hbar = 1.5 > 0.5
        self.assertAlmostEqual(prod, 1.5, places=7)

    def test_book_and_visualizer(self):
        vis = HeisenbergVisualizer()
        qho = QuantumHarmonicOscillator(n_states=5)
        comm = qho.X.commutator(qho.P)
        svg1 = vis.render_commutator_heatmap_svg(comm)
        svg2 = vis.render_uncertainty_gaussian_svg()
        self.assertIn("<svg", svg1)
        self.assertIn("<svg", svg2)

        gen = HeisenbergBookGenerator()
        html = gen.generate_html()
        self.assertIn("Werner Heisenberg", html)
        self.assertIn("Matrix Mechanics", html)

if __name__ == "__main__":
    unittest.main()
