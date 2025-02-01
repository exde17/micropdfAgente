# app/db_connection.py
import psycopg2
import os

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "evaluation"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "G@t3w@yTI-31416"),
            host=os.getenv("DB_HOST", "129.213.167.145"),
            port=os.getenv("DB_PORT", "5432")
        )
        print("✅ Conexión exitosa a la base de datos.")
        return conn
    except Exception as e:
        print("❌ Error al conectar:", e)
        return None
