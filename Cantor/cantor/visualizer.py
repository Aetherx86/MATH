from typing import List, Tuple
from .set_theory import CantorPairing, CantorTernarySet, Diagonalization, Interval

class CantorVisualizer:
    """Renders vector diagrams of Cantor's transfinite constructions in SVG format."""
    def __init__(self, width: int = 650, height: int = 400):
        self.width = width
        self.height = height

    def render_diagonal_matrix_svg(self, sequences: List[str], anti_diagonal: str) -> str:
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
            f'width="100%" height="{self.height}" class="cantor-svg">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="35" font-family="sans-serif" font-weight="bold" font-size="16" fill="#1e293b">Cantor\'s Diagonal Construction (Anti-Diagonal Witness)</text>',
        ]

        n = min(len(sequences), 8)
        start_y = 70
        row_height = 32

        for i in range(n):
            seq = sequences[i][:n]
            y = start_y + i * row_height
            svg.append(f'<text x="30" y="{y}" font-family="monospace" font-size="14" fill="#64748b">s_{i+1}: 0.</text>')
            for j, ch in enumerate(seq):
                x = 110 + j * 28
                is_diag = (i == j)
                if is_diag:
                    svg.append(f'<rect x="{x-4}" y="{y-18}" width="22" height="22" fill="#fee2e2" rx="3" stroke="#ef4444" stroke-width="1.5"/>')
                    svg.append(f'<text x="{x}" y="{y}" font-family="monospace" font-weight="bold" font-size="15" fill="#b91c1c">{ch}</text>')
                else:
                    svg.append(f'<text x="{x}" y="{y}" font-family="monospace" font-size="14" fill="#334155">{ch}</text>')

        # Anti-diagonal result row
        res_y = start_y + (n + 1) * row_height
        svg.append(f'<rect x="20" y="{res_y-24}" width="{self.width-40}" height="38" fill="#eff6ff" rx="4" stroke="#3b82f6" stroke-width="1.5"/>')
        svg.append(f'<text x="30" y="{res_y}" font-family="monospace" font-weight="bold" font-size="15" fill="#1d4ed8">Witness d (≠ s_i for all i): 0.</text>')
        for j, ch in enumerate(anti_diagonal[:n]):
            x = 350 + j * 28
            svg.append(f'<text x="{x}" y="{res_y}" font-family="monospace" font-weight="bold" font-size="16" fill="#2563eb">{ch}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_cantor_set_svg(self, stages: List[List[Interval]]) -> str:
        h = max(240, len(stages) * 45 + 50)
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {h}" width="100%" height="{h}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">The Cantor Ternary Set (Lebesgue Measure (2/3)^k → 0)</text>',
        ]

        margin_x = 40.0
        scale_x = self.width - 2 * margin_x

        for k, intervals in enumerate(stages):
            y = 60 + k * 40
            svg.append(f'<text x="15" y="{y+10}" font-family="monospace" font-size="12" fill="#64748b">k={k}</text>')
            for inv in intervals:
                x1 = margin_x + inv.left * scale_x
                w = inv.length * scale_x
                svg.append(f'<rect x="{x1:.1f}" y="{y}" width="{max(1.0, w):.1f}" height="14" fill="#2563eb" rx="2"/>')

        svg.append('</svg>')
        return "\n".join(svg)
