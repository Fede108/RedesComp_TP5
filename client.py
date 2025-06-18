import socket
import time
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = "192.168.0.10"
PORT = 12345
NUM_PAQUETES = 10
INTERVALO_SEGUNDOS = 1
LOG_FILE = "client.log"


# Obtener session_key y enc_session_key a partir de public_key del servidor
def cifrar_clave_sesion_con_rsa(public_pem):
    public_key      = RSA.import_key(public_pem)  # ahora es RsaKey
    cipher_rsa      = PKCS1_OAEP.new(public_key)
    session_key     = get_random_bytes(16)  # AES-128
    enc_session_key = cipher_rsa.encrypt(session_key)
    return session_key, enc_session_key

# Cifrado y descifrado de mensajes 
def cifrar_payload(payload_bytes, session_key):
    """
    Cifra payload_bytes con AES-CTR. Devuelve nonce y ciphertext.
    """
    # AES.new con MODE_CTR genera internamente un contador basado en nonce
    nonce = get_random_bytes(8)  # fijo 16 bytes
    cipher = AES.new(session_key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(payload_bytes)
    
    # nonce es necesario para descifrar
    return nonce, ciphertext

def descifrar_payload(nonce, ciphertext, session_key):
    """
    Descifra ciphertext con AES-CTR usando nonce y session_key.
    """
    cipher = AES.new(session_key, AES.MODE_CTR, nonce=nonce)
    datos = cipher.decrypt(ciphertext)
    return datos



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
            data = s.recv(1024)
            logging.info(f"Clave pública recibida: {len(data)} bytes")
            session_key, enc_session_key = cifrar_clave_sesion_con_rsa(data)
            logging.info(f"Session key generada: {session_key.hex()}, ciphertext: {len(enc_session_key)} bytes")
            s.sendall(enc_session_key)
            logging.info(f"Sesion key {session_key.hex()}")

        except Exception as e:
            logging.error(f"No se pudo conectar al servidor: {e}")
            return

        texto_previo = "kiritoro"
        num = 0
        for i in range(NUM_PAQUETES):
            mensaje = f"{texto_previo} {num}"
            logging.info(f"Enviando: {mensaje}")
            try:
                nonce, ciphertext = cifrar_payload(mensaje.encode('utf-8'),session_key)
                s.sendall(nonce + ciphertext)
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
            
            nonce      = data[:8]
            ciphertext = data[8:]
            data       = descifrar_payload(nonce,ciphertext,session_key)

            texto = data.decode('utf-8').strip()
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
