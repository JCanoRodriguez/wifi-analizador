# analizador_wifi.py

import sys
from utils import ejecutar_comando, es_root, interpretar_senal, limpiar_texto
from prettytable import PrettyTable

ROJO     = "\033[91m"
VERDE    = "\033[92m"
AMARILLO = "\033[93m"
RESET    = "\033[0m"


def verificar_root():
    if not es_root():
        print(f"{ROJO}Error: se requieren permisos de administrador.{RESET}")
        print("Ejecuta con: sudo python3 analizador_wifi.py")
        sys.exit(1)


def obtener_interfaz():
    salida = ejecutar_comando(["iw", "dev"])

    if not salida:
        print(f"{ROJO}No se pudo ejecutar 'iw'. ¿Está instalado?{RESET}")
        sys.exit(1)

    for linea in salida.splitlines():
        if "Interface" in linea:
            return limpiar_texto(linea.split("Interface")[1])

    print(f"{ROJO}No se encontró ninguna interfaz WiFi.{RESET}")
    sys.exit(1)


def escanear_redes(interfaz):
    print(f"{AMARILLO}Escaneando redes en {interfaz}...{RESET}")

    salida = ejecutar_comando(["iwlist", interfaz, "scan"])

    if not salida or "No scan results" in salida:
        print(f"{ROJO}No se encontraron redes. ¿Está activa la interfaz?{RESET}")
        sys.exit(1)

    return salida


def parsear_redes(salida_cruda):
    redes = []
    red_actual = {}

    for linea in salida_cruda.splitlines():
        linea = limpiar_texto(linea)

        if "Cell" in linea and "Address" in linea:
            if red_actual:
                redes.append(red_actual)
            red_actual = {
                "ssid"      : "Oculta",
                "señal_dbm" : -100,
                "canal"     : "?",
                "frecuencia": "?",
                "seguridad" : "Abierta"
            }

        elif "ESSID" in linea:
            red_actual["ssid"] = linea.split(":")[1].replace('"', '')

        elif "Frequency" in linea and "Channel" in linea:
            partes = linea.split()
            red_actual["frecuencia"] = partes[0].split(":")[1] + " GHz"
            red_actual["canal"] = linea.split("Channel")[1].replace(")", "").strip()

        elif "Signal level" in linea:
            try:
                dbm = int(linea.split("=")[1].split(" ")[0])
                red_actual["señal_dbm"] = dbm
            except:
                pass

        elif "Encryption key:on" in linea:
            red_actual["seguridad"] = "Cifrada"

        elif "WPA2" in linea:
            red_actual["seguridad"] = "WPA2"

        elif "WPA" in linea:
            red_actual["seguridad"] = "WPA"

    if red_actual:
        redes.append(red_actual)

    return redes


def mostrar_tabla(redes):
    tabla = PrettyTable()
    tabla.field_names = ["SSID", "Señal (dBm)", "Calidad", "Canal", "Frecuencia", "Seguridad"]

    redes_ordenadas = sorted(redes, key=lambda r: r["señal_dbm"], reverse=True)

    for red in redes_ordenadas:
        tabla.add_row([
            red["ssid"],
            red["señal_dbm"],
            interpretar_senal(red["señal_dbm"]),
            red["canal"],
            red["frecuencia"],
            red["seguridad"]
        ])

    print(tabla)


def recomendar_canal(redes):
    conteo = {"1": 0, "6": 0, "11": 0}

    for red in redes:
        canal = str(red["canal"])
        if canal in conteo:
            conteo[canal] += 1

    mejor = min(conteo, key=conteo.get)

    print(f"\n{VERDE}[ Recomendación de canal ]{RESET}")
    for canal, cantidad in conteo.items():
        barra = "█" * cantidad if cantidad > 0 else "-"
        print(f"  Canal {canal}: {barra} ({cantidad} redes)")
    print(f"\n  Mejor canal disponible: {VERDE}Canal {mejor}{RESET}")


def main():
    verificar_root()

    interfaz = obtener_interfaz()
    print(f"{VERDE}Interfaz detectada: {interfaz}{RESET}")

    salida_cruda = escanear_redes(interfaz)
    redes = parsear_redes(salida_cruda)

    print(f"\n{VERDE}[ Redes encontradas: {len(redes)} ]{RESET}\n")
    mostrar_tabla(redes)
    recomendar_canal(redes)


if __name__ == "__main__":
    main()