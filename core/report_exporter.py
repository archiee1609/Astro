"""
core/report_exporter.py - High Precision Report Generator & Exporter
Generates complete astrological and numerological reports in multiple formats:
1. Standalone, Print-to-PDF ready HTML Report with embedded SVGs and responsive styling.
2. Comprehensive, fully formatted Markdown (.md) Report with tables and ASCII charts.
3. Complete JSON Data Export (.json).
"""

import json
from typing import Dict, Any, List

class ReportExporter:
    @staticmethod
    def generate_json_report(report: Dict[str, Any]) -> str:
        """Serializes complete report dictionary into pretty-printed UTF-8 JSON."""
        return json.dumps(report, indent=2, ensure_ascii=False)

    @staticmethod
    def generate_markdown_report(report: Dict[str, Any]) -> str:
        """Generates a complete, publication-grade Markdown (.md) report."""
        user = report.get("user_input", {})
        astro = report.get("birth_astronomy", {})
        lagna = report.get("lagna", {})
        panchang = report.get("panchang", {})
        grahas = report.get("grahas", {})
        dashas = report.get("dashas", {})
        yogas = report.get("yogas_and_doshas", {})
        tl = report.get("timelines", {})
        num = report.get("numerology", {})
        guidance = report.get("guidance", {})
        charts = report.get("charts", {})
        transits = report.get("live_transits", {})

        md: List[str] = []

        # Header
        md.append(f"# ॐ VEDIC JYOTISH & SANKHYA SHASTRA COMPREHENSIVE REPORT ॐ")
        md.append(f"**High Precision Astrological & Numerological Analysis**  \n")
        md.append(f"*Calculated via NASA JPL DE421 Ephemeris & Chitrapaksha (Lahiri) Ayanamsha*\n")
        md.append("---\n")

        # 1. Subject & Astronomical Details
        md.append("## 1. Birth & Astronomical Coordinates\n")
        md.append("| Parameter | Value | Parameter | Value |")
        md.append("| :--- | :--- | :--- | :--- |")
        md.append(f"| **Full Name** | {user.get('full_name')} | **Place of Birth** | {user.get('place_of_birth')} |")
        md.append(f"| **Date of Birth** | {user.get('date_of_birth')} | **Resolved Location** | {astro.get('resolved_location')} |")
        md.append(f"| **Time of Birth** | {user.get('time_of_birth')} | **Latitude / Longitude** | {astro.get('latitude', 0):.4f}°, {astro.get('longitude', 0):.4f}° |")
        md.append(f"| **Timezone** | {astro.get('timezone')} | **UTC Offset** | {astro.get('utc_offset')} |")
        md.append(f"| **Lahiri Ayanamsha** | {astro.get('ayanamsha')} | **Ascendant (Lagna)** | {lagna.get('lagna_sign')} ({lagna.get('lagna_deg_formatted')}) |")
        md.append(f"| **Moon Sign (Rashi)** | {grahas.get('Moon', {}).get('sign')} ({grahas.get('Moon', {}).get('deg_formatted')}) | **Moon Nakshatra** | {grahas.get('Moon', {}).get('nakshatra')} (Pada {grahas.get('Moon', {}).get('nakshatra_pada')}) |")
        md.append(f"| **Sun Sign (Surya)** | {grahas.get('Sun', {}).get('sign')} ({grahas.get('Sun', {}).get('deg_formatted')}) | **Lagna Nakshatra** | {lagna.get('lagna_nakshatra')} (Lord: {lagna.get('lagna_nakshatra_lord')}) |\n")

        # 2. Panchanga
        md.append("## 2. Vedic Panchanga (Five Limbs of Time)\n")
        md.append("| Limb | Name / Sanskrit | Ruler / Deity | Classical Significance |")
        md.append("| :--- | :--- | :--- | :--- |")
        md.append(f"| **Vara (Day)** | {panchang.get('vara', {}).get('name')} ({panchang.get('vara', {}).get('sanskrit')}) | {panchang.get('vara', {}).get('lord')} | Vitality, health, and primary ruler of weekday energy |")
        md.append(f"| **Tithi (Lunar Day)** | {panchang.get('tithi', {}).get('name')} | {panchang.get('tithi', {}).get('paksha')} | Emotional constitution and mental relationship with society ({panchang.get('tithi', {}).get('completion_percent')}% complete) |")
        md.append(f"| **Nakshatra** | {panchang.get('nakshatra', {}).get('name')} (Pada {panchang.get('nakshatra', {}).get('pada')}) | {panchang.get('nakshatra', {}).get('lord')} / {panchang.get('nakshatra', {}).get('deity')} | Soul temperament, psychological predispositions, and dasha ruler |")
        md.append(f"| **Yoga** | {panchang.get('yoga', {}).get('name')} | {panchang.get('yoga', {}).get('nature')} | Solilunar harmony, bodily vitality, and karmic flow |")
        md.append(f"| **Karana** | {panchang.get('karana', {}).get('name')} (No. {panchang.get('karana', {}).get('number')}) | {'Vishti / Bhadra Alert' if panchang.get('karana', {}).get('is_bhadra') else 'Standard Auspicious'} | Capacity for material execution and worldly tasks |\n")

        # 3. Navagraha Positions
        md.append("## 3. Navagraha Planetary Positions (Sidereal Nirayana)\n")
        md.append("| Planet (Graha) | Sanskrit | Sign (Rashi) | Degrees | Nakshatra & Pada | D9 Navamsha | House | Dignity / Status |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        md.append(f"| **Ascendant (Lagna)** | Lagna Center | {lagna.get('lagna_sign')} | {lagna.get('lagna_deg_formatted')} | {lagna.get('lagna_nakshatra')} (P{lagna.get('lagna_nakshatra_pada')}) | {lagna.get('lagna_navamsha_sign')} | House 1 | Lagna Foundation |")
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            p = grahas.get(p_name, {})
            vkr = " [Vakri / Retro]" if p.get("is_retrograde") and p_name not in ("Rahu", "Ketu") else ""
            cst = " [Combust]" if p.get("is_combust") else ""
            status_desc = f"{p.get('dignity', 'Direct')}{vkr}{cst}"
            md.append(f"| **{p_name}** | {p.get('sanskrit', '').split()[0]} | {p.get('sign')} | {p.get('deg_formatted')} | {p.get('nakshatra')} (P{p.get('nakshatra_pada')}) | {p.get('navamsha_sign')} | House {p.get('house')} | {status_desc} |")
        md.append("")

        # 4. Kundali Charts
        md.append("## 4. Kundali Charts (D1 Rashi Bhavas)\n")
        md.append("```text")
        md.append(charts.get("ascii_chart", "Chart not available"))
        md.append("```\n")

        # 5. Yogas & Doshas
        md.append("## 5. Vedic Yogas & Doshas Analysis\n")
        m_info = yogas.get("manglik_dosha", {})
        s_info = yogas.get("sade_sati", {})
        k_info = yogas.get("kaal_sarp_dosha", {})
        b_yogas = yogas.get("benefic_yogas", [])

        md.append(f"### Manglik Dosha: {m_info.get('severity', 'None')}")
        md.append(f"- **Description:** {m_info.get('description')}")
        if m_info.get("cancellations"):
            md.append(f"- **Classical Vedic Cancellations:** {'; '.join(m_info['cancellations'])}")
        md.append("")

        md.append(f"### Shani Sade Sati: {s_info.get('phase', 'None')}")
        md.append(f"- **Description:** {s_info.get('description')}")
        md.append(f"- **Transit Saturn:** Currently in {s_info.get('transit_saturn_sign')} ({s_info.get('transit_saturn_deg')}°)\n")

        md.append(f"### Kaal Sarp Dosha: {k_info.get('severity', 'None')}")
        md.append(f"- **Description:** {k_info.get('description')}\n")

        md.append(f"### Auspicious Raja & Dhana Yogas ({len(b_yogas)} Active)")
        for y in b_yogas:
            md.append(f"- **{y.get('name')}**: {y.get('description')}")
        md.append("")

        # 6. Vimshottari Dasha
        md.append("## 6. Vimshottari Dasha Timeline\n")
        act_d = dashas.get("active_dasha", {})
        md.append(f"**Currently Active Running Dasha:** `{act_d.get('full_formatted', act_d.get('formatted'))}` (Active until {act_d.get('end_date')})  ")
        md.append(f"**Birth Dasha Balance:** `{dashas.get('balance_at_birth', {}).get('formatted')}`\n")
        md.append("| Mahadasha | Planetary Period Span | Total Duration | Active Status |")
        md.append("| :--- | :--- | :--- | :--- |")
        for md_item in dashas.get("timeline", []):
            is_cur = md_item.get("planet") == act_d.get("mahadasha")
            md.append(f"| **{md_item.get('planet')}** | {md_item.get('start_date')} → {md_item.get('end_date')} | {md_item.get('period_years')} Years | {'🌟 CURRENT RUNNING' if is_cur else 'Scheduled'} |")
        md.append("")

        # 7. Detailed Predictive Event Timeline & Life Milestones
        md.append("## 7. Detailed Timeline of Events & Life Milestones\n")
        act_sum = tl.get("active_period_summary", {})
        md.append("### Active Running Phase Deep-Dive (Today)")
        md.append(f"- **Current Dasha:** {act_sum.get('dasha')} ({act_sum.get('period')}, {act_sum.get('age')})")
        md.append(f"- **Dominant Life Theme:** {act_sum.get('dominant_theme')}")
        md.append(f"- **Career Status:** {act_sum.get('career_status')} — *{act_sum.get('career_recommendation')}*")
        md.append(f"- **Marriage & Love:** {act_sum.get('marriage_status')} — *{act_sum.get('marriage_recommendation')}*")
        md.append(f"- **Wealth & Finances:** {act_sum.get('wealth_status')} — *{act_sum.get('wealth_recommendation')}*")
        md.append(f"- **Health & Vitality:** {act_sum.get('health_status')} — *{act_sum.get('health_recommendation')}*\n")

        # Chronological Major Life Milestones
        milestones = tl.get("life_milestones", [])
        if milestones:
            md.append("### Chronological Major Predicted Life Milestones")
            md.append("| Dates & Age Window | Category | Milestone Event Title | Dasha | Favorability | Status |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for m in milestones:
                md.append(f"| {m.get('year_range')} ({m.get('age_window')}) | **{m.get('category')}** | {m.get('title')} | `{m.get('dasha')}` | {m.get('favorability_score')}% | {m.get('status_badge')} |")
            md.append("")

            md.append("#### Detailed Milestone Forecasts & Vedic Guidance")
            for m in milestones:
                md.append(f"#### ✦ {m.get('title')} ({m.get('year_range')}, {m.get('age_window')})")
                md.append(f"- **Category & Event Type:** {m.get('category')} • {m.get('event_type')}")
                md.append(f"- **Operating Dasha:** `{m.get('dasha')}` | **Favorability Rating:** {m.get('favorability_score')}% ({m.get('status_badge')})")
                md.append(f"- **Astrological Planetary Basis:** {m.get('astrological_basis')}")
                md.append(f"- **Prediction Narrative:** {m.get('prediction_narrative')}")
                md.append(f"- **Strategic Action Guidance:** {m.get('actionable_guidance')}")
                md.append(f"- **Prescribed Vedic Remedy:** {m.get('vedic_remedy')}\n")

        # Pratyantardasha Granular Calendar
        pds = tl.get("pratyantardashas", [])
        if pds:
            md.append("### Granular Pratyantardasha (Sub-Sub Period) Forecast")
            md.append("| Level 3 Dasha | Dates | Duration | Favorability | Focus Theme & Core Guidance |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for pd in pds:
                md.append(f"| **{pd.get('dasha_hierarchy')}** | {pd.get('start_date')} → {pd.get('end_date')} | {pd.get('duration_days')}d | {pd.get('favorability_score')}% ({pd.get('status_badge')}) | {pd.get('focus_theme')} *{pd.get('guidance')}* |")
            md.append("")

        # Annual 10-Year Forward Forecast
        annual = tl.get("annual_forecast", [])
        if annual:
            md.append("### Annual 10-Year Forward Forecast Roadmap")
            md.append("| Year (Age) | Dasha | Score | Primary Theme | Key Strategic Guidance |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for af in annual:
                md.append(f"| **{af.get('year')}** (Age {af.get('age_at_midyear')}) | `{af.get('dasha')}` | {af.get('overall_score')}% | {af.get('primary_theme')} | {af.get('key_recommendation')} |")
            md.append("")

        # 8. Pillar Timelines
        md.append("## 8. Specific Domain Trajectories (Career • Marriage • Wealth • Health)\n")
        # Career
        c_tl = tl.get("career", {})
        md.append(f"### Career & Professional Trajectory (10th Lord: {c_tl.get('tenth_lord')})")
        for c in c_tl.get("timeline", [])[:6]:
            md.append(f"- **{c.get('period')} ({c.get('age_display')} - {c.get('dasha')}):** {c.get('phase_type')} (Score: {c.get('score')}%)  \n  *Drivers:* {'; '.join(c.get('drivers', []))}  \n  *Advice:* {c.get('recommendation')}")
        md.append("")

        # Marriage
        m_tl = tl.get("marriage", {})
        md.append(f"### Marriage & Relationships (7th Lord: {m_tl.get('seventh_lord')}, 7th Sign: {m_tl.get('seventh_sign')})")
        sp = m_tl.get("spouse_profile", {})
        md.append(f"- **Spouse Core Temperament:** {sp.get('core_temperament')}")
        md.append(f"- **Spouse Career Affinity:** {sp.get('likely_career_affinity')}")
        md.append(f"- **Meeting Circumstances:** {sp.get('meeting_circumstances')}")
        for m_ev in m_tl.get("prime_marriage_windows", []):
            md.append(f"- **{m_ev.get('favorability')}:** {m_ev.get('period')} ({m_ev.get('age_range')} - {m_ev.get('dasha')}) — Score: {m_ev.get('score')}%")
        md.append("")

        # Wealth
        w_tl = tl.get("wealth", {})
        md.append("### Wealth & Asset Accumulation")
        for w in w_tl.get("timeline", [])[:6]:
            md.append(f"- **{w.get('period')} ({w.get('age_display')} - {w.get('dasha')}):** {w.get('phase_type')} (Score: {w.get('score')}%)  \n  *Advice:* {w.get('recommendation')}")
        md.append("")

        # Health
        h_tl = tl.get("health", {})
        md.append("### Physical Health & Anatomical Vulnerabilities")
        for v in h_tl.get("vulnerabilities", []):
            md.append(f"- {v}")
        for h in h_tl.get("timeline", [])[:6]:
            md.append(f"- **{h.get('period')} ({h.get('age_display')} - {h.get('dasha')}):** {h.get('phase_type')} (Vitality: {h.get('score')}%)  \n  *Advice:* {h.get('recommendation')}")
        md.append("")

        # 9. Sankhya Numerology
        md.append("## 9. Sankhya Numerology Profile (Vedic & Chaldean)\n")
        md.append("| Number Classification | Value & Planetary Ruler | Significance / Soul Archetype |")
        md.append("| :--- | :--- | :--- |")
        md.append(f"| **Mulank (Psychic / Birth Number)** | **{num.get('mulank', {}).get('mulank')}** ({num.get('mulank', {}).get('ruler')}) | {num.get('mulank', {}).get('archetype')} |")
        md.append(f"| **Bhagyank (Destiny / Life Path)** | **{num.get('bhagyank', {}).get('bhagyank')}** ({num.get('bhagyank', {}).get('ruler')}) | {num.get('bhagyank', {}).get('life_purpose')} |")
        md.append(f"| **Namank (Chaldean Compound)** | **{num.get('namank', {}).get('chaldean', {}).get('namank')}** (Compound {num.get('namank', {}).get('chaldean', {}).get('compound_number')}) | {num.get('namank', {}).get('chaldean', {}).get('meaning')} |")
        md.append(f"| **Soul Urge (Vowels)** | **{num.get('namank', {}).get('soul_urge', {}).get('number')}** | {num.get('namank', {}).get('soul_urge', {}).get('meaning')} |")
        md.append(f"| **Personality (Consonants)** | **{num.get('namank', {}).get('personality', {}).get('number')}** | {num.get('namank', {}).get('personality', {}).get('meaning')} |")
        md.append(f"| **Tripartite Harmony Score** | **{num.get('harmony', {}).get('harmony_score')} / 100** | {num.get('harmony', {}).get('recommendation')} |\n")

        # 10. Personalized Life Guidance & Auspicious Remedies
        md.append("## 10. Personalized Vedic Guidance & Auspicious Remedies\n")
        md.append(f"### Core Soul Temperament\n{guidance.get('temperament_summary')}\n")
        md.append(f"### Career & Prosperity Focus\n{guidance.get('career_and_wealth')}\n")
        md.append(f"### Relationships & Domestic Harmony\n{guidance.get('relationships_and_marriage')}\n")
        md.append("### Auspicious Vedic Remedies & Prescriptions")
        for r in guidance.get("remedies", []):
            md.append(f"- {r}")
        md.append("")
        md.append(f"- **Recommended Gemstone:** {guidance.get('recommended_gemstone')}")
        md.append(f"- **Lucky Days:** {', '.join(guidance.get('lucky_days', []))}")
        md.append(f"- **Harmonious Colors:** {', '.join(guidance.get('lucky_colors', []))}")
        md.append(f"- **Favorable Numbers:** {', '.join(str(n) for n in guidance.get('lucky_numbers', []))}\n")

        # 11. Live Planetary Transits (Gochara)
        md.append("## 11. Real-Time Planetary Transits (Gochara)\n")
        md.append(f"*Calculated at: {transits.get('transit_datetime_utc')} (Ayanamsha: {transits.get('ayanamsha')})*\n")
        md.append("| Planet | Sanskrit | Transit Sign | Degree | Nakshatra & Pada | Current Status |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for tr in transits.get("transits", []):
            md.append(f"| **{tr.get('graha')}** | {tr.get('sanskrit', '').split()[0]} | {tr.get('sign')} | {tr.get('degree')} | {tr.get('nakshatra')} | {tr.get('status_str')} |")
        md.append("")

        md.append("---\n*End of Comprehensive Vedic Jyotish & Numerology Report.*")

        return "\n".join(md)

    @staticmethod
    def generate_html_report(report: Dict[str, Any]) -> str:
        """
        Generates a standalone, visually rich, printable HTML report with
        embedded SVG charts, dark cosmic styling, and print-to-PDF styles.
        """
        user = report.get("user_input", {})
        astro = report.get("birth_astronomy", {})
        lagna = report.get("lagna", {})
        panchang = report.get("panchang", {})
        grahas = report.get("grahas", {})
        dashas = report.get("dashas", {})
        yogas = report.get("yogas_and_doshas", {})
        tl = report.get("timelines", {})
        num = report.get("numerology", {})
        guidance = report.get("guidance", {})
        charts = report.get("charts", {})
        transits = report.get("live_transits", {})

        full_name = user.get("full_name", "Arjun Sharma")
        d1_svg = charts.get("d1_svg", "")
        d9_svg = charts.get("d9_svg", "")
        d1_south_svg = charts.get("d1_south_svg", "")

        act_d = dashas.get("active_dasha", {})
        act_sum = tl.get("active_period_summary", {})
        milestones = tl.get("life_milestones", [])
        pds = tl.get("pratyantardashas", [])
        annual = tl.get("annual_forecast", [])
        b_yogas = yogas.get("benefic_yogas", [])

        # Build Milestone Cards HTML
        milestone_cards_html = []
        for m in milestones:
            badge_class = "badge-peak" if m.get("favorability_score", 0) >= 80 else ("badge-good" if m.get("favorability_score", 0) >= 65 else "badge-warn")
            if m.get("is_current"):
                badge_class = "badge-current"
            
            card = f"""
            <div class="milestone-card {'milestone-active' if m.get('is_current') else ''}">
                <div class="milestone-header">
                    <div>
                        <span class="milestone-category">{m.get('category')}</span>
                        <h4 class="milestone-title">{m.get('title')}</h4>
                        <div class="milestone-meta">
                            <span>📅 {m.get('year_range')} ({m.get('age_window')})</span>
                            <span>🪐 Dasha: <strong>{m.get('dasha')}</strong></span>
                            <span>⚡ Window: {m.get('period')}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge {badge_class}">{m.get('status_badge')}</span>
                        <div class="milestone-score">{m.get('favorability_score')}% <small>Favorability</small></div>
                    </div>
                </div>
                <div class="milestone-body">
                    <p><strong>Astrological Basis:</strong> {m.get('astrological_basis')}</p>
                    <p><strong>Predicted Life Event:</strong> {m.get('prediction_narrative')}</p>
                    <p style="color: #38bdf8;"><strong>Strategic Guidance:</strong> {m.get('actionable_guidance')}</p>
                    <p style="color: #fbbf24;"><strong>Vedic Remedy:</strong> {m.get('vedic_remedy')}</p>
                </div>
            </div>
            """
            milestone_cards_html.append(card)

        # Build Pratyantardasha Rows
        pd_rows_html = []
        for pd in pds:
            is_c = pd.get("is_current")
            row = f"""
            <tr style="{'background: rgba(16, 185, 129, 0.15); font-weight: bold;' if is_c else ''}">
                <td><strong style="color: {'#34d399' if is_c else '#f8fafc'};">{pd.get('dasha_hierarchy')}</strong></td>
                <td>{pd.get('start_date')} → {pd.get('end_date')}</td>
                <td>{pd.get('duration_days')} days</td>
                <td><span class="badge {'badge-current' if is_c else 'badge-good'}">{pd.get('status_badge')}</span></td>
                <td>{pd.get('favorability_score')}%</td>
                <td>{pd.get('focus_theme')} <em style="color: #cbd5e1;">({pd.get('guidance')})</em></td>
            </tr>
            """
            pd_rows_html.append(row)

        # Build Annual Forecast Rows
        annual_rows_html = []
        for af in annual:
            is_c = af.get("is_current_year")
            row = f"""
            <tr style="{'background: rgba(245, 158, 11, 0.12); font-weight: bold;' if is_c else ''}">
                <td><strong style="color: {'#fbbf24' if is_c else '#f8fafc'};">{af.get('year')}</strong> (Age {af.get('age_at_midyear')})</td>
                <td><code>{af.get('dasha')}</code></td>
                <td>{af.get('overall_score')}%</td>
                <td><span class="badge {'badge-current' if is_c else 'badge-good'}">{af.get('status_badge')}</span></td>
                <td>{af.get('primary_theme')}</td>
                <td>{af.get('key_recommendation')}</td>
            </tr>
            """
            annual_rows_html.append(row)

        # Build Grahas Rows
        graha_rows_html = []
        # Lagna first
        graha_rows_html.append(f"""
        <tr style="background: rgba(245, 158, 11, 0.1);">
            <td><strong>Ascendant (Lagna)</strong></td>
            <td>Lagna</td>
            <td><strong>{lagna.get('lagna_sign')}</strong></td>
            <td>{lagna.get('lagna_deg_formatted')}</td>
            <td>{lagna.get('lagna_nakshatra')} (P{lagna.get('lagna_nakshatra_pada')})</td>
            <td>{lagna.get('lagna_navamsha_sign')}</td>
            <td>House 1</td>
            <td><span class="badge badge-current">Lagna Center</span></td>
        </tr>
        """)
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            p = grahas.get(p_name, {})
            vkr = " [Vakri]" if p.get("is_retrograde") and p_name not in ("Rahu", "Ketu") else ""
            cst = " [Combust]" if p.get("is_combust") else ""
            dig = p.get("dignity", "Direct")
            dig_class = "badge-peak" if ("Exalted" in dig or "Own" in dig) else ("badge-warn" if ("Debilitated" in dig or "Enemy" in dig) else "badge-good")
            graha_rows_html.append(f"""
            <tr>
                <td><strong>{p_name}</strong></td>
                <td>{p.get('sanskrit', '').split()[0]}</td>
                <td>{p.get('sign')}</td>
                <td>{p.get('deg_formatted')}</td>
                <td>{p.get('nakshatra')} (P{p.get('nakshatra_pada')})</td>
                <td>{p.get('navamsha_sign')}</td>
                <td>House {p.get('house')}</td>
                <td><span class="badge {dig_class}">{dig}{vkr}{cst}</span></td>
            </tr>
            """)

        # Full HTML Document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vedic Jyotish & Numerology Complete Report - {full_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #090d16;
            --bg-card: rgba(18, 24, 43, 0.9);
            --bg-hero: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            --gold: #fbbf24;
            --gold-dark: #d97706;
            --gold-border: rgba(245, 158, 11, 0.35);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --emerald: #10b981;
            --rose: #f43f5e;
            --cyan: #06b6d4;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 50% 0%, #17153b 0%, #0d0f22 45%, #05060f 100%);
            color: var(--text-main);
            line-height: 1.6;
            padding: 2rem 1rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Action Toolbar (Hidden in print) */
        .toolbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--gold-border);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(12px);
        }}
        .toolbar h2 {{
            font-family: 'Cinzel', serif;
            color: var(--gold);
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .toolbar-btns {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        .btn {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #0f172a;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.88rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            text-decoration: none;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
        }}
        .btn-secondary {{
            background: rgba(51, 65, 85, 0.8);
            color: #f8fafc;
            border: 1px solid #475569;
        }}
        .btn-secondary:hover {{
            background: rgba(71, 85, 105, 0.9);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}

        /* Main Header Banner */
        .report-header {{
            text-align: center;
            padding: 2.5rem 1.5rem;
            background: var(--bg-hero);
            border: 1.5px solid var(--gold-border);
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 25px rgba(245, 158, 11, 0.15);
        }}
        .report-header h1 {{
            font-family: 'Cinzel', serif;
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fffbeb 0%, #fbbf24 40%, #d97706 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .report-header p {{
            color: var(--text-muted);
            font-size: 1rem;
        }}

        /* Cards & Grids */
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--gold-border);
            border-radius: 14px;
            padding: 1.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }}
        .section-title {{
            font-family: 'Cinzel', serif;
            color: var(--gold);
            font-size: 1.45rem;
            margin-bottom: 1.25rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(245, 158, 11, 0.25);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-peak {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }}
        .badge-current {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }}
        .badge-good {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; }}
        .badge-warn {{ background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid #e11d48; }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            font-size: 0.92rem;
        }}
        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(71, 85, 105, 0.4);
        }}
        th {{
            background: rgba(15, 23, 42, 0.85);
            color: var(--gold);
            font-family: 'Cinzel', serif;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        tr:hover td {{
            background: rgba(30, 41, 59, 0.4);
        }}

        /* Hero Active Dasha Banner */
        .active-dasha-hero {{
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1.5px solid #10b981;
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
        }}
        .hero-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        .hero-box {{
            background: rgba(15, 23, 42, 0.75);
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid #38bdf8;
        }}

        /* Milestone Card */
        .milestone-card {{
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            transition: all 0.2s;
        }}
        .milestone-active {{
            border: 1.5px solid #10b981;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
            background: rgba(16, 185, 129, 0.05);
        }}
        .milestone-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
            gap: 1rem;
        }}
        .milestone-category {{
            font-size: 0.75rem;
            font-weight: 700;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .milestone-title {{
            font-family: 'Cinzel', serif;
            color: #fbbf24;
            font-size: 1.2rem;
            margin: 0.2rem 0 0.4rem;
        }}
        .milestone-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: var(--text-muted);
            flex-wrap: wrap;
        }}
        .milestone-score {{
            font-size: 1.5rem;
            font-weight: 800;
            color: #fbbf24;
            margin-top: 0.35rem;
        }}
        .milestone-score small {{
            font-size: 0.75rem;
            color: var(--text-muted);
            display: block;
        }}
        .milestone-body p {{
            margin-bottom: 0.5rem;
            font-size: 0.93rem;
            line-height: 1.55;
        }}

        /* Charts Container */
        .charts-flex {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }}
        .chart-box {{
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--gold-border);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
        }}
        .chart-box svg {{
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            display: block;
            margin: 0 auto;
        }}

        /* Responsive Mobile & Tablet Rules */
        @media (max-width: 768px) {{
            .report-container {{
                padding: 1rem 0.75rem 3rem;
            }}
            .report-header {{
                padding: 1.5rem 1rem;
            }}
            .report-header h1 {{
                font-size: 1.6rem;
            }}
            .report-header p {{
                font-size: 0.9rem;
            }}
            .toolbar {{
                flex-direction: column;
                align-items: stretch;
            }}
            .toolbar-btns {{
                flex-direction: column;
            }}
            .toolbar-btns .btn {{
                width: 100%;
                justify-content: center;
            }}
            .charts-flex {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}
            .section-card {{
                padding: 1.25rem 1rem;
            }}
            .milestone-item {{
                flex-direction: column;
                gap: 0.75rem;
            }}
            .milestone-date {{
                flex: none;
                width: 100%;
            }}
            th, td {{
                padding: 0.65rem 0.65rem;
                font-size: 0.82rem;
            }}
        }}

        @media (max-width: 480px) {{
            .report-header h1 {{
                font-size: 1.35rem;
            }}
        }}

        /* Print-to-PDF Media Styles */
        @media print {{
            body {{
                background: #ffffff !important;
                color: #0f172a !important;
                padding: 0 !important;
            }}
            .toolbar {{
                display: none !important;
            }}
            .report-header {{
                background: #ffffff !important;
                border: 2px solid #0f172a !important;
                box-shadow: none !important;
                padding: 1.5rem 1rem !important;
            }}
            .report-header h1 {{
                color: #0f172a !important;
                -webkit-text-fill-color: #0f172a !important;
                font-size: 2rem !important;
            }}
            .section-card {{
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                box-shadow: none !important;
                page-break-inside: avoid;
                padding: 1rem !important;
                margin-bottom: 1.5rem !important;
            }}
            .section-title {{
                color: #0f172a !important;
                border-bottom: 2px solid #0f172a !important;
            }}
            th {{
                background: #f1f5f9 !important;
                color: #0f172a !important;
            }}
            td {{
                border-bottom: 1px solid #cbd5e1 !important;
                color: #0f172a !important;
            }}
            .active-dasha-hero {{
                background: #f8fafc !important;
                border: 2px solid #10b981 !important;
                box-shadow: none !important;
                color: #0f172a !important;
            }}
            .hero-box {{
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                color: #0f172a !important;
            }}
            .milestone-card {{
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                color: #0f172a !important;
                page-break-inside: avoid;
            }}
            .milestone-title {{
                color: #0f172a !important;
            }}
            .milestone-body p {{
                color: #1e293b !important;
            }}
            .badge {{
                border: 1px solid #0f172a !important;
                color: #0f172a !important;
                background: #e2e8f0 !important;
            }}
            svg text {{
                fill: #0f172a !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Floating Toolbar -->
        <div class="toolbar">
            <h2>ॐ Vedic Jyotish & Sacred Timelines Report</h2>
            <div class="toolbar-btns">
                <button class="btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
                <button class="btn btn-secondary" onclick="downloadJSON()">📥 Download JSON</button>
                <button class="btn btn-secondary" onclick="downloadMarkdown()">📥 Download Markdown</button>
            </div>
        </div>

        <!-- Main Banner -->
        <header class="report-header">
            <h1>ॐ VEDIC JYOTISH & NUMEROLOGY MASTER REPORT ॐ</h1>
            <p>High Precision Astrological Calculations Based on NASA JPL DE421 Ephemeris & Sankhya Shastra</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-peak">Chitrapaksha / Lahiri Ayanamsha</span>
                <span class="badge badge-current">NASA JPL DE421 High Precision</span>
                <span class="badge badge-good">Parashari Vimshottari Dasha</span>
            </div>
        </header>

        <!-- 1. Birth & Astronomy -->
        <div class="section-card">
            <h3 class="section-title">✦ 1. Birth & Astronomical Coordinates ✦</h3>
            <table>
                <tbody>
                    <tr>
                        <th>Full Name</th>
                        <td><strong>{user.get('full_name')}</strong></td>
                        <th>Place of Birth</th>
                        <td>{user.get('place_of_birth')}</td>
                    </tr>
                    <tr>
                        <th>Date of Birth</th>
                        <td>{user.get('date_of_birth')}</td>
                        <th>Resolved Location</th>
                        <td>{astro.get('resolved_location')}</td>
                    </tr>
                    <tr>
                        <th>Time of Birth</th>
                        <td>{user.get('time_of_birth')}</td>
                        <th>Coordinates</th>
                        <td>{astro.get('latitude', 0):.4f}° N/S, {astro.get('longitude', 0):.4f}° E/W</td>
                    </tr>
                    <tr>
                        <th>Timezone</th>
                        <td>{astro.get('timezone')} ({astro.get('utc_offset')})</td>
                        <th>Lahiri Ayanamsha</th>
                        <td><strong>{astro.get('ayanamsha')}</strong></td>
                    </tr>
                    <tr>
                        <th>Ascendant (Lagna)</th>
                        <td><strong style="color: #fbbf24;">{lagna.get('lagna_sign')}</strong> ({lagna.get('lagna_deg_formatted')})</td>
                        <th>Lagna Nakshatra</th>
                        <td>{lagna.get('lagna_nakshatra')} (Lord: {lagna.get('lagna_nakshatra_lord')})</td>
                    </tr>
                    <tr>
                        <th>Moon Sign (Rashi)</th>
                        <td><strong style="color: #38bdf8;">{grahas.get('Moon', {}).get('sign')}</strong> ({grahas.get('Moon', {}).get('deg_formatted')})</td>
                        <th>Moon Nakshatra</th>
                        <td>{grahas.get('Moon', {}).get('nakshatra')} (Pada {grahas.get('Moon', {}).get('nakshatra_pada')})</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 2. Panchanga -->
        <div class="section-card">
            <h3 class="section-title">✦ 2. Vedic Panchanga (Five Limbs of Time) ✦</h3>
            <table>
                <thead>
                    <tr>
                        <th>Vara (Day)</th>
                        <th>Tithi (Lunar Day)</th>
                        <th>Nakshatra (Lunar Mansion)</th>
                        <th>Yoga (Solilunar)</th>
                        <th>Karana (Half-Tithi)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>{panchang.get('vara', {}).get('name')}</strong><br><small style="color: var(--text-muted);">{panchang.get('vara', {}).get('sanskrit')}</small></td>
                        <td><strong>{panchang.get('tithi', {}).get('name')}</strong><br><small style="color: var(--text-muted);">{panchang.get('tithi', {}).get('paksha')}</small></td>
                        <td><strong>{panchang.get('nakshatra', {}).get('name')}</strong><br><small style="color: var(--text-muted);">Pada {panchang.get('nakshatra', {}).get('pada')} (Lord: {panchang.get('nakshatra', {}).get('lord')})</small></td>
                        <td><strong>{panchang.get('yoga', {}).get('name')}</strong><br><small style="color: var(--text-muted);">{panchang.get('yoga', {}).get('nature')}</small></td>
                        <td><strong>{panchang.get('karana', {}).get('name')}</strong><br><small style="color: var(--text-muted);">No. {panchang.get('karana', {}).get('number')}</small></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 3. Planetary Positions -->
        <div class="section-card">
            <h3 class="section-title">✦ 3. Navagraha Positions (Sidereal Nirayana) ✦</h3>
            <table>
                <thead>
                    <tr>
                        <th>Planet (Graha)</th>
                        <th>Sanskrit</th>
                        <th>Sign (Rashi)</th>
                        <th>Degrees</th>
                        <th>Nakshatra & Pada</th>
                        <th>D9 Navamsha</th>
                        <th>House</th>
                        <th>Dignity / Status</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(graha_rows_html)}
                </tbody>
            </table>
        </div>

        <!-- 4. Kundali Charts -->
        <div class="section-card">
            <h3 class="section-title">✦ 4. Sacred Kundali Charts (D1 Rashi & D9 Navamsha) ✦</h3>
            <div class="charts-flex">
                <div class="chart-box">
                    <h4 style="font-family: 'Cinzel', serif; color: #fbbf24; margin-bottom: 0.75rem;">D1 - Lagna Rashi Chart (North Indian)</h4>
                    <div style="max-width: 380px; margin: 0 auto;">{d1_svg}</div>
                </div>
                <div class="chart-box">
                    <h4 style="font-family: 'Cinzel', serif; color: #38bdf8; margin-bottom: 0.75rem;">D9 - Navamsha Chart (North Indian)</h4>
                    <div style="max-width: 380px; margin: 0 auto;">{d9_svg}</div>
                </div>
                <div class="chart-box">
                    <h4 style="font-family: 'Cinzel', serif; color: #34d399; margin-bottom: 0.75rem;">D1 - South Indian Kundali</h4>
                    <div style="max-width: 380px; margin: 0 auto;">{d1_south_svg}</div>
                </div>
            </div>
        </div>

        <!-- 5. Yogas & Doshas -->
        <div class="section-card">
            <h3 class="section-title">✦ 5. Vedic Yogas & Doshas Analysis ✦</h3>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Status / Severity</th>
                        <th>Classical Explanation & Impact</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Manglik Dosha</strong></td>
                        <td><span class="badge {'badge-good' if not yogas.get('manglik_dosha', {}).get('has_dosha') else ('badge-peak' if yogas.get('manglik_dosha', {}).get('is_cancelled') else 'badge-warn')}">{yogas.get('manglik_dosha', {}).get('severity')}</span></td>
                        <td>{yogas.get('manglik_dosha', {}).get('description')}</td>
                    </tr>
                    <tr>
                        <td><strong>Shani Sade Sati</strong></td>
                        <td><span class="badge {'badge-good' if not yogas.get('sade_sati', {}).get('is_sade_sati') else 'badge-warn'}">{yogas.get('sade_sati', {}).get('phase')}</span></td>
                        <td>{yogas.get('sade_sati', {}).get('description')}</td>
                    </tr>
                    <tr>
                        <td><strong>Kaal Sarp Dosha</strong></td>
                        <td><span class="badge {'badge-good' if not yogas.get('kaal_sarp_dosha', {}).get('has_dosha') else 'badge-warn'}">{yogas.get('kaal_sarp_dosha', {}).get('severity')}</span></td>
                        <td>{yogas.get('kaal_sarp_dosha', {}).get('description')}</td>
                    </tr>
                    <tr>
                        <td><strong>Auspicious Raja & Dhana Yogas</strong></td>
                        <td><span class="badge badge-peak">{len(b_yogas)} Active Yogas</span></td>
                        <td>
                            {"<br>".join([f"• <strong>{y.get('name')}</strong>: {y.get('description')}" for y in b_yogas]) if b_yogas else "None dominant"}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 6. Running Active Dasha Hero -->
        <div class="active-dasha-hero">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="font-family: 'Cinzel', serif; color: #34d399; font-size: 1.4rem;">
                    ⭐ CURRENT ACTIVE DASHA: {act_sum.get('dasha')}
                </h3>
                <span class="badge badge-current">{act_sum.get('period')}</span>
            </div>
            <div style="margin-top: 0.5rem; font-size: 1.05rem; font-weight: 600;">
                🌟 Dominant Life Focus: <span style="color: #fbbf24;">{act_sum.get('dominant_theme')}</span>
            </div>
            <div class="hero-grid">
                <div class="hero-box" style="border-left-color: #38bdf8;">
                    <strong style="color: #38bdf8;">💼 Career & Status:</strong> {act_sum.get('career_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{act_sum.get('career_recommendation')}</span>
                </div>
                <div class="hero-box" style="border-left-color: #f472b6;">
                    <strong style="color: #f472b6;">💍 Marriage & Love:</strong> {act_sum.get('marriage_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{act_sum.get('marriage_recommendation')}</span>
                </div>
                <div class="hero-box" style="border-left-color: #34d399;">
                    <strong style="color: #34d399;">💰 Wealth & Assets:</strong> {act_sum.get('wealth_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{act_sum.get('wealth_recommendation')}</span>
                </div>
                <div class="hero-box" style="border-left-color: #22d3ee;">
                    <strong style="color: #22d3ee;">🌿 Health & Vitality:</strong> {act_sum.get('health_status')}<br>
                    <span style="font-size: 0.85rem; color: #cbd5e1; font-style: italic;">{act_sum.get('health_recommendation')}</span>
                </div>
            </div>
        </div>

        <!-- 7. Detailed Chronological Event Timeline & Life Milestones -->
        <div class="section-card">
            <h3 class="section-title">⏳ 7. Detailed Chronological Event Timeline & Life Milestones ⏳</h3>
            <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
                Comprehensive Parashari Vimshottari timing synthesized with Bhava lordships, planetary karakatwas,
                dignities, and transit activations across all life stages.
            </p>
            {"".join(milestone_cards_html)}
        </div>

        <!-- 8. Pratyantardasha Granular Calendar -->
        <div class="section-card">
            <h3 class="section-title">✦ 8. Granular Pratyantardasha (Sub-Sub Period) Forecast ✦</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">
                Month-by-month timing breakdown for the currently running Antardasha window.
            </p>
            <table>
                <thead>
                    <tr>
                        <th>Dasha Level 3</th>
                        <th>Period Dates</th>
                        <th>Duration</th>
                        <th>Status</th>
                        <th>Favorability</th>
                        <th>Focus Theme & Core Action</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(pd_rows_html)}
                </tbody>
            </table>
        </div>

        <!-- 9. Annual 10-Year Forward Forecast -->
        <div class="section-card">
            <h3 class="section-title">✦ 9. Annual 10-Year Forward Forecast Roadmap ✦</h3>
            <table>
                <thead>
                    <tr>
                        <th>Year & Age</th>
                        <th>Active Dasha</th>
                        <th>Score</th>
                        <th>Status</th>
                        <th>Primary Theme</th>
                        <th>Key Strategic Recommendation</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(annual_rows_html)}
                </tbody>
            </table>
        </div>

        <!-- 10. Sankhya Numerology -->
        <div class="section-card">
            <h3 class="section-title">🔢 10. Sankhya Numerology (Vedic & Chaldean) 🔢</h3>
            <table>
                <thead>
                    <tr>
                        <th>Classification</th>
                        <th>Value & Planetary Ruler</th>
                        <th>Archetype / Core Significance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Mulank (Psychic Number)</strong></td>
                        <td><strong style="color: #fbbf24;">{num.get('mulank', {}).get('mulank')}</strong> ({num.get('mulank', {}).get('ruler')})</td>
                        <td>{num.get('mulank', {}).get('archetype')}</td>
                    </tr>
                    <tr>
                        <td><strong>Bhagyank (Destiny Number)</strong></td>
                        <td><strong style="color: #38bdf8;">{num.get('bhagyank', {}).get('bhagyank')}</strong> ({num.get('bhagyank', {}).get('ruler')})</td>
                        <td>{num.get('bhagyank', {}).get('life_purpose')}</td>
                    </tr>
                    <tr>
                        <td><strong>Namank (Chaldean Name)</strong></td>
                        <td><strong style="color: #34d399;">{num.get('namank', {}).get('chaldean', {}).get('namank')}</strong> (Compound {num.get('namank', {}).get('chaldean', {}).get('compound_number')})</td>
                        <td>{num.get('namank', {}).get('chaldean', {}).get('meaning')}</td>
                    </tr>
                    <tr>
                        <td><strong>Soul Urge (Vowels)</strong></td>
                        <td><strong>{num.get('namank', {}).get('soul_urge', {}).get('number')}</strong></td>
                        <td>{num.get('namank', {}).get('soul_urge', {}).get('meaning')}</td>
                    </tr>
                    <tr>
                        <td><strong>Personality (Consonants)</strong></td>
                        <td><strong>{num.get('namank', {}).get('personality', {}).get('number')}</strong></td>
                        <td>{num.get('namank', {}).get('personality', {}).get('meaning')}</td>
                    </tr>
                    <tr>
                        <td><strong>Tripartite Harmony Score</strong></td>
                        <td><span class="badge badge-peak">{num.get('harmony', {}).get('harmony_score')} / 100</span></td>
                        <td>{num.get('harmony', {}).get('recommendation')}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 11. Life Guidance & Remedies -->
        <div class="section-card">
            <h3 class="section-title">📜 11. Personalized Vedic Life Guidance & Auspicious Remedies 📜</h3>
            <div style="margin-bottom: 1.25rem;">
                <h4 style="color: #fbbf24; margin-bottom: 0.35rem;">🌟 Temperament & Soul Blueprint</h4>
                <p style="color: #cbd5e1; line-height: 1.6;">{guidance.get('temperament_summary')}</p>
            </div>
            <div style="margin-bottom: 1.25rem;">
                <h4 style="color: #38bdf8; margin-bottom: 0.35rem;">💼 Career & Material Success</h4>
                <p style="color: #cbd5e1; line-height: 1.6;">{guidance.get('career_and_wealth')}</p>
            </div>
            <div style="margin-bottom: 1.25rem;">
                <h4 style="color: #f472b6; margin-bottom: 0.35rem;">💍 Relationships & Domestic Harmony</h4>
                <p style="color: #cbd5e1; line-height: 1.6;">{guidance.get('relationships_and_marriage')}</p>
            </div>
            <div>
                <h4 style="color: #34d399; margin-bottom: 0.5rem;">🕉️ Auspicious Vedic Remedies & Prescriptions</h4>
                <ul style="padding-left: 1.5rem; color: #cbd5e1; line-height: 1.8;">
                    {"".join([f"<li>{r}</li>" for r in guidance.get("remedies", [])])}
                </ul>
            </div>
        </div>

        <!-- 12. Real-time Transits -->
        <div class="section-card">
            <h3 class="section-title">🪐 12. Real-Time Planetary Transits (Gochara) 🪐</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.75rem;">
                Live Ephemeris at {transits.get('transit_datetime_utc')} • Ayanamsha: {transits.get('ayanamsha')}
            </p>
            <table>
                <thead>
                    <tr>
                        <th>Planet</th>
                        <th>Sanskrit</th>
                        <th>Transit Sign</th>
                        <th>Degrees</th>
                        <th>Nakshatra & Pada</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f"<tr><td><strong>{tr.get('graha')}</strong></td><td>{tr.get('sanskrit', '').split()[0]}</td><td>{tr.get('sign')}</td><td>{tr.get('degree')}</td><td>{tr.get('nakshatra')}</td><td>{tr.get('status_str')}</td></tr>" for tr in transits.get("transits", [])])}
                </tbody>
            </table>
        </div>

        <!-- Footer -->
        <footer style="text-align: center; color: var(--text-muted); padding: 2rem 0; font-size: 0.85rem;">
            <p>ॐ Shanti Shanti Shanti ॐ</p>
            <p>Generated by Vedic Astrology & Numerology System • High Precision NASA JPL DE421 Ephemeris</p>
        </footer>
    </div>

    <!-- Client-side Data Download Helper Scripts -->
    <script>
        const reportData = {json.dumps(report, ensure_ascii=False)};
        const markdownReport = {json.dumps(ReportExporter.generate_markdown_report(report), ensure_ascii=False)};

        function downloadJSON() {{
            const blob = new Blob([JSON.stringify(reportData, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{full_name.replace(" ", "_")}_kundli_report.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        function downloadMarkdown() {{
            const blob = new Blob([markdownReport], {{ type: 'text/markdown' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{full_name.replace(" ", "_")}_kundli_report.md';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>
"""
        return html
    
    @classmethod
    def export_to_file(cls, report: Dict[str, Any], filepath: str, format_type: str = "auto") -> str:
        """
        Exports the report to a specified file path.
        format_type can be 'auto', 'html', 'markdown' ('md'), or 'json'.
        Returns the resolved file path.
        """
        import os
        lower_path = filepath.lower()
        if format_type == "auto":
            if lower_path.endswith((".html", ".htm")):
                fmt = "html"
            elif lower_path.endswith((".md", ".markdown")):
                fmt = "markdown"
            else:
                fmt = "json"
        else:
            fmt = format_type.lower()

        if fmt in ("html", "htm"):
            content = cls.generate_html_report(report)
        elif fmt in ("md", "markdown"):
            content = cls.generate_markdown_report(report)
        else:
            content = cls.generate_json_report(report)

        # Ensure directory exists
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return os.path.abspath(filepath)
