"""
ui/web/app.py - FastAPI Web Server for Vedic Astrology and Numerology
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.analyzer import AstroAnalyzer
from core.report_exporter import ReportExporter

app = FastAPI(
    title="Vedic Astrology & Numerology Application",
    description="High precision Vedic Jyotish & Sankhya Shastra calculations",
    version="2.0.0"
)

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")

os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

analyzer = AstroAnalyzer()

class AnalyzeRequest(BaseModel):
    full_name: str
    date_of_birth: str  # YYYY-MM-DD
    time_of_birth: str  # HH:MM
    place_of_birth: str

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    """Renders the main astrology and numerology web interface."""
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/api/analyze")
async def analyze_api(data: AnalyzeRequest):
    """API endpoint accepting JSON and returning full analysis report."""
    try:
        report = analyzer.analyze(
            full_name=data.full_name,
            dob_str=data.date_of_birth,
            tob_str=data.time_of_birth,
            pob_str=data.place_of_birth
        )
        return JSONResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/report/download")
async def download_report_get(
    full_name: str = "Arjun Sharma",
    dob: str = "1995-10-24",
    tob: str = "06:30",
    pob: str = "New Delhi, India",
    format: str = "html"
):
    """Downloads the complete astrological report in HTML, Markdown, or JSON format."""
    try:
        report = analyzer.analyze(full_name=full_name, dob_str=dob, tob_str=tob, pob_str=pob)
        clean_name = full_name.replace(" ", "_").lower()
        fmt = format.lower().strip()

        if fmt in ["html", "pdf"]:
            content = ReportExporter.generate_html_report(report)
            return Response(
                content=content,
                media_type="text/html",
                headers={"Content-Disposition": f'attachment; filename="{clean_name}_complete_report.html"'}
            )
        elif fmt in ["md", "markdown"]:
            content = ReportExporter.generate_markdown_report(report)
            return Response(
                content=content,
                media_type="text/markdown",
                headers={"Content-Disposition": f'attachment; filename="{clean_name}_complete_report.md"'}
            )
        else:
            content = ReportExporter.generate_json_report(report)
            return Response(
                content=content,
                media_type="application/json",
                headers={"Content-Disposition": f'attachment; filename="{clean_name}_complete_report.json"'}
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class DownloadReportRequest(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    time_of_birth: Optional[str] = None
    place_of_birth: Optional[str] = None
    dob: Optional[str] = None
    tob: Optional[str] = None
    pob: Optional[str] = None
    format: Optional[str] = "html"
    user_input: Optional[Dict[str, Any]] = None

@app.post("/api/report/download")
async def download_report_post(req: DownloadReportRequest, format: Optional[str] = None):
    """Downloads the complete report via POST request with flexible input formatting."""
    u = req.user_input or {}
    full_name = req.full_name or u.get("full_name", "Report")
    dob = req.date_of_birth or req.dob or u.get("date_of_birth") or u.get("dob")
    tob = req.time_of_birth or req.tob or u.get("time_of_birth") or u.get("tob")
    pob = req.place_of_birth or req.pob or u.get("place_of_birth") or u.get("pob")
    fmt = format or req.format or "html"

    if not (dob and tob and pob):
        raise HTTPException(status_code=400, detail="Missing required birth fields (date_of_birth, time_of_birth, place_of_birth).")

    return await download_report_get(
        full_name=full_name,
        dob=dob,
        tob=tob,
        pob=pob,
        format=fmt
    )

@app.get("/api/quick-sample")
async def quick_sample():
    """Returns a quick sample analysis for demonstration."""
    report = analyzer.analyze(
        full_name="Arjun Sharma",
        dob_str="1995-10-24",
        tob_str="06:30",
        pob_str="New Delhi, India"
    )
    return JSONResponse(content=report)
