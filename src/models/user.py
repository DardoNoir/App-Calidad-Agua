from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated
from datetime import datetime

NombreUsuario = Annotated[str, StringConstraints(min_length=3, max_length=60)]
Password = Annotated[str, StringConstraints(min_length=5)]
Rol = Annotated[str, StringConstraints(pattern="^(administrador|usuario)$")]

class CreadorUsuario(BaseModel):
    nombreUsuario: NombreUsuario
    password: Password
    rol: Rol

class LecturaUsuario(BaseModel):
    id: int
    nombreUsuario: str
    rol: str
    ultimoInicio: Optional[datetime]


