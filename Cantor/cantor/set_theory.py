import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Set, Tuple

class CantorPairing:
    """
    Cantor's polynomial pairing bijection between N x N and N.
    pi(k1, k2) = 0.5 * (k1 + k2) * (k1 + k2 + 1) + k2.
    Proves that |N x N| = |Q| = aleph_0.
    """
    @staticmethod
    def pair(k1: int, k2: int) -> int:
        if k1 < 0 or k2 < 0:
            raise ValueError("Cantor pairing is defined for non-negative integers.")
        return ((k1 + k2) * (k1 + k2 + 1)) // 2 + k2

    @staticmethod
    def unpair(z: int) -> Tuple[int, int]:
        if z < 0:
            raise ValueError("z must be a non-negative integer.")
        # w = floor((sqrt(8z + 1) - 1) / 2)
        w = int((math.isqrt(8 * z + 1) - 1) // 2)
        t = (w * (w + 1)) // 2
        k2 = z - t
        k1 = w - k2
        return (k1, k2)

class Diagonalization:
    """
    Cantor's Diagonal Argument (1891).
    Given an arbitrary enumerable list of real numbers in (0, 1) represented as infinite digit expansions,
    constructs an anti-diagonal real number differing from every element in the list at index i.
    """
    @staticmethod
    def diagonalize_binary(sequences: List[str]) -> str:
        """Constructs an anti-diagonal binary sequence differing from s_i at bit i."""
        anti_diag = []
        for i, seq in enumerate(sequences):
            bit = seq[i] if i < len(seq) else "0"
            # Flip bit: 0 -> 1, 1 -> 0
            anti_diag.append("1" if bit == "0" else "0")
        return "".join(anti_diag)

    @staticmethod
    def diagonalize_decimal(sequences: List[str]) -> str:
        """
        Constructs a decimal expansion differing from sequence i at position i.
        Avoids 0 and 9 to eliminate 0.999... = 1.0 representation ambiguities.
        """
        anti_diag = []
        for i, seq in enumerate(sequences):
            digit = int(seq[i]) if i < len(seq) and seq[i].isdigit() else 0
            # If digit is 5, choose 4; otherwise choose 5
            anti_diag.append("4" if digit == 5 else "5")
        return "".join(anti_diag)

@dataclass(frozen=True)
class Interval:
    left: float
    right: float

    @property
    def length(self) -> float:
        return self.right - self.left

    def remove_middle_third(self) -> Tuple["Interval", "Interval"]:
        l = self.length / 3.0
        return (
            Interval(self.left, self.left + l),
            Interval(self.right - l, self.right),
        )

class CantorTernarySet:
    """
    The Cantor Ternary Set C in [0, 1].
    Formed by recursively deleting the open middle third of each interval.
    Total remaining Lebesgue measure at stage k: (2/3)^k -> 0.
    Hausdorff dimension: log(2) / log(3) ≈ 0.6309.
    Cardinality: uncountable continuum (c = 2^aleph_0).
    """
    @classmethod
    def generate_stages(cls, depth: int = 5) -> List[List[Interval]]:
        stages: List[List[Interval]] = [[Interval(0.0, 1.0)]]
        for d in range(1, depth + 1):
            prev = stages[-1]
            curr = []
            for interval in prev:
                left, right = interval.remove_middle_third()
                curr.append(left)
                curr.append(right)
            stages.append(curr)
        return stages

    @classmethod
    def total_measure(cls, intervals: List[Interval]) -> float:
        return sum(inv.length for inv in intervals)

class PowerSetTheorem:
    """
    Cantor's Theorem: |S| < |P(S)|.
    Given any function f: S -> P(S), constructs the diagonal witness subset
    D = { x in S : x not in f(x) } which cannot be in the image of f.
    """
    @staticmethod
    def diagonal_witness(domain: Set[str], mapping: Callable[[str], Set[str]]) -> Set[str]:
        # D = { x in S : x not in f(x) }
        return {x for x in domain if x not in mapping(x)}
