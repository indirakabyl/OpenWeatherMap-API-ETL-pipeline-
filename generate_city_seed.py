import os, time, requests

API_KEY = os.environ["OPENWEATHER_API_KEY"]

# Midwest cities, states
CITIES = [
    ("Chicago", "IL"),
    ("Milwaukee", "WI"),
    ("Madison", "WI"),
    ("Minneapolis", "MN"),
    ("Saint Paul", "MN"),
    ("Detroit", "MI"),
    ("Columbus", "OH"),
    ("Cleveland", "OH"),
    ("Cincinnati", "OH"),
    ("Indianapolis", "IN"),
    ("St. Louis", "MO"),
    ("Kansas City", "MO"),
    ("Omaha", "NE"),
    ("Des Moines", "IA"),
    ("Wichita", "KS"),
]

def geocode(city, state):
    q = f"{city},{state},US"
    url = "https://api.openweathermap.org/geo/1.0/direct"
    r = requests.get(url, params={"q": q, "limit": 1, "appid": API_KEY}, timeout=30)
    r.raise_for_status()
    results = r.json()
    if not results:
        raise ValueError(f"No geocoding result for {q}")
    top = results[0]
    return top["name"], top["lat"], top["lon"]

rows = []
for city, state in CITIES:
    name, lat, lon = geocode(city, state)
    rows.append((name, lat, lon))
    time.sleep(1)  # keep it polite; free plan mentions 60 calls/min :contentReference[oaicite:1]{index=1}

print("-- Paste this into postgres/init.sql (seed section):")
print("INSERT INTO cities (city_name, lat, lon) VALUES")
print(",\n".join([f"('{name}', {lat}, {lon})" for name, lat, lon in rows]))
print("ON CONFLICT (city_name) DO UPDATE SET lat=EXCLUDED.lat, lon=EXCLUDED.lon;")
