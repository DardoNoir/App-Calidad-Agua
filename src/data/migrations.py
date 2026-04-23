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
    nombreUsuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('Administrador','Usuario')),
    ultimoInicio TIMESTAMP,
    idMunicipio INTEGER,
    FOREIGN KEY (idMunicipio) REFERENCES municipio(id)
);

CREATE TABLE IF NOT EXISTS lugar (
    id SERIAL PRIMARY KEY,
    provincia TEXT,
    ciudad TEXT,
    cuerpoAgua TEXT,
    zona TEXT,
    UNIQUE(provincia, ciudad, cuerpoAgua, zona)
);

CREATE TABLE IF NOT EXISTS parametro (
    id SERIAL PRIMARY KEY,
    codigo TEXT UNIQUE NOT NULL,
    nombreParametro TEXT NOT NULL,
    unidad TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS valorReferencia (
    id SERIAL PRIMARY KEY,
    idParametro INTEGER NOT NULL,
    limiteMaxAceptable REAL,
    limiteMinAceptable REAL,
    limiteMaxWarning REAL,
    limiteMinWarning REAL,
    normativa TEXT,
    rangoPosibleMin REAL,
    rangoPosibleMax REAL,
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS medicion (
    id SERIAL PRIMARY KEY,
    idLugar INTEGER NOT NULL,
    fechaMedicion TIMESTAMP NOT NULL,
    medidaTomadaPor INTEGER NOT NULL,
    comentarios TEXT,
    ica REAL,
    clasificacionICA TEXT,
    cargadaSistema TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idMunicipio INTEGER,
    FOREIGN KEY (idLugar) REFERENCES lugar(id),
    FOREIGN KEY (medidaTomadaPor) REFERENCES usuario(id),
    FOREIGN KEY (idMunicipio) REFERENCES municipio(id)
);

CREATE TABLE IF NOT EXISTS valorMedida (
    id SERIAL PRIMARY KEY,
    idMedicion INTEGER NOT NULL,
    idParametro INTEGER NOT NULL,
    valor REAL,
    estado TEXT,
    desviacion TEXT,
    FOREIGN KEY (idMedicion) REFERENCES medicion(id),
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS movimiento (
    id SERIAL PRIMARY KEY,
    idUsuario INTEGER NOT NULL,
    accion TEXT,
    tablaCambiada TEXT,
    idRegistro INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    FOREIGN KEY (idUsuario) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS ponderacionParametro (
    id SERIAL PRIMARY KEY,
    idParametro INTEGER NOT NULL,
    ponderacion REAL NOT NULL CHECK (ponderacion >= 0 AND ponderacion <= 1),
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS curvaSubindice (
    id SERIAL PRIMARY KEY,
    idParametro INTEGER NOT NULL,
    valor REAL NOT NULL,
    subindice REAL NOT NULL,
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
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