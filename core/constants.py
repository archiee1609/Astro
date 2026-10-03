"""
core/constants.py - Classical Vedic Astrology and Numerology Constants
Based on Brihat Parashara Hora Shastra, Phaladeepika, and Cheiro/Sankhya Shastra.
"""

from typing import Dict, List, Tuple, Any

# 12 Rashis (Zodiac Signs)
SIGNS = [
    {"id": 0, "name": "Aries", "sanskrit": "Mesha (मेष)", "ruler": "Mars", "element": "Fire", "modality": "Movable (Chara)", "gender": "Male"},
    {"id": 1, "name": "Taurus", "sanskrit": "Vrishabha (वृषभ)", "ruler": "Venus", "element": "Earth", "modality": "Fixed (Sthira)", "gender": "Female"},
    {"id": 2, "name": "Gemini", "sanskrit": "Mithuna (मिथुन)", "ruler": "Mercury", "element": "Air", "modality": "Dual (Dvisvabhava)", "gender": "Male"},
    {"id": 3, "name": "Cancer", "sanskrit": "Karka (कर्क)", "ruler": "Moon", "element": "Water", "modality": "Movable (Chara)", "gender": "Female"},
    {"id": 4, "name": "Leo", "sanskrit": "Simha (सिंह)", "ruler": "Sun", "element": "Fire", "modality": "Fixed (Sthira)", "gender": "Male"},
    {"id": 5, "name": "Virgo", "sanskrit": "Kanya (कन्या)", "ruler": "Mercury", "element": "Earth", "modality": "Dual (Dvisvabhava)", "gender": "Female"},
    {"id": 6, "name": "Libra", "sanskrit": "Tula (तुला)", "ruler": "Venus", "element": "Air", "modality": "Movable (Chara)", "gender": "Male"},
    {"id": 7, "name": "Scorpio", "sanskrit": "Vrishchika (वृश्चिक)", "ruler": "Mars", "element": "Water", "modality": "Fixed (Sthira)", "gender": "Female"},
    {"id": 8, "name": "Sagittarius", "sanskrit": "Dhanu (धनु)", "ruler": "Jupiter", "element": "Fire", "modality": "Dual (Dvisvabhava)", "gender": "Male"},
    {"id": 9, "name": "Capricorn", "sanskrit": "Makara (मकर)", "ruler": "Saturn", "element": "Earth", "modality": "Movable (Chara)", "gender": "Female"},
    {"id": 10, "name": "Aquarius", "sanskrit": "Kumbha (कुम्भ)", "ruler": "Saturn", "element": "Air", "modality": "Fixed (Sthira)", "gender": "Male"},
    {"id": 11, "name": "Pisces", "sanskrit": "Meena (मीन)", "ruler": "Jupiter", "element": "Water", "modality": "Dual (Dvisvabhava)", "gender": "Female"},
]

SIGN_NAMES = [s["name"] for s in SIGNS]
SIGN_SANSKRIT = [s["sanskrit"] for s in SIGNS]
SIGN_RULERS = [s["ruler"] for s in SIGNS]

# 27 Nakshatras (Lunar Mansions)
NAKSHATRAS = [
    {"id": 0, "name": "Ashwini", "sanskrit": "अश्विनी", "lord": "Ketu", "deity": "Ashvini Kumaras", "symbol": "Horse's head", "start_deg": 0.0},
    {"id": 1, "name": "Bharani", "sanskrit": "भरणी", "lord": "Venus", "deity": "Yama", "symbol": "Yoni (Vessel)", "start_deg": 13.333333},
    {"id": 2, "name": "Krittika", "sanskrit": "कृत्तिका", "lord": "Sun", "deity": "Agni", "symbol": "Razor / Flame", "start_deg": 26.666667},
    {"id": 3, "name": "Rohini", "sanskrit": "रोहिणी", "lord": "Moon", "deity": "Brahma / Prajapati", "symbol": "Chariot / Cart", "start_deg": 40.0},
    {"id": 4, "name": "Mrigashira", "sanskrit": "मृगशिरा", "lord": "Mars", "deity": "Soma", "symbol": "Deer's head", "start_deg": 53.333333},
    {"id": 5, "name": "Ardra", "sanskrit": "आर्द्रा", "lord": "Rahu", "deity": "Rudra", "symbol": "Teardrop / Diamond", "start_deg": 66.666667},
    {"id": 6, "name": "Punarvasu", "sanskrit": "पुनर्वसु", "lord": "Jupiter", "deity": "Aditi", "symbol": "Bow and quiver", "start_deg": 80.0},
    {"id": 7, "name": "Pushya", "sanskrit": "पुष्य", "lord": "Saturn", "deity": "Brihaspati", "symbol": "Lotus / Udder", "start_deg": 93.333333},
    {"id": 8, "name": "Ashlesha", "sanskrit": "आश्लेषा", "lord": "Mercury", "deity": "Sarpa / Nagas", "symbol": "Coiled serpent", "start_deg": 106.666667},
    {"id": 9, "name": "Magha", "sanskrit": "मघा", "lord": "Ketu", "deity": "Pitras", "symbol": "Royal palanquin / Throne", "start_deg": 120.0},
    {"id": 10, "name": "Purva Phalguni", "sanskrit": "पूर्वा फाल्गुनी", "lord": "Venus", "deity": "Bhaga", "symbol": "Front legs of bed", "start_deg": 133.333333},
    {"id": 11, "name": "Uttara Phalguni", "sanskrit": "उत्तरा फाल्गुनी", "lord": "Sun", "deity": "Aryaman", "symbol": "Back legs of bed", "start_deg": 146.666667},
    {"id": 12, "name": "Hasta", "sanskrit": "हस्त", "lord": "Moon", "deity": "Savitar", "symbol": "Open hand", "start_deg": 160.0},
    {"id": 13, "name": "Chitra", "sanskrit": "चित्रा", "lord": "Mars", "deity": "Vishwakarma", "symbol": "Pearl / Jewel", "start_deg": 173.333333},
    {"id": 14, "name": "Swati", "sanskrit": "स्वाति", "lord": "Rahu", "deity": "Vayu", "symbol": "Shoot of plant / Coral", "start_deg": 186.666667},
    {"id": 15, "name": "Vishakha", "sanskrit": "विशाखा", "lord": "Jupiter", "deity": "Indra-Agni", "symbol": "Triumphal arch", "start_deg": 200.0},
    {"id": 16, "name": "Anuradha", "sanskrit": "अनुराधा", "lord": "Saturn", "deity": "Mitra", "symbol": "Lotus flower", "start_deg": 213.333333},
    {"id": 17, "name": "Jyeshtha", "sanskrit": "ज्येष्ठा", "lord": "Mercury", "deity": "Indra", "symbol": "Umbrella / Talisman", "start_deg": 226.666667},
    {"id": 18, "name": "Moola", "sanskrit": "मूल", "lord": "Ketu", "deity": "Nirriti", "symbol": "Tied bunch of roots", "start_deg": 240.0},
    {"id": 19, "name": "Purva Ashadha", "sanskrit": "पूर्वाषाढ़ा", "lord": "Venus", "deity": "Apas (Waters)", "symbol": "Elephant tusk / Fan", "start_deg": 253.333333},
    {"id": 20, "name": "Uttara Ashadha", "sanskrit": "उत्तराषाढ़ा", "lord": "Sun", "deity": "Vishwadevas", "symbol": "Small cot / Elephant tusk", "start_deg": 266.666667},
    {"id": 21, "name": "Shravana", "sanskrit": "श्रवण", "lord": "Moon", "deity": "Vishnu", "symbol": "Ear / Three footprints", "start_deg": 280.0},
    {"id": 22, "name": "Dhanishta", "sanskrit": "धनिष्ठा", "lord": "Mars", "deity": "Eight Vasus", "symbol": "Drum (Mridangam)", "start_deg": 293.333333},
    {"id": 23, "name": "Shatabhisha", "sanskrit": "शतभिषा", "lord": "Rahu", "deity": "Varuna", "symbol": "100 physicians / Circle", "start_deg": 306.666667},
    {"id": 24, "name": "Purva Bhadrapada", "sanskrit": "पूर्व भाद्रपद", "lord": "Jupiter", "deity": "Aja Ekapada", "symbol": "Front of funeral cot", "start_deg": 320.0},
    {"id": 25, "name": "Uttara Bhadrapada", "sanskrit": "उत्तर भाद्रपद", "lord": "Saturn", "deity": "Ahirbudhnya", "symbol": "Back of funeral cot", "start_deg": 333.333333},
    {"id": 26, "name": "Revati", "sanskrit": "रेवती", "lord": "Mercury", "deity": "Pushan", "symbol": "Pair of fish", "start_deg": 346.666667},
]

NAKSHATRA_NAMES = [n["name"] for n in NAKSHATRAS]

# Navagrahas (Nine Celestial Bodies in Vedic Astrology)
PLANETS = {
    "Sun": {
        "sanskrit": "Surya (सूर्य)",
        "nature": "Natural Malefic (Krupa Krura / Kingly)",
        "gender": "Male",
        "element": "Fire",
        "own_signs": ["Leo"],
        "exalted": {"sign": "Aries", "deep_deg": 10.0},
        "debilitated": {"sign": "Libra", "deep_deg": 10.0},
        "moolatrikona": {"sign": "Leo", "start": 0.0, "end": 20.0},
        "friends": ["Moon", "Mars", "Jupiter"],
        "neutral": ["Mercury"],
        "enemies": ["Venus", "Saturn", "Rahu", "Ketu"],
        "gemstone": "Ruby (Manikya)",
        "metal": "Gold / Copper",
        "day": "Sunday",
        "color": "Ruby Red / Copper Gold",
        "mantra": "Om Hram Hreem Hroum Sah Suryaya Namah",
        "dasha_years": 6,
    },
    "Moon": {
        "sanskrit": "Chandra (चन्द्र)",
        "nature": "Benefic when waxing (Shukla), Mild malefic when waning (Krishna)",
        "gender": "Female",
        "element": "Water",
        "own_signs": ["Cancer"],
        "exalted": {"sign": "Taurus", "deep_deg": 3.0},
        "debilitated": {"sign": "Scorpio", "deep_deg": 3.0},
        "moolatrikona": {"sign": "Taurus", "start": 3.0, "end": 30.0},
        "friends": ["Sun", "Mercury"],
        "neutral": ["Mars", "Jupiter", "Venus", "Saturn"],
        "enemies": ["Rahu", "Ketu"],
        "gemstone": "Natural Pearl (Moti)",
        "metal": "Silver",
        "day": "Monday",
        "color": "Pearl White / Silver",
        "mantra": "Om Shram Shreem Shroum Sah Chandraya Namah",
        "dasha_years": 10,
    },
    "Mars": {
        "sanskrit": "Mangala (मङ्गल)",
        "nature": "Natural Malefic (Commander)",
        "gender": "Male",
        "element": "Fire",
        "own_signs": ["Aries", "Scorpio"],
        "exalted": {"sign": "Capricorn", "deep_deg": 28.0},
        "debilitated": {"sign": "Cancer", "deep_deg": 28.0},
        "moolatrikona": {"sign": "Aries", "start": 0.0, "end": 12.0},
        "friends": ["Sun", "Moon", "Jupiter"],
        "neutral": ["Venus", "Saturn"],
        "enemies": ["Mercury", "Rahu", "Ketu"],
        "gemstone": "Red Coral (Moonga)",
        "metal": "Copper",
        "day": "Tuesday",
        "color": "Scarlet Red / Coral",
        "mantra": "Om Kram Kreem Kroum Sah Bhaumaya Namah",
        "dasha_years": 7,
    },
    "Mercury": {
        "sanskrit": "Budha (बुध)",
        "nature": "Benefic (adopts nature of conjunct planets)",
        "gender": "Neutral",
        "element": "Earth",
        "own_signs": ["Gemini", "Virgo"],
        "exalted": {"sign": "Virgo", "deep_deg": 15.0},
        "debilitated": {"sign": "Pisces", "deep_deg": 15.0},
        "moolatrikona": {"sign": "Virgo", "start": 15.0, "end": 20.0},
        "friends": ["Sun", "Venus"],
        "neutral": ["Mars", "Jupiter", "Saturn"],
        "enemies": ["Moon"],
        "gemstone": "Emerald (Panna)",
        "metal": "Bronze / Brass",
        "day": "Wednesday",
        "color": "Emerald Green",
        "mantra": "Om Bram Breem Broum Sah Budhaya Namah",
        "dasha_years": 17,
    },
    "Jupiter": {
        "sanskrit": "Guru / Brihaspati (बृहस्पति)",
        "nature": "Supreme Benefic (Guru/Teacher)",
        "gender": "Male",
        "element": "Ether",
        "own_signs": ["Sagittarius", "Pisces"],
        "exalted": {"sign": "Cancer", "deep_deg": 5.0},
        "debilitated": {"sign": "Capricorn", "deep_deg": 5.0},
        "moolatrikona": {"sign": "Sagittarius", "start": 0.0, "end": 10.0},
        "friends": ["Sun", "Moon", "Mars"],
        "neutral": ["Saturn"],
        "enemies": ["Mercury", "Venus"],
        "gemstone": "Yellow Sapphire (Pukhraj)",
        "metal": "Gold",
        "day": "Thursday",
        "color": "Bright Yellow / Golden",
        "mantra": "Om Gram Greem Groum Sah Gurave Namah",
        "dasha_years": 16,
    },
    "Venus": {
        "sanskrit": "Shukra (शुक्र)",
        "nature": "Natural Benefic (Minister/Artist)",
        "gender": "Female",
        "element": "Water",
        "own_signs": ["Taurus", "Libra"],
        "exalted": {"sign": "Pisces", "deep_deg": 27.0},
        "debilitated": {"sign": "Virgo", "deep_deg": 27.0},
        "moolatrikona": {"sign": "Libra", "start": 0.0, "end": 15.0},
        "friends": ["Mercury", "Saturn", "Rahu", "Ketu"],
        "neutral": ["Mars", "Jupiter"],
        "enemies": ["Sun", "Moon"],
        "gemstone": "Diamond (Heera) / White Zircon",
        "metal": "Silver / Platinum",
        "day": "Friday",
        "color": "Diamond White / Pink",
        "mantra": "Om Dram Dreem Droum Sah Shukraya Namah",
        "dasha_years": 20,
    },
    "Saturn": {
        "sanskrit": "Shani (शनि)",
        "nature": "Natural Malefic (Judge of Karma)",
        "gender": "Neutral",
        "element": "Air",
        "own_signs": ["Capricorn", "Aquarius"],
        "exalted": {"sign": "Libra", "deep_deg": 20.0},
        "debilitated": {"sign": "Aries", "deep_deg": 20.0},
        "moolatrikona": {"sign": "Aquarius", "start": 0.0, "end": 20.0},
        "friends": ["Mercury", "Venus", "Rahu"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars", "Ketu"],
        "gemstone": "Blue Sapphire (Neelam)",
        "metal": "Iron",
        "day": "Saturday",
        "color": "Royal Blue / Black",
        "mantra": "Om Pram Preem Proum Sah Shanaishcharaya Namah",
        "dasha_years": 19,
    },
    "Rahu": {
        "sanskrit": "Rahu (राहु - North Node)",
        "nature": "Shadow Planet / Malefic (Desire & Illusion)",
        "gender": "Female / Neutral",
        "element": "Air",
        "own_signs": ["Aquarius"],
        "exalted": {"sign": "Taurus", "deep_deg": 15.0},
        "debilitated": {"sign": "Scorpio", "deep_deg": 15.0},
        "moolatrikona": {"sign": "Gemini", "start": 0.0, "end": 30.0},
        "friends": ["Venus", "Saturn", "Mercury"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"],
        "gemstone": "Hessonite Garnet (Gomed)",
        "metal": "Alloy / Lead",
        "day": "Saturday",
        "color": "Smoky Blue / Charcoal",
        "mantra": "Om Bhram Bhreem Bhroum Sah Rahave Namah",
        "dasha_years": 18,
    },
    "Ketu": {
        "sanskrit": "Ketu (केतु - South Node)",
        "nature": "Shadow Planet / Malefic (Moksha & Detachment)",
        "gender": "Neutral",
        "element": "Fire",
        "own_signs": ["Scorpio"],
        "exalted": {"sign": "Scorpio", "deep_deg": 15.0},
        "debilitated": {"sign": "Taurus", "deep_deg": 15.0},
        "moolatrikona": {"sign": "Sagittarius", "start": 0.0, "end": 30.0},
        "friends": ["Venus", "Saturn", "Mercury"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"],
        "gemstone": "Cat's Eye (Lehsuniya)",
        "metal": "Alloy",
        "day": "Tuesday",
        "color": "Smoky Grey / Multi-color",
        "mantra": "Om Stram Streem Stroum Sah Ketave Namah",
        "dasha_years": 7,
    },
}

# Vimshottari Dasha sequence and planetary period length (Total = 120 years)
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# 27 Yogas in Panchang
PANCHANG_YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Asiddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

# 11 Karanas in Panchang
KARANAS_MOVABLE = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti (Bhadra)"]
KARANAS_FIXED = {
    1: "Kimstughna",
    58: "Shakuni",
    59: "Chatushpada",
    60: "Naga"
}

# Tithis (1 to 15 for each paksha)
TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Purnima / Amavasya"
]

# Days of the week (Vara)
VARAS = [
    {"name": "Monday", "sanskrit": "Somavara (सोमवार)", "ruler": "Moon"},
    {"name": "Tuesday", "sanskrit": "Mangalavara (मंगलवार)", "ruler": "Mars"},
    {"name": "Wednesday", "sanskrit": "Budhavara (बुधवार)", "ruler": "Mercury"},
    {"name": "Thursday", "sanskrit": "Guruvara (गुरुवार)", "ruler": "Jupiter"},
    {"name": "Friday", "sanskrit": "Shukravara (शुक्रवार)", "ruler": "Venus"},
    {"name": "Saturday", "sanskrit": "Shanivara (शनिवार)", "ruler": "Saturn"},
    {"name": "Sunday", "sanskrit": "Ravivara (रविवार)", "ruler": "Sun"},
]

# Numerology letter mappings
# Chaldean System (Ancient & Vedic Cheiro system - 1 to 8, 9 is omitted for single letters)
CHALDEAN_MAP: Dict[str, int] = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

# Pythagorean System (1 to 9)
PYTHAGOREAN_MAP: Dict[str, int] = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

# Numerology 1-9 Planetary & Characteristic associations
NUMEROLOGY_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {
        "ruler": "Sun (Surya)",
        "title": "The Leader & Innovator",
        "archetype": "Independent, authoritative, ambitious, and visionary.",
        "strengths": ["Leadership", "Self-confidence", "Originality", "Strong willpower", "Courage"],
        "weaknesses": ["Egoism", "Impatience", "Domineering tendency", "Intolerance"],
        "lucky_numbers": [1, 2, 3, 9],
        "friendly_numbers": [1, 2, 3, 4, 7, 9],
        "neutral_numbers": [5],
        "enemy_numbers": [6, 8],
        "lucky_colors": ["Golden Yellow", "Orange", "Copper", "Crimson"],
        "lucky_days": ["Sunday", "Monday"],
        "gemstone": "Ruby (Manikya)",
        "deity": "Surya Dev",
        "favorable_careers": ["Entrepreneur", "Executive", "Government Official", "Surgeon", "Director", "Politician"]
    },
    2: {
        "ruler": "Moon (Chandra)",
        "title": "The Peacemaker & Empath",
        "archetype": "Diplomatic, intuitive, nurturing, artistic, and cooperative.",
        "strengths": ["Empathy", "Diplomacy", "Imagination", "Patience", "Artistic perception"],
        "weaknesses": ["Oversensitivity", "Mood swings", "Indecision", "Self-doubt"],
        "lucky_numbers": [1, 2, 7],
        "friendly_numbers": [1, 2, 3, 7],
        "neutral_numbers": [4, 6],
        "enemy_numbers": [8, 9],
        "lucky_colors": ["White", "Cream", "Silver", "Light Green"],
        "lucky_days": ["Monday", "Sunday"],
        "gemstone": "Natural Pearl (Moti)",
        "deity": "Chandra Dev / Goddess Parvati",
        "favorable_careers": ["Diplomat", "Psychologist", "Writer", "Nurse / Doctor", "Artist", "Teacher"]
    },
    3: {
        "ruler": "Jupiter (Guru / Brihaspati)",
        "title": "The Mentor & Creator",
        "archetype": "Wise, optimistic, communicative, philosophical, and inspiring.",
        "strengths": ["Wisdom", "Communication", "Enthusiasm", "Integrity", "Generosity"],
        "weaknesses": ["Over-optimism", "Scattering energies", "Self-indulgence", "Critical nature"],
        "lucky_numbers": [1, 3, 5, 9],
        "friendly_numbers": [1, 2, 3, 9],
        "neutral_numbers": [5, 7],
        "enemy_numbers": [6],
        "lucky_colors": ["Bright Yellow", "Saffron", "Golden", "Amber"],
        "lucky_days": ["Thursday", "Tuesday", "Sunday"],
        "gemstone": "Yellow Sapphire (Pukhraj)",
        "deity": "Lord Brihaspati / Lord Shiva",
        "favorable_careers": ["Professor", "Advisor", "Lawyer", "Author", "Spiritual Teacher", "Publisher"]
    },
    4: {
        "ruler": "Rahu (North Node)",
        "title": "The Architect & Revolutionist",
        "archetype": "Practical, unconventional, methodical, determined, and rebellious against obsolete dogma.",
        "strengths": ["Structure", "Analytical capability", "Breakthrough thinking", "Loyalty", "Resilience"],
        "weaknesses": ["Stubbornness", "Secretiveness", "Sudden anger", "Pessimism"],
        "lucky_numbers": [1, 4, 5, 6],
        "friendly_numbers": [1, 5, 6, 7],
        "neutral_numbers": [2, 8],
        "enemy_numbers": [3, 9],
        "lucky_colors": ["Electric Blue", "Grey", "Khaki", "Steel"],
        "lucky_days": ["Saturday", "Sunday", "Monday"],
        "gemstone": "Hessonite Garnet (Gomed)",
        "deity": "Lord Bhairava / Goddess Durga",
        "favorable_careers": ["Software Architect", "Engineer", "Scientist", "Aviation", "Detective", "Civil Planner"]
    },
    5: {
        "ruler": "Mercury (Budha)",
        "title": "The Communicator & Catalyst",
        "archetype": "Quick-witted, versatile, adaptable, analytical, and commercially gifted.",
        "strengths": ["Agility", "Commercial intelligence", "Charming speech", "Resourcefulness", "Curiosity"],
        "weaknesses": ["Restlessness", "Nervous tension", "Inconsistency", "Gambling instinct"],
        "lucky_numbers": [1, 5, 6],
        "friendly_numbers": [1, 3, 4, 5, 6, 7, 8],
        "neutral_numbers": [9],
        "enemy_numbers": [2],
        "lucky_colors": ["Emerald Green", "Turquoise", "Light Ash"],
        "lucky_days": ["Wednesday", "Friday"],
        "gemstone": "Emerald (Panna)",
        "deity": "Lord Budha / Lord Vishnu",
        "favorable_careers": ["Trader / Financier", "Journalist", "Public Speaker", "Marketing Strategist", "Data Analyst"]
    },
    6: {
        "ruler": "Venus (Shukra)",
        "title": "The Harmonizer & Esthete",
        "archetype": "Compassionate, refined, loving, aesthetic, and family-oriented.",
        "strengths": ["Artistic grace", "Magnanimity", "Harmonizing relationships", "Luxury consciousness", "Devotion"],
        "weaknesses": ["Possessiveness", "Over-attachment", "Extravagance", "Sensory indulgence"],
        "lucky_numbers": [5, 6, 7],
        "friendly_numbers": [1, 4, 5, 6, 7, 8],
        "neutral_numbers": [2],
        "enemy_numbers": [3],
        "lucky_colors": ["White", "Pastel Pink", "Sky Blue", "Silver"],
        "lucky_days": ["Friday", "Wednesday"],
        "gemstone": "Diamond / White Sapphire / Opal",
        "deity": "Goddess Lakshmi",
        "favorable_careers": ["Designer", "Architect", "Actor / Musician", "Hospitality", "Cosmetics", "Jeweler"]
    },
    7: {
        "ruler": "Ketu (South Node)",
        "title": "The Mystic & Thinker",
        "archetype": "Introspective, spiritual, research-driven, philosophical, and penetratingly intuitive.",
        "strengths": ["Intuition", "Philosophical depth", "Research acumen", "Independence", "Mystic vision"],
        "weaknesses": ["Aloofness", "Melancholy", "Difficulty expressing emotions", "Skepticism"],
        "lucky_numbers": [1, 2, 7],
        "friendly_numbers": [1, 2, 4, 5, 7],
        "neutral_numbers": [3, 6, 8],
        "enemy_numbers": [9],
        "lucky_colors": ["Light Green", "White", "Pale Yellow", "Sea Green"],
        "lucky_days": ["Sunday", "Monday", "Wednesday"],
        "gemstone": "Cat's Eye (Lehsuniya)",
        "deity": "Lord Ganesha",
        "favorable_careers": ["Researcher", "Spiritual Guru", "Data Scientist", "Astrologer", "Philosopher", "Surgeon"]
    },
    8: {
        "ruler": "Saturn (Shani)",
        "title": "The Master of Karma & Authority",
        "archetype": "Disciplined, hardworking, realistic, enduring, and spiritually profound through trials.",
        "strengths": ["Perseverance", "Organizational power", "Justice-oriented", "Patience", "Pragmatism"],
        "weaknesses": ["Rigidity", "Cynicism", "Delayed gratification frustration", "Isolation"],
        "lucky_numbers": [3, 5, 6, 8],
        "friendly_numbers": [3, 4, 5, 6, 7],
        "neutral_numbers": [],
        "enemy_numbers": [1, 2, 9],
        "lucky_colors": ["Dark Blue", "Navy", "Black", "Dark Violet"],
        "lucky_days": ["Saturday", "Wednesday", "Friday"],
        "gemstone": "Blue Sapphire (Neelam)",
        "deity": "Lord Shani / Lord Shiva / Hanuman Ji",
        "favorable_careers": ["Judge / Magistrate", "Industrialist", "Mining / Real Estate", "Auditor", "Administrator"]
    },
    9: {
        "ruler": "Mars (Mangala)",
        "title": "The Warrior & Humanitarian",
        "archetype": "Dynamic, courageous, passionate, fiercely loyal, and protective.",
        "strengths": ["Courage", "High vitality", "Humanitarian compassion", "Leadership in crisis", "Honesty"],
        "weaknesses": ["Quick temper", "Recklessness", "Aggression", "Impulsive decisions"],
        "lucky_numbers": [1, 2, 3, 9],
        "friendly_numbers": [1, 2, 3, 9],
        "neutral_numbers": [5],
        "enemy_numbers": [4, 7, 8],
        "lucky_colors": ["Crimson Red", "Maroon", "Rose", "Coral"],
        "lucky_days": ["Tuesday", "Thursday", "Sunday"],
        "gemstone": "Red Coral (Moonga)",
        "deity": "Lord Kartikeya (Murugan) / Hanuman Ji",
        "favorable_careers": ["Military / Defense", "Sports Champion", "Surgeon", "Civil Engineer", "Emergency Responder"]
    }
}
