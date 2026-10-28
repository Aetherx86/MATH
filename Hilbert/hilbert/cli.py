import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import HilbertBookGenerator
from .foundations import HILBERT_GEOMETRY_AXIOMS, HILBERT_PROBLEMS_HIGHLIGHTS, HilbertSpaceEngine, HilbertVector

class HilbertHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        gen = HilbertBookGenerator()
        html_bytes = gen.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def log_message(self, format, *args):
        pass

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), HilbertHTTPHandler)
    print("=== David Hilbert: Grundlagen & Functional Analysis Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_ortho(args):
    print("=== Gram-Schmidt Orthonormalization in Hilbert Space ===")
    raw = [
        HilbertVector([1.0, 1.0, 0.0]),
        HilbertVector([1.0, 0.0, 1.0]),
        HilbertVector([0.0, 1.0, 1.0]),
    ]
    ortho = HilbertSpaceEngine.gram_schmidt(raw)
    for i, v in enumerate(ortho):
        comps = [f"{c:.4f}" for c in v.components]
        print(f"  e_{i+1}: ({', '.join(comps)}), norm = {v.norm():.6f}")

    # Verify orthogonality
    print("-" * 50)
    print(f"  <e1, e2> = {ortho[0].inner_product(ortho[1]):.2e}")
    print(f"  <e1, e3> = {ortho[0].inner_product(ortho[2]):.2e}")
    print(f"  <e2, e3> = {ortho[1].inner_product(ortho[2]):.2e}")

def cmd_problems(args):
    print("=== David Hilbert's 23 Problems (Key Highlights) ===")
    for p in HILBERT_PROBLEMS_HIGHLIGHTS:
        print(f"\n[Problem {p.number}] {p.title} ({p.field})")
        print(f"  Description: {p.description}")
        print(f"  Status: {p.status}")

def _export_output(content: str, out_file: str, label: str = "book"):
    import os
    import shutil
    import subprocess
    import tempfile

    if out_file.lower().endswith(".pdf"):
        chrome_candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            shutil.which("google-chrome"),
            shutil.which("chromium"),
            shutil.which("chromium-browser"),
        ]
        chrome_bin = next((b for b in chrome_candidates if b and os.path.exists(b)), None)
        if chrome_bin:
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            try:
                cmd = [
                    chrome_bin,
                    "--headless",
                    "--disable-gpu",
                    "--run-all-compositor-stages-before-draw",
                    f"--print-to-pdf={out_file}",
                    tmp_path,
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                size = os.path.getsize(out_file)
                print(f"[OK] Exported interactive {label} to PDF: {out_file} ({size:,} bytes)")
                return
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        else:
            print("[INFO] Headless Chrome not found for direct PDF rasterization; exporting HTML publication instead.")
            out_file = out_file[:-4] + ".html"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Exported interactive {label} to {out_file} ({len(content):,} bytes)")

def cmd_export(args):
    gen = HilbertBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Hilbert book")

def main():
    parser = argparse.ArgumentParser(
        prog="hilbert",
        description="David Hilbert: Grundlagen der Geometrie & Functional Analysis Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8082, help="HTTP port")
    p_serve.set_defaults(func=cmd_serve)

    # ortho
    p_ortho = subparsers.add_parser("ortho", help="Run Gram-Schmidt orthonormalization")
    p_ortho.set_defaults(func=cmd_ortho)

    # problems
    p_prob = subparsers.add_parser("problems", help="Display 23 mathematical problems")
    p_prob.set_defaults(func=cmd_problems)

    # export
    p_exp = subparsers.add_parser("export", help="Export HTML book")
    p_exp.add_argument("-o", "--output", default="hilbert_grundlagen.html", help="Output path")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
