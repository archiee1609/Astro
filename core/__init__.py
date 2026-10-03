"""
core - Vedic Astrology and Numerology Core Engine
High-precision astrological calculations based on NASA JPL DE421 and Chitrapaksha Lahiri Ayanamsha.
"""

from core.analyzer import AstroAnalyzer
from core.timelines import TimelineEngine
from core.internet_data import InternetDataService
from core.ephemeris import EphemerisEngine
from core.ascendant import AscendantEngine
from core.panchang import PanchangEngine
from core.dashas import VimshottariDashaEngine
from core.yogas import YogaEngine
from core.numerology import NumerologyEngine
from core.geocoder import LocationResolver
from core.visualizer import ChartVisualizer
from core.report_exporter import ReportExporter

__all__ = [
    "AstroAnalyzer",
    "TimelineEngine",
    "InternetDataService",
    "EphemerisEngine",
    "AscendantEngine",
    "PanchangEngine",
    "VimshottariDashaEngine",
    "YogaEngine",
    "NumerologyEngine",
    "LocationResolver",
    "ChartVisualizer",
    "ReportExporter",
]

__version__ = "2.0.0"
