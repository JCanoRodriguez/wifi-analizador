#!/bin/bash
# iniciar_monitor.sh
# Uso: sudo bash iniciar_monitor.sh wlan0

# --- Verificar root ---
if [ "$EUID" -ne 0 ]; then
    echo "Error: ejecuta con sudo"
    echo "Uso: sudo bash iniciar_monitor.sh wlan0"
    exit 1
fi

# --- Verificar que se pasó un argumento ---
if [ -z "$1" ]; then
    echo "Error: debes indicar la interfaz"
    echo "Uso: sudo bash iniciar_monitor.sh wlan0"
    exit 1
fi

INTERFAZ=$1

# --- Verificar que la interfaz existe ---
if ! iw dev | grep -q "Interface $INTERFAZ"; then
    echo "Error: no se encontró la interfaz '$INTERFAZ'"
    exit 1
fi

# --- Cambiar a modo monitor ---
echo "Configurando $INTERFAZ en modo monitor..."

ip link set "$INTERFAZ" down
iw "$INTERFAZ" set type monitor
ip link set "$INTERFAZ" up

# --- Verificar que el cambio fue exitoso ---
MODO=$(iw dev | grep -A5 "Interface $INTERFAZ" | grep "type" | awk '{print $2}')

if [ "$MODO" = "monitor" ]; then
    echo "Listo. $INTERFAZ está en modo monitor."
else
    echo "Algo salió mal. Modo actual: $MODO"
    exit 1
fi