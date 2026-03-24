# instalar_requisitos.sh

echo "=== Actualizando repositorios ==="
sudo apt update

echo "=== Instalando herramientas de red ==="
sudo apt install -y aircrack-ng
sudo apt install -y iw
sudo apt install -y net-tools          
sudo apt install -y wireless-tools
sudo apt install -y network-manager

echo "=== Instalando Python y dependencias ==="
sudo apt install -y python3
sudo apt install -y python3-pip

pip3 install scapy                     # para escaneo de paquetes
pip3 install prettytable               # para mostrar tablas en consola

echo "=== Listo! ==="


