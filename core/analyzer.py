"""
core/analyzer.py - Master Vedic Astrology and Numerology Analyzer
Integrates ephemeris, ascendant, panchang, dashas, yogas, numerology,
visual charts, and comprehensive personalized Vedic life guidance.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional

from core.ephemeris import EphemerisEngine
from core.ascendant import AscendantEngine
from core.panchang import PanchangEngine
from core.dashas import VimshottariDashaEngine
from core.yogas import YogaEngine
from core.numerology import NumerologyEngine
from core.geocoder import LocationResolver
from core.visualizer import ChartVisualizer
from core.timelines import TimelineEngine
from core.internet_data import InternetDataService

class AstroAnalyzer:
    def __init__(self):
        self.ephem_engine = EphemerisEngine()
        self.ascendant_engine = AscendantEngine(self.ephem_engine)
        self.panchang_engine = PanchangEngine()
        self.dasha_engine = VimshottariDashaEngine()
        self.yoga_engine = YogaEngine(self.ephem_engine)
        self.numerology_engine = NumerologyEngine()
        self.geocoder = LocationResolver()
        self.timeline_engine = TimelineEngine()
        self.internet_service = InternetDataService()

    def parse_datetime(self, dob_str: str, tob_str: str) -> datetime:
        """Parses various date and time formats flexibly."""
        dob_clean = dob_str.strip()
        tob_clean = tob_str.strip()

        # Date parsing
        parsed_date = None
        for fmt in (
            "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d",
            "%B %d, %Y", "%d %b %Y", "%d %B %Y", "%B %d %Y",
            "%m/%d/%Y", "%m-%d-%Y", "%d.%m.%Y", "%Y.%m.%d", "%b %d, %Y"
        ):
            try:
                parsed_date = datetime.strptime(dob_clean, fmt).date()
                break
            except ValueError:
                continue

        if not parsed_date:
            raise ValueError(f"Unable to parse Date of Birth: '{dob_str}'. Expected formats: YYYY-MM-DD or DD-MM-YYYY.")

        # Time parsing
        parsed_time = None
        for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p", "%I %p", "%I:%M%p", "%I:%M:%S%p"):
            try:
                parsed_time = datetime.strptime(tob_clean, fmt).time()
                break
            except ValueError:
                continue

        if not parsed_time:
            # Default to 12:00 PM if time omitted
            parsed_time = datetime.strptime("12:00", "%H:%M").time()

        return datetime.combine(parsed_date, parsed_time)

    def analyze(
        self, full_name: str, dob_str: str, tob_str: str, pob_str: str,
        current_dt: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Executes full Vedic astrological and numerological computation.
        """
        if current_dt is None:
            current_dt = datetime.now()

        local_dt = self.parse_datetime(dob_str, tob_str)
        birth_date = local_dt.date()

        # 1. Geolocation & Timezone Resolution
        location = self.geocoder.resolve_location(pob_str)
        utc_dt, utc_offset_hours = self.geocoder.convert_local_to_utc(local_dt, location["timezone"])

        # 2. High Precision Ephemeris & Planetary Positions
        ephem_data = self.ephem_engine.calculate_planetary_positions(utc_dt)
        grahas = ephem_data["grahas"]
        ayanamsha = ephem_data["ayanamsha"]

        # 3. Ascendant (Lagna) and Houses
        lagna_data = self.ascendant_engine.calculate_ascendant_and_houses(
            utc_dt, location["latitude"], location["longitude"]
        )
        grahas = self.ascendant_engine.assign_houses_to_grahas(grahas, lagna_data["lagna_sign"])

        # 4. Vedic Panchang
        sun_lon = grahas["Sun"]["sidereal_lon"]
        moon_lon = grahas["Moon"]["sidereal_lon"]
        panchang = self.panchang_engine.calculate_panchang(local_dt, sun_lon, moon_lon)

        # 5. Vimshottari Dasha
        dashas = self.dasha_engine.calculate_dashas(local_dt, moon_lon, target_dt=current_dt)

        # 6. Yogas and Doshas (Manglik, Sade Sati, Kaal Sarp, Raja Yogas)
        yogas = self.yoga_engine.analyze_all_yogas_and_doshas(grahas, lagna_data["lagna_sign"], current_dt)

        # 7. Numerology (Mulank, Bhagyank, Namank, Compatibility)
        mulank = self.numerology_engine.calculate_mulank(birth_date)
        bhagyank = self.numerology_engine.calculate_bhagyank(birth_date)
        namank = self.numerology_engine.calculate_namank(full_name)
        num_harmony = self.numerology_engine.evaluate_compatibility(
            mulank["mulank"], bhagyank["bhagyank"], namank["chaldean"]["namank"]
        )

        # 8. Kundali Charts (D1 Rashi and D9 Navamsha)
        d1_houses = ChartVisualizer.get_house_contents(grahas, lagna_data)
        d9_houses = ChartVisualizer.get_navamsha_house_contents(grahas, lagna_data)

        d1_svg = ChartVisualizer.generate_north_indian_svg(d1_houses, "D1 - Lagna Rashi Chart")
        d9_svg = ChartVisualizer.generate_north_indian_svg(d9_houses, "D9 - Navamsha Chart")
        d1_south_svg = ChartVisualizer.generate_south_indian_svg(d1_houses, "D1 - South Indian Kundali")
        d9_south_svg = ChartVisualizer.generate_south_indian_svg(d9_houses, "D9 - Navamsha South Indian")
        ascii_chart = ChartVisualizer.generate_ascii_chart(d1_houses)

        # 9. Predictive Event Timelines (Career, Marriage, Wealth, Health & Master Roadmap)
        timelines = self.timeline_engine.analyze_event_timelines(
            birth_dt=local_dt,
            lagna_data=lagna_data,
            grahas=grahas,
            dashas=dashas,
            yogas=yogas,
            target_dt=current_dt
        )

        # 10. Live Internet Ephemeris & Real-Time Planetary Transits (Gochara)
        solar_ephem = self.internet_service.fetch_solar_ephemeris(
            location["latitude"], location["longitude"], birth_date
        )
        live_transits = self.internet_service.calculate_current_transits(
            self.ephem_engine, target_dt=current_dt
        )
        internet_status = self.internet_service.get_service_status()

        # 11. Synthesized Personalized Life Guidance & Interpretations
        guidance = self._synthesize_life_guidance(
            full_name=full_name,
            lagna_data=lagna_data,
            grahas=grahas,
            panchang=panchang,
            yogas=yogas,
            dashas=dashas,
            mulank=mulank,
            bhagyank=bhagyank,
            namank=namank,
            num_harmony=num_harmony
        )

        return {
            "meta": {
                "calculation_engine": "Vedic Jyotish & Sankhya Shastra",
                "ephemeris": "NASA JPL DE421",
                "ayanamsha_system": "Chitrapaksha / Lahiri",
                "calculated_at": datetime.now().isoformat(),
            },
            "user_input": {
                "full_name": full_name,
                "date_of_birth": birth_date.strftime("%Y-%m-%d"),
                "time_of_birth": local_dt.strftime("%H:%M:%S"),
                "place_of_birth": pob_str,
            },
            "birth_astronomy": {
                "local_datetime": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "utc_datetime": utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "utc_offset": f"{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours:.1f} hours",
                "timezone": location["timezone"],
                "resolved_location": location["resolved_name"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "elevation_m": location.get("elevation_m", 0.0),
                "is_online_precise": location.get("is_online_precise", False),
                "julian_day": ephem_data["julian_day"],
                "ayanamsha": ephem_data["ayanamsha_formatted"],
            },
            "lagna": lagna_data,
            "panchang": panchang,
            "solar_ephemeris": solar_ephem,
            "grahas": grahas,
            "dashas": dashas,
            "yogas_and_doshas": yogas,
            "timelines": timelines,
            "live_transits": live_transits,
            "internet_precision": internet_status,
            "numerology": {
                "mulank": mulank,
                "bhagyank": bhagyank,
                "namank": namank,
                "harmony": num_harmony,
            },
            "charts": {
                "d1_houses": d1_houses,
                "d9_houses": d9_houses,
                "d1_svg": d1_svg,
                "d9_svg": d9_svg,
                "d1_south_svg": d1_south_svg,
                "d9_south_svg": d9_south_svg,
                "ascii_chart": ascii_chart,
            },
            "guidance": guidance
        }

    def _synthesize_life_guidance(
        self, full_name: str, lagna_data: Dict[str, Any], grahas: Dict[str, Any],
        panchang: Dict[str, Any], yogas: Dict[str, Any], dashas: Dict[str, Any],
        mulank: Dict[str, Any], bhagyank: Dict[str, Any], namank: Dict[str, Any],
        num_harmony: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes classical Vedic and Numerological insight into practical, actionable guidance.
        """
        lagna_sign = lagna_data["lagna_sign"]
        lagna_lord = lagna_data["lagna_ruler"]
        moon_sign = grahas["Moon"]["sign"]
        moon_nakshatra = grahas["Moon"]["nakshatra"]
        sun_sign = grahas["Sun"]["sign"]

        # Core personality synthesis
        temperament = (
            f"{full_name} is born with {lagna_sign} Ascendant (Lagna) ruled by {lagna_lord}, "
            f"giving a natural foundation of vitality and perspective. The Moon resides in {moon_sign} "
            f"under {moon_nakshatra} Nakshatra, shaping an intuitive, responsive emotional core. "
            f"Combined with Psychic Number {mulank['mulank']} ({mulank['ruler']}) and Destiny Number {bhagyank['bhagyank']} "
            f"({bhagyank['ruler']}), there is a profound interplay between personal will and karmic opportunities."
        )

        # Career guidance
        career_focus = (
            f"With Ascendant in {lagna_sign} and 10th house indicating public authority, "
            f"careers aligned with {bhagyank['ruler']} and {lagna_lord} bring the highest fulfillment. "
            f"Favorable sectors include: {', '.join(mulank['favorable_careers'][:4])}. "
            f"During the current {dashas['active_dasha']['formatted']} dasha, career initiatives receive heightened momentum."
        )

        # Relationships
        rel_text = (
            f"In relationships, {grahas['Venus']['sign']} Venus and the 7th house dynamic define romantic expectations. "
            f"{yogas['manglik_dosha']['description']} "
            f"Seeking partners with harmonious psychic numbers ({', '.join(str(n) for n in mulank['lucky_numbers'])}) "
            f"fosters enduring domestic peace and mutual prosperity."
        )

        # Remedies & Auspicious Recommendations
        from core.constants import PLANETS
        lord_gem = PLANETS.get(lagna_lord, {}).get("gemstone", "Pearl")
        lord_mantra = PLANETS.get(lagna_lord, {}).get("mantra", "Om Namah Shivaya")

        remedies = [
            f"Ruling Deities: Worship of {mulank['deity']} enhances mental serenity and cosmic protection.",
            f"Auspicious Days: Schedule major decisions, contracts, and new beginnings on {', '.join(mulank['lucky_days'])}.",
            f"Harmonious Colors: Integrate {', '.join(mulank['lucky_colors'][:3])} in your personal environment and attire.",
            f"Recommended Gemstone: {mulank['gemstone']} or {lord_gem} (consult a qualified pandit before wearing with gold/silver).",
            f"Vedic Mantra: Chant '{lord_mantra}' 108 times daily for spiritual grounding and success.",
            f"Name Alignment: {num_harmony['recommendation']}"
        ]

        if yogas["sade_sati"]["is_sade_sati"]:
            remedies.append(
                "Shani Sade Sati Remedy: Recite the Hanuman Chalisa on Saturdays, light a mustard oil lamp under a Peepal tree, and donate black sesame or blankets to the needy."
            )

        return {
            "temperament_summary": temperament,
            "career_and_wealth": career_focus,
            "relationships_and_marriage": rel_text,
            "remedies": remedies,
            "lucky_colors": mulank["lucky_colors"],
            "lucky_days": mulank["lucky_days"],
            "lucky_numbers": mulank["lucky_numbers"],
            "recommended_gemstone": mulank["gemstone"],
        }
