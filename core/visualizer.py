"""
core/visualizer.py - Vedic Chart Visualizer
Generates North Indian Diamond and South Indian Square Kundali
in both Unicode Text (for CLI) and SVG Vector Graphics (for Web UI).
"""

from typing import Dict, Any, List
from core.constants import SIGN_NAMES

PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra",
    "Ketu": "Ke", "Ascendant": "Asc"
}

class ChartVisualizer:
    @staticmethod
    def get_house_contents(grahas: Dict[str, Any], lagna_data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """
        Organizes planets and signs by house number (1 to 12).
        """
        lagna_sign_idx = SIGN_NAMES.index(lagna_data["lagna_sign"])
        houses = {}

        for h in range(1, 13):
            sign_idx = (lagna_sign_idx + h - 1) % 12
            houses[h] = {
                "house_num": h,
                "sign_num": sign_idx + 1,
                "sign_name": SIGN_NAMES[sign_idx],
                "planets": []
            }

        # Add Lagna mark to house 1
        houses[1]["planets"].append(f"Asc ({lagna_data['lagna_deg_formatted'].split()[0]})")

        # Add planets
        for name, data in grahas.items():
            h_num = data["house"]
            abbr = PLANET_ABBR.get(name, name[:2])
            tags = ""
            if data.get("is_retrograde") and name not in ("Rahu", "Ketu"):
                tags += "(R)"
            if data.get("is_combust"):
                tags += "(c)"
            deg_int = int(data["sign_deg"])
            houses[h_num]["planets"].append(f"{abbr}{tags}{deg_int}°")

        return houses

    @staticmethod
    def get_navamsha_house_contents(grahas: Dict[str, Any], lagna_data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """
        Organizes planets by Navamsha (D9) house relative to Navamsha Lagna.
        """
        nav_lagna_sign = lagna_data["lagna_navamsha_sign"]
        nav_lagna_idx = SIGN_NAMES.index(nav_lagna_sign)
        houses = {}

        for h in range(1, 13):
            sign_idx = (nav_lagna_idx + h - 1) % 12
            houses[h] = {
                "house_num": h,
                "sign_num": sign_idx + 1,
                "sign_name": SIGN_NAMES[sign_idx],
                "planets": []
            }

        houses[1]["planets"].append("Asc")

        for name, data in grahas.items():
            nav_sign = data["navamsha_sign"]
            nav_sign_idx = SIGN_NAMES.index(nav_sign)
            h_num = (nav_sign_idx - nav_lagna_idx) % 12 + 1
            abbr = PLANET_ABBR.get(name, name[:2])
            houses[h_num]["planets"].append(abbr)

        return houses

    @classmethod
    def generate_north_indian_svg(cls, houses: Dict[int, Dict[str, Any]], title: str = "D1 - Lagna Rashi Chart") -> str:
        """
        Generates an SVG vector graphic of the North Indian Diamond Kundali.
        Fixed house positions, signs labeled inside houses, planets listed.
        """
        # House centers / text anchor coordinates for 400x400 canvas
        # 1: Center diamond top (200, 100)
        # 2: Top left triangle (100, 50)
        # 3: Left upper triangle (50, 100)
        # 4: Left diamond (100, 200)
        # 5: Left lower triangle (50, 300)
        # 6: Bottom left triangle (100, 350)
        # 7: Bottom diamond (200, 300)
        # 8: Bottom right triangle (300, 350)
        # 9: Right lower triangle (350, 300)
        # 10: Right diamond (300, 200)
        # 11: Right upper triangle (350, 100)
        # 12: Top right triangle (300, 50)
        house_pos = {
            1: (200, 120, 200, 75),
            2: (115, 65, 140, 45),
            3: (55, 115, 45, 140),
            4: (115, 200, 75, 200),
            5: (55, 285, 45, 260),
            6: (115, 335, 140, 355),
            7: (200, 280, 200, 325),
            8: (285, 335, 260, 355),
            9: (345, 285, 355, 260),
            10: (285, 200, 325, 200),
            11: (345, 115, 355, 140),
            12: (285, 65, 260, 45)
        }

        svg_elements = []
        # Definitions for gradients and shadows
        svg_elements.append("""<defs>
<radialGradient id="celestialBg" cx="50%" cy="50%" r="70%">
<stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.95"/>
<stop offset="60%" stop-color="#0f172a" stop-opacity="0.98"/>
<stop offset="100%" stop-color="#090d16" stop-opacity="1"/>
</radialGradient>
<linearGradient id="goldStroke" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#fbbf24"/>
<stop offset="50%" stop-color="#f59e0b"/>
<stop offset="100%" stop-color="#d97706"/>
</linearGradient>
</defs>
<rect x="8" y="8" width="384" height="384" fill="url(#celestialBg)" stroke="url(#goldStroke)" stroke-width="2.5" rx="10"/>
<polygon points="200,10 390,200 200,390 10,200" fill="rgba(245, 158, 11, 0.05)" stroke="url(#goldStroke)" stroke-width="2"/>
<line x1="10" y1="10" x2="390" y2="390" stroke="#f59e0b" stroke-opacity="0.6" stroke-width="1.6"/>
<line x1="390" y1="10" x2="10" y2="390" stroke="#f59e0b" stroke-opacity="0.6" stroke-width="1.6"/>
<circle cx="200" cy="200" r="4" fill="#fbbf24" opacity="0.6"/>""")

        # Add Title banner with Om
        svg_elements.append(f"""<text x="200" y="32" font-family="'Cinzel', Georgia, serif" font-size="12" font-weight="700" fill="#fbbf24" text-anchor="middle" letter-spacing="1">ॐ {title} ॐ</text>""")

        # Place sign numbers and planets in houses
        for h, (px, py, sx, sy) in house_pos.items():
            h_data = houses[h]
            sign_num = h_data["sign_num"]
            planets_str = " ".join(h_data["planets"])
            
            # Sign number in glowing saffron/gold
            svg_elements.append(
                f'<text x="{sx}" y="{sy}" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#f59e0b" text-anchor="middle">{sign_num}</text>'
            )

            # Planets in luminous celestial white with bold styling
            if planets_str:
                parts = h_data["planets"]
                if len(parts) <= 2:
                    svg_elements.append(
                        f'<text x="{px}" y="{py}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">{" ".join(parts)}</text>'
                    )
                else:
                    line1 = " ".join(parts[:2])
                    line2 = " ".join(parts[2:])
                    svg_elements.append(
                        f'<text x="{px}" y="{py - 7}" font-family="sans-serif" font-size="10" font-weight="bold" fill="#f8fafc" text-anchor="middle">{line1}</text>'
                        f'<text x="{px}" y="{py + 8}" font-family="sans-serif" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">{line2}</text>'
                    )

        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">{"".join(svg_elements)}</svg>'
        return svg_content

    @classmethod
    def generate_south_indian_svg(cls, houses: Dict[int, Dict[str, Any]], title: str = "D1 - South Indian Kundali") -> str:
        """
        Generates an SVG vector graphic of the classical South Indian Square Kundali.
        Fixed zodiac sign boxes arranged clockwise from top-left (Pisces at 0,0).
        """
        # Sign positions in 4x4 grid (sign_index 0=Aries ... 11=Pisces)
        # Sign 1 (Aries): row 0, col 1
        # Sign 2 (Taurus): row 0, col 2
        # Sign 3 (Gemini): row 0, col 3
        # Sign 4 (Cancer): row 1, col 3
        # Sign 5 (Leo): row 2, col 3
        # Sign 6 (Virgo): row 3, col 3
        # Sign 7 (Libra): row 3, col 2
        # Sign 8 (Scorpio): row 3, col 1
        # Sign 9 (Sagittarius): row 3, col 0
        # Sign 10 (Capricorn): row 2, col 0
        # Sign 11 (Aquarius): row 1, col 0
        # Sign 12 (Pisces): row 0, col 0
        sign_coords = {
            12: (10, 10), 1: (105, 10), 2: (200, 10), 3: (295, 10),
            4: (295, 105), 5: (295, 200),
            6: (295, 295), 7: (200, 295), 8: (105, 295), 9: (10, 295),
            10: (10, 200), 11: (10, 105)
        }

        # Map planets from houses into signs
        sign_planets: Dict[int, List[str]] = {s: [] for s in range(1, 13)}
        lagna_sign_num = 1
        for h, h_data in houses.items():
            s_num = h_data["sign_num"]
            if h == 1:
                lagna_sign_num = s_num
            for p in h_data.get("planets", []):
                sign_planets[s_num].append(p)

        svg = []
        svg.append("""<defs>
<radialGradient id="siBg" cx="50%" cy="50%" r="70%">
<stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.95"/>
<stop offset="60%" stop-color="#0f172a" stop-opacity="0.98"/>
<stop offset="100%" stop-color="#090d16" stop-opacity="1"/>
</radialGradient>
<linearGradient id="siGold" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#fbbf24"/>
<stop offset="50%" stop-color="#f59e0b"/>
<stop offset="100%" stop-color="#d97706"/>
</linearGradient>
</defs>
<rect x="8" y="8" width="384" height="384" fill="url(#siBg)" stroke="url(#siGold)" stroke-width="2.5" rx="8"/>
<rect x="105" y="105" width="190" height="190" fill="rgba(245, 158, 11, 0.05)" stroke="url(#siGold)" stroke-width="1.8"/>""")

        # Draw grid dividing lines
        for offset in [105, 200, 295]:
            svg.append(f'<line x1="{offset}" y1="8" x2="{offset}" y2="105" stroke="#f59e0b" stroke-opacity="0.5" stroke-width="1.2"/>')
            svg.append(f'<line x1="{offset}" y1="295" x2="{offset}" y2="392" stroke="#f59e0b" stroke-opacity="0.5" stroke-width="1.2"/>')
            svg.append(f'<line x1="8" y1="{offset}" x2="105" y2="{offset}" stroke="#f59e0b" stroke-opacity="0.5" stroke-width="1.2"/>')
            svg.append(f'<line x1="295" y1="{offset}" x2="392" y2="{offset}" stroke="#f59e0b" stroke-opacity="0.5" stroke-width="1.2"/>')

        # Center title
        svg.append(f'<text x="200" y="185" font-family="\'Cinzel\', serif" font-size="13" font-weight="700" fill="#fbbf24" text-anchor="middle">ॐ {title} ॐ</text>')
        svg.append(f'<text x="200" y="210" font-family="sans-serif" font-size="11" fill="#94a3b8" text-anchor="middle">Lagna: Sign {lagna_sign_num}</text>')

        # Populate signs
        for s_num, (x, y) in sign_coords.items():
            is_lagna = (s_num == lagna_sign_num)
            if is_lagna:
                # Diagonal slash across sign box for Lagna
                svg.append(f'<line x1="{x+2}" y1="{y+2}" x2="{x+93}" y2="{y+93}" stroke="#f59e0b" stroke-opacity="0.3" stroke-width="1"/>')
                svg.append(f'<text x="{x+8}" y="{y+18}" font-family="sans-serif" font-size="10" font-weight="bold" fill="#f59e0b">ASC</text>')

            p_list = sign_planets.get(s_num, [])
            # Filter out duplicate Asc if present
            disp_planets = [p for p in p_list if not p.startswith("Asc")]
            if is_lagna and not any(p.startswith("Asc") for p in p_list):
                disp_planets.insert(0, "Asc")

            if disp_planets:
                line_y = y + (28 if is_lagna else 22)
                for p_str in disp_planets[:3]:
                    svg.append(f'<text x="{x+47}" y="{line_y}" font-family="sans-serif" font-size="10" font-weight="bold" fill="#f8fafc" text-anchor="middle">{p_str}</text>')
                    line_y += 18

        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">{"".join(svg)}</svg>'

    @classmethod
    def generate_ascii_chart(cls, houses: Dict[int, Dict[str, Any]]) -> str:
        """
        Generates a clean text/ASCII representation of the Vedic Kundali for CLI.
        """
        lines = []
        lines.append("┌─────────────────────────────────────────────────────────────┐")
        lines.append("│                  VEDIC KUNDLI (D1 BHAVAS)                   │")
        lines.append("├──────────────────────────────┬──────────────────────────────┤")
        for h in range(1, 13):
            hd = houses[h]
            p_list = ", ".join(hd["planets"]) if hd["planets"] else "Empty"
            p_display = p_list if len(p_list) <= 39 else p_list[:36] + "..."
            lines.append(f"│ House {h:2d} ({hd['sign_name'][:8]:8}): {p_display:39s}│")
        lines.append("└──────────────────────────────┴──────────────────────────────┘")
        return "\n".join(lines)
