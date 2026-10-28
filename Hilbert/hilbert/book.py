import html
from typing import List
from .foundations import HILBERT_GEOMETRY_AXIOMS, HILBERT_PROBLEMS_HIGHLIGHTS, HilbertSpaceEngine, HilbertVector
from .visualizer import HilbertVisualizer

class HilbertBookGenerator:
    """Generates the interactive readable edition of David Hilbert's Mathematical Works."""
    def __init__(self):
        self.visualizer = HilbertVisualizer()

    def generate_html(self) -> str:
        pasch_svg = self.visualizer.render_pasch_axiom_svg()
        desargues_svg = self.visualizer.render_desargues_svg()

        axioms_html = []
        for grp in HILBERT_GEOMETRY_AXIOMS:
            ax_items = "".join([f"<li>{html.escape(a)}</li>" for a in grp.axioms])
            axioms_html.append(f"""
            <div class="axiom-group-card">
                <h3>{html.escape(grp.group_name)} <span class="german-tag">({html.escape(grp.german_name)})</span></h3>
                <p class="grp-desc">{html.escape(grp.description)}</p>
                <ul class="axiom-list">
                    {ax_items}
                </ul>
            </div>
            """)

        problems_html = []
        for p in HILBERT_PROBLEMS_HIGHLIGHTS:
            problems_html.append(f"""
            <div class="problem-card">
                <div class="prob-header">
                    <span class="prob-num">Problem {p.number}</span>
                    <h4>{html.escape(p.title)}</h4>
                    <span class="prob-field">{html.escape(p.field)}</span>
                </div>
                <p class="prob-desc">{html.escape(p.description)}</p>
                <div class="prob-status"><strong>Status:</strong> {html.escape(p.status)}</div>
            </div>
            """)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>David Hilbert: Grundlagen der Geometrie &amp; Functional Analysis — Interactive Edition</title>
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
        .axiom-group-card {{
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
            background: #fafafa;
        }}
        .german-tag {{ font-weight: normal; font-style: italic; color: var(--muted); }}
        .grp-desc {{ font-size: 0.92rem; color: var(--muted); margin: 0.3rem 0 0.75rem; }}
        .axiom-list {{ padding-left: 1.25rem; font-size: 0.95rem; }}
        .axiom-list li {{ margin-bottom: 0.4rem; }}
        .diagram-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 360px), 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }}
        svg {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .problem-card {{
            border-left: 4px solid var(--accent);
            background: #f8fafc;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            border-radius: 0 6px 6px 0;
        }}
        .prob-header {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.4rem; flex-wrap: wrap; }}
        .prob-num {{ background: var(--accent); color: #fff; font-size: 0.75rem; font-weight: bold; padding: 0.15rem 0.5rem; border-radius: 4px; }}
        .prob-field {{ background: #e2e8f0; font-size: 0.75rem; font-weight: 600; padding: 0.15rem 0.4rem; border-radius: 3px; }}
        .prob-status {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.4rem; }}
        .math-box {{
            background: #f1f5f9;
            padding: 1.25rem;
            border-radius: 6px;
            margin: 1.25rem 0;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
            text-align: center;
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
        <h1>David Hilbert: Axiomatics &amp; Functional Analysis</h1>
        <p class="subtitle">Grundlagen der Geometrie (1899), Hilbert Spaces, and the 23 Mathematical Problems</p>
    </header>

    <main>
        <section id="geometry">
            <h2 class="section-title">Grundlagen der Geometrie (1899): The Five Axiom Groups</h2>
            <p style="margin-bottom: 1.5rem;">
                Hilbert established the rigorous modern axiomatization of Euclidean geometry, eliminating implicit intuitive assumptions and classifying axioms into five independent groups.
            </p>
            {"".join(axioms_html)}

            <div class="diagram-grid">
                <div>{pasch_svg}</div>
                <div>{desargues_svg}</div>
            </div>
        </section>

        <section id="hilbert-space">
            <h2 class="section-title">Infinite-Dimensional Hilbert Space &amp; Spectral Theory</h2>
            <p>
                A Hilbert space H is a real or complex inner product space that is complete with respect to the distance metric induced by the inner product:
            </p>
            <div class="math-box">
                $$\\langle x, y \\rangle = \\sum_{{n=1}}^\\infty x_n y_n, \\quad \\|x\\| = \\sqrt{{\\langle x, x \\rangle}}$$
            </div>
            <p>
                Key theorems verified by the engine:
            </p>
            <ul style="padding-left: 1.5rem; margin-top: 0.75rem;">
                <li style="margin-bottom: 0.5rem;"><strong>Cauchy-Schwarz Inequality:</strong> $$|\\langle x, y \\rangle| \\le \\|x\\| \\cdot \\|y\\|$$</li>
                <li style="margin-bottom: 0.5rem;"><strong>Parallelogram Law:</strong> {r"$$\|x + y\|^2 + \|x - y\|^2 = 2(\|x\|^2 + \|y\|^2)$$"}</li>
                <li style="margin-bottom: 0.5rem;"><strong>Gram-Schmidt Orthogonalization:</strong> Systematic projection algorithm generating orthonormal bases.</li>
            </ul>
        </section>

        <section id="problems">
            <h2 class="section-title">Hilbert's 23 Mathematical Problems (Paris 1900)</h2>
            {"".join(problems_html)}
        </section>
    </main>
</body>
</html>
"""
