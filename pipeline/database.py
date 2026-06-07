import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(url)

def init_db():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS flights (
                id SERIAL PRIMARY KEY,
                flight_id VARCHAR(20), callsign VARCHAR(20),
                aircraft_type VARCHAR(20), category CHAR(1),
                wake_class VARCHAR(10), lat FLOAT, lon FLOAT,
                altitude_ft FLOAT, speed_kt FLOAT, heading_deg FLOAT,
                vertical_rate FLOAT, squawk VARCHAR(4),
                priority VARCHAR(20), eta_min FLOAT,
                timestamp TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sequences (
                id SERIAL PRIMARY KEY,
                scenario VARCHAR(30), algorithm VARCHAR(30),
                total_wait_min FLOAT, avg_wait_min FLOAT,
                n_flights INT, created_at TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.commit()
    print("✅ Base de données initialisée")

def save_flights(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql("flights", engine, if_exists="append", index=False)
    print(f"✅ {len(df)} vols sauvegardés")

def load_flights(limit=100) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(
        f"SELECT * FROM flights ORDER BY timestamp DESC LIMIT {limit}",
        engine
    )