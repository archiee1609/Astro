"""
ui/web/app.py - FastAPI Web Server for Vedic Astrology and Numerology
"""

import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.analyzer import AstroAnalyzer

app = FastAPI(
    title="Vedic Astrology & Numerology Application",
    description="High precision Vedic Jyotish & Sankhya Shastra calculations",
    version="1.0.0"
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
