import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import EinsteinBookGenerator
from .relativity import C_LIGHT, G_GRAV, M_SUN, FourVector, GeneralRelativityEngine, LorentzBoost, RelativisticDynamics

class EinsteinHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        gen = EinsteinBookGenerator()
        html_bytes = gen.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def log_message(self, format, *args):
        pass

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), EinsteinHTTPHandler)
    print("=== Albert Einstein: Relativity Interactive Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_boost(args):
    v4 = FourVector(ct=args.ct, x=args.x, y=args.y, z=args.z)
    boosted = LorentzBoost.boost_x(v4, args.beta)
    print("=== Special Relativity: Lorentz Boost ===")
    print(f"  Input 4-Vector:   (ct={v4.ct:.4f}, x={v4.x:.4f}, y={v4.y:.4f}, z={v4.z:.4f})")
    print(f"  Speed v/c (beta): {args.beta:.4f} (gamma = {LorentzBoost.gamma(args.beta):.4f})")
    print(f"  Boosted 4-Vector: (ct'={boosted.ct:.4f}, x'={boosted.x:.4f}, y'={boosted.y:.4f}, z'={boosted.z:.4f})")
    print(f"  Rest Interval ds^2:    {v4.spacetime_interval():.6f}")
    print(f"  Boosted Interval ds'^2: {boosted.spacetime_interval():.6f}")

def cmd_precession(args):
    # Mercury parameters
    a_merc = 57.909e9
    e_merc = 0.20563
    dphi_rad = GeneralRelativityEngine.perihelion_precession_per_revolution(M_SUN, a_merc, e_merc)
    arcsec_rev = dphi_rad * (180.0 * 3600.0 / 3.141592653589793)
    # Mercury has period ~87.97 days -> ~415.2 revolutions per century
    arcsec_century = arcsec_rev * 415.20

    print("=== General Relativity: Mercury Perihelion Advance ===")
    print(f"  Central Mass: Solar Mass (1.989e30 kg)")
    print(f"  Semi-major axis a: {a_merc/1e9:.2f} million km")
    print(f"  Orbital eccentricity e: {e_merc:.4f}")
    print(f"  Precession per revolution: {arcsec_rev:.6f} arcsec/rev")
    print(f"  Precession per century:    {arcsec_century:.2f} arcsec/century (Observed GR excess: 43.1'')")

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
    gen = EinsteinBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Einstein book")

def main():
    parser = argparse.ArgumentParser(
        prog="einstein",
        description="Albert Einstein: Special and General Relativity Simulation Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8083, help="HTTP port")
    p_serve.set_defaults(func=cmd_serve)

    # boost
    p_boost = subparsers.add_parser("boost", help="Compute Lorentz boost transformation")
    p_boost.add_argument("--beta", type=float, default=0.6, help="v/c velocity parameter")
    p_boost.add_argument("--ct", type=float, default=1.0, help="ct coordinate")
    p_boost.add_argument("--x", type=float, default=0.5, help="x coordinate")
    p_boost.add_argument("--y", type=float, default=0.0, help="y coordinate")
    p_boost.add_argument("--z", type=float, default=0.0, help="z coordinate")
    p_boost.set_defaults(func=cmd_boost)

    # precession
    p_prec = subparsers.add_parser("precession", help="Calculate General Relativistic perihelion advance")
    p_prec.set_defaults(func=cmd_precession)

    # export
    p_exp = subparsers.add_parser("export", help="Export HTML book")
    p_exp.add_argument("-o", "--output", default="einstein_relativity.html", help="Output path")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
