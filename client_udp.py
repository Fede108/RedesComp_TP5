# client_udp.py
import socket
import time
import logging

HOST = "192.168.0.10"  # IP del servidor UDP
PORT = 12345
NUM_PAQUETES = 10
INTERVALO_SEGUNDOS = 1
LOG_FILE = "client_udp.log"

def configurar_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        ]
    )

def main():
    configurar_logging()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        texto_previo = "kiritoro"
        num = 0
        for i in range(NUM_PAQUETES):
            mensaje = f"{texto_previo} {num}"
            logging.info(f"Enviando a {(HOST, PORT)}: {mensaje}")
            try:
                s.sendto(mensaje.encode('utf-8'), (HOST, PORT))
            except Exception as e:
                logging.error(f"Error al enviar datagrama: {e}")
                break

            data, addr = s.recvfrom(1024)

            if not data:
                logging.info("Respuesta UDP vacía recibida, ignorando.")
                if i < NUM_PAQUETES - 1:
                    time.sleep(INTERVALO_SEGUNDOS)
                continue

            texto = data.decode('utf-8').strip()

            logging.info(f"Recibido de {addr}: {texto}")

            if ' ' in texto:
                texto_previo, posible_num = texto.rsplit(' ', 1)
            else:
                texto_previo, posible_num = texto, ""
            try:
                valor = int(posible_num)
            except ValueError:
                logging.warning(f"Respuesta inesperada: {texto}")
                if i < NUM_PAQUETES - 1:
                    time.sleep(INTERVALO_SEGUNDOS)
                continue

            num = valor + 1
            if i < NUM_PAQUETES - 1:
                time.sleep(INTERVALO_SEGUNDOS)

        logging.info("Cliente UDP finalizó el envío de paquetes.")

if __name__ == "__main__":
    main()
