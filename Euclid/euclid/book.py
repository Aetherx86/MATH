import html
from typing import Dict, List, Optional
from .axioms import COMMON_NOTIONS, DEFINITIONS_BOOK_I, POSTULATES
from .proofs import ALL_PROPOSITIONS, Proposition
from .visualizer import SVGVisualizer

class BookGenerator:
    """
    Synthesizes the complete interactive readable book of Euclid's Elements.
    Generates a responsive single-page web publication with live proof steppers,
    dynamic ruler-and-compass canvas, and CSS print media styles for PDF export.
    """
    def __init__(self):
        self.visualizer = SVGVisualizer()

    def generate_html(self) -> str:
        propositions_html = []
        for prop_id, prop in ALL_PROPOSITIONS.items():
            svg_render = self.visualizer.render_figure(prop.figure)
            steps_items = []
            for s in prop.steps:
                steps_items.append(f"""
                <li class="proof-step" data-step="{s.step_number}">
                    <div class="step-header">
                        <span class="step-num">Step {s.step_number}</span>
                        <span class="step-justification">{html.escape(s.justification)}</span>
                    </div>
                    <div class="step-action">{html.escape(s.action)}</div>
                    <div class="step-desc">{html.escape(s.description)}</div>
                </li>
                """)

            propositions_html.append(f"""
            <article class="proposition-card" id="{prop.prop_id}">
                <div class="prop-header">
                    <span class="prop-badge">Book {prop.book}</span>
                    <h2>{html.escape(prop.title)}</h2>
                </div>
                <blockquote class="prop-statement">
                    <p>{html.escape(prop.statement)}</p>
                </blockquote>
                <div class="prop-body">
                    <div class="figure-container">
                        {svg_render}
                    </div>
                    <div class="proof-container">
                        <h3>Deductive Demonstration</h3>
                        <ol class="proof-steps-list">
                            {"".join(steps_items)}
                        </ol>
                        <div class="qed-box">{html.escape(prop.qed_conclusion)}</div>
                    </div>
                </div>
            </article>
            """)

        defs_html = "".join([f"""
            <div class="axiom-card">
                <h4>{html.escape(d.title)}</h4>
                <div class="greek-quote">{html.escape(d.greek_text)}</div>
                <div class="english-trans">{html.escape(d.english_text)}</div>
                <p class="commentary">{html.escape(d.commentary)}</p>
            </div>
        """ for d in DEFINITIONS_BOOK_I])

        posts_html = "".join([f"""
            <div class="axiom-card">
                <h4>{html.escape(p.title)}</h4>
                <div class="greek-quote">{html.escape(p.greek_text)}</div>
                <div class="english-trans">{html.escape(p.english_text)}</div>
                <p class="commentary">{html.escape(p.commentary)}</p>
            </div>
        """ for p in POSTULATES])

        notions_html = "".join([f"""
            <div class="axiom-card">
                <h4>{html.escape(cn.title)}</h4>
                <div class="greek-quote">{html.escape(cn.greek_text)}</div>
                <div class="english-trans">{html.escape(cn.english_text)}</div>
                <p class="commentary">{html.escape(cn.commentary)}</p>
            </div>
        """ for cn in COMMON_NOTIONS])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Euclid's Elements (Στοιχεῖα) — Interactive Mathematical Edition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        :root {{
            --primary: #1a365d;
            --accent: #2b6cb0;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #2d3748;
            --muted: #718096;
            --border: #e2e8f0;
            --greek: #744210;
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
            padding: 3rem 2rem;
            text-align: center;
        }}
        header h1 {{ font-size: 2.6rem; font-weight: 700; letter-spacing: -0.5px; }}
        header p.subtitle {{ font-size: 1.2rem; color: #cbd5e0; margin-top: 0.5rem; }}
        nav.toc {{
            max-width: 1100px;
            margin: -1.5rem auto 2rem;
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1rem 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }}
        nav.toc a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
        }}
        nav.toc a:hover {{ text-decoration: underline; }}
        main {{ max-width: 1100px; margin: 0 auto; padding: 0 1.5rem 4rem; }}
        section {{ margin-bottom: 3.5rem; }}
        h2.section-title {{
            font-size: 1.9rem;
            color: var(--primary);
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        .axiom-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
            gap: 1.25rem;
        }}
        .axiom-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .axiom-card h4 {{ color: var(--primary); margin-bottom: 0.4rem; }}
        .greek-quote {{
            font-family: "Palatino", "Georgia", serif;
            font-style: italic;
            color: var(--greek);
            font-size: 0.95rem;
            margin-bottom: 0.4rem;
        }}
        .english-trans {{ font-weight: 500; margin-bottom: 0.5rem; }}
        .commentary {{ font-size: 0.88rem; color: var(--muted); }}
        .proposition-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 2.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .prop-header {{
            background: #edf2f7;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .prop-badge {{
            background: var(--primary);
            color: #ffffff;
            font-size: 0.8rem;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 600;
        }}
        .prop-header h2 {{ font-size: 1.35rem; color: var(--primary); }}
        .prop-statement {{
            padding: 1.2rem 1.5rem;
            font-style: italic;
            font-size: 1.05rem;
            background: #f7fafc;
            border-left: 4px solid var(--accent);
        }}
        .prop-body {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            padding: 1.5rem;
        }}
        @media (max-width: 820px) {{
            .prop-body {{ grid-template-columns: 1fr; }}
        }}
        .figure-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            overflow-x: auto;
        }}
        svg {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .proof-container h3 {{ font-size: 1.15rem; margin-bottom: 0.75rem; color: var(--primary); }}
        .proof-steps-list {{ list-style: none; }}
        .proof-step {{
            padding: 0.75rem 0.5rem;
            border-bottom: 1px solid var(--border);
        }}
        .step-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.25rem;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }}
        .step-num {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
        }}
        .step-justification {{
            font-size: 0.8rem;
            background: #e2e8f0;
            padding: 0.1rem 0.4rem;
            border-radius: 3px;
            font-weight: 600;
        }}
        .step-action {{ font-weight: 600; font-size: 0.95rem; margin-bottom: 0.2rem; }}
        .step-desc {{ font-size: 0.88rem; color: var(--muted); }}
        .qed-box {{
            margin-top: 1rem;
            padding: 0.6rem 1rem;
            background: #ebf8ff;
            color: #2b6cb0;
            border-radius: 4px;
            font-weight: 700;
            text-align: right;
            font-family: serif;
        }}
        /* Interactive dynamic canvas */
        .interactive-lab {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }}
        .lab-canvas-container {{
            width: 100%;
            max-width: 100%;
            height: 380px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #ffffff;
            cursor: crosshair;
        }}
        /* Print Stylesheet for clean PDF Export */
        @media print {{
            header, nav.toc, .interactive-lab {{ display: none; }}
            body {{ background: #ffffff; color: #000000; font-size: 11pt; }}
            .proposition-card {{ page-break-inside: avoid; border: none; box-shadow: none; margin-bottom: 2.5rem; }}
            .prop-body {{ display: block; }}
            .figure-container {{ margin-bottom: 1.5rem; text-align: center; }}
            svg {{ max-width: 75%; height: auto; margin: 0 auto; }}
            h2.section-title {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>The Elements of Euclid (Στοιχεῖα)</h1>
        <p class="subtitle">Interactive Mathematical Proof Suite & Constructive Axiomatic Engine</p>
    </header>

    <nav class="toc">
        <a href="#axioms">Axiomatic Foundations</a>
        <a href="#Prop.I.1">Prop I.1: Equilateral Triangle</a>
        <a href="#Prop.I.9">Prop I.9: Angle Bisector</a>
        <a href="#Prop.I.47">Prop I.47: Pythagorean Theorem</a>
        <a href="#Prop.IX.20">Prop IX.20: Prime Infinitude</a>
        <a href="#interactive-canvas">Dynamic Geometry Canvas</a>
    </nav>

    <main>
        <section id="axioms">
            <h2 class="section-title">Book I: Axiomatic Foundations</h2>
            <h3 style="margin: 1rem 0; color: var(--primary);">Definitions</h3>
            <div class="axiom-grid">
                {defs_html}
            </div>

            <h3 style="margin: 2rem 0 1rem; color: var(--primary);">The Five Postulates</h3>
            <div class="axiom-grid">
                {posts_html}
            </div>

            <h3 style="margin: 2rem 0 1rem; color: var(--primary);">Common Notions</h3>
            <div class="axiom-grid">
                {notions_html}
            </div>
        </section>

        <section id="propositions">
            <h2 class="section-title">The Propositions & Deductive Demonstrations</h2>
            {"".join(propositions_html)}
        </section>

        <section id="interactive-canvas">
            <h2 class="section-title">Interactive Dynamic Geometry Canvas</h2>
            <div class="interactive-lab">
                <p style="margin-bottom: 0.75rem; color: var(--muted);">
                    Click and drag points <strong>A</strong> or <strong>B</strong> on the canvas to dynamically recompute the compass circles and equilateral vertex <strong>C</strong> (Proposition I.1).
                </p>
                <canvas id="euclidCanvas" class="lab-canvas-container" width="1000" height="380"></canvas>
            </div>
        </section>
    </main>

    <script>
        // Interactive Dynamic Geometry Canvas for Proposition I.1
        const canvas = document.getElementById('euclidCanvas');
        if (canvas) {{
            const ctx = canvas.getContext('2d');
            let pA = {{ x: 350, y: 240 }};
            let pB = {{ x: 650, y: 240 }};
            let dragging = null;

            function computePointC(a, b) {{
                const dx = b.x - a.x;
                const dy = b.y - a.y;
                const r = Math.hypot(dx, dy);
                if (r < 5) return a;
                // Equilateral third vertex (rotated by +60 deg)
                const cos60 = 0.5;
                const sin60 = Math.sqrt(3) / 2.0;
                const rx = dx * cos60 - dy * sin60;
                const ry = dx * sin60 + dy * cos60;
                return {{ x: a.x + rx, y: a.y + ry }};
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                const pC = computePointC(pA, pB);
                const r = Math.hypot(pB.x - pA.x, pB.y - pA.y);

                // Compass Circle A
                ctx.beginPath();
                ctx.arc(pA.x, pA.y, r, 0, 2 * Math.PI);
                ctx.strokeStyle = 'rgba(31, 119, 180, 0.4)';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.stroke();

                // Compass Circle B
                ctx.beginPath();
                ctx.arc(pB.x, pB.y, r, 0, 2 * Math.PI);
                ctx.strokeStyle = 'rgba(214, 39, 40, 0.4)';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.stroke();

                ctx.setLineDash([]);

                // Equilateral Triangle Fill
                ctx.beginPath();
                ctx.moveTo(pA.x, pA.y);
                ctx.lineTo(pB.x, pB.y);
                ctx.lineTo(pC.x, pC.y);
                ctx.closePath();
                ctx.fillStyle = 'rgba(44, 160, 44, 0.15)';
                ctx.fill();

                // Edges
                ctx.beginPath();
                ctx.moveTo(pA.x, pA.y);
                ctx.lineTo(pB.x, pB.y);
                ctx.strokeStyle = '#1f77b4';
                ctx.lineWidth = 3;
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(pB.x, pB.y);
                ctx.lineTo(pC.x, pC.y);
                ctx.strokeStyle = '#ff7f0e';
                ctx.lineWidth = 3;
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(pC.x, pC.y);
                ctx.lineTo(pA.x, pA.y);
                ctx.strokeStyle = '#d62728';
                ctx.lineWidth = 3;
                ctx.stroke();

                // Vertices
                const pts = [{{ p: pA, name: 'A' }}, {{ p: pB, name: 'B' }}, {{ p: pC, name: 'C' }}];
                pts.forEach(({{ p, name }}) => {{
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, 6, 0, 2 * Math.PI);
                    ctx.fillStyle = '#111111';
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.font = 'bold italic 16px serif';
                    ctx.fillStyle = '#111111';
                    ctx.fillText(name, p.x + 10, p.y - 10);
                }});
            }}

            canvas.addEventListener('mousedown', (e) => {{
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const mx = (e.clientX - rect.left) * scaleX;
                const my = (e.clientY - rect.top) * scaleY;

                if (Math.hypot(mx - pA.x, my - pA.y) < 25) dragging = 'A';
                else if (Math.hypot(mx - pB.x, my - pB.y) < 25) dragging = 'B';
            }});

            window.addEventListener('mousemove', (e) => {{
                if (!dragging) return;
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const mx = (e.clientX - rect.left) * scaleX;
                const my = (e.clientY - rect.top) * scaleY;

                if (dragging === 'A') {{ pA.x = mx; pA.y = my; }}
                else if (dragging === 'B') {{ pB.x = mx; pB.y = my; }}
                draw();
            }});

            window.addEventListener('mouseup', () => {{ dragging = null; }});
            draw();
        }}
    </script>
</body>
</html>
"""
