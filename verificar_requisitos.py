# verificar_requisitos.py

import shutil
import importlib.util
import subprocess
import sys

VERDE = "\033[92m"
ROJO  = "\033[91m"
RESET = "\033[0m"

def ok(msg):
    print(f"  {VERDE}✓ {msg}{RESET}")

def error(msg):
    print(f"  {ROJO}✗ {msg}{RESET}")

def verificar_herramientas():
    print("\n[ Herramientas del sistema ]")
    herramientas = ["aircrack-ng", "airodump-ng", "iw", "iwconfig", "nmcli"]
    faltantes = []
    for herramienta in herramientas:
        if shutil.which(herramienta):
            ok(herramienta)
        else:
            error(f"{herramienta}  ← no encontrado")
            faltantes.append(herramienta)
    return faltantes

def verificar_librerias():
    print("\n[ Librerías Python ]")
    librerias = ["scapy", "prettytable"]
    faltantes = []
    for lib in librerias:
        if importlib.util.find_spec(lib):
            ok(lib)
        else:
            error(f"{lib}  ← instalar con: pip3 install {lib}")
            faltantes.append(lib)
    return faltantes

def preguntar_instalar():
    while True:
        respuesta = input("  Resolver? [Y/N]: ").strip().lower()
        if respuesta == "y":
            return True
        elif respuesta == "n":
            return False
        else:
            print("  Por favor escribe Y o N")

def instalar_dependencias():
    script = "./scripts/instalar_requisitos.sh"
    print(f"\n  Ejecutando {script}...\n")
    resultado = subprocess.run(["bash", script])
    if resultado.returncode == 0:
        print(f"\n  {VERDE}Instalación completada. Vuelve a ejecutar este script para verificar.{RESET}")
    else:
        print(f"\n  {ROJO}Algo salió mal. Revisa los mensajes arriba.{RESET}")

def main():
    print("=== Verificando requisitos del entorno ===")
    herramientas_faltantes = verificar_herramientas()
    librerias_faltantes    = verificar_librerias()

    print("\n[ Resultado ]")
    if not herramientas_faltantes and not librerias_faltantes:
        print(f"  {VERDE}Entorno listo. Puedes continuar.{RESET}")
    else:
        total = len(herramientas_faltantes) + len(librerias_faltantes)
        print(f"  {ROJO}Faltan {total} dependencia(s).{RESET}\n")
        if preguntar_instalar():
            instalar_dependencias()
        else:
            print(f"\n  {ROJO}Saliendo. Instala las dependencias manualmente para continuar.{RESET}")
            sys.exit(1)

if __name__ == "__main__":
    main()