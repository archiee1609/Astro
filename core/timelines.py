"""
core/timelines.py - Vedic Event Timeline Engine for Career, Marriage, Health, and Wealth
Integrates Vimshottari Dashas, Bhava lordships, planetary karakatwas, yogas,
and Gochara (transits) to compute detailed chronological event timelines.
"""

from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
from core.constants import SIGN_NAMES, SIGN_RULERS, PLANETS

# Astrological lordship map: sign index -> ruling planet
RASHI_LORDS = [
    "Mars",     # 0: Aries
    "Venus",    # 1: Taurus
    "Mercury",  # 2: Gemini
    "Moon",     # 3: Cancer
    "Sun",      # 4: Leo
    "Mercury",  # 5: Virgo
    "Venus",    # 6: Libra
    "Mars",     # 7: Scorpio
    "Jupiter",  # 8: Sagittarius
    "Saturn",   # 9: Capricorn
    "Saturn",   # 10: Aquarius
    "Jupiter"   # 11: Pisces
]

class TimelineEngine:
    def __init__(self):
        pass

    def get_house_lord(self, house_num: int, lagna_sign: str) -> str:
        """Determines the planetary ruler of a specific house (1 to 12) from Lagna."""
        lagna_idx = SIGN_NAMES.index(lagna_sign)
        house_sign_idx = (lagna_idx + house_num - 1) % 12
        return RASHI_LORDS[house_sign_idx]

    def get_house_sign(self, house_num: int, lagna_sign: str) -> str:
        """Returns the sign name for a given house from Lagna."""
        lagna_idx = SIGN_NAMES.index(lagna_sign)
        return SIGN_NAMES[(lagna_idx + house_num - 1) % 12]

    def analyze_event_timelines(
        self,
        birth_dt: datetime,
        lagna_data: Dict[str, Any],
        grahas: Dict[str, Any],
        dashas: Dict[str, Any],
        yogas: Dict[str, Any],
        target_dt: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Computes predictive timelines for:
        1. Career & Karma
        2. Marriage & Relationships
        3. Wealth & Finance
        4. Health & Vitality
        5. Master Unified Chronological Roadmap (Life Journey)
        """
        if target_dt is None:
            target_dt = datetime.now()

        lagna_sign = lagna_data["lagna_sign"]

        # Map all 12 house lords
        house_lords = {h: self.get_house_lord(h, lagna_sign) for h in range(1, 13)}
        house_signs = {h: self.get_house_sign(h, lagna_sign) for h in range(1, 13)}

        # Extract all antardashas chronologically across the lifespan
        all_periods = self._flatten_dashas(dashas["timeline"], birth_dt)

        # 1. Master Unified Life Journey
        master_timeline = self._build_master_timeline(
            all_periods, birth_dt, target_dt, house_lords, grahas, yogas
        )

        # 2. Career & Karma Timeline
        career_timeline = self._build_career_timeline(
            all_periods, birth_dt, target_dt, house_lords, grahas, yogas
        )

        # 3. Marriage & Relationships Timeline
        marriage_timeline = self._build_marriage_timeline(
            all_periods, birth_dt, target_dt, house_lords, house_signs, grahas, yogas
        )

        # 4. Wealth & Finance Timeline
        wealth_timeline = self._build_wealth_timeline(
            all_periods, birth_dt, target_dt, house_lords, grahas, yogas
        )

        # 5. Health & Vitality Timeline
        health_timeline = self._build_health_timeline(
            all_periods, birth_dt, target_dt, house_lords, house_signs, grahas, yogas
        )

        # Current active period deep-dive summary
        active_summary = self._synthesize_current_period(
            master_timeline, career_timeline, marriage_timeline, wealth_timeline, health_timeline
        )

        return {
            "house_lords": house_lords,
            "house_signs": house_signs,
            "active_period_summary": active_summary,
            "master_roadmap": master_timeline,
            "career": career_timeline,
            "marriage": marriage_timeline,
            "wealth": wealth_timeline,
            "health": health_timeline,
        }

    def _flatten_dashas(self, mahadashas: List[Dict[str, Any]], birth_dt: datetime) -> List[Dict[str, Any]]:
        """Flattens Mahadasha and Antardasha hierarchy into chronological periods."""
        flat = []
        for md in mahadashas:
            md_planet = md["planet"]
            for ad in md.get("antardashas", []):
                ad_planet = ad["planet"]
                start_dt = datetime.strptime(ad["start_date"], "%Y-%m-%d")
                end_dt = datetime.strptime(ad["end_date"], "%Y-%m-%d")

                age_start = max(0.0, (start_dt - birth_dt).days / 365.2425)
                age_end = max(0.0, (end_dt - birth_dt).days / 365.2425)

                flat.append({
                    "md": md_planet,
                    "ad": ad_planet,
                    "dasha_name": f"{md_planet} - {ad_planet}",
                    "start_date": ad["start_date"],
                    "end_date": ad["end_date"],
                    "start_dt": start_dt,
                    "end_dt": end_dt,
                    "age_start": round(age_start, 1),
                    "age_end": round(age_end, 1),
                    "duration_months": round((end_dt - start_dt).days / 30.4375, 1)
                })
        return flat

    def _get_planet_dignity_score(self, planet_name: str, grahas: Dict[str, Any]) -> float:
        """Returns numeric score for planetary strength (0.0 to 1.0)."""
        if planet_name not in grahas:
            return 0.5
        g = grahas[planet_name]
        dignity = g.get("dignity", "")
        score = 0.5
        if "Param Uchha" in dignity or "Exalted" in dignity:
            score = 0.95
        elif "Moolatrikona" in dignity:
            score = 0.85
        elif "Own Sign" in dignity or "Swakshetra" in dignity:
            score = 0.80
        elif "Mitra" in dignity or "Great Friend" in dignity or "Friend" in dignity:
            score = 0.65
        elif "Sama" in dignity or "Neutral" in dignity:
            score = 0.50
        elif "Shatru" in dignity or "Enemy" in dignity:
            score = 0.35
        elif "Neecha" in dignity or "Debilitated" in dignity:
            score = 0.20

        if g.get("is_combust", False):
            score -= 0.15
        if g.get("is_retrograde", False) and planet_name in ["Jupiter", "Venus", "Mercury"]:
            score += 0.05  # Retrograde natural benefics gain Cheshta Bala
        return max(0.1, min(1.0, score))

    def _build_master_timeline(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Constructs unified life roadmap with multi-pillar evaluation."""
        master = []
        for p in periods:
            md = p["md"]
            ad = p["ad"]
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])

            # Scoring factors
            md_score = self._get_planet_dignity_score(md, grahas)
            ad_score = self._get_planet_dignity_score(ad, grahas)

            # Career score: 10th, 1st, 9th, 6th, 11th lords, Saturn, Sun
            career_weight = 0
            for lord_house in [10, 1, 9, 11, 6]:
                if house_lords[lord_house] in [md, ad]:
                    career_weight += 20
            if "Saturn" in [md, ad] or "Sun" in [md, ad] or "Mercury" in [md, ad]:
                career_weight += 15
            career_score = int(min(98, max(35, (career_weight * 0.5) + (md_score + ad_score) * 25)))

            # Marriage score: 7th, 2nd, 11th, 4th lords, Venus, Jupiter
            marriage_weight = 0
            for lord_house in [7, 2, 11, 4]:
                if house_lords[lord_house] in [md, ad]:
                    marriage_weight += 22
            if "Venus" in [md, ad] or "Jupiter" in [md, ad]:
                marriage_weight += 18
            marriage_score = int(min(98, max(30, (marriage_weight * 0.5) + (md_score + ad_score) * 25)))

            # Wealth score: 2nd, 11th, 9th, 5th, 1st lords, Jupiter, Venus
            wealth_weight = 0
            for lord_house in [2, 11, 9, 5, 1]:
                if house_lords[lord_house] in [md, ad]:
                    wealth_weight += 20
            if "Jupiter" in [md, ad] or "Venus" in [md, ad] or "Mercury" in [md, ad]:
                wealth_weight += 15
            wealth_score = int(min(98, max(35, (wealth_weight * 0.5) + (md_score + ad_score) * 25)))

            # Health score: 1st lord, Sun, Mars, vs 6th/8th/12th lords
            health_base = (self._get_planet_dignity_score(house_lords[1], grahas) * 40) + ((md_score + ad_score) * 20)
            if house_lords[6] in [md, ad] or house_lords[8] in [md, ad] or house_lords[12] in [md, ad]:
                health_base -= 15
            if "Saturn" in [md, ad] and yogas.get("sade_sati", {}).get("is_sade_sati", False):
                health_base -= 10
            health_score = int(min(96, max(35, health_base)))

            # Overall favorability
            overall_score = int((career_score * 0.3) + (wealth_score * 0.3) + (marriage_score * 0.2) + (health_score * 0.2))

            # Dominant theme
            theme = self._derive_dominant_theme(md, ad, house_lords, career_score, wealth_score, marriage_score, health_score, p["age_start"])

            master.append({
                "period_id": f"{p['start_date']}_{md}_{ad}",
                "dasha": p["dasha_name"],
                "start_date": p["start_date"],
                "end_date": p["end_date"],
                "age_start": p["age_start"],
                "age_end": p["age_end"],
                "age_display": f"Age {p['age_start']} – {p['age_end']}",
                "is_current": is_active,
                "overall_score": overall_score,
                "dominant_theme": theme,
                "scores": {
                    "career": career_score,
                    "marriage": marriage_score,
                    "wealth": wealth_score,
                    "health": health_score
                },
                "status_badge": "Current Running Period 🌟" if is_active else ("Peak Favorable" if overall_score >= 80 else ("Favorable" if overall_score >= 65 else ("Steady" if overall_score >= 50 else "Transformational / Caution"))),
            })
        return master

    def _derive_dominant_theme(
        self, md: str, ad: str, house_lords: Dict[int, str],
        c_score: int, w_score: int, m_score: int, h_score: int, age: float
    ) -> str:
        """Derives primary life theme for a period."""
        if age < 18:
            return "Formative Education, Vitality & Foundation Building"
        
        # Check active lordships
        active_lords = [md, ad]
        if house_lords[10] in active_lords and c_score >= 75:
            return "Major Career Advancement & Professional Recognition"
        elif house_lords[7] in active_lords and 20 <= age <= 45:
            return "Partnership, Marriage & Long-Term Relationship Milestones"
        elif (house_lords[2] in active_lords or house_lords[11] in active_lords) and w_score >= 75:
            return "Substantial Financial Growth & Asset Accumulation"
        elif house_lords[9] in active_lords:
            return "Spiritual Expansion, Higher Wisdom & Fortuitous Travel"
        elif house_lords[4] in active_lords:
            return "Domestic Stability, Property Acquisition & Peace of Mind"
        elif house_lords[8] in active_lords or house_lords[12] in active_lords:
            return "Deep Inner Transformation, Strategic Realignment & Rest"
        elif c_score > w_score and c_score > m_score:
            return "Career Expansion & Skill Mastery"
        else:
            return "Harmonious Life Progress & Balanced Achievements"

    def _build_career_timeline(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep dive into professional career timeline."""
        events = []
        l10 = house_lords[10]
        l1 = house_lords[1]
        l9 = house_lords[9]
        l11 = house_lords[11]
        l6 = house_lords[6]

        for p in periods:
            if p["age_end"] < 18 or p["age_start"] > 75:
                continue

            md = p["md"]
            ad = p["ad"]
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])
            dignity_avg = (self._get_planet_dignity_score(md, grahas) + self._get_planet_dignity_score(ad, grahas)) / 2.0

            # Calculate career score
            score = 50 + int(dignity_avg * 30)
            drivers = []

            if l10 in [md, ad]:
                score += 15
                drivers.append(f"Activation of 10th House Lord ({l10}) ruling professional karma & status")
            if l1 in [md, ad]:
                score += 10
                drivers.append(f"Lagna Lord ({l1}) infusing executive energy and personal leadership")
            if l9 in [md, ad]:
                score += 10
                drivers.append(f"9th Lord ({l9}) of Bhagya bestowing fortune and mentors")
            if l11 in [md, ad]:
                score += 10
                drivers.append(f"11th Lord ({l11}) activating major gains and network recognition")
            if "Saturn" in [md, ad]:
                drivers.append("Saturn (Karma Karaka) structuring long-term professional foundations")
            if "Sun" in [md, ad]:
                drivers.append("Sun (Surya) illuminating authority, government relations, and visibility")
            if "Mercury" in [md, ad]:
                drivers.append("Mercury sharpening commercial insight, communications, and strategy")

            if house_lords[8] in [md, ad] or house_lords[12] in [md, ad]:
                score -= 10
                drivers.append("Influence of 8th/12th houses prompting strategic pivots or overseas roles")

            score = min(98, max(35, score))

            if score >= 82:
                phase_type = "Peak Career Elevation / Major Promotion"
                rating = "Peak Favorable"
                recommendation = "Seize leadership initiatives, request key promotions or launch strategic projects. Visibility is at its highest."
            elif score >= 70:
                phase_type = "Dynamic Professional Growth & Recognition"
                rating = "Highly Favorable"
                recommendation = "Broaden your professional scope, expand professional networks, and invest in high-leverage responsibilities."
            elif score >= 55:
                phase_type = "Steady Progression & Competency Building"
                rating = "Steady Growth"
                recommendation = "Consolidate existing wins, acquire new technical credentials, and refine execution quality."
            else:
                phase_type = "Strategic Pivot & Consolidation Phase"
                rating = "Caution / Transition"
                recommendation = "Avoid impulsive career departures; focus on internal restructuring, skill realignment, and diplomacy."

            events.append({
                "period": f"{p['start_date']} to {p['end_date']}",
                "age_display": f"Age {p['age_start']} – {p['age_end']}",
                "dasha": p["dasha_name"],
                "score": score,
                "phase_type": phase_type,
                "rating": rating,
                "is_current": is_active,
                "drivers": drivers,
                "recommendation": recommendation
            })

        # Sort and pick top landmark windows
        peak_windows = [e for e in events if e["score"] >= 78]

        return {
            "tenth_lord": l10,
            "tenth_sign": grahas.get(l10, {}).get("sign", "Aries"),
            "favorable_sectors": PLANETS.get(l10, {}).get("friends", []) + [l10],
            "peak_milestones_count": len(peak_windows),
            "timeline": events
        }

    def _build_marriage_timeline(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        house_signs: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep dive into relationship and marriage timing."""
        events = []
        l7 = house_lords[7]
        l2 = house_lords[2]
        l11 = house_lords[11]
        l5 = house_lords[5]
        seventh_sign = house_signs[7]

        prime_marriage_windows = []

        for p in periods:
            if p["age_end"] < 19 or p["age_start"] > 65:
                continue

            md = p["md"]
            ad = p["ad"]
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])
            dignity_avg = (self._get_planet_dignity_score(md, grahas) + self._get_planet_dignity_score(ad, grahas)) / 2.0

            score = 45 + int(dignity_avg * 30)
            drivers = []

            if l7 in [md, ad]:
                score += 20
                drivers.append(f"7th Lord ({l7}) strongly active — prime marriage & commitment portal")
            if "Venus" in [md, ad]:
                score += 15
                drivers.append("Venus (Shukra - Kalatra Karaka) awakening romantic affection and marital bliss")
            if "Jupiter" in [md, ad]:
                score += 12
                drivers.append("Jupiter (Guru - sacred sanction) blessing enduring vows and marital harmony")
            if l2 in [md, ad]:
                score += 10
                drivers.append(f"2nd Lord ({l2}) expanding the family circle and domestic ties")
            if l11 in [md, ad]:
                score += 8
                drivers.append(f"11th Lord ({l11}) fulfilling heart's deepest desires and companionship")
            if l5 in [md, ad]:
                score += 8
                drivers.append("5th House of romance and mutual attraction dynamically stimulated")

            # Challenging influences
            if house_lords[6] in [md, ad] or house_lords[8] in [md, ad]:
                score -= 12
                drivers.append("6th/8th lord connection requiring patience, conscious compromise, and mutual empathy")

            score = min(98, max(30, score))

            is_prime_age = (21 <= p["age_start"] <= 38)
            if score >= 75 and is_prime_age:
                prime_marriage_windows.append({
                    "period": f"{p['start_date']} to {p['end_date']}",
                    "age_range": f"Age {p['age_start']} – {p['age_end']}",
                    "dasha": p["dasha_name"],
                    "favorability": "Golden Marriage / Commitment Window 💍",
                    "score": score
                })

            if score >= 78:
                phase_type = "Golden Marriage & Deep Commitment Window 💍"
                rating = "Peak Favorable"
                recommendation = "Highly auspicious window for engagement, wedding ceremonies, or deepening lifelong intimacy."
            elif score >= 65:
                phase_type = "Harmonious Partnership & Emotional Bonding"
                rating = "Highly Favorable"
                recommendation = "Favorable time to nurture mutual understanding, plan shared family goals, and celebrate companionship."
            elif score >= 50:
                phase_type = "Stable Domestic Routine & Compromise"
                rating = "Steady / Neutral"
                recommendation = "Maintain regular communication and ensure equal sharing of domestic responsibilities."
            else:
                phase_type = "Patience Required & Relationship Testing"
                rating = "Caution / Cultivation"
                recommendation = "Avoid escalations over trivial disagreements. Practice active listening; chant Shukra or Brihaspati mantras."

            events.append({
                "period": f"{p['start_date']} to {p['end_date']}",
                "age_display": f"Age {p['age_start']} – {p['age_end']}",
                "dasha": p["dasha_name"],
                "score": score,
                "phase_type": phase_type,
                "rating": rating,
                "is_current": is_active,
                "drivers": drivers,
                "recommendation": recommendation
            })

        # Spouse profile based on 7th sign and 7th lord
        spouse_profile = self._derive_spouse_profile(seventh_sign, l7, grahas)

        return {
            "seventh_lord": l7,
            "seventh_sign": seventh_sign,
            "spouse_profile": spouse_profile,
            "prime_marriage_windows": prime_marriage_windows[:5],
            "timeline": events
        }

    def _derive_spouse_profile(self, seventh_sign: str, seventh_lord: str, grahas: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesizes classical traits of the prospective spouse."""
        sign_archetypes = {
            "Aries": "Dynamic, energetic, courageous, athletic, independent, and direct in communication.",
            "Taurus": "Grounded, graceful, artistic, deeply affectionate, values domestic stability and financial security.",
            "Gemini": "Witty, intellectually curious, versatile, excellent conversationalist, youthful temperament.",
            "Cancer": "Nurturing, emotionally perceptive, deeply devoted to home, intuitive and family-oriented.",
            "Leo": "Magnanimous, charismatic, noble demeanor, dignified, proud, and warm-hearted.",
            "Virgo": "Detail-oriented, analytical, conscientious, practical, elegant, with strong health discipline.",
            "Libra": "Charming, diplomatic, aesthetically refined, balanced, sociable, and values equal partnership.",
            "Scorpio": "Intense, profoundly loyal, perceptive, magnetically attractive, emotionally deep, and private.",
            "Sagittarius": "Philosophical, optimistic, adventurous, honest, enthusiastic, values learning and ethics.",
            "Capricorn": "Responsible, ambitious, mature, highly dependable, disciplined, and enduringly loyal.",
            "Aquarius": "Intellectual, humanitarian, egalitarian, unconventional, forward-thinking, and broad-minded.",
            "Pisces": "Compassionate, spiritually inclined, imaginative, gentle, empathetic, and culturally refined."
        }

        lord_careers = {
            "Sun": "Government, administration, executive leadership, medicine, politics.",
            "Moon": "Healthcare, psychology, hospitality, culinary arts, education, maritime.",
            "Mars": "Engineering, sports, technology, military/defense, law enforcement, entrepreneurship.",
            "Mercury": "Finance, commerce, IT, journalism, marketing, data analytics, literature.",
            "Jupiter": "Education, law, banking, advisory, corporate consulting, spiritual teachings.",
            "Venus": "Design, creative arts, media, luxury goods, architecture, hospitality, fashion.",
            "Saturn": "Industrial management, judiciary, corporate governance, infrastructure, research."
        }

        return {
            "core_temperament": sign_archetypes.get(seventh_sign, "Balanced, dedicated, and supportive companion."),
            "likely_career_affinity": lord_careers.get(seventh_lord, "Professional administration and creative commerce."),
            "meeting_circumstances": f"Likely introduced through {PLANETS.get(seventh_lord, {}).get('day', 'Friday')} engagements, mutual networks, or shared professional/cultural endeavors.",
            "complementary_qualities": f"Complements your nature through the refined qualities of {seventh_sign} and guidance of {seventh_lord}."
        }

    def _build_wealth_timeline(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep dive into financial surges, asset building, and caution windows."""
        events = []
        l2 = house_lords[2]
        l11 = house_lords[11]
        l9 = house_lords[9]
        l5 = house_lords[5]
        l4 = house_lords[4]
        l12 = house_lords[12]

        for p in periods:
            if p["age_end"] < 18:
                continue

            md = p["md"]
            ad = p["ad"]
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])
            dignity_avg = (self._get_planet_dignity_score(md, grahas) + self._get_planet_dignity_score(ad, grahas)) / 2.0

            score = 48 + int(dignity_avg * 30)
            drivers = []

            if l2 in [md, ad]:
                score += 18
                drivers.append(f"2nd Lord ({l2}) ruling accumulated liquid wealth & family treasury")
            if l11 in [md, ad]:
                score += 18
                drivers.append(f"11th Lord ({l11}) activating lucrative income streams and profit windfalls")
            if l9 in [md, ad]:
                score += 14
                drivers.append(f"9th Lord ({l9}) of divine fortune opening fortuitous prosperity gates")
            if l5 in [md, ad]:
                score += 10
                drivers.append("5th House of speculative foresight and creative enterprise active")
            if l4 in [md, ad]:
                score += 8
                drivers.append(f"4th Lord ({l4}) supporting real estate, land, and vehicle acquisition")
            if "Jupiter" in [md, ad]:
                drivers.append("Jupiter (Dhana Karaka) expanding savings, investments, and ethical gains")
            if "Venus" in [md, ad]:
                drivers.append("Venus bringing luxury assets, artistic earnings, and material comforts")

            if l12 in [md, ad]:
                score -= 12
                drivers.append("12th House (Vyaya) triggering heightened expenditures or foreign financial outlays")

            score = min(98, max(30, score))

            if score >= 80:
                phase_type = "Major Wealth Surge & Asset Accumulation 💰"
                rating = "Peak Prosperity"
                recommendation = "Ideal period for capital deployment, major property acquisition, and scaling long-term investment portfolios."
            elif score >= 65:
                phase_type = "Steady Financial Expansion & Cashflow Gains"
                rating = "Highly Favorable"
                recommendation = "Focus on disciplined savings, diversifying income channels, and securing high-yield assets."
            elif score >= 50:
                phase_type = "Equilibrium & Normal Financial Circulation"
                rating = "Steady Growth"
                recommendation = "Maintain balanced budgets; avoid impulsive speculative risks; automate recurring investments."
            else:
                phase_type = "High Expenditure & Capital Preservation Alert"
                rating = "Prudence Advised"
                recommendation = "Curtail discretionary expenditures; safeguard capital reserves; avoid lending money or entering hasty partnerships."

            events.append({
                "period": f"{p['start_date']} to {p['end_date']}",
                "age_display": f"Age {p['age_start']} – {p['age_end']}",
                "dasha": p["dasha_name"],
                "score": score,
                "phase_type": phase_type,
                "rating": rating,
                "is_current": is_active,
                "drivers": drivers,
                "recommendation": recommendation
            })

        return {
            "dhana_lords": {"2nd_house": l2, "11th_house": l11, "9th_house": l9, "5th_house": l5},
            "timeline": events
        }

    def _build_health_timeline(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        house_signs: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep dive into physical vitality, longevity, and vulnerable periods."""
        events = []
        l1 = house_lords[1]
        l6 = house_lords[6]
        l8 = house_lords[8]
        l12 = house_lords[12]

        # Anatomical vulnerability mapping based on signs/houses
        vulnerabilities = self._map_anatomical_vulnerabilities(house_signs, grahas)

        for p in periods:
            md = p["md"]
            ad = p["ad"]
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])
            dignity_avg = (self._get_planet_dignity_score(md, grahas) + self._get_planet_dignity_score(ad, grahas)) / 2.0

            # Base vitality score
            vitality = 55 + int(dignity_avg * 30)
            drivers = []

            if l1 in [md, ad]:
                vitality += 15
                drivers.append(f"Lagna Lord ({l1}) fortifying immunity, stamina, and biological recovery")
            if "Sun" in [md, ad]:
                vitality += 10
                drivers.append("Sun (Surya - Atmakaraka) charging cellular vitality and cardiovascular strength")
            if "Mars" in [md, ad]:
                vitality += 6
                drivers.append("Mars bolstering muscular endurance and metabolic fire (Agni)")

            # Trik house lords reducing vitality
            if l6 in [md, ad]:
                vitality -= 14
                drivers.append(f"6th Lord ({l6}) of Rogas requiring digestive discipline and stress management")
            if l8 in [md, ad]:
                vitality -= 15
                drivers.append(f"8th Lord ({l8}) signaling sudden fatigue or chronic vitality fluctuations")
            if l12 in [md, ad]:
                vitality -= 10
                drivers.append(f"12th Lord ({l12}) highlighting need for restorative sleep and immunity protection")

            if "Saturn" in [md, ad] and yogas.get("sade_sati", {}).get("is_sade_sati", False):
                vitality -= 10
                drivers.append("Shani Sade Sati transit period advising joint care and mental peace")

            vitality = min(98, max(32, vitality))

            if vitality >= 80:
                phase_type = "Robust Vitality & High Physical Stamina 🌿"
                rating = "Peak Health"
                recommendation = "Optimal period for intense athletic training, physical conditioning, and cellular rejuvenation."
            elif vitality >= 65:
                phase_type = "Sound Health & Sustained Energy"
                rating = "Good Health"
                recommendation = "Maintain regular yoga, balanced Ayurvedic seasonal diet, and consistent circadian rhythms."
            elif vitality >= 50:
                phase_type = "Moderate Stamina — Preventive Care Needed"
                rating = "Care Advised"
                recommendation = "Pay attention to digestive fire (Pitta/Agni). Schedule routine health check-ups and avoid prolonged overwork."
            else:
                phase_type = "Vigilance Required — Stress & Rest Deficit Alert"
                rating = "High Vigilance"
                recommendation = "Prioritize rest, consume light sattvic warm foods, hydrate adequately, and practice Pranayama daily."

            events.append({
                "period": f"{p['start_date']} to {p['end_date']}",
                "age_display": f"Age {p['age_start']} – {p['age_end']}",
                "dasha": p["dasha_name"],
                "score": vitality,
                "phase_type": phase_type,
                "rating": rating,
                "is_current": is_active,
                "drivers": drivers,
                "recommendation": recommendation
            })

        return {
            "lagna_lord": l1,
            "sixth_lord": l6,
            "eighth_lord": l8,
            "vulnerabilities": vulnerabilities,
            "timeline": events
        }

    def _map_anatomical_vulnerabilities(self, house_signs: Dict[int, str], grahas: Dict[str, Any]) -> List[str]:
        """Identifies vulnerable organs based on 6th, 8th, and 12th house signs and afflicted planets."""
        body_parts = {
            "Aries": "Head, cranium, facial muscles, cerebral circulation",
            "Taurus": "Throat, vocal cords, thyroid, neck, tonsils",
            "Gemini": "Respiratory system, lungs, shoulders, nervous pathways",
            "Cancer": "Chest, breasts, stomach, lymphatic fluids, emotional digestion",
            "Leo": "Heart, upper spine, cardiac circulation, vitality center",
            "Virgo": "Digestive tract, small intestines, abdominal area, metabolism",
            "Libra": "Kidneys, lower back, lumbar region, renal filtration",
            "Scorpio": "Pelvic organs, reproductive system, excretory organs",
            "Sagittarius": "Hips, thighs, sciatic nerve, liver function",
            "Capricorn": "Bones, skeletal system, joints, knees, skin structure",
            "Aquarius": "Calves, ankles, circulatory flow, nervous rhythm",
            "Pisces": "Feet, lymphatic drainage, immune lymphatics, sleep quality"
        }

        vulns = []
        sign_6 = house_signs[6]
        sign_8 = house_signs[8]
        vulns.append(f"6th House ({sign_6}): Susceptibility to imbalances in {body_parts.get(sign_6, 'digestion')}.")
        vulns.append(f"8th House ({sign_8}): Requires attention to {body_parts.get(sign_8, 'lower pelvic systems')}.")
        return vulns

    def _synthesize_current_period(
        self,
        master: List[Dict[str, Any]],
        career: Dict[str, Any],
        marriage: Dict[str, Any],
        wealth: Dict[str, Any],
        health: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Provides instant high-level synthesis of running active period."""
        current_m = next((m for m in master if m["is_current"]), master[0] if master else {})
        current_c = next((c for c in career["timeline"] if c["is_current"]), {})
        current_mar = next((mar for mar in marriage["timeline"] if mar["is_current"]), {})
        current_w = next((w for w in wealth["timeline"] if w["is_current"]), {})
        current_h = next((h for h in health["timeline"] if h["is_current"]), {})

        return {
            "dasha": current_m.get("dasha", "N/A"),
            "period": f"{current_m.get('start_date', '')} to {current_m.get('end_date', '')}",
            "age": current_m.get("age_display", ""),
            "overall_score": current_m.get("overall_score", 70),
            "dominant_theme": current_m.get("dominant_theme", ""),
            "career_status": current_c.get("phase_type", "Normal Growth"),
            "marriage_status": current_mar.get("phase_type", "Normal Partnership"),
            "wealth_status": current_w.get("phase_type", "Normal Financial Circulation"),
            "health_status": current_h.get("phase_type", "Normal Health"),
            "career_recommendation": current_c.get("recommendation", ""),
            "marriage_recommendation": current_mar.get("recommendation", ""),
            "wealth_recommendation": current_w.get("recommendation", ""),
            "health_recommendation": current_h.get("recommendation", ""),
        }
