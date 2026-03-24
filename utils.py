# utils.py

import subprocess
import os

def ejecutar_comando(comando):
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True
        )
        return resultado.stdout
    except FileNotFoundError:
        return None

def es_root():
    return os.geteuid() == 0

def interpretar_senal(dbm):
    if dbm >= -50:
        return "Excelente"
    elif dbm >= -60:
        return "Buena"
    elif dbm >= -70:
        return "Regular"
    elif dbm >= -80:
        return "Debil"
    else:
        return "Sin senal"

def limpiar_texto(texto):
    if texto is None:
        return ""
    return texto.strip()