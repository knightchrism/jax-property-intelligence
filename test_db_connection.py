import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()

cursor.execute("SELECT PostGIS_Version();")

version = cursor.fetchone()

print("Connected to PostgreSQL.")
print("PostGIS Version:", version[0])

cursor.close()
