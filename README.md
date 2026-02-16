OpenWeatherMap ETL Pipeline with Airflow, Docker, Postgres & Metabase

This is end-to-end containerized data pipeline that ingests daily weather data from the OpenWeatherMap API, loads it into PostgreSQL using Apache Airflow, and visualizes insights through Metabase dashboards.

The goal is to simulate a real-world data engineering workflow including ETL orchestration, database modeling, automation, and analytics visualization.

Project Goal

    The purpose of this project is to showcase how modern data pipelines are built using orchestration tools, containerized infrastructure, and a simple analytics stack.

Key objectives:
    Build a reproducible ETL pipeline using Airflow
    Design a normalized data model (cities + weather_fact)
    Automate data ingestion from an external API
    Demonstrate container-based infrastructure using Docker Compose
    Enable downstream analytics and dashboards via Metabase

Tech Stack
Apache Airflow
    Used for ETL orchestration and scheduling.
    Runs Python tasks that fetch weather data
    Automates daily data ingestion
    Handles retries, logging, and monitoring
PostgreSQL
    Used as the data warehouse/storage layer.
    Stores normalized tables
    Supports analytics queries
    Acts as the central source for dashboards
pgAdmin
    Web-based database GUI.
    Inspect tables and schemas
    Run SQL queries
    Validate ETL results
Metabase
    Used for data visualization and dashboards.
    Connects directly to PostgreSQL
    Builds charts and analytics views
    Demonstrates the analytics layer of the pipeline
Docker
    Provides containerized environments.
    Ensures consistent setup across machines
    Eliminates dependency conflicts
Docker Compose
    Defines and runs the full infrastructure stack:
        Airflow
        PostgreSQL
        pgAdmin
        Metabase

Architecture Overview

    OpenWeather API
            ↓
    Apache Airflow DAG
            ↓
    PostgreSQL (cities + weather_fact)
            ↓
    Metabase Dashboard

    Data flows from an external API → orchestrated by Airflow → stored in Postgres → visualized in Metabase.

Features

    Fetches real-time weather data using latitude/longitude
    Normalized schema for scalable analytics
    Fully containerized infrastructure
    Automated scheduling via Airflow
    Visualization-ready dataset
    Easy setup with a single Docker command

Setup Instructions
    1️⃣ Get an OpenWeatherMap API Key
    Create an account and generate an API key:
    https://openweathermap.org/

    2️⃣ Configure Environment Variables
    Create a .env file based on .env.example.
    Add:
    OPENWEATHER_API_KEY=YOUR_API_KEY

    3️⃣ Start the Services
    From the project root:
    docker compose up --build

    4️⃣ Access the Tools

    Airflow
    http://localhost:8080

    pgAdmin
    http://localhost:5050

    Metabase
    http://localhost:3000
    Use credentials defined in your .env file.

    5️⃣ Run the Pipeline
    Open Airflow UI
    Enable the weather_etl DAG
    Trigger the DAG manually

    6️⃣ Validate the Data
    Using pgAdmin:
    SELECT * FROM cities;
    SELECT * FROM weather_fact ORDER BY recorded_at DESC LIMIT 20;

Project Structure
    dags/
    weather_etl.py

    postgres/
    init.sql

    docker-compose.yml
    generate_city_seed.py
    README.md