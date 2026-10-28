import math
from typing import List
from .matrix_mechanics import ComplexMatrix

class HeisenbergVisualizer:
    """Renders vector diagrams of matrix mechanics and quantum uncertainty in SVG."""
    def __init__(self, width: int = 600, height: int = 400):
        self.width = width
        self.height = height

    def render_commutator_heatmap_svg(self, comm_matrix: ComplexMatrix) -> str:
        size = min(comm_matrix.size, 8)
        cell_size = 46
        start_x = (self.width - size * cell_size) / 2.0
        start_y = 75

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Canonical Commutator Matrix [X, P] (Imaginary Parts)</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">Theoretical interior diagonal elements equal +1.00 i (&#8463; = 1.0)</text>',
        ]

        for i in range(size):
            y = start_y + i * cell_size
            for j in range(size):
                x = start_x + j * cell_size
                val = comm_matrix.data[i][j].imag
                if abs(val - 1.0) < 0.05:
                    fill = "#dbeafe"
                    text_color = "#1d4ed8"
                elif abs(val) > 0.05:
                    fill = "#fee2e2"
                    text_color = "#b91c1c"
                else:
                    fill = "#f8fafc"
                    text_color = "#94a3b8"

                svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" fill="{fill}" stroke="#cbd5e1" stroke-width="1"/>')
                svg.append(f'<text x="{x + cell_size / 2.0:.1f}" y="{y + cell_size / 2.0 + 4:.1f}" text-anchor="middle" font-family="monospace" font-size="11" fill="{text_color}">{val:+.2f}i</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_uncertainty_gaussian_svg(self, sigma_x: float = 1.0, sigma_p: float = 0.5) -> str:
        cx1, cy = 160.0, 220.0
        cx2 = 440.0
        scale_y = 120.0

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Conjugate Position &amp; Momentum Wavepacket Distributions</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">&Delta;x &middot; &Delta;p = ' + f'{sigma_x * sigma_p:.3f}' + ' &ge; &#8463;/2 = 0.500</text>',
            # Position distribution
            f'<text x="{cx1 - 60}" y="{cy - 120}" font-family="sans-serif" font-weight="bold" font-size="13" fill="#2563eb">Position |&psi;(x)|^2 (&sigma;_x = {sigma_x:.2f})</text>',
            f'<line x1="{cx1 - 120}" y1="{cy}" x2="{cx1 + 120}" y2="{cy}" stroke="#64748b" stroke-width="1.5"/>',
            f'<line x1="{cx1}" y1="{cy - 100}" x2="{cx1}" y2="{cy + 20}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>',
        ]

        pts1 = []
        for step in range(-50, 51):
            x_val = step / 15.0
            prob = math.exp(-0.5 * (x_val / sigma_x)**2)
            pts1.append(f"{cx1 + x_val * 35.0:.1f},{cy - prob * scale_y:.1f}")
        svg.append(f'<polyline points="{" ".join(pts1)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')

        # Momentum distribution
        svg.append(f'<text x="{cx2 - 60}" y="{cy - 120}" font-family="sans-serif" font-weight="bold" font-size="13" fill="#dc2626">Momentum |&phi;(p)|^2 (&sigma;_p = {sigma_p:.2f})</text>')
        svg.append(f'<line x1="{cx2 - 120}" y1="{cy}" x2="{cx2 + 120}" y2="{cy}" stroke="#64748b" stroke-width="1.5"/>')
        svg.append(f'<line x1="{cx2}" y1="{cy - 100}" x2="{cx2}" y2="{cy + 20}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>')

        pts2 = []
        for step in range(-50, 51):
            p_val = step / 15.0
            prob = math.exp(-0.5 * (p_val / sigma_p)**2)
            pts2.append(f"{cx2 + p_val * 35.0:.1f},{cy - prob * scale_y:.1f}")
        svg.append(f'<polyline points="{" ".join(pts2)}" fill="none" stroke="#dc2626" stroke-width="2.5"/>')

        svg.append('</svg>')
        return "\n".join(svg)
