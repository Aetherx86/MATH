import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import HeisenbergBookGenerator
from .matrix_mechanics import H_BAR, ComplexMatrix, QuantumHarmonicOscillator, UncertaintyPrinciple

class HeisenbergHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        gen = HeisenbergBookGenerator()
        html_bytes = gen.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def log_message(self, format, *args):
        pass

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), HeisenbergHTTPHandler)
    print("=== Werner Heisenberg: Matrix Mechanics Interactive Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_commutator(args):
    qho = QuantumHarmonicOscillator(n_states=args.dimension, hbar=1.0)
    comm = qho.X.commutator(qho.P)
    print(f"=== Canonical Commutator [X, P] Evaluation (Dimension {args.dimension}x{args.dimension}) ===")
    print("Diagonal Elements (Theoretical: +1.0000 i for interior states):")
    for i in range(args.dimension):
        diag_val = comm.data[i][i]
        print(f"  [{i},{i}]: {diag_val.real:+.4f} {diag_val.imag:+.4f} i")

def cmd_oscillator(args):
    qho = QuantumHarmonicOscillator(n_states=args.dimension, hbar=1.0, omega=args.omega)
    print(f"=== Quantum Harmonic Oscillator Hamiltonian (omega = {args.omega}) ===")
    print(f"{'State n':<10} {'Energy E_n':<18} {'Theoretical (n + 1/2) hbar*omega'}")
    print("-" * 55)
    for n in range(args.dimension):
        en = qho.H.data[n][n].real
        theo = (n + 0.5) * 1.0 * args.omega
        print(f"n = {n:<6} {en:<18.4f} {theo:.4f}")

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
    gen = HeisenbergBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Heisenberg book")

def main():
    parser = argparse.ArgumentParser(
        prog="heisenberg",
        description="Werner Heisenberg: Matrix Mechanics & Uncertainty Principle Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8084, help="HTTP port")
    p_serve.set_defaults(func=cmd_serve)

    # commutator
    p_comm = subparsers.add_parser("commutator", help="Evaluate [X, P] commutator")
    p_comm.add_argument("--dimension", "-d", type=int, default=6, help="Truncation dimension")
    p_comm.set_defaults(func=cmd_commutator)

    # oscillator
    p_osc = subparsers.add_parser("oscillator", help="Display quantum harmonic oscillator spectrum")
    p_osc.add_argument("--dimension", "-d", type=int, default=8, help="Number of states")
    p_osc.add_argument("--omega", type=float, default=1.0, help="Oscillator angular frequency")
    p_osc.set_defaults(func=cmd_oscillator)

    # export
    p_exp = subparsers.add_parser("export", help="Export HTML book")
    p_exp.add_argument("-o", "--output", default="heisenberg_matrix_mechanics.html", help="Output path")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
