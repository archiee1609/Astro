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

if __name__ == "__main__":
    unittest.main()
