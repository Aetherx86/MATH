from typing import List, Optional, Tuple
from .propositions import DiscreteImpulseStep

class PrincipiaVisualizer:
    """
    Renders vector diagrams of Newton's Principia Mathematica propositions
    and orbital trajectories in publication-quality SVG format.
    """
    def __init__(self, width: int = 600, height: int = 500):
        self.width = width
        self.height = height

    def render_proposition_1_svg(self, steps: List[DiscreteImpulseStep], origin_s: Tuple[float, float] = (300.0, 300.0)) -> str:
        sx, sy = origin_s
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
            f'width="100%" height="{self.height}" class="principia-svg">',
            '<rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#dcdcdc" stroke-width="1"/>'
        ]

        # Draw shaded triangular sectors to visualize equal areas
        palette = [
            "rgba(31, 119, 180, 0.20)",
            "rgba(255, 127, 14, 0.20)",
            "rgba(44, 160, 44, 0.20)",
            "rgba(214, 39, 40, 0.20)",
            "rgba(148, 103, 189, 0.20)",
            "rgba(140, 86, 75, 0.20)",
        ]

        for i in range(1, len(steps)):
            p_prev = steps[i - 1].position
            p_curr = steps[i].position
            color = palette[(i - 1) % len(palette)]
            pts = f"{sx:.1f},{sy:.1f} {p_prev[0]:.1f},{p_prev[1]:.1f} {p_curr[0]:.1f},{p_curr[1]:.1f}"
            svg.append(f'<polygon points="{pts}" fill="{color}" stroke="none"/>')

        # Radial lines from S to trajectory points
        for step in steps:
            px, py = step.position
            svg.append(
                f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                f'stroke="#888888" stroke-width="1.2" stroke-dasharray="3,3"/>'
            )

        # Draw virtual inertial points 'c', 'd'... and parallel deflection vectors
        for i, step in enumerate(steps):
            if step.inertial_projection:
                cx, cy = step.inertial_projection
                px, py = step.position
                prev_p = steps[i - 1].position
                # Dashed segment B -> c
                svg.append(
                    f'<line x1="{prev_p[0]:.1f}" y1="{prev_p[1]:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
                    f'stroke="#999999" stroke-width="1.5" stroke-dasharray="4,4"/>'
                )
                # Deflection line c -> C parallel to BS
                svg.append(
                    f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                    f'stroke="#d62728" stroke-width="1.8"/>'
                )
                # Label inertial projection point
                lbl = step.point_name.lower()
                svg.append(
                    f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#888888"/>'
                    f'<text x="{cx + 6:.1f}" y="{cy - 6:.1f}" font-family="serif" font-style="italic" font-size="13" fill="#666666">{lbl}</text>'
                )

        # Actual trajectory polygonal segments
        for i in range(1, len(steps)):
            p1 = steps[i - 1].position
            p2 = steps[i].position
            svg.append(
                f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
                f'stroke="#1a365d" stroke-width="2.8" stroke-linecap="round"/>'
            )

        # Draw Center of Force S
        svg.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6" fill="#b91c1c" stroke="#ffffff" stroke-width="2"/>'
            f'<text x="{sx + 10:.1f}" y="{sy + 5:.1f}" font-family="serif" font-weight="bold" font-size="16" fill="#b91c1c">S (Center of Force)</text>'
        )

        # Trajectory vertices and labels
        for step in steps:
            px, py = step.position
            svg.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="#1e3a8a" stroke="#ffffff" stroke-width="1.5"/>'
                f'<text x="{px + 8:.1f}" y="{py - 8:.1f}" font-family="serif" font-weight="bold" font-style="italic" font-size="14" fill="#1e3a8a">{step.point_name}</text>'
            )

        svg.append("</svg>")
        return "\n".join(svg)
