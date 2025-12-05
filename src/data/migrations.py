import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

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
limiteMaxWarning REAL,
normativa TEXT,
FOREIGN KEY (idParametro) REFERENCES parametro(id)
);

CREATE TABLE IF NOT EXISTS medicion(
id INTEGER PRIMARY KEY AUTOINCREMENT,
idLugar INTEGER NOT NULL,
fechaMedicion DATETIME NOT NULL,
medidaTomadaPor INTEGER NOT NULL,
comentarios TEXT,
estadoGeneral TEXT,
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

"""
def run_migrations(db_path: str | None = None):
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(DDL)
    conn.commit()
    conn.close()
    print(f"Migration ran. DB en: {path}")

if __name__ == "__main__":
    run_migrations()

