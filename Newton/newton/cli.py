import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import PrincipiaBookGenerator
from .mechanics import CentralForceIntegrator
from .propositions import LAWS_OF_MOTION, get_principia_propositions

class PrincipiaHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        generator = PrincipiaBookGenerator()
        html_content = generator.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content)

    def log_message(self, format, *args):
        pass

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), PrincipiaHTTPHandler)
    print("=== Newton's Principia Mathematica: Interactive Book Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_orbit(args):
    integrator = CentralForceIntegrator(mu=1.0, power_n=2.0)
    # Set initial Keplerian periapsis conditions
    # For a = 1.0, e = args.eccentricity: r0 = a * (1 - e), v0 = sqrt(mu * (1 + e) / r0)
    e = max(0.0, min(0.9, args.eccentricity))
    a = 1.0
    r0 = a * (1.0 - e)
    v0 = (1.0 * (1.0 + e) / r0) ** 0.5

    print(f"=== Symplectic Keplerian Orbit Integration (Velocity Verlet) ===")
    print(f"Parameters: Semimajor a = {a:.2f}, Eccentricity e = {e:.3f}, mu = 1.0")
    print(f"Initial State: r0 = {r0:.4f}, v0 = {v0:.4f}, dt = {args.dt}, steps = {args.steps}")
    print("-" * 88)
    print(f"{'Step':<8} {'Time (s)':<10} {'Radius r':<12} {'Velocity v':<12} {'Energy E':<14} {'Ang Mom h':<12} {'Eccentricity |e|'}")
    print("-" * 88)

    traj = integrator.integrate_verlet(x0=r0, y0=0.0, vx0=0.0, vy0=v0, dt=args.dt, steps=args.steps)
    e0 = traj[0].specific_energy()
    h0 = traj[0].specific_angular_momentum()

    stride = max(1, args.steps // 10)
    for i in range(0, len(traj), stride):
        st = traj[i]
        en = st.specific_energy()
        ang = st.specific_angular_momentum()
        ex, ey = st.eccentricity_vector()
        emag = (ex**2 + ey**2) ** 0.5
        print(f"{i:<8} {st.t:<10.3f} {st.r:<12.4f} {st.v:<12.4f} {en:<14.6f} {ang:<12.6f} {emag:.6f}")

    e_final = traj[-1].specific_energy()
    h_final = traj[-1].specific_angular_momentum()
    delta_e = abs(e_final - e0) / abs(e0)
    delta_h = abs(h_final - h0) / abs(h0)
    print("-" * 88)
    print(f"Conservation Verification over {args.steps} steps:")
    print(f"  * Relative Energy Variation dE/E:       {delta_e:.2e}")
    print(f"  * Relative Angular Momentum Variation:  {delta_h:.2e}")

def cmd_prove(args):
    props = get_principia_propositions()
    prop_id = args.prop_id
    if prop_id not in props:
        print(f"Error: Proposition '{prop_id}' not found. Available: {', '.join(props.keys())}")
        sys.exit(1)

    prop = props[prop_id]
    print("=" * 88)
    print(f"{prop.english_title} ({prop.prop_id})")
    print(f"Latin: {prop.latin_title}")
    print(f"Enunciation: {prop.enunciation}")
    print("=" * 88)
    for s in prop.steps:
        print(f"[{s.step_number}] {s.statement}")
        print(f"    Justification: {s.geometric_justification}")
        print(f"    Math: {s.analytical_relation}\n")
    print("-" * 88)
    print(f"Conclusion: {prop.qed_conclusion}\n")

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
    print(f"[OK] Exported interactive {label} to: {out_file} ({len(content):,} bytes)")

def cmd_export(args):
    generator = PrincipiaBookGenerator()
    content = generator.generate_html()
    _export_output(content, args.output, label="Newton Principia")

def cmd_list(args):
    print("=== Philosophiae Naturalis Principia Mathematica: Core Index ===")
    print("\nAxiomata sive Leges Motus:")
    for l in LAWS_OF_MOTION:
        print(f"  * {l.identifier:<8} {l.english_title}")

    props = get_principia_propositions()
    print("\nBook I Propositions:")
    for pid, prop in sorted(props.items()):
        print(f"  * {pid:<10} {prop.english_title}")

def main():
    parser = argparse.ArgumentParser(
        prog="newton",
        description="Philosophiae Naturalis Principia Mathematica: Interactive Mechanics & Fluxion Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive Principia book server")
    p_serve.add_argument("--port", type=int, default=8080, help="HTTP port (default: 8080)")
    p_serve.set_defaults(func=cmd_serve)

    # orbit
    p_orbit = subparsers.add_parser("orbit", help="Run symplectic Keplerian orbit simulation")
    p_orbit.add_argument("--eccentricity", "-e", type=float, default=0.5, help="Orbital eccentricity (0.0 to 0.9)")
    p_orbit.add_argument("--steps", type=int, default=2000, help="Integration steps")
    p_orbit.add_argument("--dt", type=float, default=0.005, help="Time step (default: 0.005)")
    p_orbit.set_defaults(func=cmd_orbit)

    # prove
    p_prove = subparsers.add_parser("prove", help="Display mathematical proof of proposition")
    p_prove.add_argument("prop_id", nargs="?", default="Prop.I.1", help="Proposition ID (e.g. Prop.I.1, Prop.I.11)")
    p_prove.set_defaults(func=cmd_prove)

    # export
    p_exp = subparsers.add_parser("export", help="Export interactive Principia book to HTML/PDF")
    p_exp.add_argument("--output", "-o", default="principia_mathematica_interactive.html", help="Output file path")
    p_exp.set_defaults(func=cmd_export)

    # list
    p_list = subparsers.add_parser("list", help="List laws of motion and propositions")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
