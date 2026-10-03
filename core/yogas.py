"""
core/yogas.py - Vedic Yogas and Doshas Analysis Engine
Evaluates Manglik Dosha, Sade Sati, Kaal Sarp Dosha, and Benefic Yogas.
"""

from typing import Dict, Any, List
from datetime import datetime

from core.constants import SIGN_NAMES, SIGNS, PLANETS
from core.ephemeris import EphemerisEngine

class YogaEngine:
    def __init__(self, ephem_engine: EphemerisEngine):
        self.ephem = ephem_engine

    def analyze_all_yogas_and_doshas(
        self, grahas: Dict[str, Any], lagna_sign: str, current_dt: datetime = None
    ) -> Dict[str, Any]:
        """Runs the complete suite of Vedic Yoga & Dosha analyses."""
        if current_dt is None:
            current_dt = datetime.now()

        manglik = self.check_manglik_dosha(grahas, lagna_sign)
        sade_sati = self.check_sade_sati(grahas, current_dt)
        kaal_sarp = self.check_kaal_sarp_dosha(grahas)
        benefic_yogas = self.identify_benefic_yogas(grahas, lagna_sign)
        inauspicious_yogas = self.identify_inauspicious_yogas(grahas, lagna_sign)

        return {
            "manglik_dosha": manglik,
            "sade_sati": sade_sati,
            "kaal_sarp_dosha": kaal_sarp,
            "benefic_yogas": benefic_yogas,
            "inauspicious_yogas": inauspicious_yogas,
        }

    def check_manglik_dosha(self, grahas: Dict[str, Any], lagna_sign: str) -> Dict[str, Any]:
        """
        Analyzes Manglik (Kuja) Dosha from Lagna and Chandra.
        Classic positions: 1st, 2nd (South tradition), 4th, 7th, 8th, 12th houses.
        """
        mars_house = grahas["Mars"]["house"]
        mars_house_moon = grahas["Mars"]["house_from_moon"]
        mars_sign = grahas["Mars"]["sign"]

        manglik_houses = {1, 2, 4, 7, 8, 12}
        is_manglik_lagna = mars_house in manglik_houses
        is_manglik_moon = mars_house_moon in manglik_houses

        has_dosha = is_manglik_lagna or is_manglik_moon
        severity = "None"
        cancellations: List[str] = []

        if has_dosha:
            if is_manglik_lagna and is_manglik_moon:
                severity = "High (Poorna Manglik)"
            elif is_manglik_lagna:
                severity = "Moderate (Lagna Manglik)"
            else:
                severity = "Mild (Chandra Manglik)"

            # Classical Vedic Cancellations (Nivritti)
            if mars_sign == "Aries" and mars_house == 1:
                cancellations.append("Mars is in its own sign (Aries) in 1st house.")
            if mars_sign == "Scorpio" and mars_house == 4:
                cancellations.append("Mars is in its own sign (Scorpio) in 4th house.")
            if mars_sign == "Capricorn" and (mars_house in (7, 8)):
                cancellations.append("Mars is exalted in Capricorn in 7th/8th house.")
            if mars_sign == "Sagittarius" or mars_sign == "Pisces":
                cancellations.append("Mars in Jupiterian signs softens aggressive Martian energy.")
            
            # Check if Jupiter aspects or conjoins Mars
            jup_house = grahas["Jupiter"]["house"]
            dist_jup_mars = (mars_house - jup_house) % 12
            if dist_jup_mars == 0:
                cancellations.append("Benefic Jupiter is conjunct Mars, calming its aggressive heat.")
            elif dist_jup_mars in [4, 6, 8]:  # 5th, 7th, 9th aspects of Jupiter
                cancellations.append(f"Benefic Jupiter casts its sacred {dist_jup_mars + 1}th aspect upon Mars.")

            # Check if Moon is with Mars
            if mars_house == grahas["Moon"]["house"]:
                cancellations.append("Mars is conjunct Moon forming Chandra-Mangala yoga, nullifying harmful traits.")

            is_cancelled = len(cancellations) > 0
        else:
            is_cancelled = False

        description = (
            "No Manglik Dosha is present in this birth chart. Marital and relationship harmony is naturally supported."
            if not has_dosha else
            ("Manglik Dosha is technically present but effectively neutralized/cancelled by strong protective Vedic planetary combinations."
             if is_cancelled else
             f"Active {severity} observed. Mars directs intense assertive and passionate energy into relationship houses.")
        )

        return {
            "has_dosha": has_dosha,
            "is_cancelled": is_cancelled,
            "severity": "Cancelled" if is_cancelled else severity,
            "mars_house_from_lagna": mars_house,
            "mars_house_from_moon": mars_house_moon,
            "mars_sign": mars_sign,
            "cancellations": cancellations,
            "description": description
        }

    def check_sade_sati(self, grahas: Dict[str, Any], current_dt: datetime) -> Dict[str, Any]:
        """
        Determines current Sade Sati and Shani Dhaiya status.
        Calculates transit Saturn position for the requested date.
        """
        natal_moon_sign = grahas["Moon"]["sign"]
        moon_sign_idx = SIGN_NAMES.index(natal_moon_sign)

        # Calculate current Saturn position
        current_data = self.ephem.calculate_planetary_positions(current_dt)
        transit_saturn_sign = current_data["grahas"]["Saturn"]["sign"]
        saturn_sign_idx = SIGN_NAMES.index(transit_saturn_sign)

        diff = (saturn_sign_idx - moon_sign_idx) % 12

        is_sade_sati = False
        phase = "None"
        description = ""

        if diff == 11:  # 12th from Moon
            is_sade_sati = True
            phase = "First Phase (Rising / Aardha Sade Sati)"
            description = (
                f"Saturn is currently in {transit_saturn_sign}, 12th from your natal Moon ({natal_moon_sign}). "
                "This phase prompts introspection, changes in expenditure, long travels, and philosophical re-evaluation."
            )
        elif diff == 0:  # 1st from Moon (Same sign)
            is_sade_sati = True
            phase = "Second Phase (Peak / Shikhar Charan)"
            description = (
                f"Saturn is currently transiting directly over your natal Moon in {natal_moon_sign}. "
                "This is the core transformative period demanding patience, emotional resilience, discipline, and hard work."
            )
        elif diff == 1:  # 2nd from Moon
            is_sade_sati = True
            phase = "Third Phase (Setting / Antya Charan)"
            description = (
                f"Saturn is in {transit_saturn_sign}, 2nd from natal Moon ({natal_moon_sign}). "
                "The most intense pressure eases as family stability and financial restructuring take center stage."
            )
        elif diff == 3:  # 4th from Moon
            phase = "Kantaka Shani (Dhaiya / Small 2.5 Yr Cycle)"
            description = (
                f"Saturn is transiting the 4th house from your natal Moon ({natal_moon_sign}). "
                "Brings focus to domestic affairs, real estate, and inner emotional balance."
            )
        elif diff == 7:  # 8th from Moon
            phase = "Ashtama Shani (Dhaiya / 8th House Cycle)"
            description = (
                f"Saturn is transiting the 8th house from your natal Moon ({natal_moon_sign}). "
                "Demands careful attention to health, unexpected transitions, and deep spiritual discipline."
            )
        else:
            description = (
                f"You are currently free from Shani Sade Sati and Dhaiya. "
                f"Transit Saturn in {transit_saturn_sign} is positioned favorably in the {diff + 1}th house from your natal Moon."
            )

        return {
            "is_sade_sati": is_sade_sati,
            "has_dhaiya": "Dhaiya" in phase,
            "phase": phase,
            "natal_moon_sign": natal_moon_sign,
            "transit_saturn_sign": transit_saturn_sign,
            "transit_saturn_deg": round(current_data["grahas"]["Saturn"]["sign_deg"], 2),
            "description": description
        }

    def check_kaal_sarp_dosha(self, grahas: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines if all classical planets are hemmed between Rahu and Ketu.
        """
        rahu_lon = grahas["Rahu"]["sidereal_lon"]
        ketu_lon = grahas["Ketu"]["sidereal_lon"]

        classical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        side_a = 0
        side_b = 0

        for p in classical_planets:
            p_lon = grahas[p]["sidereal_lon"]
            # Distance from Rahu to planet moving forward
            dist_from_rahu = (p_lon - rahu_lon) % 360.0
            if dist_from_rahu < 180.0:
                side_a += 1
            else:
                side_b += 1

        total = len(classical_planets)
        has_dosha = False
        dosha_type = "None"
        severity = "None"

        # Kaal Sarp names based on Rahu's house from Lagna
        rahu_house = grahas["Rahu"]["house"]
        kaal_sarp_names = {
            1: "Anant Kaal Sarp Dosha",
            2: "Kulik Kaal Sarp Dosha",
            3: "Vasuki Kaal Sarp Dosha",
            4: "Shankhpal Kaal Sarp Dosha",
            5: "Padma Kaal Sarp Dosha",
            6: "Mahapadma Kaal Sarp Dosha",
            7: "Takshak Kaal Sarp Dosha",
            8: "Karkotak Kaal Sarp Dosha",
            9: "Shankhachood Kaal Sarp Dosha",
            10: "Ghatak Kaal Sarp Dosha",
            11: "Vishdhar Kaal Sarp Dosha",
            12: "Sheshnag Kaal Sarp Dosha",
        }

        if side_a == total or side_b == total:
            has_dosha = True
            severity = "Full (Poorna Kaal Sarp)"
            dosha_type = kaal_sarp_names.get(rahu_house, "Kaal Sarp Dosha")
        elif side_a == total - 1 or side_b == total - 1:
            has_dosha = True
            severity = "Partial (Anshik Kaal Sarp)"
            dosha_type = f"Anshik {kaal_sarp_names.get(rahu_house, 'Kaal Sarp')}"

        return {
            "has_dosha": has_dosha,
            "severity": severity,
            "type": dosha_type,
            "rahu_house": rahu_house,
            "description": (
                f"{dosha_type} ({severity}) is detected. Inspires intense life lessons, deep karmic drive, and sudden elevation once remedies/maturity are embraced."
                if has_dosha else
                "No Kaal Sarp Dosha present. Planets are distributed naturally across both sides of the nodal axis."
            )
        }

    def identify_benefic_yogas(self, grahas: Dict[str, Any], lagna_sign: str) -> List[Dict[str, Any]]:
        """Identifies auspicious classical Vedic Yogas."""
        yogas = []

        # 1. Gaja Kesari Yoga (Jupiter in Kendra from Moon: 1, 4, 7, 10)
        dist_moon_jup = (grahas["Jupiter"]["house"] - grahas["Moon"]["house"]) % 12
        if dist_moon_jup in [0, 3, 6, 9]:
            yogas.append({
                "name": "Gaja Kesari Yoga",
                "category": "Auspicious Raja Yoga",
                "planets": ["Jupiter", "Moon"],
                "description": "Jupiter is in a Kendra (angular house) from the Moon. Bestows profound wisdom, lasting honor, high social standing, and invincibility against adversity."
            })

        # 2. Budhaditya Yoga (Sun + Mercury in same house)
        if grahas["Sun"]["house"] == grahas["Mercury"]["house"]:
            combust_text = " (Note: Mercury is combust)" if grahas["Mercury"]["is_combust"] else ""
            yogas.append({
                "name": "Budhaditya Yoga",
                "category": "Intellectual Brilliance",
                "planets": ["Sun", "Mercury"],
                "description": f"Sun and Mercury share the same house{combust_text}. Bestows sharp analytical intellect, eloquent speech, commercial foresight, and executive authority."
            })

        # 3. Chandra-Mangala Yoga (Moon + Mars in same house)
        if grahas["Moon"]["house"] == grahas["Mars"]["house"]:
            yogas.append({
                "name": "Chandra-Mangala Yoga",
                "category": "Dhana / Wealth Yoga",
                "planets": ["Moon", "Mars"],
                "description": "Conjunction of Moon and Mars creates a potent drive for enterprise, real estate, dynamic resourcefulness, and high financial acumen."
            })

        # 4. Pancha Mahapurusha Yogas (Mars, Mercury, Jupiter, Venus, Saturn in Kendra and in Own/Exalted sign)
        kendra_houses = {1, 4, 7, 10}

        # Ruchaka (Mars)
        if grahas["Mars"]["house"] in kendra_houses and ("Exalted" in grahas["Mars"]["dignity"] or "Own Sign" in grahas["Mars"]["dignity"]):
            yogas.append({
                "name": "Ruchaka Yoga (Pancha Mahapurusha)",
                "category": "Supreme Hero / Commander",
                "planets": ["Mars"],
                "description": "Mars resides in an angular house in exaltation or own sign. Imparts tremendous physical vitality, leadership, courage, victory in competition, and administrative power."
            })

        # Bhadra (Mercury)
        if grahas["Mercury"]["house"] in kendra_houses and ("Exalted" in grahas["Mercury"]["dignity"] or "Own Sign" in grahas["Mercury"]["dignity"]):
            yogas.append({
                "name": "Bhadra Yoga (Pancha Mahapurusha)",
                "category": "Supreme Scholar / Intellect",
                "planets": ["Mercury"],
                "description": "Mercury is placed in Kendra in Gemini or Virgo. Confers brilliant communicative gifts, exceptional mathematical or scientific acumen, and longevity."
            })

        # Hamsa (Jupiter)
        if grahas["Jupiter"]["house"] in kendra_houses and ("Exalted" in grahas["Jupiter"]["dignity"] or "Own Sign" in grahas["Jupiter"]["dignity"]):
            yogas.append({
                "name": "Hamsa Yoga (Pancha Mahapurusha)",
                "category": "Supreme Sage / Mentor",
                "planets": ["Jupiter"],
                "description": "Jupiter is placed in Kendra in Cancer, Sagittarius, or Pisces. Confers a pure, righteous nature, profound spiritual wisdom, veneration by society, and lifelong blessings."
            })

        # Malavya (Venus)
        if grahas["Venus"]["house"] in kendra_houses and ("Exalted" in grahas["Venus"]["dignity"] or "Own Sign" in grahas["Venus"]["dignity"]):
            yogas.append({
                "name": "Malavya Yoga (Pancha Mahapurusha)",
                "category": "Supreme Esthete / Luxury",
                "planets": ["Venus"],
                "description": "Venus is in Kendra in Taurus, Libra, or Pisces. Grants refined aesthetic taste, artistic brilliance, abundant material luxuries, charisma, and a happy romantic life."
            })

        # Sasa / Shasha (Saturn)
        if grahas["Saturn"]["house"] in kendra_houses and ("Exalted" in grahas["Saturn"]["dignity"] or "Own Sign" in grahas["Saturn"]["dignity"]):
            yogas.append({
                "name": "Sasa Yoga (Pancha Mahapurusha)",
                "category": "Supreme Ruler / Strategist",
                "planets": ["Saturn"],
                "description": "Saturn is in Kendra in Libra, Capricorn, or Aquarius. Confers authority over institutions, enduring endurance, judicial acumen, and great mastery through patient labor."
            })

        # 5. Lakshmi Yoga (Venus and 9th lord strongly placed)
        if "Exalted" in grahas["Venus"]["dignity"] or "Own Sign" in grahas["Venus"]["dignity"]:
            yogas.append({
                "name": "Lakshmi Yoga",
                "category": "Prosperity & Grace",
                "planets": ["Venus"],
                "description": "Dignified Venus bestows the grace of Goddess Lakshmi: continuous prosperity, high cultural reputation, and generous fortune."
            })

        return yogas

    def identify_inauspicious_yogas(self, grahas: Dict[str, Any], lagna_sign: str) -> List[Dict[str, Any]]:
        """Identifies specific doshas and challenging yogas."""
        inauspicious = []

        # Guru-Chandal Yoga (Jupiter conjunct Rahu or Ketu)
        jup_house = grahas["Jupiter"]["house"]
        if jup_house == grahas["Rahu"]["house"] or jup_house == grahas["Ketu"]["house"]:
            inauspicious.append({
                "name": "Guru-Chandal Yoga",
                "planets": ["Jupiter", "Rahu/Ketu"],
                "description": "Jupiter conjoins Rahu or Ketu in the same house. Prompts unconventional philosophical questioning and requires conscious integrity in financial/ethical matters."
            })

        # Surya Grahan / Chandra Grahan Dosha
        if grahas["Sun"]["house"] in [grahas["Rahu"]["house"], grahas["Ketu"]["house"]]:
            inauspicious.append({
                "name": "Surya Grahan Dosha",
                "planets": ["Sun", "Rahu/Ketu"],
                "description": "Sun is conjunct Rahu or Ketu. Advises worship of Surya Dev to enhance vitality, self-confidence, and smooth relations with authority figures."
            })

        if grahas["Moon"]["house"] in [grahas["Rahu"]["house"], grahas["Ketu"]["house"]]:
            inauspicious.append({
                "name": "Chandra Grahan Dosha",
                "planets": ["Moon", "Rahu/Ketu"],
                "description": "Moon is conjunct Rahu or Ketu. Advises mindfulness and meditation to steady emotional clarity and intuitive balance."
            })

        return inauspicious
