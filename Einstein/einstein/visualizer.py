import math
from typing import List, Tuple

class RelativityVisualizer:
    """Renders vector diagrams of Minkowski spacetime and relativistic orbits in SVG."""
    def __init__(self, width: int = 600, height: int = 420):
        self.width = width
        self.height = height

    def render_minkowski_diagram_svg(self, beta: float = 0.6) -> str:
        cx, cy = self.width / 2.0, self.height / 2.0
        scale = 140.0
        g = 1.0 / math.sqrt(1.0 - beta**2)

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Minkowski Spacetime Diagram & Lorentz Boost (v/c = ' + f'{beta:.2f}' + ')</text>',
            # Light Cone lines (ct = ± x)
            f'<line x1="{cx - scale}" y1="{cy + scale}" x2="{cx + scale}" y2="{cy - scale}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4,4"/>',
            f'<line x1="{cx - scale}" y1="{cy - scale}" x2="{cx + scale}" y2="{cy + scale}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4,4"/>',
            '<text x="440" y="80" font-family="sans-serif" font-size="12" fill="#d97706">Light Cone (c = 1)</text>',
            # Rest frame axes ct and x
            f'<line x1="{cx}" y1="{cy + scale + 20}" x2="{cx}" y2="{cy - scale - 20}" stroke="#0f172a" stroke-width="2"/>',
            f'<line x1="{cx - scale - 20}" y1="{cy}" x2="{cx + scale + 20}" y2="{cy}" stroke="#0f172a" stroke-width="2"/>',
            f'<text x="{cx + 8}" y="{cy - scale - 25}" font-family="serif" font-weight="bold" font-size="15">ct</text>',
            f'<text x="{cx + scale + 25}" y="{cy + 15}" font-family="serif" font-weight="bold" font-size="15">x</text>',
            # Boosted frame axes ct' (slope = 1/beta -> dx/dct = beta) and x' (slope = beta -> dct/dx = beta)
            # ct' axis: x = beta * ct -> screen x = cx + beta * (cy - screen_y)
            f'<line x1="{cx - beta * scale}" y1="{cy + scale}" x2="{cx + beta * scale}" y2="{cy - scale}" stroke="#2563eb" stroke-width="2.5"/>',
            f'<text x="{cx + beta * scale + 8}" y="{cy - scale}" font-family="serif" font-weight="bold" font-size="15" fill="#2563eb">ct\'</text>',
            # x' axis: ct = beta * x -> screen_y = cy - beta * (screen_x - cx)
            f'<line x1="{cx - scale}" y1="{cy + beta * scale}" x2="{cx + scale}" y2="{cy - beta * scale}" stroke="#2563eb" stroke-width="2.5"/>',
            f'<text x="{cx + scale + 8}" y="{cy - beta * scale + 5}" font-family="serif" font-weight="bold" font-size="15" fill="#2563eb">x\'</text>',
            '</svg>'
        ]
        return "\n".join(svg)

    def render_precession_svg(self, trajectory: List[Tuple[float, float, float]]) -> str:
        cx, cy = self.width / 2.0, self.height / 2.0
        scale = 90.0

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#0f172a" rx="8" stroke="#334155" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#f8fafc">General Relativistic Precession of Perihelion (Rosette Orbit)</text>',
            # Central Star (Sun)
            f'<circle cx="{cx}" cy="{cy}" r="8" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>',
            f'<text x="{cx + 12}" y="{cy + 5}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#fbbf24">Sun</text>',
        ]

        # Draw trajectory
        points_str = " ".join([f"{cx + x * scale:.1f},{cy + y * scale:.1f}" for _, _, x, y in trajectory])
        svg.append(f'<polyline points="{points_str}" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-opacity="0.85"/>')

        svg.append('</svg>')
        return "\n".join(svg)
