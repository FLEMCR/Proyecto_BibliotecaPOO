import os
import hashlib
from modulos.config import archivo_usuarios
from modulos import utilidades

# Crear carpeta si no existe
os.makedirs(os.path.dirname(archivo_usuarios), exist_ok=True)

def _cifrar_clave(clave):
    """Convierte contraseña en código seguro"""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()

def guardar_usuario(usuario, clave):
    clave_segura = _cifrar_clave(clave)
    with open(archivo_usuarios, "a", encoding="utf-8") as f:
        f.write(f"{usuario}:{clave_segura}\n")
    return True

def existe_usuario(usuario):
    if not os.path.exists(archivo_usuarios):
        return False
    with open(archivo_usuarios, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip().startswith(f"{usuario}:"):
                return True
    return False

def validar_credenciales(usuario, clave):
    if not os.path.exists(archivo_usuarios):
        return False
    clave_segura = _cifrar_clave(clave)
    with open(archivo_usuarios, "r", encoding="utf-8") as f:
        for linea in f:
            try:
                u, c = linea.strip().split(":")
                if u == usuario and c == clave_segura:
                    return True
            except:
                continue
    return False

def registrar_usuario():
    utilidades.limpiar_pantalla()
    utilidades.divisor("REGISTRO DE USUARIO")

    # Nombre de usuario
    while True:
        usuario = input("Usuario: ").strip()
        if len(usuario) < 3:
            print(" Mínimo 3 caracteres")
            continue
        if existe_usuario(usuario):
            print(" Ya existe ese usuario")
            continue
        break

    # Contraseña
    while True:
        clave = input("Contraseña: ").strip()
        if len(clave) < 4:
            print("Mínimo 4 caracteres")
            continue
        confirmar = input("Confirmar contraseña: ").strip()
        if clave != confirmar:
            print(" No coinciden")
            continue
        break

    guardar_usuario(usuario, clave)
    print(f"\n Usuario '{usuario}' registrado!")
    utilidades.pausa()
    return usuario

def iniciar_sesion():
    utilidades.limpiar_pantalla()
    utilidades.divisor("INICIO DE SESIÓN")
    intentos = 3

    while intentos > 0:
        usuario = input("Usuario: ").strip()
        clave = input("Contraseña: ").strip()

        if validar_credenciales(usuario, clave):
            print(f"\n Bienvenido, {usuario}!")
            utilidades.pausa()
            return usuario

        intentos -= 1
        if intentos > 0:
            print(f" Datos incorrectos. Intentos: {intentos}\n")
        else:
            print(" Se agotaron los intentos")

    utilidades.pausa()
    return None