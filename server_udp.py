# servidor_udp.py
import socket
import logging

HOST = "0.0.0.0"
PORT = 12345
LOG_FILE = "server_udp.log"

def configurar_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        ]
    )

def run_server():
    configurar_logging()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        logging.info(f"Escuchando (UDP) en {HOST}:{PORT}...")
        while True:
            try:
                data, addr = s.recvfrom(1024)
            except Exception as e:
                logging.error(f"Error al recibir datagrama: {e}")
                continue

            if not data:
                logging.info("Datagrama vacío recibido, ignorando.")
                continue

            try:
                texto = data.decode('utf-8').strip()
            except UnicodeDecodeError:
                logging.info(f"Recibido dato no UTF-8 de {addr}, ignorando.")
                continue

            logging.info(f"Recibido de {addr}: {texto}")

            if ' ' in texto:
                texto_previo, posible_num = texto.rsplit(' ', 1)
            else:
                texto_previo, posible_num = texto, ""
            try:
                num = int(posible_num)
                num += 1
                respuesta_texto = f"{texto_previo} {num}"
                respuesta_bytes = respuesta_texto.encode('utf-8')
            except ValueError:
                respuesta_texto = "ERROR: No es un entero válido"
                respuesta_bytes = respuesta_texto.encode('utf-8')

            try:
                s.sendto(respuesta_bytes, addr)
                logging.info(f"Enviado a {addr}: {respuesta_texto}")
            except Exception as e:
                logging.error(f"Error al enviar datagrama a {addr}: {e}")

if __name__ == "__main__":
    run_server()
