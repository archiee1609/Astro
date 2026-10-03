"""
core/ascendant.py - Ascendant (Lagna) and Vedic Bhava (House) System
Calculates exact Local Sidereal Time, Lagna, MC, and 12 Bhavas.
"""

import math
from datetime import datetime
from typing import Dict, Any, List

from skyfield.api import load
from core.constants import SIGNS, SIGN_NAMES, NAKSHATRAS
from core.ephemeris import EphemerisEngine

class AscendantEngine:
    def __init__(self, ephem_engine: EphemerisEngine):
        self.ephem = ephem_engine

    def calculate_ascendant_and_houses(
        self, dt_utc: datetime, latitude: float, longitude: float
    ) -> Dict[str, Any]:
        """
        Calculates:
        1. Local Sidereal Time (RAMC)
        2. Obliquity of Ecliptic
        3. Tropical Ascendant & Midheaven (MC)
        4. Sidereal Lagna (Ascendant) using Lahiri Ayanamsha
        5. 12 Bhavas (Whole Sign and Sripati / Bhava Chalita)
        """
        t = self.ephem.ts.utc(
            dt_utc.year, dt_utc.month, dt_utc.day,
            dt_utc.hour, dt_utc.minute, dt_utc.second + dt_utc.microsecond / 1e6
        )
        jd = t.ut1
        ayanamsha = self.ephem.calculate_lahiri_ayanamsha(jd)

        # Greenwich Apparent Sidereal Time in degrees
        gast_hours = t.gast
        gast_deg = (gast_hours * 15.0) % 360.0

        # Local Apparent Sidereal Time (RAMC)
        last_deg = (gast_deg + longitude) % 360.0
        theta_rad = math.radians(last_deg)

        # True Obliquity of Ecliptic (IAU polynomial)
        T = (jd - 2451545.0) / 36525.0
        eps = 23.4392911 - (46.8150 * T + 0.00059 * (T ** 2) - 0.001813 * (T ** 3)) / 3600.0
        eps_rad = math.radians(eps)
        lat_rad = math.radians(latitude)

        # Ascendant on Eastern Horizon:
        # tan(L) = -cos(theta) / (sin(theta)*cos(eps) + tan(phi)*sin(eps))
        y = -math.cos(theta_rad)
        x = math.sin(theta_rad) * math.cos(eps_rad) + math.tan(lat_rad) * math.sin(eps_rad)
        asc_tropical = (math.degrees(math.atan2(y, x)) + 360.0) % 360.0

        # Verify rising condition (Hour Angle H must correspond to eastern horizon)
        L_rad = math.radians(asc_tropical)
        ra_rad = math.atan2(math.sin(L_rad) * math.cos(eps_rad), math.cos(L_rad))
        H_rad = (theta_rad - ra_rad + 2 * math.pi) % (2 * math.pi)
        
        # In the eastern hemisphere, sin(H) < 0 (or H between pi and 2*pi)
        if math.sin(H_rad) > 0.0001:
            asc_tropical = (asc_tropical + 180.0) % 360.0

        # Sidereal Lagna
        asc_sidereal = (asc_tropical - ayanamsha) % 360.0
        lagna_sign_idx = int(asc_sidereal // 30)
        lagna_sign_deg = asc_sidereal % 30.0

        # Midheaven (MC): Point on ecliptic at meridian (H = 0)
        # tan(MC) = tan(theta) / cos(eps)
        mc_tropical = (math.degrees(math.atan2(math.sin(theta_rad), math.cos(theta_rad) * math.cos(eps_rad))) + 360.0) % 360.0
        mc_sidereal = (mc_tropical - ayanamsha) % 360.0

        # Nakshatra for Lagna
        nak_span = 40.0 / 3.0
        nak_idx = int(asc_sidereal // nak_span)
        nak_offset = asc_sidereal % nak_span
        pada = int(nak_offset // (nak_span / 4.0)) + 1
        nak_info = NAKSHATRAS[nak_idx]

        # Navamsha for Lagna
        nav_idx = int(asc_sidereal // (40.0 / 12.0))
        nav_sign_idx = nav_idx % 12

        # 12 Bhavas (Whole Sign System: standard in Vedic Jyotish)
        # 1st Bhava is the entire sign containing Lagna
        whole_sign_houses: List[Dict[str, Any]] = []
        for h in range(1, 13):
            sign_i = (lagna_sign_idx + h - 1) % 12
            whole_sign_houses.append({
                "house": h,
                "sign": SIGNS[sign_i]["name"],
                "sign_sanskrit": SIGNS[sign_i]["sanskrit"],
                "ruler": SIGNS[sign_i]["ruler"],
                "start_deg": sign_i * 30.0,
                "end_deg": (sign_i + 1) * 30.0
            })

        # Sripati / Equal Bhava Chalita Cusps (Cusp center = Lagna degree)
        sripati_houses: List[Dict[str, Any]] = []
        for h in range(1, 13):
            center = (asc_sidereal + (h - 1) * 30.0) % 360.0
            start = (center - 15.0) % 360.0
            end = (center + 15.0) % 360.0
            sripati_houses.append({
                "house": h,
                "cusp_center_deg": center,
                "start_deg": start,
                "end_deg": end,
                "sign": SIGNS[int(center // 30)]["name"]
            })

        return {
            "last_deg": last_deg,
            "ascendant_sidereal": asc_sidereal,
            "ascendant_tropical": asc_tropical,
            "lagna_sign": SIGNS[lagna_sign_idx]["name"],
            "lagna_sign_sanskrit": SIGNS[lagna_sign_idx]["sanskrit"],
            "lagna_ruler": SIGNS[lagna_sign_idx]["ruler"],
            "lagna_deg": lagna_sign_deg,
            "lagna_deg_formatted": self.ephem.format_dms(lagna_sign_deg),
            "lagna_nakshatra": nak_info["name"],
            "lagna_nakshatra_lord": nak_info["lord"],
            "lagna_nakshatra_pada": pada,
            "lagna_navamsha_sign": SIGNS[nav_sign_idx]["name"],
            "lagna_navamsha_ruler": SIGNS[nav_sign_idx]["ruler"],
            "mc_sidereal": mc_sidereal,
            "mc_deg_formatted": self.ephem.format_dms(mc_sidereal % 30.0),
            "whole_sign_houses": whole_sign_houses,
            "sripati_houses": sripati_houses
        }

    def assign_houses_to_grahas(
        self, grahas: Dict[str, Any], lagna_sign_name: str
    ) -> Dict[str, Any]:
        """
        Assigns house number (1 to 12) from Lagna and from Chandra (Moon)
        for every planet.
        """
        lagna_sign_idx = SIGN_NAMES.index(lagna_sign_name)
        moon_sign_idx = SIGN_NAMES.index(grahas["Moon"]["sign"])

        for name, data in grahas.items():
            planet_sign_idx = SIGN_NAMES.index(data["sign"])
            # House from Lagna (1-indexed)
            house_from_lagna = (planet_sign_idx - lagna_sign_idx) % 12 + 1
            # House from Moon (Chandra Lagna)
            house_from_moon = (planet_sign_idx - moon_sign_idx) % 12 + 1

            data["house"] = house_from_lagna
            data["house_from_moon"] = house_from_moon

        return grahas
