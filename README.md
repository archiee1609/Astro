# ॐ Vedic Jyotish & Sankhya Numerology Application

A high-precision Python-based application for **Hindu Vedic Astrology (Parashari Jyotish)** and **Vedic & Chaldean Numerology (Sankhya Shastra)** with **Predictive Event Timelines**, **Live Internet-Powered Astronomical Precision**, and an interactive **Streamlit Web Dashboard**.

---

## 🌟 Key Features

### 1. ⏳ Predictive Event Timelines (Career • Marriage • Wealth • Health)
- **Master Life Journey Roadmap**: Chronological sequence of all Vimshottari Mahadasha/Antardasha phases across life with age spans, overall favorability scores (0–100%), and dominant themes.
- **💼 Career & Karma Timeline**:
  - 10th House Lord (Karma Bhavesha), 1st Lord, 9th Lord, 11th Lord, Sun, and Saturn activation analysis.
  - Identification of promotion windows, executive elevation milestones, entrepreneurial phases, and career pivots.
- **💍 Marriage & Relationships Timeline**:
  - 7th House Lord (Kalatra Bhavesha), Venus, Jupiter, and 2nd/11th lords tracking.
  - Prime marriage windows (age 21–38+), prospective spouse profile (core temperament, career affinity, meeting circumstances), and relationship harmony advice.
- **💰 Wealth & Prosperity Timeline**:
  - Dhana Yogas triggered across 2nd (accumulated wealth), 11th (gains/cashflow), 9th (fortune), and 5th houses.
  - Wealth surge phases, real estate/property acquisition windows, and expenditure caution periods.
- **🌿 Health & Vitality Timeline**:
  - 1st Lord (vitality/immunity), 6th Lord (acute illness), 8th Lord (chronic health/longevity), 12th Lord (rest/hospitalization).
  - Anatomical vulnerability map by afflicted signs/houses and Ayurvedic balancing recommendations.

### 2. 🌐 Internet Astrological Precision & Live Ephemeris
- **OpenStreetMap Nominatim Geocoding**: Real-time worldwide geocoding with full address hierarchy for any city, town, or village.
- **Open-Meteo High Precision Elevation API**: Fetches exact ground topographic elevation in meters above sea level to refine topocentric horizon and ascendant computations.
- **Open-Meteo Solar Ephemeris**: Synchronizes local astronomical sunrise, sunset, and daylight duration to authenticate Vedic Dina-Māna and Ratri-Māna.
- **Real-Time Planetary Transits (Gochara)**: Live celestial positions of Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu computed for today with active impacts on natal Moon and Lagna (e.g. Sade Sati, Kantaka Shani, Jupiter's blessings).

### 3. 🖥️ Interactive Streamlit Web Application
- **Modern Cosmic Theme**: Styled with Sanskrit typography, Vedic spiritual aesthetic, interactive sliders, cards, and dataframes.
- **Live Geocode Search Button**: Instant online location lookup displaying latitude, longitude, and elevation.
- **Preset Quick Profiles**: One-click analysis for sample profiles (Arjun Sharma, Priya Patel, Steve Jobs, Vikramaditya).
- **Interactive SVG Kundali Visualizer**: Vector rendering of North Indian Diamond Kundali for D1 (Lagna Rashi) and D9 (Navamsha) charts.
- **Instant JSON Export**: One-click full report export for downstream integration.

### 4. 🔭 High-Precision Astronomical & Vedic Ephemeris
- **NASA JPL DE421 Ephemeris**: Sub-arcsecond accuracy for celestial longitudes of Sun, Moon, Mars, Mercury, Jupiter, Venus, and Saturn.
- **Chitrapaksha (Lahiri) Ayanamsha**: Standard Indian Astronomical Ephemeris standard (epoch J2000.0 $23^\circ 51' 25.532"$, precession $50.28796"$ per year).
- **Lunar Nodes (Rahu & Ketu)**: Analytical mean lunar node calculations and 180° counter-position for Ketu.
- **Planetary Motion & States**: Retrograde (*Vakri*), Combustion (*Asta*), and 9 levels of planetary dignity (*Param Uchha*, *Uchha*, *Moolatrikona*, *Swakshetra*, *Mitra*, *Sama*, *Shatru*, *Neecha*, *Param Neecha*).
- **Ascendant (Lagna) & Bhavas**: Local Sidereal Time (RAMC) derived Lagna cusp on the eastern horizon and Parashari Whole Sign Houses.

### 5. 🕉️ Vedic Panchanga & Yogas/Doshas
- **Five Limbs of Time**: Vara, Tithi (% completed), Nakshatra (Pada, Deity, Symbol), Yoga, Karana (Vishti/Bhadra detection).
- **Doshas Analysis**: Manglik Dosha with classical cancellations (*Nivritti*), Shani Sade Sati & Dhaiya, Kaal Sarp Dosha (all 12 classical types).
- **Auspicious Raja Yogas**: Gaja Kesari, Budhaditya, Chandra-Mangala, Lakshmi Yoga, and the five Pancha Mahapurusha Yogas (Ruchaka, Bhadra, Hamsa, Malavya, Sasa).

### 6. 🔢 Vedic & Chaldean Numerology (Sankhya Shastra)
- **Mulank (Psychic Number)**: Innate nature and subconscious drive.
- **Bhagyank (Destiny Number)**: Life purpose and karmic mission.
- **Namank (Name Number)**: Chaldean vibration and compound number (e.g. 23 - Royal Star of the Lion) + Pythagorean expression.
- **Tripartite Harmony**: Planetary compatibility matrix between Mulank, Bhagyank, and Namank with tuning suggestions.

---

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate
```

Dependencies include `streamlit`, `skyfield`, `timezonefinder`, `geopy`, `fastapi`, `uvicorn`, `rich`, `requests`, and `jinja2`.

### 2. Launch the Streamlit Web Application (Hosted on Port 8501)
Launch the primary interactive Streamlit dashboard:

```bash
# Direct Streamlit launch
streamlit run ui/streamlit_app.py

# Or via unified main.py (default mode)
python main.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

### 3. Launch the FastAPI Web Server (Port 8000)
If you prefer the FastAPI REST API and server-rendered dashboard:

```bash
python main.py --web
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### 4. Launch Interactive Terminal CLI
Run the rich terminal interface:

```bash
python main.py --cli
```

### 5. Direct Batch / Scripting Mode
```bash
python main.py \
  --name "Arjun Sharma" \
  --dob "1995-10-24" \
  --tob "06:30" \
  --pob "New Delhi, India" \
  --export "report.json"
```

---

## 📁 Project Architecture

```
Astro/
├── core/
│   ├── constants.py      # Rashis, Nakshatras, Planets, Yogas, Chaldean/Pythagorean maps
│   ├── ephemeris.py      # NASA JPL DE421 ephemeris & Chitrapaksha Lahiri ayanamsha
│   ├── ascendant.py      # Sidereal Lagna, MC, Whole Sign & Sripati Bhavas
│   ├── panchang.py       # Tithi, Vara, Nakshatra, Yoga, Karana
│   ├── dashas.py         # Vimshottari Mahadashas & Antardashas (120-year cycle)
│   ├── yogas.py          # Manglik, Sade Sati, Kaal Sarp, and Raja Yogas
│   ├── timelines.py      # Event Timelines (Career, Marriage, Wealth, Health & Roadmap)
│   ├── internet_data.py  # OSM Geocoding, Open-Meteo Elevation & Solar Ephemeris
│   ├── numerology.py     # Mulank, Bhagyank, Namank, Soul Urge, Harmony
│   ├── geocoder.py       # Offline/Online city lookup & timezone resolution
│   ├── visualizer.py     # North Indian Diamond & South Indian Kundali SVG/ASCII
│   └── analyzer.py       # Master orchestrator combining all modules
├── ui/
│   ├── streamlit_app.py  # Modern Streamlit Web Application
│   ├── cli.py            # Rich terminal UI
│   └── web/
│       ├── app.py        # FastAPI web server and REST API
│       └── templates/
│           └── index.html # Responsive dashboard with SVG Kundali & Timelines tab
├── tests/
│   └── test_analyzer.py  # Comprehensive unit test suite
├── de421.bsp             # NASA JPL Planetary Kernel (1899-2053)
├── main.py               # Unified application entry point (Streamlit / Web / CLI)
└── README.md             # Documentation
```

---

## 🧪 Running Unit Tests

```bash
./.venv/bin/python -m unittest tests/test_analyzer.py
```
All unit tests verify astronomical precision, Lahiri ayanamsha, event timelines logic, internet data enrichment, and numerology calculations.
