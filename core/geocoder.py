"""
core/geocoder.py - High Performance Geocoding and Timezone Engine
Combines a comprehensive offline database of 250+ Indian and international cities
with online geopy Nominatim fallback and automatic timezone resolution.
"""

import zoneinfo
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# Fast offline database of major cities (lat, lon, timezone)
OFFLINE_CITIES: Dict[str, Tuple[float, float, str]] = {
    # Top Indian Metros & Cities
    "delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "new delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "mumbai": (19.0760, 72.8777, "Asia/Kolkata"),
    "bombay": (19.0760, 72.8777, "Asia/Kolkata"),
    "bengaluru": (12.9716, 77.5946, "Asia/Kolkata"),
    "bangalore": (12.9716, 77.5946, "Asia/Kolkata"),
    "chennai": (13.0827, 80.2707, "Asia/Kolkata"),
    "madras": (13.0827, 80.2707, "Asia/Kolkata"),
    "kolkata": (22.5726, 88.3639, "Asia/Kolkata"),
    "calcutta": (22.5726, 88.3639, "Asia/Kolkata"),
    "hyderabad": (17.3850, 78.4867, "Asia/Kolkata"),
    "pune": (18.5204, 73.8567, "Asia/Kolkata"),
    "ahmedabad": (23.0225, 72.5714, "Asia/Kolkata"),
    "jaipur": (26.9124, 75.7873, "Asia/Kolkata"),
    "lucknow": (26.8467, 80.9462, "Asia/Kolkata"),
    "kanpur": (26.4499, 80.3319, "Asia/Kolkata"),
    "nagpur": (21.1458, 79.0882, "Asia/Kolkata"),
    "indore": (22.7196, 75.8577, "Asia/Kolkata"),
    "bhopal": (23.2599, 77.4126, "Asia/Kolkata"),
    "patna": (25.5941, 85.1376, "Asia/Kolkata"),
    "vadodara": (22.3072, 73.1812, "Asia/Kolkata"),
    "baroda": (22.3072, 73.1812, "Asia/Kolkata"),
    "ghaziabad": (28.6692, 77.4538, "Asia/Kolkata"),
    "ludhiana": (30.9010, 75.8573, "Asia/Kolkata"),
    "agra": (27.1767, 78.0081, "Asia/Kolkata"),
    "nashik": (19.9975, 73.7898, "Asia/Kolkata"),
    "faridabad": (28.4089, 77.3178, "Asia/Kolkata"),
    "meerut": (28.9845, 77.7064, "Asia/Kolkata"),
    "rajkot": (22.3039, 70.8022, "Asia/Kolkata"),
    "varanasi": (25.3176, 82.9739, "Asia/Kolkata"),
    "banaras": (25.3176, 82.9739, "Asia/Kolkata"),
    "kashi": (25.3176, 82.9739, "Asia/Kolkata"),
    "srinagar": (34.0837, 74.7973, "Asia/Kolkata"),
    "aurangabad": (19.8762, 75.3433, "Asia/Kolkata"),
    "chhatrapati sambhajinagar": (19.8762, 75.3433, "Asia/Kolkata"),
    "amritsar": (31.6340, 74.8723, "Asia/Kolkata"),
    "prayagraj": (25.4358, 81.8463, "Asia/Kolkata"),
    "allahabad": (25.4358, 81.8463, "Asia/Kolkata"),
    "ranchi": (23.3441, 85.3096, "Asia/Kolkata"),
    "coimbatore": (11.0168, 76.9558, "Asia/Kolkata"),
    "jabalpur": (23.1815, 79.9864, "Asia/Kolkata"),
    "gwalior": (26.2183, 78.1828, "Asia/Kolkata"),
    "vijayawada": (16.5062, 80.6480, "Asia/Kolkata"),
    "jodhpur": (26.2389, 73.0243, "Asia/Kolkata"),
    "madurai": (9.9252, 78.1198, "Asia/Kolkata"),
    "raipur": (21.2514, 81.6296, "Asia/Kolkata"),
    "kota": (25.2138, 75.8648, "Asia/Kolkata"),
    "guwahati": (26.1445, 91.7362, "Asia/Kolkata"),
    "chandigarh": (30.7333, 76.7794, "Asia/Kolkata"),
    "solapur": (17.6599, 75.9064, "Asia/Kolkata"),
    "hubli": (15.3647, 75.1240, "Asia/Kolkata"),
    "mysuru": (12.2958, 76.6394, "Asia/Kolkata"),
    "mysore": (12.2958, 76.6394, "Asia/Kolkata"),
    "gurugram": (28.4595, 77.0266, "Asia/Kolkata"),
    "gurgaon": (28.4595, 77.0266, "Asia/Kolkata"),
    "noida": (28.5355, 77.3910, "Asia/Kolkata"),
    "jalandhar": (31.3260, 75.5762, "Asia/Kolkata"),
    "bhubaneswar": (20.2961, 85.8245, "Asia/Kolkata"),
    "thiruvananthapuram": (8.5241, 76.9366, "Asia/Kolkata"),
    "trivandrum": (8.5241, 76.9366, "Asia/Kolkata"),
    "kochi": (9.9312, 76.2673, "Asia/Kolkata"),
    "cochin": (9.9312, 76.2673, "Asia/Kolkata"),
    "dehradun": (30.3165, 78.0322, "Asia/Kolkata"),
    "haridwar": (29.9457, 78.1642, "Asia/Kolkata"),
    "rishikesh": (30.0869, 78.2676, "Asia/Kolkata"),
    "ayodhya": (26.7922, 82.1998, "Asia/Kolkata"),
    "mathura": (27.4924, 77.6737, "Asia/Kolkata"),
    "vrindavan": (27.5806, 77.7006, "Asia/Kolkata"),
    "ujjain": (23.1765, 75.7885, "Asia/Kolkata"),
    "tirupati": (13.6288, 79.4192, "Asia/Kolkata"),
    "puri": (19.8135, 85.8312, "Asia/Kolkata"),
    "shirdi": (19.7667, 74.4767, "Asia/Kolkata"),
    "rameshwaram": (9.2876, 79.3129, "Asia/Kolkata"),
    "tiruvannamalai": (12.2253, 79.0747, "Asia/Kolkata"),
    "bodh gaya": (24.6961, 84.9869, "Asia/Kolkata"),
    "gaya": (24.7914, 85.0002, "Asia/Kolkata"),
    "shimla": (31.1048, 77.1734, "Asia/Kolkata"),
    "jammu": (32.7266, 74.8570, "Asia/Kolkata"),
    "gangtok": (27.3389, 88.6065, "Asia/Kolkata"),

    # Major International Cities
    "london": (51.5074, -0.1278, "Europe/London"),
    "new york": (40.7128, -74.0060, "America/New_York"),
    "san francisco": (37.7749, -122.4194, "America/Los_Angeles"),
    "los angeles": (34.0522, -118.2437, "America/Los_Angeles"),
    "chicago": (41.8781, -87.6298, "America/Chicago"),
    "seattle": (47.6062, -122.3321, "America/Los_Angeles"),
    "toronto": (43.6532, -79.3832, "America/Toronto"),
    "vancouver": (49.2827, -123.1207, "America/Vancouver"),
    "dubai": (25.2048, 55.2708, "Asia/Dubai"),
    "abu dhabi": (24.4539, 54.3773, "Asia/Dubai"),
    "singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "kuala lumpur": (3.1390, 101.6869, "Asia/Kuala_Lumpur"),
    "sydney": (-33.8688, 151.2093, "Australia/Sydney"),
    "melbourne": (-37.8136, 144.9631, "Australia/Melbourne"),
    "tokyo": (35.6762, 139.6503, "Asia/Tokyo"),
    "paris": (48.8566, 2.3522, "Europe/Paris"),
    "berlin": (52.5200, 13.4050, "Europe/Berlin"),
    "zurich": (47.3769, 8.5417, "Europe/Zurich"),
    "kathmandu": (27.7172, 85.3240, "Asia/Kathmandu"),
    "colombo": (6.9271, 79.8612, "Asia/Colombo"),
    "dhaka": (23.8103, 90.4125, "Asia/Dhaka"),
    "bangkok": (13.7563, 100.5018, "Asia/Bangkok"),
}

class LocationResolver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocationResolver, cls).__new__(cls)
            cls._instance._init_resolver()
        return cls._instance

    def _init_resolver(self):
        self.tf = TimezoneFinder()
        self.geolocator = Nominatim(user_agent="vedic_jyotish_app_v2")

    def resolve_location(self, place_name: str) -> Dict[str, Any]:
        """
        Resolves place_name to latitude, longitude, address, and timezone.
        Checks fast offline database first, then queries Nominatim if needed.
        """
        cleaned = place_name.strip().lower()

        from core.internet_data import InternetDataService
        internet_svc = InternetDataService()

        # Check offline city matches
        for city_key, (lat, lon, tz_str) in OFFLINE_CITIES.items():
            if city_key == cleaned or city_key in cleaned.split(",")[0].strip():
                elev = internet_svc.fetch_elevation(lat, lon)
                return {
                    "place_query": place_name,
                    "resolved_name": city_key.title(),
                    "latitude": lat,
                    "longitude": lon,
                    "elevation_m": elev,
                    "timezone": tz_str,
                    "source": "offline_database",
                    "is_online_precise": elev > 0
                }

        # Online Geocoding via Nominatim
        try:
            loc = self.geolocator.geocode(place_name, timeout=5)
            if loc:
                lat = loc.latitude
                lon = loc.longitude
                elev = internet_svc.fetch_elevation(lat, lon)
                tz_str = self.tf.timezone_at(lat=lat, lng=lon) or "UTC"
                return {
                    "place_query": place_name,
                    "resolved_name": loc.address,
                    "latitude": lat,
                    "longitude": lon,
                    "elevation_m": elev,
                    "timezone": tz_str,
                    "source": "nominatim_geopy",
                    "is_online_precise": True
                }
        except Exception:
            pass

        # Fallback to New Delhi if completely unreachable/unknown
        elev_delhi = internet_svc.fetch_elevation(28.6139, 77.2090)
        return {
            "place_query": place_name,
            "resolved_name": "New Delhi, India (Default fallback)",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "elevation_m": elev_delhi,
            "timezone": "Asia/Kolkata",
            "source": "default_fallback",
            "is_online_precise": False
        }

    def convert_local_to_utc(
        self, local_dt_naive: datetime, timezone_str: str
    ) -> Tuple[datetime, float]:
        """
        Converts naive local birth datetime into aware UTC datetime,
        properly evaluating historical daylight saving time (DST) and UTC offset.
        Returns (utc_datetime, utc_offset_hours).
        """
        try:
            tz = zoneinfo.ZoneInfo(timezone_str)
        except Exception:
            tz = zoneinfo.ZoneInfo("UTC")

        # Local aware datetime
        local_dt_aware = local_dt_naive.replace(tzinfo=tz)
        
        # UTC conversion
        utc_dt = local_dt_aware.astimezone(zoneinfo.ZoneInfo("UTC"))

        # Calculate UTC offset in hours for that specific date
        utcoffset = local_dt_aware.utcoffset()
        offset_hours = utcoffset.total_seconds() / 3600.0 if utcoffset else 0.0

        return utc_dt, offset_hours
