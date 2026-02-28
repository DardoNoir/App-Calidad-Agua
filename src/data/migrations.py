import sqlite3
from pathlib import Path

# Ruta del archivo de base de datos (igual que en db.py)
DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

# Script SQL que crea todas las tablas necesarias para el sistema.
# Cada CREATE TABLE usa IF NOT EXISTS para evitar errores si la tabla ya existe.
DDL = """
CREATE TABLE IF NOT EXISTS usuario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreUsuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('Administrador','Usuario')),
    ultimoInicio DATETIME
);

CREATE TABLE IF NOT EXISTS lugar(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT,
    ciudad TEXT,
    cuerpoAgua TEXT,
    zona TEXT,
    UNIQUE(provincia, ciudad, cuerpoAgua)
);

CREATE TABLE IF NOT EXISTS parametro(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nombreParametro TEXT NOT NULL,
    unidad TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS valorReferencia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

CREATE TABLE IF NOT EXISTS medicion(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idLugar INTEGER NOT NULL,
    fechaMedicion DATETIME NOT NULL,
    medidaTomadaPor INTEGER NOT NULL,
    comentarios TEXT,
    ica REAL,
    clasificacionICA TEXT,
    cargadaSistema DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idLugar) REFERENCES lugar(id),
    FOREIGN KEY (medidaTomadaPor) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS valorMedida(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idMedicion INTEGER NOT NULL,
    idParametro INTEGER NOT NULL,
    valor REAL,
    estado TEXT,
    desviacion TEXT,
    FOREIGN KEY (idMedicion) REFERENCES medicion(id),
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS movimiento(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idUsuario INTEGER NOT NULL,
    accion TEXT,
    tablaCambiada TEXT,
    idRegistro INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    FOREIGN KEY (idUsuario) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS ponderacionParametro(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idParametro INTEGER NOT NULL,
    ponderacion REAL NOT NULL CHECK (ponderacion >= 0 AND ponderacion <= 1),
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);  

CREATE TABLE IF NOT EXISTS curvaSubindice(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idParametro INTEGER NOT NULL,
    valor REAL NOT NULL,
    subindice REAL NOT NULL,
    FOREIGN KEY (idParametro) REFERENCES parametro(id)
);
"""

def run_migrations(db_path: str | None = None):
    """
    Ejecuta el script DDL para crear las tablas.

    ✔ Abre la base
    ✔ Crea las tablas si no existen
    ✔ Cierra la base
    """
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(DDL)  # Ejecuta todo el SQL de una vez
    conn.commit()
    conn.close()
    print(f"Migration ran. DB en: {path}")

# Permite ejecutar: python migrations.py
if __name__ == "__main__":
    run_migrations()
