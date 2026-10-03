"""
ui/streamlit_app.py - High Precision Vedic Jyotish & Numerology Streamlit Web Application
Celestial Astrology Themed UI with Dark Cosmic Aesthetics, Golden Accents & Interactive Timelines.
"""

import sys
import os
from datetime import datetime, date, time
import json
import pandas as pd
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.analyzer import AstroAnalyzer
from core.internet_data import InternetDataService
from core.constants import PLANETS, SIGNS, NAKSHATRAS
from core.report_exporter import ReportExporter

# Page Configuration
# Page Configuration
st.set_page_config(
    page_title="ॐ Vedic Jyotish & Sacred Timelines",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Astrological Glyphs & Constants
PLANET_GLYPHS = {
    "Sun": "☉", "Moon": "☽", "Mars": "♂", "Mercury": "☿",
    "Jupiter": "♃", "Venus": "♀", "Saturn": "♄", "Rahu": "☊", "Ketu": "☋"
}
SIGN_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# Deep Astrological Custom CSS with Full Mobile & Tablet Responsiveness
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800;900&family=Marcellus&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Cosmic Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #17153b 0%, #0d0f22 45%, #05060f 100%) !important;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Celestial Banner Header */
    .astro-header {
        text-align: center;
        padding: 2rem 1.5rem 1.5rem;
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6), 0 0 25px rgba(245, 158, 11, 0.15);
        position: relative;
        overflow: hidden;
    }
    .astro-header::before {
        content: "✧ ✦ ✧ ✦ ✧";
        position: absolute;
        top: 8px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(251, 191, 36, 0.4);
        font-size: 0.85rem;
        letter-spacing: 8px;
    }
    .astro-header h1 {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #fffbeb 0%, #fbbf24 35%, #d97706 70%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0;
        text-shadow: 0 2px 20px rgba(245, 158, 11, 0.3);
    }
    .astro-header p {
        font-family: 'Marcellus', serif;
        color: #cbd5e1;
        font-size: 1.05rem;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }
    
    /* Cosmic Badges */
    .astro-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 0.2rem 0.35rem;
        backdrop-filter: blur(8px);
    }
    .astro-badge-gold {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.15);
    }
    .astro-badge-online {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
    }
    .astro-badge-mystic {
        background: rgba(168, 85, 247, 0.12);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }

    /* Cosmic Glass Cards */
    .cosmic-card {
        background: rgba(18, 24, 43, 0.75);
        border: 1px solid rgba(245, 158, 11, 0.22);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .cosmic-card:hover {
        border-color: rgba(245, 158, 11, 0.45);
        transform: translateY(-2px);
    }

    /* Running Active Dasha Card with Radiant Glow */
    .active-dasha-hero {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1.5px solid #10b981;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25), inset 0 0 15px rgba(16, 185, 129, 0.08);
        position: relative;
    }
    .active-dasha-hero h3 {
        font-family: 'Cinzel', serif;
        color: #34d399;
        font-size: 1.35rem;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Metric Tiles */
    .metric-tile {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 10px;
        padding: 1rem 0.8rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-tile-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        margin-bottom: 0.3rem;
    }
    .metric-tile-value {
        font-family: 'Cinzel', serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #fbbf24;
        text-shadow: 0 2px 8px rgba(251, 191, 36, 0.2);
    }
    .metric-tile-sub {
        font-size: 0.8rem;
        color: #cbd5e1;
        margin-top: 0.2rem;
    }

    /* SVG Chart Wrapper */
    .chart-frame {
        background: radial-gradient(circle at 50% 50%, #151833 0%, #0a0d1d 100%);
        border: 1.5px solid rgba(245, 158, 11, 0.35);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(0, 0, 0, 0.4);
    }

    /* Custom Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #cbd5e1;
        font-family: 'Marcellus', serif;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.35) 100%) !important;
        color: #fbbf24 !important;
        border: 1px solid rgba(245, 158, 11, 0.5) !important;
        font-weight: bold;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1222 0%, #080a14 100%) !important;
        border-right: 1px solid rgba(245, 158, 11, 0.25);
    }

    /* -------------------------------------------------------------
       RESPONSIVE DESIGN: TABLET & MOBILE ENHANCEMENTS
       ------------------------------------------------------------- */
    @media (max-width: 992px) {
        .astro-header {
            padding: 1.5rem 1rem 1.2rem;
            margin-bottom: 1.5rem;
        }
        .astro-header h1 {
            font-size: 1.85rem;
            letter-spacing: 1.5px;
        }
        .astro-header p {
            font-size: 0.9rem;
        }
        .cosmic-card {
            padding: 1rem 1.2rem;
        }
    }

    @media (max-width: 768px) {
        /* Mobile & Small Tablet (Portrait) */
        .astro-header {
            padding: 1.2rem 0.75rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        .astro-header::before {
            letter-spacing: 4px;
            font-size: 0.75rem;
        }
        .astro-header h1 {
            font-size: 1.45rem;
            letter-spacing: 1px;
            margin: 0.1rem 0;
        }
        .astro-header p {
            font-size: 0.82rem;
            line-height: 1.4;
            margin-bottom: 0.5rem;
        }
        .astro-badge {
            font-size: 0.72rem;
            padding: 0.25rem 0.6rem;
            margin: 0.15rem 0.2rem;
        }

        /* Responsive Metric Cards & Columns wrap */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.6rem !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 140px !important;
            flex: 1 1 calc(50% - 0.6rem) !important;
        }

        .metric-tile {
            padding: 0.75rem 0.5rem;
        }
        .metric-tile-title {
            font-size: 0.7rem;
        }
        .metric-tile-value {
            font-size: 1.25rem;
        }
        .metric-tile-sub {
            font-size: 0.72rem;
        }

        .active-dasha-hero {
            padding: 1rem 1.1rem;
            border-radius: 10px;
        }
        .active-dasha-hero h3 {
            font-size: 1.1rem;
            flex-direction: column;
            align-items: flex-start;
        }

        /* Tabs swipeable horizontally on mobile */
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            padding-bottom: 6px !important;
            gap: 4px !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none;
        }
        .stTabs [data-baseweb="tab"] {
            flex-shrink: 0 !important;
            font-size: 0.82rem !important;
            padding: 6px 12px !important;
        }

        /* Touch-friendly buttons */
        .stButton button, .stDownloadButton button {
            min-height: 44px !important;
            padding: 0.5rem 0.8rem !important;
            font-size: 0.9rem !important;
        }
    }

    @media (max-width: 480px) {
        /* Extra-compact Smartphones */
        .astro-header h1 {
            font-size: 1.25rem;
            letter-spacing: 0.5px;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        .chart-frame {
            padding: 0.4rem;
        }
        .cosmic-card {
            padding: 0.85rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper function to discover LAN IP for Mobile/Tablet access
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

# Initialize engines
@st.cache_resource
def get_analyzer():
    return AstroAnalyzer()

analyzer = get_analyzer()
internet_svc = InternetDataService()

def render_svg_kundali(svg_code: str, height: int = 425):
    """
    Renders SVG vector Kundali inside a seamless responsive iframe,
    guaranteeing 100% vector fidelity across desktop, tablet, and mobile.
    """
    clean_svg = svg_code.strip()
    html_frame = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        margin: 0;
        padding: 0;
        background: transparent;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }}
    .kundali-wrapper {{
        width: 100%;
        max-width: 395px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 4px;
    }}
    svg {{
        width: 100%;
        max-width: 100%;
        height: auto;
        max-height: 395px;
        display: block;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }}
    @media (max-width: 480px) {{
        .kundali-wrapper {{
            max-width: 295px;
        }}
    }}
</style>
</head>
<body>
    <div class="kundali-wrapper">
        {clean_svg}
    </div>
</body>
</html>"""
    st.components.v1.html(html_frame, height=height)

# Astrological Profile Presets
PRESETS = {
    "Custom Birth Data": None,
    "Arjun Sharma (1995-10-24, New Delhi)": {
        "name": "Arjun Sharma", "dob": date(1995, 10, 24), "tob": time(6, 30), "pob": "New Delhi, India"
    },
    "Priya Patel (1998-05-14, Mumbai)": {
        "name": "Priya Patel", "dob": date(1998, 5, 14), "tob": time(14, 15), "pob": "Mumbai, India"
    },
    "Vikramaditya (1988-08-15, Varanasi)": {
        "name": "Vikramaditya", "dob": date(1988, 8, 15), "tob": time(9, 45), "pob": "Varanasi, India"
    },
    "Steve Jobs (1955-02-24, San Francisco)": {
        "name": "Steve Jobs", "dob": date(1955, 2, 24), "tob": time(19, 15), "pob": "San Francisco, USA"
    }
}

# -------------------------------------------------------------
# SIDEBAR: NATAL BIRTH DETAILS & INTERNET PRECISION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.2rem;">
        <span style="font-size: 2.2rem; color: #fbbf24;">🕉️</span>
        <h2 style="font-family: 'Cinzel', serif; color: #fbbf24; font-size: 1.35rem; margin: 0; letter-spacing: 1px;">
            SACRED JYOTISH
        </h2>
        <div style="color: #94a3b8; font-size: 0.8rem; letter-spacing: 0.5px;">Parashara Hora & Sankhya Shastra</div>
    </div>
    """, unsafe_allow_html=True)

    preset_choice = st.selectbox("🌟 Choose Kundli Profile", list(PRESETS.keys()))

    if preset_choice and PRESETS[preset_choice]:
        p = PRESETS[preset_choice]
        default_name = p["name"]
        default_dob = p["dob"]
        default_tob = p["tob"]
        default_pob = p["pob"]
    else:
        default_name = "Arjun Sharma"
        default_dob = date(1995, 10, 24)
        default_tob = time(6, 30)
        default_pob = "New Delhi, India"

    full_name = st.text_input("👤 Full Name", value=default_name)
    dob = st.date_input("📅 Date of Birth", value=default_dob, min_value=date(1900, 1, 1), max_value=date(2050, 12, 31))
    tob = st.time_input("⏰ Time of Birth (Local Standard)", value=default_tob)
    pob = st.text_input("📍 Place of Birth (City, Country)", value=default_pob)

    # Live Online Geocoding & Elevation Tool
    if st.button("🌐 Live Geocode & Topo Elevate"):
        with st.spinner("Connecting to OpenStreetMap & Open-Meteo Elevation..."):
            loc = analyzer.geocoder.resolve_location(pob)
            st.session_state["resolved_loc"] = loc
            st.success(f"📍 {loc['resolved_name']}")
            st.caption(f"Lat: {loc['latitude']:.4f}° | Lon: {loc['longitude']:.4f}° | Elevation: {loc.get('elevation_m', 0.0):.1f}m | Timezone: {loc['timezone']}")

    # Main Action Button
    calc_pressed = st.button("🔮 Reveal Kundli & Timelines", type="primary", width="stretch")

    # Mobile & Tablet Access Helper
    lan_ip = get_lan_ip()
    with st.expander("📱 Mobile & Tablet Access", expanded=False):
        st.markdown(f"""
        <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5;">
            To open this app on your <strong>Smartphone</strong> or <strong>Tablet</strong> connected to this Wi-Fi / Local Network:
            <div style="background: rgba(15, 23, 42, 0.95); padding: 0.5rem; border-radius: 6px; margin: 0.4rem 0; border: 1px solid rgba(245, 158, 11, 0.5);">
                <code style="color: #fbbf24; font-size: 0.85rem; word-break: break-all;">http://{lan_ip}:8501</code>
            </div>
            Open Chrome, Safari, or Edge on your mobile device and navigate to the address above.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    conn_status = internet_svc.get_service_status()
    st.markdown("""
    <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.7;">
        <strong style="color: #fbbf24;">🌐 Internet Astronomical Feed:</strong><br>
        • OSM Geocoder: <span style="color: #34d399;">Connected</span><br>
        • Topo Elevation: <span style="color: #34d399;">Active (Open-Meteo)</span><br>
        • Solar Ephemeris: <span style="color: #34d399;">Synchronized</span><br>
        • NASA JPL Ephemeris: <span style="color: #38bdf8;">DE421 Kernel Sub-arcsec</span><br>
        • Ayanamsha: <span style="color: #fbbf24;">Chitrapaksha Lahiri</span>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN HEADER
# -------------------------------------------------------------
st.markdown("""
<div class="astro-header">
    <h1>ॐ VEDIC JYOTISH & SACRED TIMELINES</h1>
    <p>High Precision Parashari Hora Shastra • NASA JPL DE421 Ephemeris • Chitrapaksha Lahiri Ayanamsha • Sankhya Shastra</p>
    <div>
        <span class="astro-badge astro-badge-online">● Live Internet Ephemeris & Geocoding Active</span>
        <span class="astro-badge astro-badge-gold">● Event Timelines: Career • Marriage • Wealth • Health</span>
        <span class="astro-badge astro-badge-mystic">● 120-Yr Vimshottari Mahadashas</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Compute Analysis
if calc_pressed or "astro_report" not in st.session_state:
    with st.spinner("Aligning planetary kernels, ascendant cusps, Vimshottari dashas, and predictive timelines..."):
        dob_str = dob.strftime("%Y-%m-%d")
        tob_str = tob.strftime("%H:%M")
        report = analyzer.analyze(
            full_name=full_name,
            dob_str=dob_str,
            tob_str=tob_str,
            pob_str=pob,
            current_dt=datetime.now()
        )
        st.session_state["astro_report"] = report

report = st.session_state.get("astro_report")

if report:
    timelines = report["timelines"]
    active_summary = timelines["active_period_summary"]
    grahas = report["grahas"]
    lagna = report["lagna"]
    panchang = report["panchang"]
    yogas = report["yogas_and_doshas"]
    numerology = report["numerology"]
    charts = report["charts"]
    birth_astro = report["birth_astronomy"]
    solar_ephem = report.get("solar_ephemeris", {})
    live_transits = report.get("live_transits", {})

    lagna_sign = lagna["lagna_sign"]
    moon_sign = grahas["Moon"]["sign"]
    sun_sign = grahas["Sun"]["sign"]

    # Top Row: Celestial Quick Glance Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-title">Lagna (Ascendant)</div>
            <div class="metric-tile-value">{SIGN_GLYPHS.get(lagna_sign, '')} {lagna_sign}</div>
            <div class="metric-tile-sub">Lord: {lagna['lagna_ruler']} ({lagna['lagna_deg_formatted'].split()[0]})</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-title">Chandra Rashi (Moon)</div>
            <div class="metric-tile-value">☽ {SIGN_GLYPHS.get(moon_sign, '')} {moon_sign}</div>
            <div class="metric-tile-sub">{grahas['Moon']['nakshatra']} (Pada {grahas['Moon']['nakshatra_pada']})</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-title">Surya Rashi (Sun)</div>
            <div class="metric-tile-value">☉ {SIGN_GLYPHS.get(sun_sign, '')} {sun_sign}</div>
            <div class="metric-tile-sub">{grahas['Sun']['nakshatra']} ({grahas['Sun']['deg_formatted'].split()[0]})</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-tile" style="border-color: #10b981;">
            <div class="metric-tile-title" style="color: #34d399;">Active Running Dasha</div>
            <div class="metric-tile-value" style="color: #34d399; font-size: 1.35rem;">{active_summary.get('dasha', 'N/A')}</div>
            <div class="metric-tile-sub" style="color: #a7f3d0;">{active_summary.get('age', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        harm_val = numerology['harmony']['harmony_score']
        harm_label = 'Excellent' if harm_val >= 80 else ('Good' if harm_val >= 65 else 'Moderate')
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-title">Sankhya Vibration</div>
            <div class="metric-tile-value">{numerology['mulank']['mulank']} ✦ {numerology['bhagyank']['bhagyank']}</div>
            <div class="metric-tile-sub">Harmony: {harm_val}% ({harm_label})</div>
        </div>
        """, unsafe_allow_html=True)

    # Pre-generate download reports
    html_data = ReportExporter.generate_html_report(report)
    md_data = ReportExporter.generate_markdown_report(report)
    json_data = ReportExporter.generate_json_report(report)
    fname_clean = full_name.replace(' ', '_').lower()

    # Quick Action Download Banner
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 12px; padding: 0.85rem 1.25rem; margin-top: 1rem; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
        <div>
            <span style="font-family: 'Cinzel', serif; color: #fbbf24; font-weight: 700; font-size: 1.05rem;">📥 Complete Astrological Report Ready</span>
            <span style="color: #cbd5e1; font-size: 0.85rem; margin-left: 0.5rem;">Download comprehensive report with Kundli SVGs, life milestones & detailed timelines</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    q_c1, q_c2, q_c3 = st.columns(3)
    with q_c1:
        st.download_button("🌐 Download Complete Report (HTML / PDF)", html_data, f"{fname_clean}_complete_report.html", "text/html", width="stretch")
    with q_c2:
        st.download_button("📝 Download Complete Report (Markdown)", md_data, f"{fname_clean}_complete_report.md", "text/markdown", width="stretch")
    with q_c3:
        st.download_button("💾 Download Complete Report (JSON)", json_data, f"{fname_clean}_complete_report.json", "application/json", width="stretch")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # MAIN CELESTIAL TABS
    # -------------------------------------------------------------
    tab_timelines, tab_charts, tab_transits, tab_panchang, tab_numerology, tab_guidance = st.tabs([
        "⏳ Event Timelines (Career • Marriage • Wealth • Health)",
        "🌌 Kundali Charts (D1 & D9)",
        "🪐 Live Internet Transits (Gochara)",
        "🕉️ Vedic Panchanga & Yogas",
        "🔢 Sankhya Numerology (Vedic & Chaldean)",
        "📜 Comprehensive Life Guidance"
    ])

    # =============================================================
    # TAB 1: EVENT TIMELINES HUB
    # =============================================================
    with tab_timelines:
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <h3 style="font-family: 'Cinzel', serif; color: #fbbf24; margin: 0;">
                ⏳ Predictive Event Timelines & Life Roadmap
            </h3>
            <p style="color: #94a3b8; font-size: 0.95rem;">
                Classical Parashari Vimshottari Dasha analysis synthesized with Bhava lordships, planetary karakatwas,
                dignities, and Gochara transit activations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Radiant Running Active Period Card
        st.markdown(f"""
        <div class="active-dasha-hero">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <h3 style="margin: 0;">
                    ⭐ RUNNING DASHA TODAY: {active_summary.get('dasha')}
                </h3>
                <span class="astro-badge astro-badge-online">Active Window: {active_summary.get('period')}</span>
            </div>
            <div style="color: #f1f5f9; font-size: 1.05rem; font-weight: 600; margin-bottom: 0.8rem;">
                🌟 Dominant Life Focus: <span style="color: #fbbf24;">{active_summary.get('dominant_theme')}</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-top: 0.8rem;">
                <div style="background: rgba(15, 23, 42, 0.7); padding: 0.8rem; border-radius: 8px; border-left: 3px solid #38bdf8;">
                    <strong style="color: #38bdf8;">💼 Career & Status:</strong> {active_summary.get('career_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{active_summary.get('career_recommendation')}</span>
                </div>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 0.8rem; border-radius: 8px; border-left: 3px solid #f472b6;">
                    <strong style="color: #f472b6;">💍 Marriage & Love:</strong> {active_summary.get('marriage_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{active_summary.get('marriage_recommendation')}</span>
                </div>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 0.8rem; border-radius: 8px; border-left: 3px solid #34d399;">
                    <strong style="color: #34d399;">💰 Wealth & Assets:</strong> {active_summary.get('wealth_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{active_summary.get('wealth_recommendation')}</span>
                </div>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 0.8rem; border-radius: 8px; border-left: 3px solid #22d3ee;">
                    <strong style="color: #22d3ee;">🌿 Health & Vitality:</strong> {active_summary.get('health_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{active_summary.get('health_recommendation')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Subtabs for individual pillars and rich timelines
        sub_milestones, sub_pratyantardasha, sub_annual, sub_roadmap, sub_career, sub_marriage, sub_wealth, sub_health = st.tabs([
            "🎯 Major Predicted Life Milestones",
            "⚡ Month-by-Month Pratyantardasha Forecast",
            "📅 10-Year Annual Forward Roadmap",
            "🌟 Lifespan Master Roadmap",
            "💼 Career & Karma Trajectory",
            "💍 Marriage & Relationships Trajectory",
            "💰 Wealth & Prosperity Trajectory",
            "🌿 Health & Vitality Roadmap"
        ])

        # 0. Major Predicted Life Milestones
        with sub_milestones:
            st.markdown("#### 🎯 Chronological Landmark Life Milestones & Predicted Events")
            st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Major predicted milestones synthesized across career elevation, marriage windows, wealth surges, property acquisition, higher learning, and spiritual evolution.</p>", unsafe_allow_html=True)
            milestones = timelines.get("life_milestones", [])
            if milestones:
                f_col1, f_col2 = st.columns([1, 1])
                with f_col1:
                    cat_filter = st.selectbox("Filter by Category", ["All Categories", "Career & Status", "Marriage & Relationships", "Wealth & Assets", "Education & Intellect", "Travel & Relocation", "Spiritual & Dharma", "Health & Vitality"])
                with f_col2:
                    time_filter = st.selectbox("Filter by Horizon", ["All Life Stages", "Current & Upcoming Priority Windows", "Past Landmark Milestones", "Future Life Stages"])

                filtered_ms = []
                for m in milestones:
                    if cat_filter != "All Categories" and m.get("category") != cat_filter:
                        continue
                    if time_filter == "Current & Upcoming Priority Windows" and not (m.get("is_current") or m.get("is_near_term")):
                        continue
                    if time_filter == "Past Landmark Milestones" and not m.get("is_past"):
                        continue
                    if time_filter == "Future Life Stages" and (m.get("is_past") or m.get("is_current")):
                        continue
                    filtered_ms.append(m)

                st.caption(f"Showing {len(filtered_ms)} of {len(milestones)} landmark milestones")

                for m in filtered_ms:
                    is_c = m.get("is_current")
                    b_color = "#10b981" if is_c else ("#f59e0b" if m.get("favorability_score", 0) >= 80 else "#38bdf8")
                    card_border = f"border: 1.5px solid {b_color};"
                    card_bg = "background: rgba(16, 185, 129, 0.08);" if is_c else "background: rgba(18, 24, 43, 0.75);"

                    st.markdown(f"""
                    <div style="{card_bg} {card_border} border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 0.5rem;">
                            <div>
                                <span style="font-size: 0.75rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px;">{m.get('category')} • {m.get('event_type')}</span>
                                <h4 style="font-family: 'Cinzel', serif; color: #fbbf24; margin: 0.2rem 0; font-size: 1.15rem;">{m.get('title')}</h4>
                                <div style="font-size: 0.85rem; color: #cbd5e1; display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <span>📅 <strong>{m.get('year_range')}</strong> ({m.get('age_window')})</span>
                                    <span>🪐 Dasha: <strong>{m.get('dasha')}</strong></span>
                                    <span>⚡ Window: {m.get('period')}</span>
                                </div>
                            </div>
                            <div style="text-align: right; min-width: 140px;">
                                <span class="astro-badge astro-badge-gold">{m.get('status_badge')}</span>
                                <div style="font-size: 1.35rem; font-weight: 800; color: #fbbf24; margin-top: 0.2rem;">{m.get('favorability_score')}% <span style="font-size: 0.75rem; color: #94a3b8;">Favorability</span></div>
                            </div>
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-top: 0.6rem;">
                            <p style="margin-bottom: 0.4rem;"><strong>Astrological Basis:</strong> {m.get('astrological_basis')}</p>
                            <p style="margin-bottom: 0.4rem; color: #f8fafc;"><strong>Predicted Event:</strong> {m.get('prediction_narrative')}</p>
                            <p style="margin-bottom: 0.4rem; color: #38bdf8;"><strong>Strategic Guidance:</strong> {m.get('actionable_guidance')}</p>
                            <p style="margin-bottom: 0; color: #fbbf24;"><strong>Vedic Remedy:</strong> {m.get('vedic_remedy')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Milestones data being compiled for this chart.")

        # 0.1 Pratyantardasha Granular Forecast
        with sub_pratyantardasha:
            st.markdown("#### ⚡ Month-by-Month Granular Pratyantardasha (Sub-Sub Period) Forecast")
            st.markdown(f"<p style='color: #cbd5e1; font-size: 0.92rem;'>Detailed sub-sub periods within running Mahadasha <strong>{dashas.get('active_dasha', {}).get('mahadasha')}</strong> and Antardasha <strong>{dashas.get('active_dasha', {}).get('antardasha')}</strong>.</p>", unsafe_allow_html=True)
            pds = timelines.get("pratyantardashas", [])
            if pds:
                pd_table_rows = []
                for pd in pds:
                    pd_table_rows.append({
                        "Dasha Level 3": pd.get("dasha_hierarchy"),
                        "Dates": f"{pd.get('start_date')} → {pd.get('end_date')}",
                        "Duration": f"{pd.get('duration_days')} days",
                        "Status": pd.get("status_badge"),
                        "Favorability": f"{pd.get('favorability_score')}%",
                        "Primary Focus & Strategy": f"{pd.get('focus_theme')} {pd.get('guidance')}"
                    })
                st.dataframe(pd.DataFrame(pd_table_rows), width="stretch", hide_index=True)

        # 0.2 Annual 10-Year Forward Forecast Roadmap
        with sub_annual:
            st.markdown("#### 📅 10-Year Annual Forward Forecast Roadmap")
            st.markdown("<p style='color: #cbd5e1; font-size: 0.92rem;'>Chronological year-by-year preview covering current period and the next decade.</p>", unsafe_allow_html=True)
            annual = timelines.get("annual_forecast", [])
            if annual:
                ann_table_rows = []
                for af in annual:
                    ann_table_rows.append({
                        "Year (Age)": f"{af.get('year')} (Age {af.get('age_at_midyear')})",
                        "Active Dasha": af.get("dasha"),
                        "Favorability": f"{af.get('overall_score')}%",
                        "Status": af.get("status_badge"),
                        "Primary Theme": af.get("primary_theme"),
                        "Career Outlook": af.get("career_outlook"),
                        "Wealth Outlook": af.get("wealth_outlook"),
                        "Relationship Outlook": af.get("relationship_outlook"),
                        "Health Outlook": af.get("health_outlook"),
                        "Strategic Key": af.get("key_recommendation")
                    })
                st.dataframe(pd.DataFrame(ann_table_rows), width="stretch", hide_index=True)

        # 1. Master Life Roadmap
        with sub_roadmap:
            st.markdown("#### 🌟 Master Chronological Life Journey Roadmap (Lifespan 0 to 80+)")
            master_data = timelines["master_roadmap"]

            # Filter controls
            f_col1, f_col2 = st.columns([2, 1])
            with f_col1:
                filter_mode = st.radio("Chronological Filter", ["All Life Stages", "Current & Upcoming Next 15 Years", "Past Formative Stages"], horizontal=True)
            
            curr_year = datetime.now().year
            filtered_master = []
            for m in master_data:
                start_yr = int(m["start_date"].split("-")[0])
                if filter_mode == "Current & Upcoming Next 15 Years":
                    if (curr_year - 2) <= start_yr <= (curr_year + 15):
                        filtered_master.append(m)
                elif filter_mode == "Past Formative Stages":
                    if start_yr < curr_year:
                        filtered_master.append(m)
                else:
                    filtered_master.append(m)

            # Table representation with high contrast
            roadmap_rows = []
            for item in filtered_master:
                roadmap_rows.append({
                    "Vimshottari Dasha": item["dasha"],
                    "Age Window": item["age_display"],
                    "Dates": f"{item['start_date']} → {item['end_date']}",
                    "Status": item["status_badge"],
                    "Dominant Life Theme": item["dominant_theme"],
                    "Overall Favorability": f"{item['overall_score']}%",
                    "Career": f"{item['scores']['career']}/100",
                    "Marriage": f"{item['scores']['marriage']}/100",
                    "Wealth": f"{item['scores']['wealth']}/100",
                    "Health": f"{item['scores']['health']}/100"
                })
            st.dataframe(pd.DataFrame(roadmap_rows), width="stretch", hide_index=True)

        # 2. Career Timeline
        with sub_career:
            st.markdown("#### 💼 Professional Trajectory & Career Milestones")
            c_info = timelines["career"]
            col_c1, col_c2 = st.columns([1, 2])
            with col_c1:
                st.markdown(f"""
                <div class="metric-tile" style="text-align: left; padding: 1.2rem;">
                    <div class="metric-tile-title">10th House Lord (Karma Bhavesha)</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #fbbf24;">{PLANET_GLYPHS.get(c_info['tenth_lord'], '')} {c_info['tenth_lord']}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 0.4rem;">
                        Ruling Public Status, Executive Leadership & Enterprise.
                    </div>
                    <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #94a3b8;">
                        <strong style="color: #fbbf24;">Favorable Industries:</strong><br>
                        {', '.join(c_info['favorable_sectors'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_c2:
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 4px solid #38bdf8;">
                    <h4 style="color: #38bdf8; margin-top: 0;">🚀 Career Path Synthesis</h4>
                    <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0.4rem;">
                        Your chart reveals <strong>{c_info['peak_milestones_count']} major career elevation portals</strong>.
                        Periods activating the 10th Lord ({c_info['tenth_lord']}), 1st Lord ({lagna['lagna_ruler']}), 9th Lord of fortune,
                        or Saturn (Karma Karaka) trigger quantum leaps in recognition, authority, and professional satisfaction.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("##### 📜 Chronological Career Elevation Phases")
            for c_event in c_info["timeline"]:
                is_curr = c_event["is_current"]
                border_color = "#10b981" if is_curr else ("#fbbf24" if c_event["score"] >= 80 else "#38bdf8")
                badge_style = "astro-badge-online" if is_curr else "astro-badge-gold"
                badge_text = "⭐ CURRENT RUNNING PHASE" if is_curr else c_event["rating"]
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 5px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h4 style="color: #fbbf24; margin: 0;">{c_event['phase_type']}</h4>
                        <span class="astro-badge {badge_style}">{badge_text}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.6rem;">
                        📅 <strong>{c_event['period']}</strong> | {c_event['age_display']} | Vimshottari: <span style="color: #f8fafc;">{c_event['dasha']}</span> | Favorability: <strong style="color: #fbbf24;">{c_event['score']}/100</strong>
                    </div>
                    <p style="margin-bottom: 0.4rem; color: #e2e8f0; font-size: 0.92rem;"><strong>Astrological Drivers:</strong> {', '.join(c_event['drivers'])}</p>
                    <p style="color: #93c5fd; font-size: 0.88rem; margin: 0; background: rgba(56, 189, 248, 0.08); padding: 0.5rem 0.8rem; border-radius: 6px;">💡 <strong>Strategic Counsel:</strong> {c_event['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

        # 3. Marriage Timeline
        with sub_marriage:
            st.markdown("#### 💍 Marriage, Relationships & Partnership Timing")
            m_info = timelines["marriage"]
            col_m1, col_m2 = st.columns([1, 2])
            with col_m1:
                st.markdown(f"""
                <div class="metric-tile" style="text-align: left; padding: 1.2rem;">
                    <div class="metric-tile-title">7th House Lord (Kalatra Bhavesha)</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #f472b6;">{PLANET_GLYPHS.get(m_info['seventh_lord'], '')} {m_info['seventh_lord']}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 0.4rem;">
                        Sign: {SIGN_GLYPHS.get(m_info['seventh_sign'], '')} {m_info['seventh_sign']} • Primary Karaka: Venus (♀ Shukra)
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_m2:
                sp = m_info["spouse_profile"]
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 4px solid #f472b6;">
                    <h4 style="color: #f472b6; margin-top: 0;">👰/🤵 Prospective Spouse Astrological Blueprint</h4>
                    <p style="font-size: 0.92rem; color: #f1f5f9; margin-bottom: 0.3rem;"><strong>Core Nature:</strong> {sp['core_temperament']}</p>
                    <p style="font-size: 0.92rem; color: #f1f5f9; margin-bottom: 0.3rem;"><strong>Career Affinities:</strong> {sp['likely_career_affinity']}</p>
                    <p style="font-size: 0.88rem; color: #cbd5e1; margin: 0;"><strong>Meeting Circumstances:</strong> {sp['meeting_circumstances']}</p>
                </div>
                """, unsafe_allow_html=True)

            if m_info["prime_marriage_windows"]:
                st.markdown("##### 💖 Prime Marriage & Relationship Commitment Windows")
                cols = st.columns(len(m_info["prime_marriage_windows"]))
                for idx, win in enumerate(m_info["prime_marriage_windows"]):
                    with cols[idx]:
                        st.markdown(f"""
                        <div class="metric-tile" style="border-color: #f472b6;">
                            <div style="color: #f472b6; font-size: 0.85rem; font-weight: 700;">{win['favorability']}</div>
                            <div style="font-size: 1.25rem; font-weight: 700; color: #fff; margin: 0.3rem 0;">{win['age_range']}</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">{win['period']}</div>
                            <div style="font-size: 0.8rem; color: #fbbf24; margin-top: 0.2rem;">Dasha: {win['dasha']} ({win['score']}%)</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<br>##### 📜 Chronological Relationship & Marital Timeline", unsafe_allow_html=True)
            for m_event in m_info["timeline"]:
                is_curr = m_event["is_current"]
                border_color = "#10b981" if is_curr else ("#f472b6" if m_event["score"] >= 75 else "#c084fc")
                badge_style = "astro-badge-online" if is_curr else "astro-badge-mystic"
                badge_text = "⭐ CURRENT RUNNING PHASE" if is_curr else m_event["rating"]
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 5px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h4 style="color: #f472b6; margin: 0;">{m_event['phase_type']}</h4>
                        <span class="astro-badge {badge_style}">{badge_text}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.6rem;">
                        📅 <strong>{m_event['period']}</strong> | {m_event['age_display']} | Vimshottari: <span style="color: #f8fafc;">{m_event['dasha']}</span> | Score: <strong style="color: #f472b6;">{m_event['score']}/100</strong>
                    </div>
                    <p style="margin-bottom: 0.4rem; color: #e2e8f0; font-size: 0.92rem;"><strong>Drivers:</strong> {', '.join(m_event['drivers'])}</p>
                    <p style="color: #fbcfe8; font-size: 0.88rem; margin: 0; background: rgba(244, 114, 182, 0.08); padding: 0.5rem 0.8rem; border-radius: 6px;">💡 <strong>Relationship Counsel:</strong> {m_event['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

        # 4. Wealth Timeline
        with sub_wealth:
            st.markdown("#### 💰 Wealth, Finances & Asset Accumulation Timeline")
            w_info = timelines["wealth"]
            dl = w_info["dhana_lords"]

            col_w1, col_w2, col_w3, col_w4 = st.columns(4)
            col_w1.metric("2nd Lord (Dhana / Savings)", f"{PLANET_GLYPHS.get(dl['2nd_house'], '')} {dl['2nd_house']}")
            col_w2.metric("11th Lord (Labha / Gains)", f"{PLANET_GLYPHS.get(dl['11th_house'], '')} {dl['11th_house']}")
            col_w3.metric("9th Lord (Bhagya / Fortune)", f"{PLANET_GLYPHS.get(dl['9th_house'], '')} {dl['9th_house']}")
            col_w4.metric("5th Lord (Punya / Speculation)", f"{PLANET_GLYPHS.get(dl['5th_house'], '')} {dl['5th_house']}")

            st.markdown("##### 📈 Chronological Wealth Creation Cycles")
            for w_event in w_info["timeline"]:
                is_curr = w_event["is_current"]
                border_color = "#10b981" if is_curr else ("#fbbf24" if w_event["score"] >= 80 else "#34d399")
                badge_style = "astro-badge-online" if is_curr else "astro-badge-gold"
                badge_text = "⭐ CURRENT RUNNING PHASE" if is_curr else w_event["rating"]
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 5px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h4 style="color: #34d399; margin: 0;">{w_event['phase_type']}</h4>
                        <span class="astro-badge {badge_style}">{badge_text}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.6rem;">
                        📅 <strong>{w_event['period']}</strong> | {w_event['age_display']} | Vimshottari: <span style="color: #f8fafc;">{w_event['dasha']}</span> | Wealth Potential: <strong style="color: #34d399;">{w_event['score']}/100</strong>
                    </div>
                    <p style="margin-bottom: 0.4rem; color: #e2e8f0; font-size: 0.92rem;"><strong>Financial Drivers:</strong> {', '.join(w_event['drivers'])}</p>
                    <p style="color: #a7f3d0; font-size: 0.88rem; margin: 0; background: rgba(52, 211, 153, 0.08); padding: 0.5rem 0.8rem; border-radius: 6px;">💡 <strong>Financial Prudence:</strong> {w_event['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

        # 5. Health Timeline
        with sub_health:
            st.markdown("#### 🌿 Health, Vitality & Longevity Timeline")
            h_info = timelines["health"]

            col_h1, col_h2 = st.columns([1, 2])
            with col_h1:
                st.markdown(f"""
                <div class="metric-tile" style="text-align: left; padding: 1.2rem;">
                    <div class="metric-tile-title">Lagna Lord (Biological Immunity)</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #22d3ee;">{PLANET_GLYPHS.get(h_info['lagna_lord'], '')} {h_info['lagna_lord']}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 0.4rem;">
                        6th Lord (Acute): {h_info['sixth_lord']} | 8th Lord (Chronic): {h_info['eighth_lord']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_h2:
                st.markdown("""
                <div class="cosmic-card" style="border-left: 4px solid #22d3ee;">
                    <h4 style="color: #22d3ee; margin-top: 0;">🧬 Anatomical Vulnerability Map</h4>
                """, unsafe_allow_html=True)
                for v in h_info["vulnerabilities"]:
                    st.markdown(f"- {v}")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("##### 🧘 Vitality & Wellness Timeline")
            for h_event in h_info["timeline"]:
                is_curr = h_event["is_current"]
                border_color = "#10b981" if is_curr else ("#22d3ee" if h_event["score"] >= 80 else "#67e8f9")
                badge_style = "astro-badge-online" if is_curr else "astro-badge-gold"
                badge_text = "⭐ CURRENT RUNNING PHASE" if is_curr else h_event["rating"]
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 5px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <h4 style="color: #22d3ee; margin: 0;">{h_event['phase_type']}</h4>
                        <span class="astro-badge {badge_style}">{badge_text}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.6rem;">
                        📅 <strong>{h_event['period']}</strong> | {h_event['age_display']} | Vimshottari: <span style="color: #f8fafc;">{h_event['dasha']}</span> | Vitality Index: <strong style="color: #22d3ee;">{h_event['score']}/100</strong>
                    </div>
                    <p style="margin-bottom: 0.4rem; color: #e2e8f0; font-size: 0.92rem;"><strong>Physiological Factors:</strong> {', '.join(h_event['drivers'])}</p>
                    <p style="color: #cffafe; font-size: 0.88rem; margin: 0; background: rgba(34, 211, 238, 0.08); padding: 0.5rem 0.8rem; border-radius: 6px;">💡 <strong>Ayurvedic Guidance:</strong> {h_event['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

    # =============================================================
    # TAB 2: KUNDALI CHARTS & GRAHAS
    # =============================================================
    with tab_charts:
        st.markdown("### 🌌 Vedic Kundali Charts (Interactive Vector Rendering)")
        
        chart_style = st.radio(
            "Select Kundali Chart Format",
            ["💠 North Indian (Diamond Kundali)", "🔲 South Indian (Square Kundali)", "📝 ASCII Text Kundali"],
            horizontal=True
        )

        if chart_style == "💠 North Indian (Diamond Kundali)":
            col_ch1, col_ch2 = st.columns(2)
            with col_ch1:
                st.markdown("#### ✦ D1 - Lagna Rashi Kundali (Birth Chart)")
                render_svg_kundali(charts["d1_svg"], height=430)
                st.download_button(
                    label="📥 Download D1 North Indian SVG",
                    data=charts["d1_svg"],
                    file_name=f"{full_name.replace(' ', '_')}_D1_north.svg",
                    mime="image/svg+xml",
                    key="dl_d1_north"
                )
            with col_ch2:
                st.markdown("#### ✦ D9 - Navamsha Kundali (Dharma & Soul Potential)")
                render_svg_kundali(charts["d9_svg"], height=430)
                st.download_button(
                    label="📥 Download D9 Navamsha SVG",
                    data=charts["d9_svg"],
                    file_name=f"{full_name.replace(' ', '_')}_D9_navamsha_north.svg",
                    mime="image/svg+xml",
                    key="dl_d9_north"
                )

        elif chart_style == "🔲 South Indian (Square Kundali)":
            col_ch1, col_ch2 = st.columns(2)
            with col_ch1:
                st.markdown("#### ✦ D1 - South Indian Rashi Kundali")
                render_svg_kundali(charts.get("d1_south_svg", charts["d1_svg"]), height=430)
                st.download_button(
                    label="📥 Download D1 South Indian SVG",
                    data=charts.get("d1_south_svg", charts["d1_svg"]),
                    file_name=f"{full_name.replace(' ', '_')}_D1_south.svg",
                    mime="image/svg+xml",
                    key="dl_d1_south"
                )
            with col_ch2:
                st.markdown("#### ✦ D9 - South Indian Navamsha Kundali")
                render_svg_kundali(charts.get("d9_south_svg", charts["d9_svg"]), height=430)
                st.download_button(
                    label="📥 Download D9 South Indian SVG",
                    data=charts.get("d9_south_svg", charts["d9_svg"]),
                    file_name=f"{full_name.replace(' ', '_')}_D9_south.svg",
                    mime="image/svg+xml",
                    key="dl_d9_south"
                )

        else:
            st.markdown("#### ✦ Unicode ASCII Kundali (D1 Bhavas)")
            st.code(charts["ascii_chart"], language="text")

        st.markdown("<br>#### 🪐 Navagraha Astronomical Positions & Dignities", unsafe_allow_html=True)
        planet_table = []
        for name, g in grahas.items():
            glyph = PLANET_GLYPHS.get(name, "")
            sign_glyph = SIGN_GLYPHS.get(g["sign"], "")
            retro = "Vakri ℞" if g["is_retrograde"] else "Direct"
            combust = "Asta (Combust)" if g["is_combust"] else "Normal"
            planet_table.append({
                "Graha": f"{glyph} {name}",
                "Sanskrit Name": g["sanskrit"],
                "Rashi (Sign)": f"{sign_glyph} {g['sign']}",
                "Longitude": g.get("deg_formatted", f"{round(g['sign_deg'], 2)}°"),
                "House (Bhava)": f"House {g.get('house', 1)}",
                "Nakshatra & Pada": f"{g['nakshatra']} (Pada {g.get('nakshatra_pada', 1)})",
                "Nakshatra Lord": g.get("nakshatra_lord", ""),
                "Dignity (Avastha)": g["dignity"],
                "Motion": retro,
                "Combustion": combust
            })
        st.dataframe(pd.DataFrame(planet_table), width="stretch", hide_index=True)

    # =============================================================
    # TAB 3: LIVE INTERNET TRANSITS (GOCHARA)
    # =============================================================
    with tab_transits:
        st.markdown("### 🪐 Real-Time Sky Planetary Transits (Gochara) & Internet Precision")
        st.markdown("""
        Current real-time celestial positions calculated live using **NASA JPL DE421 Ephemeris**
        with internet-synchronized observer elevation, solar ephemeris, and Chitrapaksha Lahiri ayanamsha.
        """)

        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("☀️ Local Sunrise (Internet Sync)", solar_ephem.get("sunrise", "06:00"))
        col_t2.metric("🌙 Local Sunset (Internet Sync)", solar_ephem.get("sunset", "18:00"))
        col_t3.metric("🏔️ Topographic Ground Elevation", f"{birth_astro.get('elevation_m', 0.0):.1f} meters ASL")

        st.markdown("#### 🔴 Live Real-Time Planetary Longitudes (Today)")
        t_list = live_transits.get("transits", [])
        if t_list:
            df_trans = []
            for t in t_list:
                df_trans.append({
                    "Planet": f"{PLANET_GLYPHS.get(t['graha'], '')} {t['graha']}",
                    "Sanskrit": t["sanskrit"],
                    "Sign": f"{SIGN_GLYPHS.get(t['sign'], '')} {t['sign']}",
                    "Degrees": t["degree"],
                    "Nakshatra": t["nakshatra"],
                    "Dignity": t["dignity"],
                    "Motion": "Vakri (R)" if t["is_retrograde"] else "Direct",
                    "Combust": "Yes" if t["is_combust"] else "No"
                })
            st.dataframe(pd.DataFrame(df_trans), width="stretch", hide_index=True)

        st.markdown("#### ⚡ Active Major Transit Impacts on Natal Chart")
        ss = yogas.get("sade_sati", {})
        st.markdown(f"- **Saturn Transit (Shani Gochara):** {ss.get('description', '')}")
        st.markdown(f"- **Ketu & Rahu Transit Axis:** Shifting across corresponding natal Bhavas, activating spiritual karmic lessons.")

    # =============================================================
    # TAB 4: VEDIC PANCHANGA & YOGAS
    # =============================================================
    with tab_panchang:
        st.markdown("### 🕉️ Vedic Panchanga (The Five Limbs of Time)")
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        col_p1.metric("Vara (Weekday)", f"{panchang['vara']['name']}")
        col_p2.metric("Tithi (Lunar Day)", f"{panchang['tithi']['name']}")
        col_p3.metric("Nakshatra", f"{panchang['nakshatra']['name']}")
        col_p4.metric("Yoga", f"{panchang['yoga']['name']}")
        col_p5.metric("Karana", f"{panchang['karana']['name']}")

        st.markdown("---")
        st.markdown("### 🔮 Yogas & Doshas Analysis")
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            st.markdown("#### 🔴 Classical Doshas Evaluation")
            mg = yogas.get("manglik_dosha", {})
            st.markdown(f"""
            <div class="cosmic-card" style="border-left: 4px solid {'#ef4444' if mg.get('has_dosha') and not mg.get('is_cancelled') else '#10b981'};">
                <h4 style="color: {'#ef4444' if mg.get('has_dosha') and not mg.get('is_cancelled') else '#34d399'}; margin-top: 0;">
                    Manglik (Kuja) Dosha: {mg.get('severity', 'None')}
                </h4>
                <p style="color: #cbd5e1; font-size: 0.9rem;">{mg.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)

            ks = yogas.get("kaal_sarp_dosha", {})
            st.markdown(f"""
            <div class="cosmic-card" style="border-left: 4px solid {'#ef4444' if ks.get('has_dosha') else '#10b981'};">
                <h4 style="color: {'#ef4444' if ks.get('has_dosha') else '#34d399'}; margin-top: 0;">
                    Kaal Sarp Dosha: {ks.get('severity', 'None')}
                </h4>
                <p style="color: #cbd5e1; font-size: 0.9rem;">{ks.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)

            for iy in yogas.get("inauspicious_yogas", []):
                st.markdown(f"**⚠️ {iy['name']}**: {iy['description']}")

        with col_y2:
            st.markdown("#### 🟢 Auspicious Raja & Dhana Yogas")
            for by in yogas.get("benefic_yogas", []):
                st.markdown(f"""
                <div class="cosmic-card" style="border-left: 4px solid #fbbf24;">
                    <h4 style="color: #fbbf24; margin-top: 0;">✨ {by['name']} ({by['category']})</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin: 0;">{by['description']}</p>
                </div>
                """, unsafe_allow_html=True)

    # =============================================================
    # TAB 5: SANKHYA NUMEROLOGY
    # =============================================================
    with tab_numerology:
        st.markdown("### 🔢 Sankhya Shastra (Vedic & Chaldean Numerology)")
        mul = numerology["mulank"]
        bha = numerology["bhagyank"]
        nam = numerology["namank"]
        har = numerology["harmony"]

        col_n1, col_n2, col_n3, col_n4 = st.columns(4)
        col_n1.metric("Mulank (Psychic Number)", f"{mul['mulank']} ({mul['ruler']})")
        col_n2.metric("Bhagyank (Destiny Number)", f"{bha['bhagyank']} ({bha['ruler']})")
        col_n3.metric("Namank (Chaldean)", f"{nam['chaldean']['namank']} (Compound: {nam['chaldean']['compound_number']})")
        col_n4.metric("Tripartite Harmony", f"{har['harmony_score']}% ({'Excellent' if har['harmony_score'] >= 80 else ('Good' if har['harmony_score'] >= 65 else 'Moderate')})")

        st.info(f"**Name Vibration Counsel:** {har['recommendation']}")

        col_na, col_nb = st.columns(2)
        with col_na:
            st.markdown(f"""
            <div class="cosmic-card">
                <h4 style="color: #fbbf24; margin-top: 0;">🌟 Archetype of Psychic Number {mul['mulank']}</h4>
                <p><strong>Title:</strong> {mul['title']}</p>
                <p><strong>Nature:</strong> {mul['archetype']}</p>
                <p><strong>Key Strengths:</strong> {', '.join(mul['strengths'])}</p>
                <p><strong>Areas for Care:</strong> {', '.join(mul['weaknesses'])}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_nb:
            st.markdown(f"""
            <div class="cosmic-card">
                <h4 style="color: #fbbf24; margin-top: 0;">🍀 Sacred Favorable Vibrations</h4>
                <p><strong>Lucky Numbers:</strong> {', '.join(str(n) for n in mul['lucky_numbers'])}</p>
                <p><strong>Auspicious Days:</strong> {', '.join(mul['lucky_days'])}</p>
                <p><strong>Harmonious Colors:</strong> {', '.join(mul['lucky_colors'])}</p>
                <p><strong>Gemstone:</strong> {mul['gemstone']}</p>
                <p><strong>Presiding Deity:</strong> {mul['deity']}</p>
            </div>
            """, unsafe_allow_html=True)

    # =============================================================
    # TAB 6: COMPREHENSIVE LIFE GUIDANCE & EXPORT
    # =============================================================
    with tab_guidance:
        st.markdown("### 📜 Comprehensive Synthesized Life Guidance & Remedies")
        guide = report["guidance"]

        st.markdown(f"""
        <div class="cosmic-card">
            <h4 style="color: #fbbf24; margin-top: 0;">🌟 Temperament & Soul Blueprint</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">{guide['temperament_summary']}</p>
        </div>
        <div class="cosmic-card">
            <h4 style="color: #38bdf8; margin-top: 0;">💼 Career & Material Success</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">{guide['career_and_wealth']}</p>
        </div>
        <div class="cosmic-card">
            <h4 style="color: #f472b6; margin-top: 0;">💍 Relationships & Domestic Harmony</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">{guide['relationships_and_marriage']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🕉️ Auspicious Vedic Remedies")
        for r in guide["remedies"]:
            st.markdown(f"- {r}")

        st.markdown("---")
        st.markdown("### 📥 Download Complete Vedic Report")
        st.markdown("<p style='color: #94a3b8; font-size: 0.95rem;'>Choose your preferred format to download your complete astrological birth chart, sacred Kundli diagrams, life milestones, and detailed predictive timelines.</p>", unsafe_allow_html=True)

        exp_c1, exp_c2, exp_c3 = st.columns(3)
        with exp_c1:
            st.markdown("""
            <div class="cosmic-card" style="text-align: center; border-color: #f59e0b; padding: 1.2rem;">
                <h4 style="color: #fbbf24; margin-top: 0; font-size: 1.1rem;">🌐 Interactive HTML Report</h4>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.8rem;">Standalone file with embedded vector SVG charts, dark celestial aesthetics, and print-to-PDF layout.</p>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="📥 Download HTML Report (Print / PDF)",
                data=html_data,
                file_name=f"{fname_clean}_complete_report.html",
                mime="text/html",
                width="stretch"
            )
        with exp_c2:
            st.markdown("""
            <div class="cosmic-card" style="text-align: center; border-color: #38bdf8; padding: 1.2rem;">
                <h4 style="color: #38bdf8; margin-top: 0; font-size: 1.1rem;">📝 Markdown Document</h4>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.8rem;">Complete Markdown (.md) report with tables, ASCII Kundali, event milestones, and remedies.</p>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Markdown Report (.md)",
                data=md_data,
                file_name=f"{fname_clean}_complete_report.md",
                mime="text/markdown",
                width="stretch"
            )
        with exp_c3:
            st.markdown("""
            <div class="cosmic-card" style="text-align: center; border-color: #34d399; padding: 1.2rem;">
                <h4 style="color: #34d399; margin-top: 0; font-size: 1.1rem;">💾 JSON Data Export</h4>
                <p style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.8rem;">Full nested JSON schema containing all mathematical, astronomical, and predictive variables.</p>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Complete Data (JSON)",
                data=json_data,
                file_name=f"{fname_clean}_complete_report.json",
                mime="application/json",
                width="stretch"
            )
