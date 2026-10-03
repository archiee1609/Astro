"""
core/numerology.py - Vedic Numerology (Sankhya Shastra) and Chaldean Engine
Calculates Mulank (Birth No.), Bhagyank (Destiny No.), Namank (Chaldean & Pythagorean),
Soul Urge, Personality, compatibility harmony, and personalized life guidance.
"""

import re
from datetime import date
from typing import Dict, Any, List, Tuple
from core.constants import (
    CHALDEAN_MAP, PYTHAGOREAN_MAP, NUMEROLOGY_PROFILES
)

class NumerologyEngine:
    @staticmethod
    def reduce_to_single_digit(num: int, keep_master: bool = False) -> int:
        """Reduces any positive integer to a single digit 1-9 (or 11/22/33 if keep_master is True)."""
        while num > 9:
            if keep_master and num in (11, 22, 33):
                return num
            num = sum(int(d) for d in str(num))
        return num

    @classmethod
    def calculate_mulank(cls, birth_date: date) -> Dict[str, Any]:
        """
        Calculates Mulank (Psychic / Birth Number) from the day of birth (1-31).
        Represents inner nature, daily mindset, and subconscious instincts.
        """
        day = birth_date.day
        root_num = cls.reduce_to_single_digit(day)
        profile = NUMEROLOGY_PROFILES[root_num]

        return {
            "day_of_birth": day,
            "mulank": root_num,
            "compound_num": day,
            "ruler": profile["ruler"],
            "title": profile["title"],
            "archetype": profile["archetype"],
            "strengths": profile["strengths"],
            "weaknesses": profile["weaknesses"],
            "lucky_numbers": profile["lucky_numbers"],
            "lucky_colors": profile["lucky_colors"],
            "lucky_days": profile["lucky_days"],
            "gemstone": profile["gemstone"],
            "deity": profile["deity"],
            "favorable_careers": profile["favorable_careers"]
        }

    @classmethod
    def calculate_bhagyank(cls, birth_date: date) -> Dict[str, Any]:
        """
        Calculates Bhagyank (Destiny / Life Path Number) from Day + Month + Year.
        Represents life mission, ultimate potential, and karmic trajectory.
        """
        day_sum = sum(int(d) for d in str(birth_date.day))
        month_sum = sum(int(d) for d in str(birth_date.month))
        year_sum = sum(int(d) for d in str(birth_date.year))

        total_sum = day_sum + month_sum + year_sum
        root_num = cls.reduce_to_single_digit(total_sum)
        master_val = cls.reduce_to_single_digit(total_sum, keep_master=True)
        profile = NUMEROLOGY_PROFILES[root_num]

        return {
            "total_sum": total_sum,
            "bhagyank": root_num,
            "master_number": master_val if master_val in (11, 22, 33) else None,
            "ruler": profile["ruler"],
            "title": profile["title"],
            "archetype": profile["archetype"],
            "life_purpose": f"To master the qualities of {profile['ruler']}: embodying {', '.join(profile['strengths'][:3])}.",
            "lucky_numbers": profile["lucky_numbers"],
            "lucky_colors": profile["lucky_colors"],
            "lucky_days": profile["lucky_days"],
            "gemstone": profile["gemstone"]
        }

    @classmethod
    def calculate_namank(cls, full_name: str) -> Dict[str, Any]:
        """
        Calculates Chaldean and Pythagorean Namank (Name Number),
        Soul Urge (Vowels), and Personality (Consonants).
        """
        cleaned_name = re.sub(r'[^A-Za-z]', '', full_name).upper()
        words = re.findall(r'[A-Za-z]+', full_name.upper())

        # 1. Chaldean Name Calculation
        chaldean_compound = 0
        word_chaldean_breakdown = []
        for word in words:
            word_val = sum(CHALDEAN_MAP.get(char, 0) for char in word)
            word_chaldean_breakdown.append({
                "word": word,
                "value": word_val,
                "letters": [{"char": c, "val": CHALDEAN_MAP.get(c, 0)} for c in word]
            })
            chaldean_compound += word_val

        chaldean_root = cls.reduce_to_single_digit(chaldean_compound)
        chaldean_profile = NUMEROLOGY_PROFILES.get(chaldean_root, NUMEROLOGY_PROFILES[1])

        # 2. Pythagorean Name Calculation
        pythagorean_compound = sum(PYTHAGOREAN_MAP.get(char, 0) for char in cleaned_name)
        pythagorean_root = cls.reduce_to_single_digit(pythagorean_compound)

        # 3. Soul Urge (Vowels only: A, E, I, O, U)
        vowels = set("AEIOU")
        vowel_chars = [c for c in cleaned_name if c in vowels]
        soul_urge_compound = sum(CHALDEAN_MAP.get(c, 0) for c in vowel_chars)
        soul_urge_root = cls.reduce_to_single_digit(soul_urge_compound) if vowel_chars else 0

        # 4. Personality (Consonants only)
        consonant_chars = [c for c in cleaned_name if c not in vowels]
        personality_compound = sum(CHALDEAN_MAP.get(c, 0) for c in consonant_chars)
        personality_root = cls.reduce_to_single_digit(personality_compound) if consonant_chars else 0

        # Cheiro Compound Number Meanings
        compound_meaning = cls.get_compound_meaning(chaldean_compound)

        return {
            "full_name": full_name,
            "cleaned_name": cleaned_name,
            "chaldean": {
                "compound_number": chaldean_compound,
                "namank": chaldean_root,
                "ruler": chaldean_profile["ruler"],
                "meaning": compound_meaning,
                "word_breakdown": word_chaldean_breakdown
            },
            "pythagorean": {
                "compound_number": pythagorean_compound,
                "namank": pythagorean_root,
            },
            "soul_urge": {
                "number": soul_urge_root,
                "compound": soul_urge_compound,
                "vowels_found": "".join(vowel_chars),
                "meaning": "Heart's deep inner calling and subconscious emotional cravings."
            },
            "personality": {
                "number": personality_root,
                "compound": personality_compound,
                "meaning": "Outer persona, first impressions, and magnetic presentation."
            }
        }

    @classmethod
    def evaluate_compatibility(
        cls, mulank: int, bhagyank: int, namank: int
    ) -> Dict[str, Any]:
        """
        Evaluates the tripartite harmony between Psychic Number (Mulank),
        Destiny Number (Bhagyank), and Name Number (Namank).
        """
        mul_prof = NUMEROLOGY_PROFILES.get(mulank, NUMEROLOGY_PROFILES[1])
        bhag_prof = NUMEROLOGY_PROFILES.get(bhagyank, NUMEROLOGY_PROFILES[1])

        # Check Mulank vs Bhagyank
        if bhagyank in mul_prof["friendly_numbers"]:
            mb_status = "Harmonious (Mitra)"
            mb_score = 90
        elif bhagyank in mul_prof["enemy_numbers"]:
            mb_status = "Challenging / Inimical (Shatru)"
            mb_score = 45
        else:
            mb_status = "Neutral (Sama)"
            mb_score = 70

        # Check Namank vs Mulank
        if namank in mul_prof["friendly_numbers"]:
            nm_status = "Harmonious"
            nm_score = 95
        elif namank in mul_prof["enemy_numbers"]:
            nm_status = "Inharmonious (Friction with inner self)"
            nm_score = 40
        else:
            nm_status = "Neutral"
            nm_score = 75

        # Check Namank vs Bhagyank
        if namank in bhag_prof["friendly_numbers"]:
            nb_status = "Harmonious (Boosts Life Destiny)"
            nb_score = 95
        elif namank in bhag_prof["enemy_numbers"]:
            nb_status = "Inharmonious (Resists Destiny Flow)"
            nb_score = 40
        else:
            nb_status = "Neutral"
            nb_score = 75

        total_harmony_score = round((mb_score + nm_score + nb_score) / 3.0)

        recommendation = ""
        if total_harmony_score >= 80:
            recommendation = "Excellent harmony! Your Name Number naturally amplifies both your innate personality (Mulank) and karmic path (Bhagyank)."
        elif total_harmony_score >= 65:
            recommendation = "Good overall alignment. Minor adjustments in spelling could elevate your vibration to supreme resonance, but current setup is supportive."
        else:
            favorable_targets = list(set(mul_prof["friendly_numbers"]) & set(bhag_prof["friendly_numbers"]))
            fav_str = ", ".join(str(n) for n in favorable_targets) if favorable_targets else "5, 6, 1"
            recommendation = (
                f"Noticeable friction detected between your Name Number ({namank}) and core birth numbers. "
                f"In traditional Sankhya Shastra, tuning the spelling of the name to resonate with Number {fav_str} brings smoother success and reduces friction."
            )

        return {
            "harmony_score": total_harmony_score,
            "mulank_vs_bhagyank": mb_status,
            "namank_vs_mulank": nm_status,
            "namank_vs_bhagyank": nb_status,
            "recommendation": recommendation
        }

    @staticmethod
    def get_compound_meaning(num: int) -> str:
        """Returns traditional Cheiro meanings for common Chaldean compound numbers."""
        meanings = {
            10: "Wheel of Fortune: Honor, self-confidence, creative power, success in undertakings.",
            14: "Movement and Combination: Adaptability, commercial enterprise, caution with speculative risks.",
            15: "Magical Charisma: Magnetism, artistic charm, eloquence, mastery of luxury.",
            19: "Prince of Heaven: Highly fortunate number of success, honor, and victory.",
            21: "Crown of the Magi: Great advancement, elevation, victory achieved after patient endurance.",
            23: "Royal Star of the Lion: Outstandingly fortunate number promising success, protection, and leadership.",
            24: "Help from Elevated Ranks: Prosperity, assistance from powerful superiors, enduring love.",
            27: "The Scepter: Command, creative intellect, high literary/spiritual honors.",
            28: "Trusting Nature: Great capability, warning to secure contracts and select honest associates.",
            32: "Magnetic Communications: Extraordinary speaking and writing ability, international recognition.",
            33: "Master Teacher / Spiritual Love: Deep spiritual elevation, supreme artistic or humanitarian devotion.",
            37: "Love and Good Fortune: Harmonious partnerships, creative talent, steady financial fortune.",
            41: "Dynamic Action: Leadership, swift intellect, resilience through challenges.",
            42: "Grace and Wisdom: Artistic, gentle, blessed by social affection and peace.",
            45: "Master of Enterprise: Practical builder, organizational command, commercial triumphs.",
            51: "Warrior's Victory: Tremendous willpower, overcoming adversaries, bold originality."
        }
        return meanings.get(num, f"Compound vibration {num}: Combines individual numerical components into unique creative and karmic momentum.")
