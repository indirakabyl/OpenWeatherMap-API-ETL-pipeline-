from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2
import os
import logging

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(lat, lon, city_name):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    return {
        "city": city_name,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "recorded_at": datetime.utcnow(),  # timestamp
    }


def store_weather():
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not set")

    conn = psycopg2.connect(
        host="postgres",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur = conn.cursor()

    # Pull from dimension table
    cur.execute("SELECT city_id, city_name, lat, lon FROM cities ORDER BY city_id;")
    cities = cur.fetchall()

    for city_id, city_name, lat, lon in cities:
        try:
            weather = fetch_weather(lat, lon, city_name)
            logging.info(f"Fetched weather for {city_name}: {weather}")

            cur.execute(
                """
                INSERT INTO weather_fact
                  (city_id, temperature, humidity, weather_description, recorded_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    city_id,
                    weather["temperature"],
                    weather["humidity"],
                    weather["description"],
                    weather["recorded_at"],
                ),
            )
            logging.info(f"Inserted weather_fact for {city_name} (city_id={city_id}).")

        except Exception as e:
            logging.error(f"Error with {city_name}: {e}")

    conn.commit()
    cur.close()
    conn.close()


default_args = {"start_date": datetime(2026, 1, 1)}

with DAG(
    dag_id="weather_etl",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    store_weather_task = PythonOperator(
        task_id="store_weather",
        python_callable=store_weather,
    )

    store_weather_task

