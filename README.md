# Analizador de WiFi

Herramienta en Python para análisis y auditoría básica de redes WiFi en Linux.

---

## Estructura del proyecto

wifi-analizador/
│
├── analizador_wifi.py          # Escanea y muestra redes cercanas
├── auditoria_wifi.py           # Genera comandos de auditoría para redes autorizadas
├── utils.py                    # Funciones reutilizables compartidas entre módulos
├── verificar_requisitos.py     # Verifica e instala dependencias del entorno
├── scripts/
│   ├── instalar_requisitos.sh  # Instala herramientas del sistema y librerías Python
│   ├── iniciar_monitor.sh      # Pone la interfaz WiFi en modo monitor
│   └── detener_monitor.sh      # Restaura la interfaz WiFi a modo normal
│
└── README.md

---

## Instalación
```bash
python3 verificar_requisitos.py
```

## Uso

### 1. Analizar redes cercanas
```bash
sudo python3 analizador_wifi.py
```
Muestra una tabla con SSID, señal, canal, frecuencia y seguridad de cada red cercana. Recomienda el canal menos congestionado.

### 2. Auditar una red

Pon la interfaz en modo monitor:
```bash
sudo bash scripts/iniciar_monitor.sh wlan0
```

Ejecuta la auditoría:
```bash
sudo python3 auditoria_wifi.py
```

Al terminar, restaura la interfaz:
```bash
sudo bash scripts/detener_monitor.sh wlan0
```

---

## Aviso ético

Esta herramienta es exclusivamente para uso en redes propias o con autorización explícita del propietario. El uso no autorizado en redes ajenas es ilegal. Los autores no se responsabilizan por el uso indebido de esta herramienta.