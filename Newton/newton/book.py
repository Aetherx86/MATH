import html
from typing import Dict, List, Optional
from .mechanics import CentralForceIntegrator
from .propositions import LAWS_OF_MOTION, compute_proposition_1_discrete_impulses, get_principia_propositions
from .visualizer import PrincipiaVisualizer

class PrincipiaBookGenerator:
    """
    Synthesizes the complete interactive readable edition of Newton's Principia Mathematica.
    Includes live symplectic numerical simulators, geometric proposition proofs,
    Latin texts, and print styles for publication-grade PDF export.
    """
    def __init__(self):
        self.visualizer = PrincipiaVisualizer()

    def generate_html(self) -> str:
        propositions = get_principia_propositions()
        prop1_steps = compute_proposition_1_discrete_impulses()
        prop1_svg = self.visualizer.render_proposition_1_svg(prop1_steps)

        laws_html = "".join([f"""
            <div class="law-card">
                <span class="law-badge">{html.escape(l.identifier)}</span>
                <h3>{html.escape(l.english_title)}</h3>
                <div class="latin-quote">{html.escape(l.latin_text)}</div>
                <div class="english-trans">{html.escape(l.english_text)}</div>
                <div class="math-box">Formula: <span class="math-formula">$${l.mathematical_formulation}$$</span></div>
                <p class="commentary">{html.escape(l.commentary)}</p>
            </div>
        """ for l in LAWS_OF_MOTION])

        props_html = []
        for pid, prop in propositions.items():
            steps_items = []
            for s in prop.steps:
                steps_items.append(f"""
                <li class="proof-step">
                    <div class="step-num">Step {s.step_number}</div>
                    <div class="step-statement">{html.escape(s.statement)}</div>
                    <div class="step-meta">
                        <span class="step-just">Justification: {html.escape(s.geometric_justification)}</span>
                        <span class="step-math">$${s.analytical_relation}$$</span>
                    </div>
                </li>
                """)

            svg_block = f'<div class="figure-container">{prop1_svg}</div>' if pid == "Prop.I.1" else ""

            props_html.append(f"""
            <article class="proposition-card" id="{prop.prop_id}">
                <div class="prop-header">
                    <span class="prop-badge">Book {prop.book}</span>
                    <h2>{html.escape(prop.english_title)}</h2>
                </div>
                <div class="latin-title">{html.escape(prop.latin_title)}</div>
                <blockquote class="prop-enunciation">
                    <p>{html.escape(prop.enunciation)}</p>
                </blockquote>
                <div class="prop-content">
                    {svg_block}
                    <div class="steps-container">
                        <h3>Deductive Geometric Demonstration</h3>
                        <ol class="steps-list">
                            {"".join(steps_items)}
                        </ol>
                        <div class="qed-box">{html.escape(prop.qed_conclusion)}</div>
                    </div>
                </div>
            </article>
            """)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Philosophiae Naturalis Principia Mathematica — Interactive Edition</title>
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
            --latin: #78350f;
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
        header h1 {{ font-size: 2.6rem; font-weight: 800; letter-spacing: -0.5px; }}
        header p.subtitle {{ font-size: 1.25rem; color: #94a3b8; margin-top: 0.5rem; }}
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
        section {{ margin-bottom: 4rem; }}
        h2.section-title {{
            font-size: 1.9rem;
            color: var(--primary);
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        .laws-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
            gap: 1.5rem;
        }}
        .law-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .law-badge {{
            display: inline-block;
            background: var(--primary);
            color: #ffffff;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }}
        .law-card h3 {{ color: var(--primary); margin-bottom: 0.5rem; }}
        .latin-quote {{
            font-family: "Palatino", "Georgia", serif;
            font-style: italic;
            color: var(--latin);
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
            border-left: 2px solid #d97706;
            padding-left: 0.6rem;
        }}
        .english-trans {{ font-weight: 500; margin-bottom: 0.5rem; }}
        .math-box {{
            background: #f1f5f9;
            padding: 0.6rem 0.8rem;
            border-radius: 4px;
            font-size: 0.95rem;
            margin-bottom: 0.6rem;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
        }}
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
            background: #f1f5f9;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .prop-badge {{
            background: var(--accent);
            color: #ffffff;
            font-size: 0.8rem;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 600;
        }}
        .prop-header h2 {{ font-size: 1.35rem; color: var(--primary); }}
        .latin-title {{
            padding: 0.5rem 1.5rem 0;
            font-family: serif;
            font-style: italic;
            color: var(--latin);
        }}
        .prop-enunciation {{
            padding: 1rem 1.5rem;
            font-style: italic;
            font-size: 1.05rem;
            background: #f8fafc;
            border-left: 4px solid var(--accent);
            margin: 0.5rem 1.5rem 1.5rem;
        }}
        .prop-content {{
            padding: 0 1.5rem 1.5rem;
        }}
        svg {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .figure-container {{
            width: 100%;
            overflow-x: auto;
            margin-bottom: 1.5rem;
        }}
        .steps-list {{ list-style: none; margin-top: 1rem; }}
        .proof-step {{
            padding: 0.85rem 0;
            border-bottom: 1px solid var(--border);
        }}
        .step-num {{ font-size: 0.8rem; font-weight: 700; color: var(--accent); text-transform: uppercase; }}
        .step-statement {{ font-size: 0.98rem; font-weight: 500; margin: 0.2rem 0; }}
        .step-meta {{ display: flex; gap: 0.75rem; font-size: 0.88rem; color: var(--muted); flex-wrap: wrap; align-items: center; margin-top: 0.35rem; }}
        .step-just {{ background: #e2e8f0; padding: 0.15rem 0.5rem; border-radius: 3px; font-weight: 600; }}
        .step-math {{ background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 3px; overflow-x: auto; max-width: 100%; box-sizing: border-box; }}
        .qed-box {{
            margin-top: 1.25rem;
            padding: 0.75rem 1rem;
            background: #eff6ff;
            color: #1e40af;
            border-radius: 4px;
            font-weight: 700;
            text-align: right;
            font-family: serif;
        }}
        /* Orbit Lab */
        .orbit-lab {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
        }}
        .lab-controls {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
            background: #f8fafc;
            padding: 1rem;
            border-radius: 6px;
        }}
        .control-group {{ display: flex; flex-direction: column; gap: 0.3rem; }}
        .control-group label {{ font-size: 0.85rem; font-weight: 600; color: var(--muted); }}
        .canvas-row {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
        }}
        @media (max-width: 800px) {{
            .canvas-row {{ grid-template-columns: 1fr; }}
        }}
        .orbit-canvas {{
            width: 100%;
            height: 420px;
            background: #0f172a;
            border-radius: 6px;
        }}
        .hud-panel {{
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.85rem;
        }}
        .hud-stat {{ margin-bottom: 0.75rem; }}
        .hud-stat span.label {{ color: var(--muted); display: block; font-size: 0.75rem; }}
        .hud-stat span.value {{ color: var(--primary); font-size: 1rem; font-weight: bold; }}
        /* Print Styles */
        @media print {{
            header, nav.toc, .orbit-lab, .lab-controls {{ display: none; }}
            body {{ background: #ffffff; color: #000000; font-size: 11pt; }}
            .proposition-card {{ page-break-inside: avoid; border: none; box-shadow: none; margin-bottom: 2rem; }}
            svg {{ max-width: 85%; margin: 0 auto; }}
            h2.section-title {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Philosophiae Naturalis Principia Mathematica</h1>
        <p class="subtitle">Interactive Mechanics, Central Forces, and Geometric Fluxions</p>
    </header>

    <nav class="toc">
        <a href="#axiomata">Axiomata sive Leges Motus</a>
        <a href="#Prop.I.1">Prop I.1: Areal Velocity Conservation</a>
        <a href="#Prop.I.11">Prop I.11: Inverse-Square Orbit Determination</a>
        <a href="#orbit-lab">Symplectic Keplerian Laboratory</a>
    </nav>

    <main>
        <section id="axiomata">
            <h2 class="section-title">Axiomata sive Leges Motus (The Three Laws of Motion)</h2>
            <div class="laws-grid">
                {laws_html}
            </div>
        </section>

        <section id="propositions">
            <h2 class="section-title">Book I: The Motion of Bodies under Central Forces</h2>
            {"".join(props_html)}
        </section>

        <section id="orbit-lab">
            <h2 class="section-title">Symplectic Keplerian Orbit Laboratory</h2>
            <div class="orbit-lab">
                <div class="lab-controls">
                    <div class="control-group">
                        <label for="eccRange">Eccentricity e (0.0 to 0.8):</label>
                        <input type="range" id="eccRange" min="0" max="80" value="50">
                    </div>
                    <div class="control-group">
                        <label for="speedRange">Simulation Speed:</label>
                        <input type="range" id="speedRange" min="1" max="10" value="4">
                    </div>
                </div>
                <div class="canvas-row">
                    <canvas id="orbitCanvas" class="orbit-canvas" width="600" height="420"></canvas>
                    <div class="hud-panel">
                        <h4 style="margin-bottom: 0.75rem; font-family: sans-serif; color: var(--primary);">Real-Time Conserved Quantities</h4>
                        <div class="hud-stat">
                            <span class="label">Time elapsed t:</span>
                            <span class="value" id="hudTime">0.00 s</span>
                        </div>
                        <div class="hud-stat">
                            <span class="label">Specific Energy E (Const):</span>
                            <span class="value" id="hudEnergy">-0.5000</span>
                        </div>
                        <div class="hud-stat">
                            <span class="label">Angular Momentum h (Const):</span>
                            <span class="value" id="hudAngMom">1.0000</span>
                        </div>
                        <div class="hud-stat">
                            <span class="label">Current Radius r:</span>
                            <span class="value" id="hudRadius">1.0000 AU</span>
                        </div>
                        <div class="hud-stat">
                            <span class="label">Current Velocity v:</span>
                            <span class="value" id="hudVel">1.0000</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Real-Time Symplectic Orbit Simulation
        const canvas = document.getElementById('orbitCanvas');
        if (canvas) {{
            const ctx = canvas.getContext('2d');
            const mu = 10000.0;
            let ecc = 0.5;
            let a = 140.0;
            let r0 = a * (1.0 - ecc);
            let v0 = Math.sqrt(mu * (1.0 + ecc) / r0);

            let x = r0, y = 0.0;
            let vx = 0.0, vy = v0;
            let simTime = 0.0;
            let sectors = [];
            let lastSectorTime = 0;

            const eccInput = document.getElementById('eccRange');
            if (eccInput) {{
                eccInput.addEventListener('input', (e) => {{
                    ecc = e.target.value / 100.0;
                    r0 = a * (1.0 - ecc);
                    v0 = Math.sqrt(mu * (1.0 + ecc) / r0);
                    x = r0; y = 0.0;
                    vx = 0.0; vy = v0;
                    sectors = [];
                    simTime = 0.0;
                }});
            }}

            function stepSymplectic(dt) {{
                const r = Math.hypot(x, y);
                if (r < 1e-4) return;
                const ax = -mu * x / Math.pow(r, 3);
                const ay = -mu * y / Math.pow(r, 3);

                vx += 0.5 * ax * dt;
                vy += 0.5 * ay * dt;
                x += vx * dt;
                y += vy * dt;

                const r_new = Math.hypot(x, y);
                const ax_new = -mu * x / Math.pow(r_new, 3);
                const ay_new = -mu * y / Math.pow(r_new, 3);
                vx += 0.5 * ax_new * dt;
                vy += 0.5 * ay_new * dt;

                simTime += dt;
            }}

            function loop() {{
                const speed = document.getElementById('speedRange') ? document.getElementById('speedRange').value : 4;
                const subSteps = speed * 2;
                const dt = 0.015;

                for (let i = 0; i < subSteps; i++) {{
                    stepSymplectic(dt);
                    if (simTime - lastSectorTime > 0.45) {{
                        sectors.push({{ x: x, y: y }});
                        if (sectors.length > 12) sectors.shift();
                        lastSectorTime = simTime;
                    }}
                }}

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                const cx = canvas.width / 2 - 30;
                const cy = canvas.height / 2;

                // Central Star / Sun (Focus S)
                ctx.beginPath();
                ctx.arc(cx, cy, 8, 0, 2 * Math.PI);
                ctx.fillStyle = '#f59e0b';
                ctx.fill();
                ctx.font = 'bold 12px sans-serif';
                ctx.fillStyle = '#fbbf24';
                ctx.fillText('S (Focus)', cx - 18, cy - 14);

                // Areal Sweeps
                for (let i = 1; i < sectors.length; i++) {{
                    ctx.beginPath();
                    ctx.moveTo(cx, cy);
                    ctx.lineTo(cx + sectors[i - 1].x, cy + sectors[i - 1].y);
                    ctx.lineTo(cx + sectors[i].x, cy + sectors[i].y);
                    ctx.closePath();
                    ctx.fillStyle = (i % 2 === 0) ? 'rgba(59, 130, 246, 0.25)' : 'rgba(16, 185, 129, 0.25)';
                    ctx.fill();
                }}

                // Orbit Trajectory
                ctx.beginPath();
                ctx.arc(cx - a * ecc, cy, a, 0, 2 * Math.PI);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Current Planet Position
                const px = cx + x;
                const py = cy + y;
                ctx.beginPath();
                ctx.arc(px, py, 6, 0, 2 * Math.PI);
                ctx.fillStyle = '#38bdf8';
                ctx.fill();

                // Radius Vector
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(px, py);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
                ctx.lineWidth = 1;
                ctx.setLineDash([3, 3]);
                ctx.stroke();
                ctx.setLineDash([]);

                // Velocity vector
                ctx.beginPath();
                ctx.moveTo(px, py);
                ctx.lineTo(px + vx * 2.0, py + vy * 2.0);
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Update HUD
                const cur_r = Math.hypot(x, y);
                const cur_v = Math.hypot(vx, vy);
                const energy = 0.5 * cur_v * cur_v - mu / cur_r;
                const h = x * vy - y * vx;

                document.getElementById('hudTime').textContent = simTime.toFixed(2) + ' s';
                document.getElementById('hudEnergy').textContent = energy.toFixed(2);
                document.getElementById('hudAngMom').textContent = h.toFixed(2);
                document.getElementById('hudRadius').textContent = (cur_r / 100.0).toFixed(3) + ' AU';
                document.getElementById('hudVel').textContent = cur_v.toFixed(2);

                requestAnimationFrame(loop);
            }}

            loop();
        }}
    </script>
</body>
</html>
"""
