"""
core/internet_data.py - High Precision Internet Astronomy, Geolocation & Transit Engine
Provides real-time internet data enrichment:
1. OpenStreetMap (OSM) Nominatim live geocoding with detailed address hierarchy.
2. Open-Meteo High Precision Topographic Elevation API for topocentric astronomical corrections.
3. Open-Meteo Solar Ephemeris API for exact local sunrise, sunset, and day/night length.
4. Real-time planetary transits (Gochara) using NASA JPL DE421 ephemeris and Chitrapaksha Lahiri ayanamsha.
"""

import requests
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from core.constants import SIGN_NAMES, SIGNS, PLANETS

class InternetDataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InternetDataService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "VedicJyotishApp/2.0 (HighPrecisionAstrology; Contact: support@vedicastrology.app)"
        })
        self._elevation_cache: Dict[str, float] = {}
        self._solar_cache: Dict[str, Dict[str, Any]] = {}
        self._geocode_cache: Dict[str, List[Dict[str, Any]]] = {}

    def is_internet_available(self) -> bool:
        """Checks if active internet connection is accessible."""
        try:
            r = self.session.get("https://api.open-meteo.com/v1/elevation?latitude=0&longitude=0", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def get_service_status(self) -> Dict[str, Any]:
        """Returns live status of internet data providers."""
        osm_status = False
        meteo_status = False
        try:
            r = self.session.get("https://api.open-meteo.com/v1/elevation?latitude=28.6139&longitude=77.2090", timeout=3)
            meteo_status = (r.status_code == 200)
        except Exception:
            pass

        try:
            r = self.session.get("https://nominatim.openstreetmap.org/search?q=Delhi&format=json&limit=1", timeout=3)
            osm_status = (r.status_code == 200)
        except Exception:
            pass

        is_online = meteo_status or osm_status
        return {
            "is_online": is_online,
            "osm_nominatim": "Connected" if osm_status else "Offline / Cached",
            "elevation_api": "Connected (Open-Meteo High Precision)" if meteo_status else "Offline / Fallback",
            "solar_ephemeris": "Connected (Open-Meteo Solar Forecast)" if meteo_status else "Analytical Fallback",
            "ephemeris_kernel": "Active (NASA JPL DE421 Sub-arcsecond)"
        }

    def fetch_elevation(self, lat: float, lon: float) -> float:
        """
        Fetches precise topographic ground elevation (meters above sea level) via Open-Meteo API.
        Topocentric observer height refines local horizon and ascendant computations.
        """
        cache_key = f"{round(lat, 4)},{round(lon, 4)}"
        if cache_key in self._elevation_cache:
            return self._elevation_cache[cache_key]

        try:
            url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
            res = self.session.get(url, timeout=4)
            if res.status_code == 200:
                data = res.json()
                elev_list = data.get("elevation", [])
                if elev_list and isinstance(elev_list, list):
                    elev = float(elev_list[0])
                    self._elevation_cache[cache_key] = elev
                    return elev
        except Exception:
            pass

        # Default fallback sea-level elevation
        return 0.0

    def fetch_solar_ephemeris(self, lat: float, lon: float, date_obj: datetime.date) -> Dict[str, Any]:
        """
        Fetches official astronomical sunrise, sunset, and daylight duration from Open-Meteo API.
        Used to calibrate Vedic Dina-Māna (daytime span) and Ratri-Māna (night span) for Vara calculations.
        """
        date_str = date_obj.strftime("%Y-%m-%d")
        cache_key = f"{round(lat, 4)},{round(lon, 4)},{date_str}"
        if cache_key in self._solar_cache:
            return self._solar_cache[cache_key]

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&daily=sunrise,sunset,daylight_duration&timezone=auto"
                f"&start_date={date_str}&end_date={date_str}"
            )
            res = self.session.get(url, timeout=4)
            if res.status_code == 200:
                daily = res.json().get("daily", {})
                sunrise_arr = daily.get("sunrise", [])
                sunset_arr = daily.get("sunset", [])
                duration_arr = daily.get("daylight_duration", [])

                sunrise_iso = sunrise_arr[0] if sunrise_arr else None
                sunset_iso = sunset_arr[0] if sunset_arr else None
                duration_sec = duration_arr[0] if duration_arr else None

                result = {
                    "source": "Open-Meteo Solar API (Internet Synchronized)",
                    "sunrise": sunrise_iso.split("T")[-1] if sunrise_iso else "06:00",
                    "sunset": sunset_iso.split("T")[-1] if sunset_iso else "18:00",
                    "daylight_hours": round(duration_sec / 3600.0, 2) if duration_sec else 12.0,
                    "date": date_str,
                    "is_live": True
                }
                self._solar_cache[cache_key] = result
                return result
        except Exception:
            pass

        # Fallback estimation
        return {
            "source": "Standard Astronomical Approximation (Offline Fallback)",
            "sunrise": "06:00",
            "sunset": "18:00",
            "daylight_hours": 12.0,
            "date": date_str,
            "is_live": False
        }

    def search_locations_online(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Queries OpenStreetMap Nominatim for live worldwide place search with pinpoint coordinates.
        """
        clean_q = query.strip()
        if not clean_q:
            return []

        if clean_q in self._geocode_cache:
            return self._geocode_cache[clean_q]

        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": clean_q,
                "format": "json",
                "addressdetails": 1,
                "limit": limit
            }
            res = self.session.get(url, params=params, timeout=5)
            if res.status_code == 200:
                raw_items = res.json()
                results = []
                for item in raw_items:
                    addr = item.get("address", {})
                    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or item.get("name")
                    country = addr.get("country", "")
                    state = addr.get("state", "")
                    lat = float(item["lat"])
                    lon = float(item["lon"])

                    elev = self.fetch_elevation(lat, lon)

                    display = f"{city}, {state}, {country}".replace(", ,", ",").strip(", ")
                    results.append({
                        "name": display or item.get("display_name", ""),
                        "full_address": item.get("display_name", ""),
                        "latitude": lat,
                        "longitude": lon,
                        "elevation_m": elev,
                        "type": item.get("type", "locality"),
                        "source": "OpenStreetMap Nominatim (Live Internet)"
                    })
                self._geocode_cache[clean_q] = results
                return results
        except Exception:
            pass

        return []

    def calculate_current_transits(self, ephem_engine, target_dt: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Calculates real-time celestial transit positions (Gochara) right now
        using NASA JPL DE421 Ephemeris and Chitrapaksha Lahiri Ayanamsha.
        """
        if target_dt is None:
            target_dt = datetime.now(timezone.utc)
        elif target_dt.tzinfo is None:
            target_dt = target_dt.replace(tzinfo=timezone.utc)

        ephem_data = ephem_engine.calculate_planetary_positions(target_dt)
        grahas = ephem_data["grahas"]
        ayanamsha = ephem_data["ayanamsha_formatted"]

        transit_summary = []
        for name, g in grahas.items():
            retro = " (Vakri / Retrograde)" if g["is_retrograde"] else ""
            combust = " (Combust)" if g["is_combust"] else ""
            transit_summary.append({
                "graha": name,
                "sanskrit": g["sanskrit"],
                "sign": g["sign"],
                "degree": g.get("deg_formatted", f"{round(g['sign_deg'], 2)}°"),
                "nakshatra": f"{g['nakshatra']} (Pada {g.get('nakshatra_pada', 1)})",
                "dignity": g["dignity"],
                "is_retrograde": g["is_retrograde"],
                "is_combust": g["is_combust"],
                "status_str": f"{g['sign']} {g.get('deg_formatted', '')}{retro}{combust}"
            })

        return {
            "transit_datetime_utc": target_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "transit_datetime_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ayanamsha": ayanamsha,
            "transits": transit_summary,
            "raw_grahas": grahas
        }
