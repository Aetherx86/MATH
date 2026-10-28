import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import BookGenerator
from .proofs import ALL_PROPOSITIONS

class BookHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        generator = BookGenerator()
        html_content = generator.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content)

    def log_message(self, format, *args):
        pass  # Suppress default server logs

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), BookHTTPHandler)
    print(f"=== Euclid's Elements: Interactive Mathematical Book Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_prove(args):
    prop_id = args.prop_id
    if prop_id not in ALL_PROPOSITIONS:
        print(f"Error: Proposition '{prop_id}' not found. Available: {', '.join(ALL_PROPOSITIONS.keys())}")
        sys.exit(1)

    prop = ALL_PROPOSITIONS[prop_id]
    print(f"================================================================================")
    print(f"{prop.title} ({prop.prop_id})")
    print(f"Statement: {prop.statement}")
    print(f"================================================================================")
    print(f"{'Step':<6} {'Justification':<20} {'Action'}")
    print("-" * 80)
    for s in prop.steps:
        print(f"{s.step_number:<6} {s.justification:<20} {s.action}")
        print(f"       -> {s.description}\n")
    print("-" * 80)
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
    generator = BookGenerator()
    content = generator.generate_html()
    _export_output(content, args.output, label="Euclid Elements")

def cmd_list(args):
    print(f"=== Euclid's Elements: Available Propositions ===")
    for pid, prop in sorted(ALL_PROPOSITIONS.items()):
        print(f"  * {pid:<12} Book {prop.book} Prop {prop.number:<3} - {prop.title}")

def main():
    parser = argparse.ArgumentParser(
        prog="euclid",
        description="Euclid's Elements: Interactive Mathematical Proof Suite & Constructive Axiomatic Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive book web server")
    p_serve.add_argument("--port", type=int, default=8000, help="HTTP port (default: 8000)")
    p_serve.set_defaults(func=cmd_serve)

    # prove
    p_prove = subparsers.add_parser("prove", help="Display deductive proof steps in terminal")
    p_prove.add_argument("prop_id", nargs="?", default="Prop.I.47", help="Proposition ID (e.g. Prop.I.1, Prop.I.47)")
    p_prove.set_defaults(func=cmd_prove)

    # export
    p_exp = subparsers.add_parser("export", help="Export interactive readable book to HTML/PDF")
    p_exp.add_argument("--output", "-o", default="euclid_elements_interactive.html", help="Output file path")
    p_exp.set_defaults(func=cmd_export)

    # list
    p_list = subparsers.add_parser("list", help="List available propositions")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
