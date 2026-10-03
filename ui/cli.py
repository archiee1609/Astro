"""
ui/cli.py - Interactive Rich Terminal Interface for Vedic Astrology & Numerology
"""

import sys
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from core.analyzer import AstroAnalyzer

console = Console()

def run_cli_interactive():
    console.print(Panel.fit(
        "[bold gold1]ॐ VEDIC JYOTISH & NUMEROLOGY ENGINE ॐ[/bold gold1]\n"
        "[italic bright_yellow]High Precision Astrological Calculations Based on NASA JPL DE421 & Sankhya Shastra[/italic bright_yellow]",
        border_style="gold1"
    ))

    console.print("\n[bold cyan]Please enter birth details to begin analysis:[/bold cyan]")
    
    full_name = Prompt.ask("[bold white]1. Full Name[/bold white]", default="Arjun Sharma")
    dob_str = Prompt.ask("[bold white]2. Date of Birth (YYYY-MM-DD or DD-MM-YYYY)[/bold white]", default="1995-10-24")
    tob_str = Prompt.ask("[bold white]3. Time of Birth (HH:MM or HH:MM AM/PM)[/bold white]", default="06:30")
    pob_str = Prompt.ask("[bold white]4. Place of Birth (City, Country)[/bold white]", default="New Delhi, India")

    analyzer = AstroAnalyzer()

    with Progress(
        SpinnerColumn(style="bold gold1"),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[bold gold1]Resolving coordinates, computing planetary ephemeris & numerology...", total=None)
        try:
            report = analyzer.analyze(
                full_name=full_name,
                dob_str=dob_str,
                tob_str=tob_str,
                pob_str=pob_str
            )
        except Exception as e:
            console.print(f"[bold red]Error calculating astrology report: {e}[/bold red]")
            return

    display_full_report(report)

    # Prompt for export
    console.print()
    if Prompt.ask("[bold yellow]Would you like to export this full report to a JSON file?[/bold yellow]", choices=["y", "n"], default="n") == "y":
        filename = f"kundli_{full_name.replace(' ', '_').lower()}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        console.print(f"[bold green]✓ Report exported successfully to [white]{filename}[/white]![/bold green]")

def display_full_report(report: dict):
    user = report["user_input"]
    astro = report["birth_astronomy"]
    lagna = report["lagna"]
    panchang = report["panchang"]
    grahas = report["grahas"]
    dashas = report["dashas"]
    yogas = report["yogas_and_doshas"]
    numerology = report["numerology"]
    guidance = report["guidance"]

    # 1. Header Overview Table
    overview_table = Table(title="[bold gold1]✦ BIRTH & ASTRONOMICAL DETAILS ✦[/bold gold1]", border_style="gold1", show_header=False)
    overview_table.add_column("Field", style="bold cyan", width=22)
    overview_table.add_column("Value", style="white")
    overview_table.add_column("Field", style="bold cyan", width=22)
    overview_table.add_column("Value", style="white")

    overview_table.add_row("Full Name", user["full_name"], "Place of Birth", user["place_of_birth"])
    overview_table.add_row("Date of Birth", user["date_of_birth"], "Resolved Location", astro["resolved_location"])
    overview_table.add_row("Time of Birth", user["time_of_birth"], "Coordinates", f"{astro['latitude']:.4f}° N/S, {astro['longitude']:.4f}° E/W")
    overview_table.add_row("Timezone", astro["timezone"], "UTC Offset", astro["utc_offset"])
    overview_table.add_row("Ayanamsha (Lahiri)", astro["ayanamsha"], "Lagna (Ascendant)", f"{lagna['lagna_sign']} ({lagna['lagna_deg_formatted']})")
    overview_table.add_row("Moon Sign (Rashi)", f"{grahas['Moon']['sign']} ({grahas['Moon']['deg_formatted']})", "Moon Nakshatra", f"{grahas['Moon']['nakshatra']} (Pada {grahas['Moon']['nakshatra_pada']})")
    overview_table.add_row("Sun Sign (Surya)", f"{grahas['Sun']['sign']} ({grahas['Sun']['deg_formatted']})", "Lagna Nakshatra", f"{lagna['lagna_nakshatra']} (Lord: {lagna['lagna_nakshatra_lord']})")

    console.print("\n")
    console.print(overview_table)

    # 2. Vedic Panchanga
    pan_table = Table(title="[bold gold1]✦ VEDIC PANCHANGA (FIVE LIMBS OF TIME) ✦[/bold gold1]", border_style="bright_yellow")
    pan_table.add_column("Vara (Day)", style="cyan")
    pan_table.add_column("Tithi (Lunar Day)", style="green")
    pan_table.add_column("Nakshatra (Mansion)", style="yellow")
    pan_table.add_column("Yoga (Solilunar)", style="magenta")
    pan_table.add_column("Karana (Half Tithi)", style="red")

    pan_table.add_row(
        f"{panchang['vara']['name']}\n[dim]({panchang['vara']['lord']})[/dim]",
        f"{panchang['tithi']['name']}\n[dim]({panchang['tithi']['paksha'].split()[0]})[/dim]",
        f"{panchang['nakshatra']['name']}\n[dim](Pada {panchang['nakshatra']['pada']})[/dim]",
        f"{panchang['yoga']['name']}\n[dim]({panchang['yoga']['nature'].split()[0]})[/dim]",
        f"{panchang['karana']['name']}\n[dim](No. {panchang['karana']['number']})[/dim]"
    )
    console.print("\n")
    console.print(pan_table)

    # 3. Navagraha Planetary Positions
    planet_table = Table(title="[bold gold1]✦ NAVAGRAHA POSITIONS (SIDEREAL NIRAYANA) ✦[/bold gold1]", border_style="gold1")
    planet_table.add_column("Graha (Planet)", style="bold cyan")
    planet_table.add_column("Sign (Rashi)", style="white")
    planet_table.add_column("Degrees", style="bright_yellow")
    planet_table.add_column("Nakshatra & Pada", style="green")
    planet_table.add_column("D9 Navamsha", style="magenta")
    planet_table.add_column("House (Bhava)", style="bright_cyan")
    planet_table.add_column("Status / Dignity", style="bold")

    # Add Ascendant row first
    planet_table.add_row(
        "Ascendant (Lagna)",
        lagna["lagna_sign"],
        lagna["lagna_deg_formatted"],
        f"{lagna['lagna_nakshatra']} (P{lagna['lagna_nakshatra_pada']})",
        lagna["lagna_navamsha_sign"],
        "House 1",
        "[bold cyan]Lagna Center[/bold cyan]"
    )

    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        p = grahas[p_name]
        status_parts = []
        if p["is_retrograde"] and p_name not in ("Rahu", "Ketu"):
            status_parts.append("[bold red]Retrograde (Vakri)[/bold red]")
        if p["is_combust"]:
            status_parts.append("[bold red]Combust (Asta)[/bold red]")
        
        # Colorize dignity
        dignity = p["dignity"]
        if "Exalted" in dignity or "Own Sign" in dignity or "Moolatrikona" in dignity:
            status_parts.append(f"[bold green]{dignity}[/bold green]")
        elif "Debilitated" in dignity or "Enemy" in dignity:
            status_parts.append(f"[bold red]{dignity}[/bold red]")
        else:
            status_parts.append(f"[dim]{dignity}[/dim]")

        status_str = " | ".join(status_parts) if status_parts else "Direct"

        planet_table.add_row(
            f"{p_name} ({p['sanskrit'].split()[0]})",
            p["sign"],
            p["deg_formatted"],
            f"{p['nakshatra']} (P{p['nakshatra_pada']})",
            p["navamsha_sign"],
            f"House {p['house']}",
            status_str
        )

    console.print("\n")
    console.print(planet_table)

    # 4. Kundali Text Chart
    console.print("\n")
    console.print(Panel(report["charts"]["ascii_chart"], title="[bold gold1]✦ NORTH INDIAN D1 KUNDALI ✦[/bold gold1]", border_style="gold1"))

    # 5. Yogas & Doshas Analysis
    dosha_table = Table(title="[bold gold1]✦ VEDIC YOGAS & DOSHAS ANALYSIS ✦[/bold gold1]", border_style="gold1")
    dosha_table.add_column("Category", style="bold cyan", width=22)
    dosha_table.add_column("Status / Severity", style="bold", width=26)
    dosha_table.add_column("Classical Explanation & Impact", style="white")

    # Manglik
    m_info = yogas["manglik_dosha"]
    m_status = "[green]Non-Manglik[/green]" if not m_info["has_dosha"] else (
        "[bright_yellow]Cancelled Manglik[/bright_yellow]" if m_info["is_cancelled"] else f"[bold red]{m_info['severity']}[/bold red]"
    )
    dosha_table.add_row("Manglik Dosha", m_status, m_info["description"])

    # Sade Sati
    s_info = yogas["sade_sati"]
    s_status = f"[bold red]{s_info['phase']}[/bold red]" if s_info["is_sade_sati"] else (
        f"[yellow]{s_info['phase']}[/yellow]" if s_info["has_dhaiya"] else "[green]Inactive (Free)[/green]"
    )
    dosha_table.add_row("Shani Sade Sati", s_status, s_info["description"])

    # Kaal Sarp
    k_info = yogas["kaal_sarp_dosha"]
    k_status = f"[bold red]{k_info['severity']}[/bold red]" if k_info["has_dosha"] else "[green]Not Present[/green]"
    dosha_table.add_row("Kaal Sarp Dosha", k_status, k_info["description"])

    # Benefic Yogas
    b_yogas = yogas["benefic_yogas"]
    b_str = "\n".join([f"• [bold green]{y['name']}[/bold green]: {y['description']}" for y in b_yogas]) if b_yogas else "None dominant"
    dosha_table.add_row("Auspicious Yogas", f"[bold green]{len(b_yogas)} Active[/bold green]", b_str)

    console.print("\n")
    console.print(dosha_table)

    # 6. Vimshottari Dasha
    dasha_table = Table(title="[bold gold1]✦ VIMSHOTTARI DASHA TIMELINE ✦[/bold gold1]", border_style="gold1")
    dasha_table.add_column("Dasha Type", style="bold cyan", width=20)
    dasha_table.add_column("Planet / Sequence", style="bold yellow")
    dasha_table.add_column("Period Span", style="white")

    active_d = dashas["active_dasha"]
    dasha_table.add_row("[bold green]Currently Active Dasha[/bold green]", f"[bold green]{active_d['formatted']}[/bold green]", f"Until: {active_d['end_date']}")
    dasha_table.add_row("Birth Dasha Balance", dashas["balance_at_birth"]["formatted"], f"Started at birth")

    for md in dashas["timeline"][:6]:
        is_cur = md["planet"] == active_d["mahadasha"]
        tag = "[bold green]▶ ACTIVE[/bold green]" if is_cur else ""
        dasha_table.add_row(f"Mahadasha: {md['planet']}", f"{md['period_years']} Years {tag}", f"{md['start_date']} to {md['end_date']}")

    console.print("\n")
    console.print(dasha_table)

    # 7. Numerology Profile (Sankhya Shastra)
    num = numerology
    num_table = Table(title="[bold gold1]✦ VEDIC & CHALDEAN NUMEROLOGY (SANKHYA SHASTRA) ✦[/bold gold1]", border_style="gold1")
    num_table.add_column("Number Type", style="bold cyan", width=24)
    num_table.add_column("Value & Ruling Planet", style="bold yellow", width=28)
    num_table.add_column("Core Significance", style="white")

    num_table.add_row("Mulank (Psychic / Birth)", f"[bold green]{num['mulank']['mulank']}[/bold green] ({num['mulank']['ruler']})", num['mulank']['archetype'])
    num_table.add_row("Bhagyank (Destiny Path)", f"[bold green]{num['bhagyank']['bhagyank']}[/bold green] ({num['bhagyank']['ruler']})", num['bhagyank']['life_purpose'])
    num_table.add_row("Namank (Chaldean Name)", f"[bold green]{num['namank']['chaldean']['namank']}[/bold green] (Compound: {num['namank']['chaldean']['compound_number']})", num['namank']['chaldean']['meaning'])
    num_table.add_row("Namank (Pythagorean)", f"{num['namank']['pythagorean']['namank']} (Compound: {num['namank']['pythagorean']['compound_number']})", "Western expression frequency")
    num_table.add_row("Soul Urge (Vowels)", f"{num['namank']['soul_urge']['number']}", num['namank']['soul_urge']['meaning'])
    num_table.add_row("Personality (Consonants)", f"{num['namank']['personality']['number']}", num['namank']['personality']['meaning'])
    num_table.add_row("Tripartite Harmony Score", f"[bold green]{num['harmony']['harmony_score']} / 100[/bold green]", num['harmony']['recommendation'])

    console.print("\n")
    console.print(num_table)

    # 8. Event Timelines & Life Roadmap
    if "timelines" in report:
        tl = report["timelines"]
        act = tl.get("active_period_summary", {})
        tl_table = Table(title="[bold gold1]✦ PREDICTIVE EVENT TIMELINES (CAREER • MARRIAGE • WEALTH • HEALTH) ✦[/bold gold1]", border_style="gold1")
        tl_table.add_column("Life Domain", style="bold cyan", width=22)
        tl_table.add_column("Current Active Phase (Today)", style="bold yellow", width=34)
        tl_table.add_column("Vedic Astrological Strategy & Key Insight", style="white")

        tl_table.add_row("Overall Running Theme", f"[bold green]{act.get('dasha', '')}[/bold green] ({act.get('period', '')})", act.get("dominant_theme", ""))
        tl_table.add_row("💼 Career & Status", act.get("career_status", ""), act.get("career_recommendation", ""))
        tl_table.add_row("💍 Marriage & Love", act.get("marriage_status", ""), act.get("marriage_recommendation", ""))
        tl_table.add_row("💰 Wealth & Assets", act.get("wealth_status", ""), act.get("wealth_recommendation", ""))
        tl_table.add_row("🌿 Health & Vitality", act.get("health_status", ""), act.get("health_recommendation", ""))

        console.print("\n")
        console.print(tl_table)

    # 8. Life Guidance & Vedic Remedies Panel
    guidance_text = (
        f"[bold gold1]TEMPERAMENT & PERSONALITY:[/bold gold1]\n{guidance['temperament_summary']}\n\n"
        f"[bold gold1]CAREER & PROSPERITY:[/bold gold1]\n{guidance['career_and_wealth']}\n\n"
        f"[bold gold1]RELATIONSHIPS & HARMONY:[/bold gold1]\n{guidance['relationships_and_marriage']}\n\n"
        f"[bold gold1]VEDIC REMEDIES & AUSPICIOUS RECOMMENDATIONS:[/bold gold1]\n" +
        "\n".join([f"• {r}" for r in guidance['remedies']])
    )
    console.print("\n")
    console.print(Panel(guidance_text, title="[bold gold1]✦ PERSONALIZED VEDIC GUIDANCE & REMEDIES ✦[/bold gold1]", border_style="gold1"))

if __name__ == "__main__":
    run_cli_interactive()
