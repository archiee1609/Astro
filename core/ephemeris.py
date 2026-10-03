"""
core/ephemeris.py - High Precision Vedic Ephemeris Engine
Uses NASA JPL DE421 Ephemeris via Skyfield and Chitrapaksha (Lahiri) Ayanamsha.
"""

import math
import os
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

from skyfield.api import load, wgs84
from skyfield.framelib import ecliptic_frame

from core.constants import (
    SIGNS, NAKSHATRAS, PLANETS, SIGN_NAMES,
    SIGN_RULERS, DASHA_ORDER, DASHA_YEARS
)

class EphemerisEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EphemerisEngine, cls).__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        # Locate DE421 BSP file
        bsp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "de421.bsp")
        if not os.path.exists(bsp_path):
            # Fallback to local working directory
            bsp_path = "de421.bsp"
        
        self.ts = load.timescale()
        self.eph = load(bsp_path)
        self.earth = self.eph['earth']
        
        # Target bodies in JPL DE421
        self.planet_targets = {
            "Sun": self.eph['sun'],
            "Moon": self.eph['moon'],
            "Mars": self.eph['mars'],
            "Mercury": self.eph['mercury'],
            "Jupiter": self.eph['jupiter barycenter'],
            "Venus": self.eph['venus'],
            "Saturn": self.eph['saturn barycenter'],
        }

    def calculate_lahiri_ayanamsha(self, jd_ut1: float) -> float:
        """
        Calculates Chitrapaksha (Lahiri) Ayanamsha for a given Julian Day UT1.
        Matches Indian Astronomical Ephemeris and NC Lahiri recommendations.
        Epoch J2000.0 (JD 2451545.0) = 23° 51' 25.532" = 23.857092°
        Precession rate = 50.28796 arcsec / Julian year = 1.3968878° / century
        """
        T = (jd_ut1 - 2451545.0) / 36525.0
        ayan = 23.85709167 + 1.3968878 * T + 0.000308 * (T ** 2)
        return ayan % 360.0

    def calculate_mean_lunar_node(self, jd_ut1: float) -> float:
        """
        Calculates Mean Ascending Node of the Moon (Rahu) in tropical degrees.
        Based on IAU / ELP-2000 analytical precision formulas.
        """
        T = (jd_ut1 - 2451545.0) / 36525.0
        # Omega (degrees)
        omega = 125.04452 - 1934.136261 * T + 0.0020708 * (T ** 2) + (T ** 3) / 450000.0
        return omega % 360.0

    def calculate_planetary_positions(self, dt_utc: datetime) -> Dict[str, Any]:
        """
        Calculates sidereal planetary positions, velocities (retrograde),
        combustion, nakshatra, and pada for all 9 Vedic Grahas.
        """
        # Time object in Skyfield
        t = self.ts.utc(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour, dt_utc.minute, dt_utc.second + dt_utc.microsecond / 1e6)
        
        jd = t.ut1
        ayanamsha = self.calculate_lahiri_ayanamsha(jd)

        # Delta time (+1 hour) to compute apparent velocity / retrograde status
        t_plus = self.ts.utc(dt_utc.year, dt_utc.month, dt_utc.day,
                             dt_utc.hour + 1, dt_utc.minute, dt_utc.second + dt_utc.microsecond / 1e6)
        
        # Calculate Sun position first for combustion checks
        lat_sun, lon_sun, dist_sun = self.earth.at(t).observe(self.planet_targets["Sun"]).apparent().frame_latlon(ecliptic_frame)
        sun_sidereal = (lon_sun.degrees - ayanamsha) % 360.0

        grahas: Dict[str, Any] = {}

        # 1. Classical 7 physical planets
        for name, target in self.planet_targets.items():
            obs = self.earth.at(t).observe(target).apparent()
            lat, lon, dist = obs.frame_latlon(ecliptic_frame)
            tropical_lon = lon.degrees % 360.0
            sidereal_lon = (tropical_lon - ayanamsha) % 360.0

            # Velocity check (+1 hour)
            obs_plus = self.earth.at(t_plus).observe(target).apparent()
            lat_p, lon_p, _ = obs_plus.frame_latlon(ecliptic_frame)
            # Shortest difference
            diff = float((lon_p.degrees - tropical_lon + 180.0) % 360.0 - 180.0)
            hourly_speed = diff
            daily_speed = float(diff * 24.0)

            # Retrograde: true if apparent motion is negative
            is_retrograde = bool(daily_speed < 0.0 and name not in ["Sun", "Moon"])

            # Combustion (Asta): Angular distance from Sun
            angular_distance_from_sun = float(min((sidereal_lon - sun_sidereal) % 360.0, (sun_sidereal - sidereal_lon) % 360.0))
            combustion_limits = {
                "Moon": 12.0, "Mars": 17.0, "Mercury": 14.0 if not is_retrograde else 12.0,
                "Jupiter": 11.0, "Venus": 10.0 if not is_retrograde else 8.0, "Saturn": 15.0
            }
            is_combust = False
            if name in combustion_limits:
                is_combust = bool(angular_distance_from_sun < combustion_limits[name])

            graha_data = self._build_graha_details(
                name=name,
                sidereal_lon=float(sidereal_lon),
                tropical_lon=float(tropical_lon),
                speed=float(daily_speed),
                is_retrograde=bool(is_retrograde),
                is_combust=bool(is_combust),
                distance_au=float(dist.au) if dist is not None else None
            )
            grahas[name] = graha_data

        # 2. Lunar Nodes (Rahu and Ketu)
        rahu_trop = self.calculate_mean_lunar_node(jd)
        rahu_sidereal = (rahu_trop - ayanamsha) % 360.0
        ketu_sidereal = (rahu_sidereal + 180.0) % 360.0
        ketu_trop = (rahu_trop + 180.0) % 360.0

        # Mean nodes constantly retrograde at ~ -0.05295 deg/day
        grahas["Rahu"] = self._build_graha_details(
            name="Rahu",
            sidereal_lon=rahu_sidereal,
            tropical_lon=rahu_trop,
            speed=-0.05295,
            is_retrograde=True,
            is_combust=False,
            distance_au=None
        )

        grahas["Ketu"] = self._build_graha_details(
            name="Ketu",
            sidereal_lon=ketu_sidereal,
            tropical_lon=ketu_trop,
            speed=-0.05295,
            is_retrograde=True,
            is_combust=False,
            distance_au=None
        )

        return {
            "julian_day": jd,
            "ayanamsha": ayanamsha,
            "ayanamsha_formatted": self.format_dms(ayanamsha),
            "grahas": grahas
        }

    def _build_graha_details(
        self, name: str, sidereal_lon: float, tropical_lon: float,
        speed: float, is_retrograde: bool, is_combust: bool, distance_au: Optional[float]
    ) -> Dict[str, Any]:
        """Maps longitudes to Rashi, Nakshatra, Pada, Dignity, Navamsha."""
        sign_idx = int(sidereal_lon // 30)
        sign_deg = sidereal_lon % 30.0
        sign_info = SIGNS[sign_idx]

        # Nakshatra calculation: each nakshatra is 360 / 27 = 13° 20' = 13.333333°
        nak_span = 40.0 / 3.0  # 13.333333 degrees
        nak_idx = int(sidereal_lon // nak_span)
        nak_offset = sidereal_lon % nak_span
        # Pada: each pada is 3° 20' = 3.333333° (4 padas per nakshatra)
        pada = int(nak_offset // (nak_span / 4.0)) + 1
        nak_info = NAKSHATRAS[nak_idx]

        # Navamsha calculation: 108 parts of 3°20'
        navamsha_idx = int(sidereal_lon // (40.0 / 12.0)) # 3.333333° = 200 arcminutes
        navamsha_sign_idx = navamsha_idx % 12
        navamsha_sign_info = SIGNS[navamsha_sign_idx]

        # Dignity (Avastha / Dignity status)
        dignity = self.evaluate_dignity(name, sign_info["name"], sign_deg)

        return {
            "name": name,
            "sanskrit": PLANETS[name]["sanskrit"],
            "sidereal_lon": sidereal_lon,
            "tropical_lon": tropical_lon,
            "sign": sign_info["name"],
            "sign_sanskrit": sign_info["sanskrit"],
            "sign_ruler": sign_info["ruler"],
            "sign_deg": sign_deg,
            "deg_formatted": self.format_dms(sign_deg),
            "nakshatra": nak_info["name"],
            "nakshatra_sanskrit": nak_info["sanskrit"],
            "nakshatra_lord": nak_info["lord"],
            "nakshatra_pada": pada,
            "nakshatra_deity": nak_info["deity"],
            "nakshatra_symbol": nak_info["symbol"],
            "navamsha_sign": navamsha_sign_info["name"],
            "navamsha_sanskrit": navamsha_sign_info["sanskrit"],
            "navamsha_ruler": navamsha_sign_info["ruler"],
            "speed": speed,
            "is_retrograde": is_retrograde,
            "is_combust": is_combust,
            "dignity": dignity,
            "distance_au": distance_au
        }

    def evaluate_dignity(self, planet: str, sign_name: str, deg: float) -> str:
        """
        Determines the planetary dignity (Exaltation, Debilitation,
        Moolatrikona, Swakshetra / Own Sign, Friend, Neutral, Enemy).
        """
        info = PLANETS.get(planet)
        if not info:
            return "Neutral"

        # Exaltation check
        ex = info.get("exalted")
        if ex and ex["sign"] == sign_name:
            if abs(deg - ex["deep_deg"]) <= 3.0:
                return "Deeply Exalted (Param Uchha)"
            return "Exalted (Uchha)"

        # Debilitation check
        deb = info.get("debilitated")
        if deb and deb["sign"] == sign_name:
            if abs(deg - deb["deep_deg"]) <= 3.0:
                return "Deeply Debilitated (Param Neecha)"
            return "Debilitated (Neecha)"

        # Moolatrikona check
        mt = info.get("moolatrikona")
        if mt and mt["sign"] == sign_name:
            if mt["start"] <= deg <= mt["end"]:
                return "Moolatrikona"

        # Own sign (Swakshetra)
        if sign_name in info.get("own_signs", []):
            return "Own Sign (Swakshetra)"

        # Relationship with Sign Ruler
        sign_idx = SIGN_NAMES.index(sign_name)
        sign_ruler = SIGN_RULERS[sign_idx]

        if sign_ruler == planet:
            return "Own Sign (Swakshetra)"

        if sign_ruler in info.get("friends", []):
            return "Friendly Sign (Mitra Rashi)"
        elif sign_ruler in info.get("enemies", []):
            return "Enemy Sign (Shatru Rashi)"
        else:
            return "Neutral Sign (Sama Rashi)"

    @staticmethod
    def format_dms(degrees: float) -> str:
        """Formats degrees to DD° MM' SS\"."""
        d = int(degrees)
        m_float = (degrees - d) * 60.0
        m = int(m_float)
        s = (m_float - m) * 60.0
        return f"{d:02d}° {m:02d}' {s:04.1f}\""
