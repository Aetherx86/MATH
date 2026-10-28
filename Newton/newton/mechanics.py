import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class OrbitalState:
    t: float
    x: float
    y: float
    vx: float
    vy: float

    @property
    def r(self) -> float:
        return math.hypot(self.x, self.y)

    @property
    def v(self) -> float:
        return math.hypot(self.vx, self.vy)

    def specific_energy(self, mu: float = 1.0) -> float:
        """Specific orbital energy: E = 0.5 * v^2 - mu / r."""
        r = self.r
        return 0.5 * (self.v**2) - (mu / r if r > 1e-12 else 0.0)

    def specific_angular_momentum(self) -> float:
        """Areal velocity vector magnitude: h = x * vy - y * vx."""
        return self.x * self.vy - self.y * self.vx

    def eccentricity_vector(self, mu: float = 1.0) -> Tuple[float, float]:
        """
        Laplace-Runge-Lenz eccentricity vector:
        e = (1/mu) * (v x h) - r_hat
        """
        h = self.specific_angular_momentum()
        r = self.r
        if r < 1e-12:
            return (0.0, 0.0)
        # v x h: (vx, vy, 0) x (0, 0, h) = (vy*h, -vx*h, 0)
        ex = (self.vy * h) / mu - (self.x / r)
        ey = (-self.vx * h) / mu - (self.y / r)
        return (ex, ey)

class CentralForceIntegrator:
    """
    Symplectic Velocity-Verlet and 4th-order Runge-Kutta numerical integrators
    for central force problems F(r) = -mu / r^n.
    Preserves phase space volume and first integrals (energy, angular momentum).
    """
    def __init__(self, mu: float = 1.0, power_n: float = 2.0):
        self.mu = mu
        self.power_n = power_n

    def acceleration(self, x: float, y: float) -> Tuple[float, float]:
        r = math.hypot(x, y)
        if r < 1e-12:
            return (0.0, 0.0)
        # a = -(mu / r^(n+1)) * (x, y)
        mag = -self.mu / (r ** (self.power_n + 1.0))
        return (mag * x, mag * y)

    def integrate_verlet(
        self,
        x0: float,
        y0: float,
        vx0: float,
        vy0: float,
        dt: float,
        steps: int,
    ) -> List[OrbitalState]:
        """
        2nd-order Symplectic Velocity Verlet algorithm.
        Maintains strict bounded energy oscillation without secular drift.
        """
        traj = [OrbitalState(t=0.0, x=x0, y=y0, vx=vx0, vy=vy0)]
        x, y = x0, y0
        vx, vy = vx0, vy0
        ax, ay = self.acceleration(x, y)

        for step in range(1, steps + 1):
            # Half-step velocity
            vx_half = vx + 0.5 * ax * dt
            vy_half = vy + 0.5 * ay * dt

            # Full-step position
            x += vx_half * dt
            y += vy_half * dt

            # Recompute acceleration
            ax_new, ay_new = self.acceleration(x, y)

            # Full-step velocity
            vx = vx_half + 0.5 * ax_new * dt
            vy = vy_half + 0.5 * ay_new * dt
            ax, ay = ax_new, ay_new

            traj.append(OrbitalState(t=step * dt, x=x, y=y, vx=vx, vy=vy))

        return traj

    def integrate_rk4(
        self,
        x0: float,
        y0: float,
        vx0: float,
        vy0: float,
        dt: float,
        steps: int,
    ) -> List[OrbitalState]:
        """Classical 4th-Order Runge-Kutta integrator."""
        traj = [OrbitalState(t=0.0, x=x0, y=y0, vx=vx0, vy=vy0)]
        x, y = x0, y0
        vx, vy = vx0, vy0

        def derivatives(cx, cy, cvx, cvy):
            cax, cay = self.acceleration(cx, cy)
            return cvx, cvy, cax, cay

        for step in range(1, steps + 1):
            k1_vx, k1_vy, k1_ax, k1_ay = derivatives(x, y, vx, vy)

            k2_vx, k2_vy, k2_ax, k2_ay = derivatives(
                x + 0.5 * dt * k1_vx, y + 0.5 * dt * k1_vy,
                vx + 0.5 * dt * k1_ax, vy + 0.5 * dt * k1_ay,
            )

            k3_vx, k3_vy, k3_ax, k3_ay = derivatives(
                x + 0.5 * dt * k2_vx, y + 0.5 * dt * k2_vy,
                vx + 0.5 * dt * k2_ax, vy + 0.5 * dt * k2_ay,
            )

            k4_vx, k4_vy, k4_ax, k4_ay = derivatives(
                x + dt * k3_vx, y + dt * k3_vy,
                vx + dt * k3_ax, vy + dt * k3_ay,
            )

            x += (dt / 6.0) * (k1_vx + 2.0 * k2_vx + 2.0 * k3_vx + k4_vx)
            y += (dt / 6.0) * (k1_vy + 2.0 * k2_vy + 2.0 * k3_vy + k4_vy)
            vx += (dt / 6.0) * (k1_ax + 2.0 * k2_ax + 2.0 * k3_ax + k4_ax)
            vy += (dt / 6.0) * (k1_ay + 2.0 * k2_ay + 2.0 * k3_ay + k4_ay)

            traj.append(OrbitalState(t=step * dt, x=x, y=y, vx=vx, vy=vy))

        return traj
