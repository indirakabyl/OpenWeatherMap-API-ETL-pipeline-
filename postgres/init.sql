-- postgres/init.sql
-- Creates a simple star-schema: cities (dimension) + weather_fact (fact)
-- and seeds 10 UK cities.

CREATE TABLE IF NOT EXISTS cities (
  city_id SERIAL PRIMARY KEY,
  city_name VARCHAR(50) UNIQUE NOT NULL,
  lat DOUBLE PRECISION NOT NULL,
  lon DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_fact (
  weather_id BIGSERIAL PRIMARY KEY,
  city_id INT NOT NULL REFERENCES cities(city_id),
  temperature DOUBLE PRECISION,
  humidity INT,
  weather_description TEXT,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_weather_fact_city_time
  ON weather_fact(city_id, recorded_at);

-- Seed cities (safe to re-run)
INSERT INTO cities (city_name, lat, lon) VALUES
('Chicago', 41.8755616, -87.6244212),
('Milwaukee', 43.0349931, -87.922497),
('Madison', 43.074761, -89.3837613),
('Minneapolis', 44.9772995, -93.2654692),
('Saint Paul', 44.9497487, -93.0931028),
('Detroit', 42.3315509, -83.0466403),
('Columbus', 39.9622601, -83.0007065),
('Cleveland', 41.4996574, -81.6936772),
('Cincinnati', 39.1014537, -84.5124602),
('Indianapolis', 39.7683331, -86.1583502),
('Saint Louis', 38.6319657, -90.2428756),
('Kansas City', 39.100105, -94.5781416),
('Omaha', 41.2587459, -95.9383758),
('Des Moines', 41.5910323, -93.6046655),
('Wichita', 37.6922361, -97.3375448)
ON CONFLICT (city_name) DO UPDATE
SET lat = EXCLUDED.lat,
    lon = EXCLUDED.lon;
