import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

C_LIGHT = 299792458.0  # Speed of light in m/s
G_GRAV = 6.67430e-11   # Gravitational constant in m^3 / (kg * s^2)
M_SUN = 1.98847e30     # Solar mass in kg

@dataclass(frozen=True)
class FourVector:
    """Minkowski 4-vector x^mu = (ct, x, y, z)."""
    ct: float
    x: float
    y: float
    z: float

    def spacetime_interval(self) -> float:
        """Minkowski metric interval ds^2 = -(ct)^2 + x^2 + y^2 + z^2."""
        return -(self.ct**2) + (self.x**2) + (self.y**2) + (self.z**2)

class LorentzBoost:
    """Special Relativistic Lorentz transformation engine."""
    @staticmethod
    def gamma(v_over_c: float) -> float:
        beta = v_over_c
        if abs(beta) >= 1.0:
            raise ValueError("Relativistic speed parameter |v/c| must be strictly less than 1.")
        return 1.0 / math.sqrt(1.0 - beta**2)

    @classmethod
    def boost_x(cls, v4: FourVector, beta: float) -> FourVector:
        """Boost along x-axis: ct' = gamma*(ct - beta*x), x' = gamma*(x - beta*ct)."""
        g = cls.gamma(beta)
        new_ct = g * (v4.ct - beta * v4.x)
        new_x = g * (v4.x - beta * v4.ct)
        return FourVector(ct=new_ct, x=new_x, y=v4.y, z=v4.z)

    @classmethod
    def time_dilation(cls, proper_time_tau: float, beta: float) -> float:
        return cls.gamma(beta) * proper_time_tau

    @classmethod
    def length_contraction(cls, rest_length_l0: float, beta: float) -> float:
        return rest_length_l0 / cls.gamma(beta)

class RelativisticDynamics:
    """Relativistic 4-momentum and invariant mass relations."""
    @classmethod
    def momentum_energy(cls, rest_mass_m0: float, v: float, c: float = C_LIGHT) -> Tuple[float, float]:
        beta = v / c
        g = LorentzBoost.gamma(beta)
        p = g * rest_mass_m0 * v
        energy = g * rest_mass_m0 * (c**2)
        return p, energy

    @classmethod
    def verify_mass_shell(cls, rest_mass_m0: float, p: float, energy: float, c: float = C_LIGHT) -> float:
        """Verifies E^2 - (p*c)^2 = (m0 * c^2)^2."""
        lhs = energy**2 - (p * c)**2
        rhs = (rest_mass_m0 * (c**2))**2
        return abs(lhs - rhs)

class GeneralRelativityEngine:
    """General Relativistic spacetime geometry and geodesic solvers."""
    @staticmethod
    def schwarzschild_radius(mass_m: float, g_const: float = G_GRAV, c_light: float = C_LIGHT) -> float:
        """r_s = 2 * G * M / c^2."""
        return (2.0 * g_const * mass_m) / (c_light**2)

    @classmethod
    def perihelion_precession_per_revolution(
        cls,
        mass_m: float,
        semi_major_axis_a: float,
        eccentricity_e: float,
        g_const: float = G_GRAV,
        c_light: float = C_LIGHT,
    ) -> float:
        """
        Anomalous relativistic perihelion advance (Einstein 1915):
        delta_phi = 6 * pi * G * M / (c^2 * a * (1 - e^2)) in radians per revolution.
        """
        num = 6.0 * math.pi * g_const * mass_m
        denom = (c_light**2) * semi_major_axis_a * (1.0 - eccentricity_e**2)
        return num / denom

    @classmethod
    def gravitational_light_deflection(
        cls,
        mass_m: float,
        impact_parameter_r: float,
        g_const: float = G_GRAV,
        c_light: float = C_LIGHT,
    ) -> float:
        """Einstein light bending: delta_theta = 4 * G * M / (c^2 * R)."""
        return (4.0 * g_const * mass_m) / ((c_light**2) * impact_parameter_r)

    @classmethod
    def integrate_relativistic_orbit(
        cls,
        a: float = 1.0,
        e: float = 0.5,
        gr_perturbation_scale: float = 0.015, # Stable relativistic precession parameter
        num_orbits: int = 3,
        steps_per_orbit: int = 720,
    ) -> List[Tuple[float, float, float]]: # (phi, r, x, y)
        """
        Integrates the relativistic Binet orbit equation:
        d^2 u / dphi^2 + u = 1/p + 3 * (GM/c^2) * u^2
        """
        p = a * (1.0 - e**2)
        u = (1.0 + e) / p  # At perihelion phi=0, u is maximal
        du = 0.0
        dphi = (2.0 * math.pi) / steps_per_orbit
        total_steps = num_orbits * steps_per_orbit

        trajectory = []
        phi = 0.0

        for _ in range(total_steps):
            r = 1.0 / u if u > 1e-12 else 1e12
            x = r * math.cos(phi)
            y = r * math.sin(phi)
            trajectory.append((phi, r, x, y))

            # Symplectic Velocity Verlet for Binet equation
            d2u = (1.0 / p) - u + 3.0 * gr_perturbation_scale * (u**2)
            du += 0.5 * d2u * dphi
            u += du * dphi
            d2u_new = (1.0 / p) - u + 3.0 * gr_perturbation_scale * (u**2)
            du += 0.5 * d2u_new * dphi
            phi += dphi

        return trajectory
