"""
core/timelines.py - Vedic Event Timeline Engine for Career, Marriage, Health, and Wealth
Integrates Vimshottari Dashas, Bhava lordships, planetary karakatwas, yogas,
and Gochara (transits) to compute detailed chronological event timelines.
"""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple
from core.constants import SIGN_NAMES, SIGN_RULERS, PLANETS, DASHA_ORDER, DASHA_YEARS

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

        # 6. Key Landmark Life Milestones & Events Timeline
        life_milestones = self._build_key_life_milestones(
            all_periods, birth_dt, target_dt, house_lords, house_signs, grahas, yogas
        )

        # 7. Granular Pratyantardasha Forecast Timeline (Near-term Precision)
        pratyantardashas = self._build_pratyantardasha_forecast(
            dashas, birth_dt, target_dt, house_lords, grahas
        )

        # 8. Annual 10-Year Forward Forecast Roadmap (Year-by-Year Outlook)
        annual_forecast = self._build_annual_forecast(
            all_periods, birth_dt, target_dt, house_lords, grahas, yogas
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
            "life_milestones": life_milestones,
            "annual_forecast": annual_forecast,
            "pratyantardashas": pratyantardashas,
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

    def _build_key_life_milestones(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        house_signs: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Synthesizes a chronological sequence of landmark life milestone events
        across education, career, marriage, wealth, relocation, spirituality, and health.
        """
        milestones = []
        l10 = house_lords[10]
        l7 = house_lords[7]
        l2 = house_lords[2]
        l11 = house_lords[11]
        l9 = house_lords[9]
        l4 = house_lords[4]
        l5 = house_lords[5]
        l1 = house_lords[1]
        l12 = house_lords[12]
        l6 = house_lords[6]
        l8 = house_lords[8]

        for p in periods:
            md = p["md"]
            ad = p["ad"]
            active_lords = [md, ad]
            age_s = p["age_start"]
            age_e = p["age_end"]
            start_yr = p["start_date"][:4]
            end_yr = p["end_date"][:4]
            year_range = f"{start_yr} – {end_yr}" if start_yr != end_yr else start_yr
            is_active = (p["start_dt"] <= target_dt < p["end_dt"])
            is_past = (p["end_dt"] <= target_dt)
            is_near_term = (not is_past and not is_active and (p["start_dt"] - target_dt).days <= 365.2425 * 7)

            if is_active:
                status = "Current Running Period 🌟"
                status_badge = "Active Now 🌟"
            elif is_near_term:
                status = "Upcoming Priority Window ⏳"
                status_badge = "Upcoming Window ⏳"
            elif is_past:
                status = "Past Landmark Milestone ✓"
                status_badge = "Completed Phase ✓"
            else:
                status = "Future Life Stage 🔮"
                status_badge = "Future Milestone 🔮"

            dignity_avg = (self._get_planet_dignity_score(md, grahas) + self._get_planet_dignity_score(ad, grahas)) / 2.0
            candidate_events = []

            # 1. Formative Education (Ages 10-24)
            if 10 <= age_s <= 24:
                if l5 in active_lords or l4 in active_lords or l9 in active_lords or "Mercury" in active_lords or "Jupiter" in active_lords:
                    score = min(96, int(55 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Education & Intellect",
                        "title": "Academic Excellence & Intellectual Foundation Milestone",
                        "event_type": "Formative Academic Achievement",
                        "score": score,
                        "basis": f"5th/9th house intelligence rays triggered by {md} - {ad} dasha, stimulating Vidya Karaka Mercury/Jupiter.",
                        "narrative": f"During Age {age_s} to {age_e} ({year_range}), scholarly focus and cognitive abilities experience acceleration. Favorable for qualifying exams, higher admissions, and building enduring foundational credentials.",
                        "guidance": "Dedicate focused effort to technical and creative learning; honor teachers and mentors.",
                        "remedy": "Recite Saraswati Vandana or chant 'Om Aim Saraswatyai Namah' 21 times at dawn."
                    })

            # 2. Career Elevation & Promotion (Ages 21-70)
            if 21 <= age_s <= 70:
                if l10 in active_lords or (l1 in active_lords and l9 in active_lords) or ("Sun" in active_lords and l10 in active_lords) or ("Saturn" in active_lords and l10 in active_lords):
                    score = min(98, int(60 + dignity_avg * 35))
                    title = "Major Career Elevation & Executive Recognition" if score >= 78 else "Professional Growth & Strategic Responsibility Milestone"
                    candidate_events.append({
                        "category": "Career & Status",
                        "title": title,
                        "event_type": "Professional Elevation",
                        "score": score,
                        "basis": f"Direct activation of 10th Lord ({l10}) and Lagna Lord ({l1}) infusing executive command and karmic recognition.",
                        "narrative": f"A prime professional phase unfolding between {p['start_date']} and {p['end_date']} (Age {age_s} – {age_e}). Auspicious planetary transits foster leadership roles, prominent authority, and institutional standing.",
                        "guidance": "Step up boldly for high-stakes leadership assignments; expand corporate networks and visibility.",
                        "remedy": f"Offer water to the rising Sun daily (Surya Arghya) with Gayatri Mantra for enduring career radiance."
                    })

            # 3. Golden Marriage & Sacred Commitment Window (Ages 20-45)
            if 20 <= age_s <= 45:
                if l7 in active_lords or "Venus" in active_lords or (l2 in active_lords and "Jupiter" in active_lords):
                    score = min(98, int(58 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Marriage & Relationships",
                        "title": "Golden Vivaha (Marriage) & Soulmate Partnership Portal 💍",
                        "event_type": "Sacred Relationship Commitment",
                        "score": score,
                        "basis": f"Activation of 7th Lord of marital destiny ({l7}) alongside Kalatra Karaka Venus/Jupiter.",
                        "narrative": f"An exceptionally auspicious window between {p['start_date']} and {p['end_date']} (Age {age_s} – {age_e}) triggering marital union, engagement, or profound relationship consolidation. Mutual devotion and domestic harmony are highlighted.",
                        "guidance": "Ideal time for matrimonial conversations, engagement ceremonies, and shared future planning.",
                        "remedy": "Worship Goddess Lakshmi and Lord Vishnu together on Fridays; cultivate patient communication."
                    })

            # 4. Wealth Surge & Asset Accumulation (Ages 22+)
            if age_s >= 22:
                if (l2 in active_lords or l11 in active_lords) and (l9 in active_lords or "Jupiter" in active_lords or "Venus" in active_lords or l1 in active_lords):
                    score = min(98, int(60 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Wealth & Assets",
                        "title": "Major Dhana Yoga Surge & Wealth Accumulation Milestone 💰",
                        "event_type": "Financial Expansion & Capital Growth",
                        "score": score,
                        "basis": f"2nd Lord of accumulated wealth ({l2}) and 11th Lord of gains ({l11}) energized in harmonious angle.",
                        "narrative": f"Financial gates open substantially from {p['start_date']} to {p['end_date']}. Lucrative income streams, investment windfalls, and multi-fold asset growth manifest under benevolent planetary radiation.",
                        "guidance": "Deploy surplus capital into enduring appreciating assets; establish diversified financial pillars.",
                        "remedy": "Chant Sri Suktam on Fridays or donate yellow grains/pulses to a worthy educational cause."
                    })

            # 5. Property, Home & Real Estate Acquisition (Ages 25+)
            if age_s >= 25:
                if l4 in active_lords and ("Mars" in active_lords or "Venus" in active_lords or l1 in active_lords):
                    score = min(96, int(56 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Wealth & Assets",
                        "title": "Auspicious Real Estate, Home & Property Acquisition 🏡",
                        "event_type": "Real Estate / Asset Milestone",
                        "score": score,
                        "basis": f"4th Lord of Sukha ({l4}) and Bhumi Karaka Mars aligning to foster immovable property ownership.",
                        "narrative": f"Between {p['start_date']} and {p['end_date']}, strong planetary support emerges for purchasing residential real estate, upgrading living spaces, or acquiring luxury transport.",
                        "guidance": "Conduct thorough legal due diligence on title deeds and finalize property investments with confidence.",
                        "remedy": "Perform Vastu Puja or keep a sacred silver coin in the north-east corner of your residence."
                    })

            # 6. Foreign Relocation, International Breakthrough & Travel
            if age_s >= 18:
                if (l12 in active_lords or l9 in active_lords) and ("Rahu" in active_lords or l10 in active_lords or l1 in active_lords):
                    score = min(95, int(54 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Travel & Relocation",
                        "title": "Foreign Relocation, Cross-Border Breakthrough & Long-Distance Voyage ✈️",
                        "event_type": "Global Expansion / Relocation",
                        "score": score,
                        "basis": f"12th Lord of foreign horizons ({l12}) and 9th Lord of long journeys activated under Rahu/Jupiter.",
                        "narrative": f"A major gateway opens for overseas employment, foreign relocation, or high-impact international projects during {year_range} (Age {age_s} – {age_e}). Cultural broadening and cross-border gains follow.",
                        "guidance": "Keep passports and international visas updated; embrace global cross-cultural opportunities.",
                        "remedy": "Donate food to traveling pilgrims or support shelters on Thursday evenings."
                    })

            # 7. Spiritual Awakening & Dharmic Evolution (Ages 28+)
            if age_s >= 28:
                if (l9 in active_lords or l8 in active_lords) and ("Jupiter" in active_lords or "Ketu" in active_lords or l1 in active_lords):
                    score = min(97, int(58 + dignity_avg * 35))
                    candidate_events.append({
                        "category": "Spiritual & Dharma",
                        "title": "Deep Spiritual Awakening, Higher Wisdom & Dharmic Initiation 🕉️",
                        "event_type": "Inner Evolution & Dharma Milestone",
                        "score": score,
                        "basis": f"9th house of Guru's grace and Moksha Karaka Ketu illuminating deep intuitive perception.",
                        "narrative": f"Between {p['start_date']} and {p['end_date']}, profound philosophical insights, spiritual pilgrimages, and inner clarity transform your perspective. A mentor or spiritual guide offers vital direction.",
                        "guidance": "Deepen meditation, study sacred philosophy, and practice regular acts of seva (selfless service).",
                        "remedy": "Recite the Maha Mrityunjaya Mantra 108 times during Monday twilight hours."
                    })

            # 8. Health Vigilance & Balancing Alert
            if l6 in active_lords or l8 in active_lords or ("Saturn" in active_lords and yogas.get("sade_sati", {}).get("is_sade_sati", False)):
                score = max(38, int(68 - dignity_avg * 25))
                candidate_events.append({
                    "category": "Health & Vitality",
                    "title": "Health & Vitality Balancing Alert — Preventive Care & Rejuvenation 🌿",
                    "event_type": "Vitality & Wellness Balancing",
                    "score": score,
                    "basis": f"Influence of 6th/8th Rogakara houses signaling stress sensitivity and metabolic fluctuations.",
                    "narrative": f"The phase from {p['start_date']} to {p['end_date']} advises mindful pacing. Guard against excessive fatigue, prioritize restorative sleep, and harmonize digestive fire (Agni).",
                    "guidance": "Schedule regular comprehensive health check-ups; eliminate stimulants; follow an Ayurvedic seasonal regimen.",
                    "remedy": "Perform Pranayama at dawn and donate warm clothing or sesame seeds on Saturdays."
                })

            # Select the top candidate event for this period
            if candidate_events:
                best_ev = max(candidate_events, key=lambda x: x["score"])
                milestones.append({
                    "milestone_id": f"MS_{p['start_date']}_{best_ev['category'][:3].upper()}",
                    "title": best_ev["title"],
                    "category": best_ev["category"],
                    "event_type": best_ev["event_type"],
                    "period": f"{p['start_date']} to {p['end_date']}",
                    "start_date": p["start_date"],
                    "end_date": p["end_date"],
                    "year_range": year_range,
                    "age_window": f"Age {age_s} – {age_e}",
                    "age_start": age_s,
                    "age_end": age_e,
                    "dasha": p["dasha_name"],
                    "status": status,
                    "status_badge": status_badge,
                    "is_current": is_active,
                    "is_near_term": is_near_term,
                    "is_past": is_past,
                    "favorability_score": best_ev["score"],
                    "astrological_basis": best_ev["basis"],
                    "prediction_narrative": best_ev["narrative"],
                    "actionable_guidance": best_ev["guidance"],
                    "vedic_remedy": best_ev["remedy"]
                })

        return milestones

    def _build_pratyantardasha_forecast(
        self,
        dashas: Dict[str, Any],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        grahas: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Builds a granular month-by-month Pratyantardasha (sub-sub period) forecast
        for the active running Antardasha.
        """
        active_pds = dashas.get("active_pratyantardashas", [])
        active_md = dashas.get("active_dasha", {}).get("mahadasha", "Jupiter")
        active_ad = dashas.get("active_dasha", {}).get("antardasha", "Moon")

        # Fallback if empty
        if not active_pds and "active_dasha" in dashas:
            from core.dashas import VimshottariDashaEngine
            ad_start = datetime.strptime(dashas["active_dasha"].get("start_date", "2024-01-01"), "%Y-%m-%d")
            ad_end = datetime.strptime(dashas["active_dasha"].get("end_date", "2026-01-01"), "%Y-%m-%d")
            active_pds = VimshottariDashaEngine.calculate_pratyantardashas(active_md, active_ad, ad_start, ad_end)

        results = []
        for pd in active_pds:
            pd_planet = pd["planet"]
            s_dt = datetime.strptime(pd["start_date"], "%Y-%m-%d")
            e_dt = datetime.strptime(pd["end_date"], "%Y-%m-%d")
            is_active = (s_dt <= target_dt < e_dt)

            score_p = self._get_planet_dignity_score(pd_planet, grahas)
            score = int(min(96, max(38, 48 + score_p * 45)))

            themes = {
                "Sun": "Authority, leadership initiative, government interactions, and heightened vitality.",
                "Moon": "Emotional peace, maternal bonding, public popularity, and creative intuition.",
                "Mars": "Physical stamina, decisive action, engineering/technical breakthroughs, competitive courage.",
                "Mercury": "Commercial enterprise, communications, analytical contracts, data strategy.",
                "Jupiter": "Wisdom expansion, auspicious blessings, mentorship, ethical investments.",
                "Venus": "Artistic fulfillment, relationship joy, luxury acquisition, diplomatic harmony.",
                "Saturn": "Systematic discipline, structural organization, enduring foundation building.",
                "Rahu": "Unconventional innovation, foreign affairs, technological leaps, sudden insights.",
                "Ketu": "Intuitive clarity, spiritual detachment, research depth, contemplative breakthroughs."
            }

            results.append({
                "pratyantardasha": pd_planet,
                "dasha_hierarchy": f"{active_md} - {active_ad} - {pd_planet}",
                "start_date": pd["start_date"],
                "end_date": pd["end_date"],
                "duration_days": pd.get("duration_days", round((e_dt - s_dt).days, 1)),
                "is_current": is_active,
                "status_badge": "Active Running Window 🌟" if is_active else ("Upcoming" if s_dt > target_dt else "Completed"),
                "favorability_score": score,
                "focus_theme": themes.get(pd_planet, "Balanced energetic progress."),
                "guidance": f"Harmonize with {pd_planet}'s vibration: prioritize quality execution and patience."
            })

        return results

    def _build_annual_forecast(
        self,
        periods: List[Dict[str, Any]],
        birth_dt: datetime,
        target_dt: datetime,
        house_lords: Dict[int, str],
        grahas: Dict[str, Any],
        yogas: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Builds a comprehensive year-by-year chronological roadmap
        covering the current year and the subsequent 10 years.
        """
        current_year = target_dt.year
        annual = []

        for yr in range(current_year - 1, current_year + 11):
            mid_year = datetime(yr, 7, 1)
            age = round((mid_year - birth_dt).days / 365.2425, 1)

            matched_p = next((p for p in periods if p["start_dt"] <= mid_year < p["end_dt"]), periods[0] if periods else {})
            md = matched_p.get("md", "Sun")
            ad = matched_p.get("ad", "Moon")

            md_score = self._get_planet_dignity_score(md, grahas)
            ad_score = self._get_planet_dignity_score(ad, grahas)
            score = int(min(96, max(38, 48 + (md_score + ad_score) * 24)))

            is_cur_yr = (yr == current_year)

            career_out = (
                f"Under {md}-{ad}, professional focus is high. Favorable for consolidating authority and establishing strategic alliances."
                if score >= 70 else
                f"A consolidation and learning phase in career under {md}-{ad}. Prioritize steady execution over impulsive risks."
            )
            wealth_out = (
                f"Income circulation is robust. Good opportunities for capital growth and asset diversification."
                if score >= 68 else
                f"Maintain budget discipline; safeguard reserves against unexpected discretionary outlays."
            )
            rel_out = (
                f"Harmonious domestic ties and relationship support bring emotional stability."
                if score >= 65 else
                f"Practice empathetic listening; resolve domestic misunderstandings with calm patience."
            )
            health_out = (
                f"Sound vitality and resilient energy levels support sustained productivity."
                if score >= 65 else
                f"Watch for fatigue and stress. Prioritize circadian sleep rhythms and a sattvic diet."
            )

            annual.append({
                "year": yr,
                "age_at_midyear": age,
                "dasha": f"{md} - {ad}",
                "is_current_year": is_cur_yr,
                "overall_score": score,
                "status_badge": "Current Year 🌟" if is_cur_yr else ("Upcoming Year" if yr > current_year else "Past Year"),
                "primary_theme": f"Karmic expansion in {matched_p.get('dasha_name', '')} under {md} & {ad}",
                "career_outlook": career_out,
                "wealth_outlook": wealth_out,
                "relationship_outlook": rel_out,
                "health_outlook": health_out,
                "key_recommendation": f"Focus conscious effort on {PLANETS.get(ad, {}).get('day', 'Wednesday')} auspicious activities."
            })

        return annual
