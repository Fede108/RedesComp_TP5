import socket
import time
import logging

HOST = "192.168.0.10"
PORT = 12345
NUM_PAQUETES = 10
INTERVALO_SEGUNDOS = 1
LOG_FILE = "client.log"

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            logging.info(f"Conectado al servidor {HOST}:{PORT}")
        except Exception as e:
            logging.error(f"No se pudo conectar al servidor: {e}")
            return

        texto_previo = "kiritoro"
        num = 0
        for i in range(NUM_PAQUETES):
            mensaje = f"{texto_previo} {num}"
            logging.info(f"Enviando: {mensaje}")
            try:
                s.sendall(mensaje.encode('utf-8'))
            except Exception as e:
                logging.error(f"Error al enviar paquete: {e}")
                break

            try:
                data = s.recv(1024)
            except Exception as e:
                logging.error(f"Error al recibir respuesta: {e}")
                break

            if not data:
                logging.info("El servidor cerró la conexión inesperadamente.")
                break
            try:
                texto = data.decode('utf-8').strip()
            except UnicodeDecodeError:
                logging.info("Respuesta recibida no es UTF-8, ignorando.")
                continue

            logging.info(f"Recibido del servidor: {texto}")

            if ' ' in texto:
                texto_previo, posible_num = texto.rsplit(' ', 1)
            else:
                texto_previo, posible_num = texto, ""
            try:
                valor = int(posible_num)
            except ValueError:
                logging.warning(f"Respuesta inesperada: {texto}")
                continue

            num = valor + 1
            if i < NUM_PAQUETES - 1:
                time.sleep(INTERVALO_SEGUNDOS)

        logging.info("Cliente finalizó el envío de paquetes.")

if __name__ == "__main__":
    main()
