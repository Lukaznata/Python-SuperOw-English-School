from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Limpar versão do Alembic
    conn.execute(text("DELETE FROM alembic_version"))
    conn.commit()
    print("✅ Tabela alembic_version limpa!")

print("\nAgora execute:")
print("alembic revision --autogenerate -m 'Initial complete migration'")
print("alembic upgrade head")