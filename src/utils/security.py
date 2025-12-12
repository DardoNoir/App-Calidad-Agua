import bcrypt 

def hash_password(plain: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve un hash seguro usando bcrypt.
    - Se usa al crear un usuario.
    - El resultado se guarda en la base de datos.
    """
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica si la contraseña ingresada coincide con el hash guardado.
    - Se usa al iniciar sesión.
    """
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
