import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DDL = """
CREATE TABLE IF NOT EXISTS municipio (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nombre_usuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('Administrador','Usuario')),
    ultimo_inicio TIMESTAMP,
    id_municipio INTEGER,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id)
);

CREATE TABLE IF NOT EXISTS lugar (
    id SERIAL PRIMARY KEY,
    provincia TEXT,
    ciudad TEXT,
    cuerpo_agua TEXT,
    zona TEXT,
    UNIQUE(provincia, ciudad, cuerpo_agua, zona)
);

CREATE TABLE IF NOT EXISTS parametro (
    id SERIAL PRIMARY KEY,
    codigo TEXT UNIQUE NOT NULL,
    nombre_parametro TEXT NOT NULL,
    unidad TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS valor_referencia (
    id SERIAL PRIMARY KEY,
    id_parametro INTEGER NOT NULL,
    limite_max_aceptable REAL,
    limite_min_aceptable REAL,
    limite_max_warning REAL,
    limite_min_warning REAL,
    normativa TEXT,
    rango_posible_min REAL,
    rango_posible_max REAL,
    FOREIGN KEY (id_parametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS medicion (
    id SERIAL PRIMARY KEY,
    id_lugar INTEGER NOT NULL,
    fecha_medicion TIMESTAMP NOT NULL,
    medida_tomada_por INTEGER NOT NULL,
    comentarios TEXT,
    ica REAL,
    clasificacion_ica TEXT,
    cargada_sistema TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_municipio INTEGER,
    FOREIGN KEY (id_lugar) REFERENCES lugar(id),
    FOREIGN KEY (medida_tomada_por) REFERENCES usuario(id),
    FOREIGN KEY (id_municipio) REFERENCES municipio(id)
);

CREATE TABLE IF NOT EXISTS valor_medida (
    id SERIAL PRIMARY KEY,
    id_medicion INTEGER NOT NULL,
    id_parametro INTEGER NOT NULL,
    valor REAL,
    estado TEXT,
    desviacion TEXT,
    FOREIGN KEY (id_medicion) REFERENCES medicion(id),
    FOREIGN KEY (id_parametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS ponderacion_parametro (
    id SERIAL PRIMARY KEY,
    id_parametro INTEGER NOT NULL,
    ponderacion REAL NOT NULL CHECK (ponderacion >= 0 AND ponderacion <= 1),
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (id_parametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS curva_subindice (
    id SERIAL PRIMARY KEY,
    id_parametro INTEGER NOT NULL,
    valor REAL NOT NULL,
    subindice REAL NOT NULL,
    FOREIGN KEY (id_parametro) REFERENCES parametro(id)
);
"""

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode=os.getenv("DB_SSLMODE")
    )

def run_migrations():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(DDL)
        conn.commit()
        print("✅ Migraciones ejecutadas correctamente en PostgreSQL (Supabase)")
    except Exception as e:
        conn.rollback()
        print("❌ Error en migraciones:", e)
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    run_migrations()