"""
core/panchang.py - Vedic Panchang (Five Limbs of Time) Engine
Calculates Tithi, Vara, Nakshatra, Yoga, and Karana.
"""

from datetime import datetime
from typing import Dict, Any

from core.constants import (
    PANCHANG_YOGAS, KARANAS_MOVABLE, KARANAS_FIXED,
    TITHI_NAMES, VARAS, NAKSHATRAS
)

class PanchangEngine:
    @staticmethod
    def calculate_panchang(
        dt_local: datetime, sun_sidereal_lon: float, moon_sidereal_lon: float
    ) -> Dict[str, Any]:
        """
        Calculates all 5 limbs of the Panchang at the given moment.
        """
        # 1. Vara (Day of the Week)
        weekday = dt_local.weekday()  # 0 is Monday, 6 is Sunday
        vara_info = VARAS[weekday]

        # 2. Tithi (Moon longitude - Sun longitude)
        diff = (moon_sidereal_lon - sun_sidereal_lon) % 360.0
        tithi_index = int(diff // 12.0) + 1  # 1 to 30
        
        if tithi_index <= 15:
            paksha = "Shukla Paksha (Bright Fortnight - Waxing)"
            tithi_in_paksha = tithi_index
        else:
            paksha = "Krishna Paksha (Dark Fortnight - Waning)"
            tithi_in_paksha = tithi_index - 15

        if tithi_index == 15:
            tithi_name = "Purnima (Full Moon)"
        elif tithi_index == 30:
            tithi_name = "Amavasya (New Moon)"
        else:
            tithi_name = TITHI_NAMES[tithi_in_paksha - 1]

        tithi_completion_percent = ((diff % 12.0) / 12.0) * 100.0

        # 3. Nakshatra (Moon's Nakshatra)
        nak_span = 40.0 / 3.0
        nak_idx = int(moon_sidereal_lon // nak_span)
        nak_offset = moon_sidereal_lon % nak_span
        pada = int(nak_offset // (nak_span / 4.0)) + 1
        nak_info = NAKSHATRAS[nak_idx]

        # 4. Yoga (Sun longitude + Moon longitude)
        sum_deg = (sun_sidereal_lon + moon_sidereal_lon) % 360.0
        yoga_idx = int(sum_deg // nak_span)
        yoga_name = PANCHANG_YOGAS[yoga_idx % 27]

        # Benefic / Inauspicious classification of yogas
        inauspicious_yogas = {"Vishkambha", "Atiganda", "Shoola", "Ganda", "Vyaghata", "Vajra", "Vyatipata", "Parigha", "Vaidhriti"}
        yoga_nature = "Challenging / Malefic (Ashubha)" if yoga_name in inauspicious_yogas else "Auspicious / Benefic (Shubha)"

        # 5. Karana (Half Tithi, 6 degrees)
        karana_idx = int(diff // 6.0) + 1  # 1 to 60

        if karana_idx == 1:
            karana_name = KARANAS_FIXED[1]
        elif karana_idx in KARANAS_FIXED:
            karana_name = KARANAS_FIXED[karana_idx]
        else:
            # Repeating 7 movable karanas from index 2 to 57
            karana_name = KARANAS_MOVABLE[(karana_idx - 2) % 7]

        is_vishti = "Vishti" in karana_name or "Bhadra" in karana_name

        return {
            "vara": {
                "name": vara_info["name"],
                "sanskrit": vara_info["sanskrit"],
                "lord": vara_info["ruler"],
            },
            "tithi": {
                "number": tithi_index,
                "name": tithi_name,
                "paksha": paksha,
                "completion_percent": round(tithi_completion_percent, 1),
            },
            "nakshatra": {
                "name": nak_info["name"],
                "sanskrit": nak_info["sanskrit"],
                "lord": nak_info["lord"],
                "pada": pada,
                "deity": nak_info["deity"],
                "symbol": nak_info["symbol"],
            },
            "yoga": {
                "name": yoga_name,
                "nature": yoga_nature,
            },
            "karana": {
                "number": karana_idx,
                "name": karana_name,
                "is_bhadra": is_vishti,
            }
        }
