import html
from typing import List
from .matrix_mechanics import QuantumHarmonicOscillator
from .visualizer import HeisenbergVisualizer

class HeisenbergBookGenerator:
    """Generates the interactive readable edition of Werner Heisenberg's Quantum Mechanics."""
    def __init__(self):
        self.visualizer = HeisenbergVisualizer()

    def generate_html(self) -> str:
        qho = QuantumHarmonicOscillator(n_states=8, hbar=1.0)
        comm = qho.X.commutator(qho.P)
        comm_svg = self.visualizer.render_commutator_heatmap_svg(comm)
        uncert_svg = self.visualizer.render_uncertainty_gaussian_svg(sigma_x=1.0, sigma_p=0.5)

        # Diagonal energy values
        energies = [f"E<sub>{n}</sub> = {qho.H.data[n][n].real:.1f} &#8463;&omega;" for n in range(min(5, qho.n))]

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Werner Heisenberg: Matrix Mechanics &amp; Uncertainty — Interactive Edition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        :root {{
            --primary: #0f172a;
            --accent: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Charter", Georgia, serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        header {{
            background: var(--primary);
            color: #ffffff;
            padding: 3.5rem 2rem;
            text-align: center;
        }}
        header h1 {{ font-size: 2.6rem; font-weight: 800; }}
        header p.subtitle {{ font-size: 1.25rem; color: #94a3b8; margin-top: 0.5rem; }}
        main {{ max-width: 1050px; margin: -1.5rem auto 4rem; padding: 0 1.5rem; }}
        section {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        h2.section-title {{ font-size: 1.7rem; color: var(--primary); margin-bottom: 1.25rem; border-bottom: 2px solid var(--border); padding-bottom: 0.4rem; }}
        .equation-box {{
            background: #f1f5f9;
            padding: 1.25rem;
            border-left: 4px solid var(--accent);
            border-radius: 0 6px 6px 0;
            font-size: 1.15rem;
            margin: 1.25rem 0;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
            text-align: center;
        }}
        .figure-box {{
            margin: 1.5rem 0;
            width: 100%;
            overflow-x: auto;
        }}
        svg {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .eigenvalues-list {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }}
        .eigen-card {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-family: monospace;
            font-weight: bold;
            color: #1d4ed8;
        }}
        @media print {{
            header {{ display: none; }}
            body {{ background: #ffffff; color: #000000; font-size: 11pt; }}
            section {{ page-break-inside: avoid; border: none; box-shadow: none; margin-bottom: 2rem; }}
            svg {{ max-width: 85%; margin: 0 auto; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Werner Heisenberg: Quantum Matrix Mechanics</h1>
        <p class="subtitle">The Canonical Commutation Relations, Spectral Eigenvalues, and the Uncertainty Principle (1925–1927)</p>
    </header>

    <main>
        <section id="matrix-mechanics">
            <h2 class="section-title">Matrix Mechanics (1925): The Born-Jordan-Heisenberg Commutator</h2>
            <p>
                In July 1925, Heisenberg rejected classical unobservable electron orbits and formulated quantum theory based exclusively on relations between observable transition radiation amplitudes.
                Born and Jordan recognized that Heisenberg's multiplication rule represented non-commutative matrix algebra:
            </p>
            <div class="equation-box">
                $$[X, P] \\equiv XP - PX = i \\hbar I$$
            </div>
            <p>
                Because XP &ne; PX, position and momentum observables do not share a common eigenbasis and cannot be simultaneously determined.
            </p>
            <div class="figure-box">
                {comm_svg}
            </div>
        </section>

        <section id="harmonic-oscillator">
            <h2 class="section-title">The Quantum Harmonic Oscillator &amp; Zero-Point Energy</h2>
            <p>
                Expressing the Hamiltonian in terms of creation (a<sup>&dagger;</sup>) and annihilation (a) operators:
                H = &#8463;&omega; (a<sup>&dagger;</sup> a + &frac12; I).
                The exact stationary energy eigenvalues are quantized with non-zero ground-state energy:
            </p>
            <div class="eigenvalues-list">
                {"".join([f'<div class="eigen-card">{e}</div>' for e in energies])}
            </div>
        </section>

        <section id="uncertainty">
            <h2 class="section-title">The Uncertainty Principle (1927)</h2>
            <p>
                Heisenberg demonstrated through his gamma-ray microscope thought experiment and operator algebra that measurement precision is fundamentally constrained:
            </p>
            <div class="equation-box">
                $$\\sigma_X \\cdot \\sigma_P \\ge \\frac{{\\hbar}}{{2}}$$
            </div>
            <div class="figure-box">
                {uncert_svg}
            </div>
        </section>
    </main>
</body>
</html>
"""
