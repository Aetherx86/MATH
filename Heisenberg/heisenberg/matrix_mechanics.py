import cmath
import math
from typing import List, Optional, Tuple

H_BAR = 1.054571817e-34  # Reduced Planck constant in J*s

class ComplexMatrix:
    """Zero-dependency pure Python square complex matrix engine."""
    def __init__(self, size: int, data: Optional[List[List[complex]]] = None):
        self.size = size
        if data is None:
            self.data = [[0j for _ in range(size)] for _ in range(size)]
        else:
            self.data = data

    @classmethod
    def identity(cls, size: int) -> "ComplexMatrix":
        mat = cls(size)
        for i in range(size):
            mat.data[i][i] = 1.0 + 0j
        return mat

    def __add__(self, other: "ComplexMatrix") -> "ComplexMatrix":
        res = ComplexMatrix(self.size)
        for i in range(self.size):
            for j in range(self.size):
                res.data[i][j] = self.data[i][j] + other.data[i][j]
        return res

    def __sub__(self, other: "ComplexMatrix") -> "ComplexMatrix":
        res = ComplexMatrix(self.size)
        for i in range(self.size):
            for j in range(self.size):
                res.data[i][j] = self.data[i][j] - other.data[i][j]
        return res

    def __mul__(self, other: "ComplexMatrix") -> "ComplexMatrix":
        res = ComplexMatrix(self.size)
        for i in range(self.size):
            for k in range(self.size):
                sik = self.data[i][k]
                if sik != 0:
                    for j in range(self.size):
                        res.data[i][j] += sik * other.data[k][j]
        return res

    def scale(self, scalar: complex) -> "ComplexMatrix":
        res = ComplexMatrix(self.size)
        for i in range(self.size):
            for j in range(self.size):
                res.data[i][j] = self.data[i][j] * scalar
        return res

    def conjugate_transpose(self) -> "ComplexMatrix":
        """Hermitian adjoint A^dagger."""
        res = ComplexMatrix(self.size)
        for i in range(self.size):
            for j in range(self.size):
                res.data[i][j] = self.data[j][i].conjugate()
        return res

    def commutator(self, other: "ComplexMatrix") -> "ComplexMatrix":
        """Lie bracket commutator [A, B] = A * B - B * A."""
        return (self * other) - (other * self)

    def is_hermitian(self, tol: float = 1e-10) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if abs(self.data[i][j] - self.data[j][i].conjugate()) > tol:
                    return False
        return True

    def trace(self) -> complex:
        return sum(self.data[i][i] for i in range(self.size))

class QuantumHarmonicOscillator:
    """
    Constructs Heisenberg's matrix mechanics operators for the Quantum Harmonic Oscillator
    using creation/annihilation ladder operators.
    """
    def __init__(self, n_states: int = 10, m: float = 1.0, omega: float = 1.0, hbar: float = 1.0):
        self.n = n_states
        self.m = m
        self.omega = omega
        self.hbar = hbar

        self.a = self._build_annihilation()
        self.a_dag = self.a.conjugate_transpose()
        self.X = self._build_position()
        self.P = self._build_momentum()
        self.H = self._build_hamiltonian()

    def _build_annihilation(self) -> ComplexMatrix:
        mat = ComplexMatrix(self.n)
        for i in range(self.n - 1):
            mat.data[i][i + 1] = math.sqrt(i + 1) + 0j
        return mat

    def _build_position(self) -> ComplexMatrix:
        """X = sqrt(hbar / (2 * m * omega)) * (a + a^dagger)."""
        factor = math.sqrt(self.hbar / (2.0 * self.m * self.omega))
        return (self.a + self.a_dag).scale(factor)

    def _build_momentum(self) -> ComplexMatrix:
        """P = i * sqrt(hbar * m * omega / 2) * (a^dagger - a)."""
        factor = 1j * math.sqrt((self.hbar * self.m * self.omega) / 2.0)
        return (self.a_dag - self.a).scale(factor)

    def _build_hamiltonian(self) -> ComplexMatrix:
        """H = hbar * omega * (a^dagger * a + 0.5 * I)."""
        num_op = self.a_dag * self.a
        id_op = ComplexMatrix.identity(self.n).scale(0.5)
        return (num_op + id_op).scale(self.hbar * self.omega)

class UncertaintyPrinciple:
    """Evaluates state expectation values and standard deviation products sigma_X * sigma_P."""
    @staticmethod
    def expectation_value(operator: ComplexMatrix, state: List[complex]) -> float:
        # <psi| A |psi>
        val = 0j
        for i in range(operator.size):
            row_sum = 0j
            for j in range(operator.size):
                row_sum += operator.data[i][j] * state[j]
            val += state[i].conjugate() * row_sum
        return val.real

    @classmethod
    def standard_deviation(cls, operator: ComplexMatrix, state: List[complex]) -> float:
        exp_a = cls.expectation_value(operator, state)
        op_sq = operator * operator
        exp_a2 = cls.expectation_value(op_sq, state)
        var = max(0.0, exp_a2 - exp_a**2)
        return math.sqrt(var)

    @classmethod
    def verify_uncertainty(cls, x_op: ComplexMatrix, p_op: ComplexMatrix, state: List[complex], hbar: float = 1.0) -> Tuple[bool, float, float]:
        """Validates sigma_X * sigma_P >= hbar / 2."""
        sx = cls.standard_deviation(x_op, state)
        sp = cls.standard_deviation(p_op, state)
        product = sx * sp
        bound = hbar / 2.0
        return product >= bound - 1e-10, product, bound
