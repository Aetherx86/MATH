import html
from typing import List
from .set_theory import CantorPairing, CantorTernarySet, Diagonalization, PowerSetTheorem
from .visualizer import CantorVisualizer

class CantorBookGenerator:
    """Generates the interactive readable edition of Cantor's Transfinite Set Theory."""
    def __init__(self):
        self.visualizer = CantorVisualizer()

    def generate_html(self) -> str:
        sample_seqs = [
            "1011001011",
            "0100110100",
            "1101011010",
            "0010100111",
            "1001110001",
            "0110001110",
        ]
        anti_diag = Diagonalization.diagonalize_binary(sample_seqs)
        diag_svg = self.visualizer.render_diagonal_matrix_svg(sample_seqs, anti_diag)

        stages = CantorTernarySet.generate_stages(depth=5)
        cantor_svg = self.visualizer.render_cantor_set_svg(stages)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Georg Cantor: Transfinite Set Theory — Interactive Edition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        :root {{
            --primary: #0f172a;
            --accent: #3b82f6;
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
        main {{ max-width: 1000px; margin: -1.5rem auto 4rem; padding: 0 1.5rem; }}
        section {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        h2.section-title {{ font-size: 1.7rem; color: var(--primary); margin-bottom: 1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.4rem; }}
        .math-statement {{
            background: #f1f5f9;
            border-left: 4px solid var(--accent);
            padding: 1.25rem;
            margin: 1.25rem 0;
            font-style: italic;
            border-radius: 0 6px 6px 0;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
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
        /* Print Styles */
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
        <h1>Transfinite Set Theory (Mengenlehre)</h1>
        <p class="subtitle">Georg Cantor's Foundations of the Infinite, Diagonalization, and Cardinal Arithmetic</p>
    </header>

    <main>
        <section id="diagonal-argument">
            <h2 class="section-title">The Diagonal Argument (1891): Uncountability of the Continuum</h2>
            <div class="math-statement">
                <strong>Theorem (Cantor 1891):</strong> The set of real numbers $\\mathbb{{R}}$ (or infinite binary sequences $2^\\mathbb{{N}}$) is strictly uncountably infinite: $$|\\mathbb{{R}}| > |\\mathbb{{N}}|$$
            </div>
            <p>
                Assume for contradiction that the continuum could be enumerated into a countable succession: $s_1, s_2, s_3, \\dots$.
                Cantor constructs a new sequence $d$ differing from the $n$-th element at its $n$-th digit (the anti-diagonal):
            </p>
            <div class="math-statement" style="text-align: center;">
                $$d_n = 1 - s_{{n,n}}$$
            </div>
            <p>
                Because $d$ differs from every listed sequence $s_i$ at index $i$, $d$ cannot belong to the enumeration, proving that no countable sequence can encompass all real numbers.
            </p>
            <div class="figure-box">
                {diag_svg}
            </div>
        </section>

        <section id="cantor-set">
            <h2 class="section-title">The Cantor Ternary Set: Uncountable Zero-Measure Continuum</h2>
            <div class="math-statement">
                <strong>Definition:</strong> The Cantor ternary set $\\mathcal{{C}}$ is formed by starting with the closed interval $[0, 1]$ and iteratively removing the open middle third of each remaining interval.
            </div>
            <p>
                At step $k$, there are $2^k$ intervals, each of length $(1/3)^k$. The total remaining Lebesgue measure is:
            </p>
            <div class="math-statement" style="text-align: center;">
                $$\\lambda(\\mathcal{{C}}_k) = \\left(\\frac{{2}}{{3}}\\right)^k \\longrightarrow 0 \\quad \\text{{as }} k \\to \\infty$$
            </div>
            <p>
                Yet every point in $\\mathcal{{C}}$ has a base-3 representation consisting exclusively of 0s and 2s, proving a direct bijection to $2^\\mathbb{{N}}$: the set contains as many points as the entire real continuum!
            </p>
            <div class="figure-box">
                {cantor_svg}
            </div>
        </section>

        <section id="powers-set-theorem">
            <h2 class="section-title">Cantor's Theorem: $|S| &lt; |\\mathcal{{P}}(S)|$</h2>
            <p style="margin-bottom: 0.75rem;">
                For every set $S$, finite or infinite, the power set $\\mathcal{{P}}(S)$ has strictly greater cardinality than $S$.
            </p>
            <p style="margin-bottom: 0.75rem;">
                <strong>Proof:</strong> Suppose $f: S \\longrightarrow \\mathcal{{P}}(S)$ is a surjective function. Consider the diagonal witness subset:
            </p>
            <div class="math-statement" style="text-align: center;">
                $$D = \\{{ x \\in S : x \\notin f(x) \\}}$$
            </div>
            <p style="margin-bottom: 0.75rem;">
                Since $f$ is surjective, there must exist some $d \\in S$ such that $f(d) = D$.
            </p>
            <ul style="padding-left: 1.5rem; margin-bottom: 0.75rem;">
                <li>If $d \\in D$, then by definition $d \\notin f(d) = D$, a contradiction.</li>
                <li>If $d \\notin D$, then by definition $d \\in f(d) = D$, a contradiction.</li>
            </ul>
            <p>
                Therefore no surjection exists, establishing the infinite hierarchy of transfinite cardinalities:
            </p>
            <div class="math-statement" style="text-align: center;">
                $$\\aleph_0 &lt; 2^{{\\aleph_0}} &lt; 2^{{2^{{\\aleph_0}}}} &lt; \\dots$$
            </div>
        </section>
    </main>
</body>
</html>
"""
