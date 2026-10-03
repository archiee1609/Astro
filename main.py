"""
main.py - Vedic Astrology and Numerology Application
Entry point for Streamlit Web Application, FastAPI Server, CLI, and Batch Execution.
"""

import sys
import os
import argparse

def get_lan_ip() -> str:
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    parser = argparse.ArgumentParser(
        description="Vedic Astrology & Numerology System (High Precision NASA JPL DE421 + Sankhya Shastra)"
    )
    parser.add_argument("--streamlit", action="store_true", help="Launch interactive Streamlit web dashboard (Default)")
    parser.add_argument("--web", action="store_true", help="Launch FastAPI web server")
    parser.add_argument("--cli", action="store_true", help="Launch interactive Rich terminal interface")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Web server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=None, help="Web server port (default: 8501 for Streamlit, 8000 for FastAPI)")
    parser.add_argument("--name", type=str, help="Full Name for direct batch run")
    parser.add_argument("--dob", type=str, help="Date of Birth (YYYY-MM-DD)")
    parser.add_argument("--tob", type=str, help="Time of Birth (HH:MM)")
    parser.add_argument("--pob", type=str, help="Place of Birth (City, Country)")
    parser.add_argument("--export", type=str, help="Path to export report (.html, .md, .json)")
    parser.add_argument("--format", type=str, default="auto", choices=["auto", "html", "markdown", "json"], help="Export format: html, markdown, json, or auto (default: auto)")

    args = parser.parse_args()

    # Direct CLI batch run if arguments provided
    if args.name and args.dob and args.tob and args.pob:
        from core.analyzer import AstroAnalyzer
        from core.report_exporter import ReportExporter
        from ui.cli import display_full_report

        analyzer = AstroAnalyzer()
        report = analyzer.analyze(
            full_name=args.name,
            dob_str=args.dob,
            tob_str=args.tob,
            pob_str=args.pob
        )
        display_full_report(report)

        if args.export:
            saved_path = ReportExporter.export_to_file(report, args.export, format_type=args.format)
            print(f"\n✓ Complete report successfully exported to: {saved_path}")
        return

    # If --cli explicitly passed
    if args.cli:
        from ui.cli import run_cli_interactive
        run_cli_interactive()
        return
    # If --web explicitly passed (FastAPI)
    if args.web:
        import uvicorn
        web_port = args.port or 8000
        lan_ip = get_lan_ip()
        print("=" * 72)
        print("ॐ VEDIC JYOTISH & NUMEROLOGY FASTAPI SERVER ॐ")
        print("=" * 72)
        print(f"💻 Local Computer Access:   http://localhost:{web_port}")
        print(f"📱 Mobile & Tablet Access:  http://{lan_ip}:{web_port}")
        print("   (Ensure your phone or tablet is connected to the same Wi-Fi network)")
        print("=" * 72)
        print("Press Ctrl+C to terminate.")
        uvicorn.run("ui.web.app:app", host=args.host, port=web_port, reload=False)
        return

    # Default to Streamlit web application
    from streamlit.web import cli as stcli
    st_port = args.port or 8501
    st_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "streamlit_app.py")
    lan_ip = get_lan_ip()

    print("=" * 72)
    print("ॐ VEDIC JYOTISH & NUMEROLOGY STREAMLIT WEB APPLICATION ॐ")
    print("=" * 72)
    print(f"💻 Local Computer Access:   http://localhost:{st_port}")
    print(f"📱 Mobile & Tablet Access:  http://{lan_ip}:{st_port}")
    print("   (Ensure your phone or tablet is connected to the same Wi-Fi network)")
    print("=" * 72)
    sys.argv = [
        "streamlit", "run", st_app_path,
        "--server.port", str(st_port),
        "--server.address", args.host,
        "--server.headless", "true"
    ]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()

