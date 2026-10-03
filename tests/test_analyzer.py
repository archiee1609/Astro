"""
tests/test_analyzer.py - Comprehensive Unit Test Suite
"""

import unittest
from datetime import datetime, date
from core.analyzer import AstroAnalyzer
from core.numerology import NumerologyEngine
from core.ephemeris import EphemerisEngine
from core.geocoder import LocationResolver
from core.yogas import YogaEngine
from core.dashas import VimshottariDashaEngine

class TestVedicAstroEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = AstroAnalyzer()
        cls.geocoder = LocationResolver()

    def test_geocoder_offline_and_tz(self):
        # Offline city test
        res_delhi = self.geocoder.resolve_location("New Delhi, India")
        self.assertEqual(res_delhi["timezone"], "Asia/Kolkata")
        self.assertAlmostEqual(res_delhi["latitude"], 28.6139, places=2)

        res_london = self.geocoder.resolve_location("London, UK")
        self.assertEqual(res_london["timezone"], "Europe/London")

        # UTC conversion with offset check
        dt_local = datetime(2024, 1, 15, 12, 0)
        utc_dt, offset = self.geocoder.convert_local_to_utc(dt_local, "Asia/Kolkata")
        self.assertEqual(offset, 5.5)
        self.assertEqual(utc_dt.hour, 6)
        self.assertEqual(utc_dt.minute, 30)

    def test_numerology_all_rules(self):
        # 1. Mulank test
        m1 = NumerologyEngine.calculate_mulank(date(1990, 1, 1))
        self.assertEqual(m1["mulank"], 1)
        self.assertEqual(m1["ruler"], "Sun (Surya)")

        m9 = NumerologyEngine.calculate_mulank(date(1990, 1, 27))
        self.assertEqual(m9["mulank"], 9)  # 2 + 7 = 9

        m8 = NumerologyEngine.calculate_mulank(date(1990, 1, 26))
        self.assertEqual(m8["mulank"], 8)  # 2 + 6 = 8

        # 2. Bhagyank test
        # 1990-01-27: 9 + 1 + 19 = 29 -> 11 -> 2
        b2 = NumerologyEngine.calculate_bhagyank(date(1990, 1, 27))
        self.assertEqual(b2["bhagyank"], 2)

        # 3. Chaldean Name test
        # CHEIRO: C=3, H=5, E=5, I=1, R=2, O=7 -> 23 -> 5
        nam_cheiro = NumerologyEngine.calculate_namank("CHEIRO")
        self.assertEqual(nam_cheiro["chaldean"]["compound_number"], 23)
        self.assertEqual(nam_cheiro["chaldean"]["namank"], 5)

    def test_ephemeris_lahiri_ayanamsha(self):
        # Standard benchmark: Jan 1, 2000 J2000.0 (JD 2451545.0)
        ayan_2000 = self.analyzer.ephem_engine.calculate_lahiri_ayanamsha(2451545.0)
        self.assertAlmostEqual(ayan_2000, 23.85709, places=2)

        # Jan 1, 2024 (JD ~ 2460310.5)
        ayan_2024 = self.analyzer.ephem_engine.calculate_lahiri_ayanamsha(2460310.5)
        self.assertGreater(ayan_2024, 24.18)
        self.assertLess(ayan_2024, 24.22)

    def test_dasha_calculation(self):
        # Test Moon at 0 deg Aries (Ashwini nakshatra, Lord = Ketu, total years = 7)
        # Moon at 0 deg means 100% of Ketu dasha remaining at birth (7 years)
        b_dt = datetime(2000, 1, 1, 12, 0)
        dasha_res = VimshottariDashaEngine.calculate_dashas(b_dt, moon_sidereal_lon=0.0)
        self.assertEqual(dasha_res["birth_nakshatra_lord"], "Ketu")
        self.assertEqual(dasha_res["balance_at_birth"]["years"], 7)

        # Moon at 6.666666 deg (50% through Ashwini) -> 3.5 years of Ketu remaining
        dasha_res_half = VimshottariDashaEngine.calculate_dashas(b_dt, moon_sidereal_lon=6.66666667)
        self.assertEqual(dasha_res_half["balance_at_birth"]["years"], 3)
        self.assertEqual(dasha_res_half["balance_at_birth"]["months"], 6)

    def test_full_analysis_pipeline(self):
        # Comprehensive end-to-end check
        result = self.analyzer.analyze(
            full_name="Deepak Chopra",
            dob_str="1946-10-22",
            tob_str="15:45",
            pob_str="New Delhi, India"
        )
        self.assertIn("meta", result)
        self.assertIn("birth_astronomy", result)
        self.assertIn("lagna", result)
        self.assertIn("grahas", result)
        self.assertIn("panchang", result)
        self.assertIn("dashas", result)
        self.assertIn("yogas_and_doshas", result)
        self.assertIn("numerology", result)
        self.assertIn("charts", result)
        self.assertIn("guidance", result)

        # Check charts output
        self.assertTrue("<svg" in result["charts"]["d1_svg"])
        self.assertTrue("<svg" in result["charts"]["d9_svg"])
        self.assertTrue("VEDIC KUNDLI" in result["charts"]["ascii_chart"])

        # Check timelines output
        self.assertIn("timelines", result)
        self.assertIn("career", result["timelines"])
        self.assertIn("marriage", result["timelines"])
        self.assertIn("wealth", result["timelines"])
        self.assertIn("health", result["timelines"])
        self.assertIn("master_roadmap", result["timelines"])
        self.assertGreater(len(result["timelines"]["master_roadmap"]), 0)

        # Check internet precision & live transits
        self.assertIn("live_transits", result)
        self.assertIn("transits", result["live_transits"])
        self.assertGreater(len(result["live_transits"]["transits"]), 0)
        self.assertIn("internet_precision", result)
        self.assertIn("elevation_m", result["birth_astronomy"])

    def test_timelines_domain_logic(self):
        result = self.analyzer.analyze(
            full_name="Arjun Sharma",
            dob_str="1995-10-24",
            tob_str="06:30",
            pob_str="New Delhi, India"
        )
        t = result["timelines"]
        self.assertIn("tenth_lord", t["career"])
        self.assertIn("seventh_lord", t["marriage"])
        self.assertIn("dhana_lords", t["wealth"])
        self.assertIn("vulnerabilities", t["health"])
        self.assertIn("active_period_summary", t)

        # Check prime marriage windows structure
        self.assertIsInstance(t["marriage"]["prime_marriage_windows"], list)
        # Check spouse profile
        self.assertIn("core_temperament", t["marriage"]["spouse_profile"])

    def test_internet_services_direct(self):
        from core.internet_data import InternetDataService
        svc = InternetDataService()
        status = svc.get_service_status()
        self.assertIn("ephemeris_kernel", status)

        # Solar ephemeris check
        solar = svc.fetch_solar_ephemeris(28.6139, 77.2090, date(1995, 10, 24))
        self.assertIn("sunrise", solar)
        self.assertIn("sunset", solar)

        # Live transits check
        transits = svc.calculate_current_transits(self.analyzer.ephem_engine)
        self.assertEqual(len(transits["transits"]), 9)

    def test_detailed_timeline_events(self):
        """Validates that detailed timeline of events has milestones, PDs, and 10-year forecasts."""
        result = self.analyzer.analyze(
            full_name="Pooja Verma",
            dob_str="1992-04-18",
            tob_str="14:20",
            pob_str="Mumbai, India"
        )
        tl = result["timelines"]
        
        # 1. Life Milestones
        self.assertIn("life_milestones", tl)
        self.assertIsInstance(tl["life_milestones"], list)
        self.assertGreater(len(tl["life_milestones"]), 0)
        first_m = tl["life_milestones"][0]
        for key in ["title", "category", "period", "start_date", "end_date", "age_window", 
                    "astrological_basis", "prediction_narrative", "actionable_guidance", "vedic_remedy"]:
            self.assertIn(key, first_m, f"Missing key '{key}' in milestone")

        # 2. Pratyantardashas
        self.assertIn("pratyantardashas", tl)
        self.assertIsInstance(tl["pratyantardashas"], list)
        self.assertGreater(len(tl["pratyantardashas"]), 0)
        first_pd = tl["pratyantardashas"][0]
        for key in ["pratyantardasha", "dasha_hierarchy", "start_date", "end_date", "focus_theme", "guidance"]:
            self.assertIn(key, first_pd, f"Missing key '{key}' in pratyantardasha")

        # 3. 10-Year Annual Forecast
        self.assertIn("annual_forecast", tl)
        self.assertIsInstance(tl["annual_forecast"], list)
        self.assertGreaterEqual(len(tl["annual_forecast"]), 10)
        first_af = tl["annual_forecast"][0]
        for key in ["year", "age_at_midyear", "dasha", "primary_theme", "career_outlook", "wealth_outlook", "key_recommendation"]:
            self.assertIn(key, first_af, f"Missing key '{key}' in annual forecast")

    def test_pratyantardasha_engine_divisions(self):
        """Validates that VimshottariDashaEngine computes 9 continuous pratyantardasha sub-periods."""
        start_dt = datetime(2024, 1, 1)
        end_dt = datetime(2026, 1, 1)
        pds = VimshottariDashaEngine.calculate_pratyantardashas("Jupiter", "Saturn", start_dt, end_dt)
        self.assertEqual(len(pds), 9)
        self.assertEqual(pds[0]["planet"], "Saturn")  # 1st PD starts with Antardasha lord
        
        # Continuity check
        for i in range(len(pds) - 1):
            self.assertEqual(pds[i]["end_date"], pds[i + 1]["start_date"], "Pratyantardasha dates must be strictly continuous")

    def test_report_exporter_all_formats(self):
        """Tests that ReportExporter successfully generates JSON, Markdown, and HTML reports."""
        import tempfile
        import os
        from core.report_exporter import ReportExporter

        result = self.analyzer.analyze(
            full_name="Rohan Mehra",
            dob_str="1988-07-12",
            tob_str="09:15",
            pob_str="Bangalore, India"
        )

        # JSON Export
        json_str = ReportExporter.generate_json_report(result)
        self.assertIsInstance(json_str, str)
        self.assertIn("user_input", json_str)
        self.assertIn("Rohan Mehra", json_str)

        # Markdown Export
        md_str = ReportExporter.generate_markdown_report(result)
        self.assertIsInstance(md_str, str)
        self.assertIn("# ॐ VEDIC JYOTISH & SANKHYA SHASTRA COMPREHENSIVE REPORT ॐ", md_str)
        self.assertIn("## 1. Birth & Astronomical Coordinates", md_str)
        self.assertIn("## 6. Vimshottari Dasha Timeline", md_str)
        self.assertIn("## 7. Detailed Timeline of Events & Life Milestones", md_str)
        self.assertIn("## 10. Personalized Vedic Guidance & Auspicious Remedies", md_str)

        # HTML Export (Standalone, Print-to-PDF ready)
        html_str = ReportExporter.generate_html_report(result)
        self.assertIsInstance(html_str, str)
        self.assertIn("<!DOCTYPE html>", html_str)
        self.assertIn("<title>Vedic Jyotish & Numerology Complete Report - Rohan Mehra</title>", html_str)
        self.assertIn("<svg", html_str)
        self.assertIn("@media print", html_str)

        # File export test
        with tempfile.TemporaryDirectory() as tmpdir:
            h_path = os.path.join(tmpdir, "test.html")
            m_path = os.path.join(tmpdir, "test.md")
            j_path = os.path.join(tmpdir, "test.json")

            ReportExporter.export_to_file(result, h_path, "html")
            ReportExporter.export_to_file(result, m_path, "markdown")
            ReportExporter.export_to_file(result, j_path, "json")

            self.assertTrue(os.path.exists(h_path) and os.path.getsize(h_path) > 1000)
            self.assertTrue(os.path.exists(m_path) and os.path.getsize(m_path) > 1000)
            self.assertTrue(os.path.exists(j_path) and os.path.getsize(j_path) > 1000)

    def test_fastapi_report_downloads(self):
        """Tests FastAPI /api/report/download GET and POST endpoints for html, markdown, and json."""
        from fastapi.testclient import TestClient
        from ui.web.app import app

        client = TestClient(app)

        params = {
            "full_name": "Kavita Rao",
            "dob": "1993-11-05",
            "tob": "18:45",
            "pob": "Hyderabad, India"
        }

        # 1. GET HTML
        resp_html = client.get("/api/report/download", params={**params, "format": "html"})
        self.assertEqual(resp_html.status_code, 200)
        self.assertIn("text/html", resp_html.headers.get("content-type", ""))
        self.assertIn("attachment", resp_html.headers.get("content-disposition", ""))
        self.assertIn("<!DOCTYPE html>", resp_html.text)

        # 2. GET Markdown
        resp_md = client.get("/api/report/download", params={**params, "format": "markdown"})
        self.assertEqual(resp_md.status_code, 200)
        self.assertIn("text/markdown", resp_md.headers.get("content-type", ""))
        self.assertIn("attachment", resp_md.headers.get("content-disposition", ""))
        self.assertIn("# ॐ VEDIC JYOTISH", resp_md.text)

        # 3. GET JSON
        resp_json = client.get("/api/report/download", params={**params, "format": "json"})
        self.assertEqual(resp_json.status_code, 200)
        self.assertIn("application/json", resp_json.headers.get("content-type", ""))
        self.assertIn("attachment", resp_json.headers.get("content-disposition", ""))
        data = resp_json.json()
        self.assertEqual(data["user_input"]["full_name"], "Kavita Rao")

        # 4. POST HTML Download
        post_resp = client.post("/api/report/download", json={
            "user_input": {
                "full_name": "Kavita Rao",
                "dob": "1993-11-05",
                "tob": "18:45",
                "pob": "Hyderabad, India"
            },
            "format": "html"
        })
        self.assertEqual(post_resp.status_code, 200)
        self.assertIn("text/html", post_resp.headers.get("content-type", ""))

if __name__ == "__main__":
    unittest.main()
