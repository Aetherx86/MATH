from typing import Dict, List, Optional
from .geometry import Circle, Point, Polygon, Segment
from .proofs import GeometricFigure, Proposition

class SVGVisualizer:
    """
    Renders high-precision vector illustrations of Euclidean propositions
    styled in the classical Byrne chromatic aesthetic.
    """
    def __init__(self, width: int = 500, height: int = 420):
        self.width = width
        self.height = height

    def render_figure(self, figure: GeometricFigure, active_step: Optional[int] = None) -> str:
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
            f'width="100%" height="{self.height}" class="euclid-svg">'
        ]
        # Background canvas styling
        svg_parts.append(
            '<rect width="100%" height="100%" fill="#fcfcfc" rx="8" '
            'stroke="#e0e0e0" stroke-width="1"/>'
        )

        # Polygons
        for poly_points, fill in figure.polygons:
            pts_str = " ".join([f"{figure.points[name].x:.1f},{figure.points[name].y:.1f}" for name in poly_points if name in figure.points])
            svg_parts.append(
                f'<polygon points="{pts_str}" fill="{fill}" stroke="none"/>'
            )

        # Circles
        for center_name, rad_name, stroke in figure.circles:
            if center_name in figure.points and rad_name in figure.points:
                c = figure.points[center_name]
                r = c.distance_to(figure.points[rad_name])
                svg_parts.append(
                    f'<circle cx="{c.x:.1f}" cy="{c.y:.1f}" r="{r:.1f}" fill="none" '
                    f'stroke="{stroke}" stroke-width="1.8" stroke-dasharray="4,3"/>'
                )

        # Segments
        for p1_name, p2_name, color in figure.segments:
            if p1_name in figure.points and p2_name in figure.points:
                p1 = figure.points[p1_name]
                p2 = figure.points[p2_name]
                svg_parts.append(
                    f'<line x1="{p1.x:.1f}" y1="{p1.y:.1f}" x2="{p2.x:.1f}" y2="{p2.y:.1f}" '
                    f'stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
                )

        # Points & Labels
        for name, pt in figure.points.items():
            svg_parts.append(
                f'<circle cx="{pt.x:.1f}" cy="{pt.y:.1f}" r="4.5" fill="#111111" '
                f'stroke="#ffffff" stroke-width="1.5"/>'
            )
            # Offset label position slightly
            lx = pt.x + 8.0
            ly = pt.y - 8.0
            svg_parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="serif" font-size="15" '
                f'font-style="italic" font-weight="bold" fill="#111111">{name}</text>'
            )

        svg_parts.append("</svg>")
        return "\n".join(svg_parts)
