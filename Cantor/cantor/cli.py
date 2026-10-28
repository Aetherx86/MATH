import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import CantorBookGenerator
from .set_theory import CantorPairing, CantorTernarySet, Diagonalization, PowerSetTheorem

class CantorHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        gen = CantorBookGenerator()
        html_bytes = gen.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def log_message(self, format, *args):
        pass

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), CantorHTTPHandler)
    print("=== Georg Cantor: Transfinite Set Theory Interactive Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_diagonalize(args):
    seqs = args.sequences
    if not seqs:
        seqs = ["10110", "01001", "11010", "00101", "10011"]
    witness = Diagonalization.diagonalize_binary(seqs)
    print("=== Cantor's Diagonal Argument: Binary Construction ===")
    for i, s in enumerate(seqs):
        print(f"  s_{i+1}: 0.{s}")
    print("-" * 45)
    print(f"  Witness d: 0.{witness}")
    print("Witness differs from each s_i at index i (d != s_i for all i).")

def cmd_pairing(args):
    z = CantorPairing.pair(args.x, args.y)
    inv = CantorPairing.unpair(z)
    print(f"=== Cantor Pairing Bijection N x N <-> N ===")
    print(f"  pair({args.x}, {args.y}) = {z}")
    print(f"  unpair({z}) = {inv}")
    assert inv == (args.x, args.y)

def cmd_cantor_set(args):
    stages = CantorTernarySet.generate_stages(depth=args.depth)
    print(f"=== Cantor Ternary Set Iterations (Depth {args.depth}) ===")
    for k, intervals in enumerate(stages):
        m = CantorTernarySet.total_measure(intervals)
        print(f"  k={k}: {len(intervals):<4} intervals, Total Measure = {m:.6f} ((2/3)^{k} = {(2/3)**k:.6f})")

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
    gen = CantorBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Cantor book")

def main():
    parser = argparse.ArgumentParser(
        prog="cantor",
        description="Georg Cantor: Transfinite Set Theory & Diagonalization Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8081, help="HTTP port")
    p_serve.set_defaults(func=cmd_serve)

    # diagonalize
    p_diag = subparsers.add_parser("diagonalize", help="Run diagonal witness construction")
    p_diag.add_argument("sequences", nargs="*", help="Binary sequences")
    p_diag.set_defaults(func=cmd_diagonalize)

    # pairing
    p_pair = subparsers.add_parser("pairing", help="Cantor pairing bijection")
    p_pair.add_argument("x", type=int, help="x integer")
    p_pair.add_argument("y", type=int, help="y integer")
    p_pair.set_defaults(func=cmd_pairing)

    # cantor_set
    p_cs = subparsers.add_parser("cantor-set", help="Cantor ternary set iteration metrics")
    p_cs.add_argument("--depth", type=int, default=6, help="Iteration depth")
    p_cs.set_defaults(func=cmd_cantor_set)

    # export
    p_exp = subparsers.add_parser("export", help="Export readable HTML book")
    p_exp.add_argument("-o", "--output", default="cantor_set_theory.html", help="Output path")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
