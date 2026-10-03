"""
main.py - Vedic Astrology and Numerology Application
Entry point for Streamlit Web Application, FastAPI Server, CLI, and Batch Execution.
"""

import sys
import os
import argparse

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
    parser.add_argument("--export", type=str, help="Path to export JSON report")

    args = parser.parse_args()

    # Direct CLI batch run if arguments provided
    if args.name and args.dob and args.tob and args.pob:
        from core.analyzer import AstroAnalyzer
        from ui.cli import display_full_report
        import json

        analyzer = AstroAnalyzer()
        report = analyzer.analyze(
            full_name=args.name,
            dob_str=args.dob,
            tob_str=args.tob,
            pob_str=args.pob
        )
        display_full_report(report)

        if args.export:
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Report exported to {args.export}")
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
        print(f"Starting Vedic Astrology & Numerology FastAPI Server on http://{args.host}:{web_port}")
        print("Press Ctrl+C to terminate.")
        uvicorn.run("ui.web.app:app", host=args.host, port=web_port, reload=False)
        return

    # Default to Streamlit web application
    from streamlit.web import cli as stcli
    st_port = args.port or 8501
    st_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "streamlit_app.py")

    print(f"Starting Vedic Astrology & Numerology Streamlit Web Application on http://{args.host}:{st_port}")
    sys.argv = [
        "streamlit", "run", st_app_path,
        "--server.port", str(st_port),
        "--server.address", args.host,
        "--server.headless", "true"
    ]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()

