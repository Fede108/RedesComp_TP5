import socket
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = "0.0.0.0"
PORT = 12345
LOG_FILE = "server.log"



# Generar claves publicas y privadas
def generar_claves_rsa(ruta_privada="private.pem", ruta_publica="public.pem", tamaño=2048):
    key = RSA.generate(tamaño)
    private_key = key.export_key()
    public_key  = key.publickey().export_key()
    # Guardar en archivos
    with open(ruta_privada, "wb") as f:
        f.write(private_key)
    with open(ruta_publica, "wb") as f:
        f.write(public_key)
    print(f"Claves RSA generadas:\n - Privada: {ruta_privada}\n - Pública: {ruta_publica}")

def get_public_key(ruta_publica="public.pem"):
    with open(ruta_publica, "rb") as f:
        return f.read()  # bytes PEM

# Función para descifrar la clave de sesión en el servidor usando RSA privada
def descifrar_clave_sesion_con_rsa(enc_session_key, ruta_privada="private.pem"):
    with open(ruta_privada, "rb") as f:
        private_pem = f.read()  # bytes PEM
    private_key     = RSA.import_key(private_pem)  # ahora es RsaKey
    cipher_rsa      = PKCS1_OAEP.new(private_key)
    session_key     = cipher_rsa.decrypt(enc_session_key)
    return session_key

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

def run_server():
    configurar_logging()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Escuchando en {HOST}:{PORT}...")
        conn, addr = s.accept()

        with conn:
            logging.info(f"Conectado por {addr}")
            public_key = get_public_key()
            conn.sendall(public_key)
            enc_session_key = conn.recv(256)
            logging.info(f"Sesion key encriptada recibida {addr}")
            session_key = descifrar_clave_sesion_con_rsa(enc_session_key)
            logging.info(f"Sesion key {session_key.hex()}")

            while True:
                data       = conn.recv(1024)
                nonce      = data[:8]
                ciphertext = data[8:]
                data       = descifrar_payload(nonce,ciphertext,session_key)
                if not data:
                    logging.info("Cliente desconectado, cerrando servidor.")
                    break
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

                nonce, ciphertext = cifrar_payload(respuesta_bytes,session_key)
                conn.sendall(nonce + ciphertext)

                logging.info(f"Enviado a {addr}: {respuesta_texto}")

if __name__ == "__main__":
    generar_claves_rsa()
    run_server()
