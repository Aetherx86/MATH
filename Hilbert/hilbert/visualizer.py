class HilbertVisualizer:
    """Renders vector diagrams of Hilbert's axiomatic geometry in SVG format."""
    def __init__(self, width: int = 600, height: int = 400):
        self.width = width
        self.height = height

    def render_pasch_axiom_svg(self) -> str:
        """Illustrates Pasch's Axiom: line entering triangle through AB must exit through AC or BC."""
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0f172a">Axiom II.4: Pasch\'s Axiom of Planar Betweenness</text>',
            # Triangle ABC
            '<polygon points="300,70 120,320 480,320" fill="rgba(37, 99, 235, 0.08)" stroke="#2563eb" stroke-width="2.5"/>',
            # Transversal line a cutting AB and AC
            '<line x1="50" y1="260" x2="520" y2="120" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4"/>',
            # Intersections
            '<circle cx="180" cy="226" r="5" fill="#dc2626"/>',
            '<circle cx="372" cy="165" r="5" fill="#dc2626"/>',
            # Vertices
            '<circle cx="300" cy="70" r="5" fill="#0f172a"/><text x="295" y="55" font-family="serif" font-weight="bold" font-size="16">A</text>',
            '<circle cx="120" cy="320" r="5" fill="#0f172a"/><text x="100" y="335" font-family="serif" font-weight="bold" font-size="16">B</text>',
            '<circle cx="480" cy="320" r="5" fill="#0f172a"/><text x="490" y="335" font-family="serif" font-weight="bold" font-size="16">C</text>',
            '<text x="60" y="250" font-family="serif" font-style="italic" font-weight="bold" font-size="16" fill="#dc2626">line a</text>',
            '</svg>'
        ]
        return "\n".join(svg)

    def render_desargues_svg(self) -> str:
        """Illustrates Desargues's Theorem: perspective from point implies collinear edge intersections."""
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0f172a">Desargues\'s Theorem: Projective Perspective</text>',
            # Center of perspective O
            '<circle cx="80" cy="200" r="5" fill="#7c3aed"/><text x="65" y="195" font-family="serif" font-weight="bold" font-size="15" fill="#7c3aed">O</text>',
            # Perspective rays from O
            '<line x1="80" y1="200" x2="520" y2="80" stroke="#cbd5e1" stroke-width="1.5"/>',
            '<line x1="80" y1="200" x2="520" y2="200" stroke="#cbd5e1" stroke-width="1.5"/>',
            '<line x1="80" y1="200" x2="520" y2="320" stroke="#cbd5e1" stroke-width="1.5"/>',
            # Triangle 1: ABC
            '<polygon points="200,167 220,200 180,227" fill="rgba(37, 99, 235, 0.15)" stroke="#2563eb" stroke-width="2"/>',
            # Triangle 2: A'B'C'
            '<polygon points="360,123 400,200 320,265" fill="rgba(16, 185, 129, 0.15)" stroke="#059669" stroke-width="2"/>',
            # Axis of homology (Collinear intersection line)
            '<line x1="520" y1="50" x2="520" y2="350" stroke="#dc2626" stroke-width="2.5"/>',
            '<text x="440" y="40" font-family="serif" font-weight="bold" font-size="14" fill="#dc2626">Desargues Axis</text>',
            '</svg>'
        ]
        return "\n".join(svg)
