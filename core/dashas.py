"""
core/dashas.py - Vimshottari Dasha System Engine
Calculates Mahadashas, Antardashas (Bhukti), birth balance, and current running dasha.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from core.constants import DASHA_ORDER, DASHA_YEARS, NAKSHATRAS

DAYS_PER_YEAR = 365.2425

class VimshottariDashaEngine:
    @staticmethod
    def calculate_dashas(
        birth_dt: datetime, moon_sidereal_lon: float, target_dt: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculates Vimshottari Mahadasha and Antardasha sequence.
        """
        if target_dt is None:
            target_dt = datetime.now()

        # Moon Nakshatra and its lord
        nak_span = 40.0 / 3.0
        nak_idx = int(moon_sidereal_lon // nak_span)
        nak_offset = moon_sidereal_lon % nak_span
        nak_info = NAKSHATRAS[nak_idx]
        birth_lord = nak_info["lord"]

        # Fraction remaining of birth nakshatra
        fraction_traversed = nak_offset / nak_span
        fraction_remaining = 1.0 - fraction_traversed

        # Balance at birth
        total_lord_years = DASHA_YEARS[birth_lord]
        balance_years = fraction_remaining * total_lord_years
        balance_days = balance_years * DAYS_PER_YEAR

        # Sequence starting from birth lord
        start_idx = DASHA_ORDER.index(birth_lord)
        
        # Build 120-year Mahadasha timeline
        mahadashas: List[Dict[str, Any]] = []
        current_start = birth_dt

        # First dasha is partial (balance)
        first_dasha_end = current_start + timedelta(days=balance_days)
        mahadashas.append({
            "planet": birth_lord,
            "total_years": total_lord_years,
            "period_years": round(balance_years, 2),
            "start_date": current_start.strftime("%Y-%m-%d"),
            "end_date": first_dasha_end.strftime("%Y-%m-%d"),
            "is_birth_dasha": True,
            "antardashas": VimshottariDashaEngine._calculate_antardashas(birth_lord, current_start, first_dasha_end, balance_ratio=fraction_remaining)
        })
        current_start = first_dasha_end

        # Subsequent dashas
        for i in range(1, len(DASHA_ORDER) + 3):  # cover standard lifespan
            planet = DASHA_ORDER[(start_idx + i) % len(DASHA_ORDER)]
            years = DASHA_YEARS[planet]
            dasha_end = current_start + timedelta(days=years * DAYS_PER_YEAR)
            
            mahadashas.append({
                "planet": planet,
                "total_years": years,
                "period_years": years,
                "start_date": current_start.strftime("%Y-%m-%d"),
                "end_date": dasha_end.strftime("%Y-%m-%d"),
                "is_birth_dasha": False,
                "antardashas": VimshottariDashaEngine._calculate_antardashas(planet, current_start, dasha_end)
            })
            current_start = dasha_end
            if (current_start - birth_dt).days > 110 * DAYS_PER_YEAR:
                break

        # Identify currently active Mahadasha and Antardasha as of target_dt
        active_md = None
        active_ad = None

        for md in mahadashas:
            md_start = datetime.strptime(md["start_date"], "%Y-%m-%d")
            md_end = datetime.strptime(md["end_date"], "%Y-%m-%d")
            if md_start <= target_dt < md_end:
                active_md = md
                for ad in md["antardashas"]:
                    ad_start = datetime.strptime(ad["start_date"], "%Y-%m-%d")
                    ad_end = datetime.strptime(ad["end_date"], "%Y-%m-%d")
                    if ad_start <= target_dt < ad_end:
                        active_ad = ad
                        break
                break

        # Fallback if beyond range
        if not active_md and mahadashas:
            active_md = mahadashas[-1]
            active_ad = active_md["antardashas"][-1]

        # Balance breakdown in years, months, days
        rounded_bal = round(balance_years, 5)
        bal_y = int(rounded_bal)
        rem_months = round((rounded_bal - bal_y) * 12.0, 4)
        bal_m = int(rem_months)
        rem_days = round((rem_months - bal_m) * 30.4375, 2)
        bal_d = max(0, int(round(rem_days)))

        return {
            "birth_nakshatra_lord": birth_lord,
            "balance_at_birth": {
                "planet": birth_lord,
                "years": bal_y,
                "months": bal_m,
                "days": bal_d,
                "formatted": f"{bal_y} Years, {bal_m} Months, {bal_d} Days of {birth_lord}"
            },
            "active_dasha": {
                "mahadasha": active_md["planet"] if active_md else "N/A",
                "antardasha": active_ad["planet"] if active_ad else "N/A",
                "start_date": active_ad["start_date"] if active_ad else "N/A",
                "end_date": active_ad["end_date"] if active_ad else "N/A",
                "formatted": f"{active_md['planet']} - {active_ad['planet']}" if active_md and active_ad else "N/A"
            },
            "timeline": mahadashas
        }

    @staticmethod
    def _calculate_antardashas(
        md_planet: str, md_start: datetime, md_end: datetime, balance_ratio: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Calculates the 9 Antardashas within a Mahadasha.
        Duration of AD = (MD_years * AD_years / 120) years.
        """
        start_idx = DASHA_ORDER.index(md_planet)
        md_years = DASHA_YEARS[md_planet]

        antardashas = []
        curr_date = md_start

        # For the birth dasha, calculate the normal span of each AD and clip
        if balance_ratio < 1.0:
            # Reconstruct nominal start of this MD
            nominal_start = md_end - timedelta(days=md_years * DAYS_PER_YEAR)
            temp_date = nominal_start
            for j in range(len(DASHA_ORDER)):
                ad_planet = DASHA_ORDER[(start_idx + j) % len(DASHA_ORDER)]
                ad_years = DASHA_YEARS[ad_planet]
                ad_duration_days = (md_years * ad_years / 120.0) * DAYS_PER_YEAR
                ad_nominal_end = temp_date + timedelta(days=ad_duration_days)

                # If this AD ends after actual birth date
                if ad_nominal_end > md_start:
                    actual_start = max(temp_date, md_start)
                    actual_end = min(ad_nominal_end, md_end)
                    if actual_end > actual_start:
                        antardashas.append({
                            "planet": ad_planet,
                            "start_date": actual_start.strftime("%Y-%m-%d"),
                            "end_date": actual_end.strftime("%Y-%m-%d"),
                        })
                temp_date = ad_nominal_end
        else:
            for j in range(len(DASHA_ORDER)):
                ad_planet = DASHA_ORDER[(start_idx + j) % len(DASHA_ORDER)]
                ad_years = DASHA_YEARS[ad_planet]
                ad_duration_days = (md_years * ad_years / 120.0) * DAYS_PER_YEAR
                ad_end = curr_date + timedelta(days=ad_duration_days)

                antardashas.append({
                    "planet": ad_planet,
                    "start_date": curr_date.strftime("%Y-%m-%d"),
                    "end_date": ad_end.strftime("%Y-%m-%d"),
                })
                curr_date = ad_end

        return antardashas
