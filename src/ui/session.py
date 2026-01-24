from dataclasses import dataclass
from typing import Optional

@dataclass
class SesionUsuario:
    id: int
    nombreUsuario: str
    rol: str

currentUser: Optional[SesionUsuario]=None
