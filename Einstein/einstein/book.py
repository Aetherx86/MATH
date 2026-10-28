import html
from typing import List
from .relativity import C_LIGHT, G_GRAV, M_SUN, GeneralRelativityEngine, LorentzBoost
from .visualizer import RelativityVisualizer

class EinsteinBookGenerator:
    """Generates the interactive readable edition of Albert Einstein's Relativity."""
    def __init__(self):
        self.visualizer = RelativityVisualizer()

    def generate_html(self) -> str:
        minkowski_svg = self.visualizer.render_minkowski_diagram_svg(beta=0.6)
        traj = GeneralRelativityEngine.integrate_relativistic_orbit(a=1.0, e=0.3, gr_perturbation_scale=0.015, num_orbits=4)
        precession_svg = self.visualizer.render_precession_svg(traj)

        r_s_sun = GeneralRelativityEngine.schwarzschild_radius(M_SUN)
        # Mercury parameters: a = 57.9e9 m, e = 0.2056
        prec_rad = GeneralRelativityEngine.perihelion_precession_per_revolution(M_SUN, 57.909e9, 0.2056)
        # In arcseconds per century (Mercury completes ~415 revolutions per century)
        prec_arcsec_century = prec_rad * (180.0 * 3600.0 / 3.141592653589793) * 415.0

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Albert Einstein: Special &amp; General Relativity — Interactive Edition</title>
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
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
            gap: 1.25rem;
            margin-top: 1.25rem;
        }}
        .metric-card {{
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 1.25rem;
            border-radius: 6px;
        }}
        .metric-card h4 {{ color: var(--primary); margin-bottom: 0.4rem; }}
        .metric-val {{ font-size: 1.2rem; font-weight: bold; color: var(--accent); margin-top: 0.3rem; display: block; }}
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
        <h1>Relativity: Special and General Theory</h1>
        <p class="subtitle">Albert Einstein's Spacetime Geodesics, Lorentz Symmetry, and Gravitational Field Equations</p>
    </header>

    <main>
        <section id="special-relativity">
            <h2 class="section-title">Special Theory of Relativity (1905)</h2>
            <p>
                Based on two fundamental postulates: the principle of relativity across all inertial frames, and the universal constancy of the speed of light in vacuum c.
            </p>
            <div class="equation-box">
                $$ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2 = \\text{{invariant}}$$
            </div>
            <div class="figure-box">
                {minkowski_svg}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Time Dilation</h4>
                    <p>&Delta;t = &gamma; &Delta;&tau;</p>
                    <span class="metric-val">$$\\gamma = \\frac{{1}}{{\\sqrt{{1 - v^2/c^2}}}}$$</span>
                </div>
                <div class="metric-card">
                    <h4>Mass-Energy Equivalence</h4>
                    <p>Invariant Mass Shell</p>
                    <span class="metric-val">$$E^2 - (pc)^2 = (m_0 c^2)^2$$</span>
                </div>
            </div>
        </section>

        <section id="general-relativity">
            <h2 class="section-title">General Theory of Relativity (1915)</h2>
            <p>
                Gravity is not an impressed force, but the manifestation of the curvature of four-dimensional spacetime induced by energy-momentum:
            </p>
            <div class="equation-box">
                $$G_{{\\mu\\nu}} + \\Lambda g_{{\\mu\\nu}} = \\frac{{8\\pi G}}{{c^4}} T_{{\\mu\\nu}}$$
            </div>
            <div class="figure-box">
                {precession_svg}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Solar Schwarzschild Radius</h4>
                    <p>$$r_s = \\frac{{2GM}}{{c^2}}$$</p>
                    <span class="metric-val">{r_s_sun / 1000.0:.2f} km</span>
                </div>
                <div class="metric-card">
                    <h4>Mercury Perihelion Precession</h4>
                    <p>&Delta;&phi; per century (General Relativity)</p>
                    <span class="metric-val">{prec_arcsec_century:.1f}&Prime; / century</span>
                </div>
            </div>
        </section>
    </main>
</body>
</html>
"""
