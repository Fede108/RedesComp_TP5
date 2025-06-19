# Trabajo práctico 5

*Facultad de Ciencias Exactas, Fisicas y Naturales de la U.N.C**

**Redes de Computadoras**

**Profesores**
- Santiago M. Henn
- Facundo N. Oliva C.
  
**Nombre del grupo : Kiritoro** 

**Integrantes**
- Federico Cechich
- Juan Manuel Ferrero
- Luciano Trachta


**19 de Junio de 2025**


**Información de contacto**:  _juan.manuel.ferrero@mi.unc.edu.ar_, _federico.cechich@mi.unc.edu.ar_, _ltrachta@mi.unc.edu.ar_ 

---

## Marco Teórico

### 1. Capa de Transporte en Redes
La capa de transporte es la responsable de entregar datos de extremo a extremo entre procesos en diferentes hosts. Sus dos protocolos principales son **TCP** y **UDP**.

#### 1.1. Protocolo TCP (Transmission Control Protocol)
- **Orientado a conexión**: establece un “handshake” de 3 pasos (SYN, SYN‑ACK, ACK) antes de transferir datos.
- **Fiabilidad**: garantiza la entrega y orden de los bytes mediante:
  - Números de secuencia (Sequence Number)
  - Acuses de recibo (Acknowledgment Number)
  - Control de congestión y flujo (Window Size, algoritmos TCP Tahoe/Reno/CUBIC)
- **Estructura de segmento**:
  - Encabezado mínimo de 20 bytes (más opciones si existen).
  - Campos clave:  
    - **Sequence Number**, **Ack Number**  
    - **Flags**: SYN, ACK, FIN, PSH, RST, URG  
    - **Window Size**, **Checksum**, **Urgent Pointer**, **Opciones**  
  - **Payload**: datos de usuario que siguen al encabezado.
- **Ventajas**: entrega fiable, control de congestión, control de flujo.  
- **Desventajas**: sobrecarga de control y mayor latencia/jitter en entornos con pérdidas.

#### 1.2. Protocolo UDP (User Datagram Protocol)
- **Sin conexión**: no hay establecimiento ni cierre de sesión.
- **No fiable**: no garantiza entrega, orden ni detección de duplicados.
- **Estructura de datagrama**:
  - Encabezado fijo de 8 bytes.
  - Campos:  
    - **Puerto origen** y **puerto destino**  
    - **Longitud** (header + payload)  
    - **Checksum** (opcional para IPv4, obligatorio en IPv6)  
  - **Payload**: datos de usuario inmediatamente tras los 8 bytes.
- **Ventajas**: baja latencia, baja sobrecarga.  
- **Desventajas**: sin garantías de entrega ni orden.

---

### 2. Análisis de Tráfico y Captura de Paquetes
- **Wireshark**: herramienta gráfica para capturar y analizar paquetes en vivo o desde archivos `.pcap`.
  - Panel de capas: muestra Ethernet → IP → TCP/UDP → Data.
  - **Payload**: bytes resaltados después de todos los encabezados, en la vista hexa‑ASCII.
- **Identificación de carga útil**:  
  1. Seleccionar el paquete en la lista.  
  2. Expandir la sección “TCP segment data” o “Data” / “User Datagram Protocol → Data”.  
  3. Observar el offset y la conversión ASCII para leer el contenido.

---

### 3. Métricas de Rendimiento

Para evaluar la calidad de la transmisión de paquetes:

- **Latencia (RTT – Round‑Trip Time)**  
  - `L_i = T_{recv,i} - T_{send,i}`  
  - **Promedio**: `L_{avg} = (1/N) · Σ_{i=1}^N L_i`  
  - **Mínima**: `L_{min} = min_i L_i`  
  - **Máxima**: `L_{max} = max_i L_i`

- **Jitter**  
  Variación absoluta entre latencias sucesivas:  
  `J = (1/(N-1)) · Σ_{i=2}^N |L_i - L_{i-1}|`

- **Registro y Timestamps**  
  - Almacenar en log: identificador de paquete + timestamp ISO 8601  
  - Permite calcular métricas posteriores en local o con scripts externos.

---

### 4. Librerías de Networking
- **Sockets BSD** (C/Python/Java/etc.): abstracción básica de puertos y direcciones.
- **Librerías “net” / “socket”** en distintos lenguajes: permiten `bind()`, `connect()`, `send()`, `recv()`.
- **Parámetros configurables**:  
  - Intervalo de envío (por ej. 1 segundo)  
  - Tamaño de buffer, timeouts, modo no bloqueante.

---

### 5. Criptografía en la Capa de Transporte
#### 5.1. Encriptación Simétrica
- **Descripción**: una misma clave secreta (K) cifra y descifra.
- **Algoritmos comunes**: AES (128/192/256 bits), DES, 3DES, ChaCha20.
- **Ventajas**: rápida, eficiente en CPU, adecuada para grandes volúmenes.
- **Desventajas**: gestión y distribución de la clave, no repudio.

#### 5.2. Encriptación Asimétrica
- **Descripción**: par de claves (pública, privada).  
  - Cifrado con clave pública → solo la privada descifra.
- **Algoritmos comunes**: RSA, ECC (ECDSA, ECDH), Diffie–Hellman.
- **Ventajas**: no requiere canal seguro para clave pública, permite firmas digitales.
- **Desventajas**: más lenta, claves más grandes, mayor consumo de recursos.

#### 5.3. Criptografía Híbrida
1. **Intercambio de clave**: usar asimétrico (Diffie–Hellman o RSA‑OAEP) para compartir una clave simétrica.
2. **Transmisión de datos**: cifrar el payload con AES‑GCM/EAX usando la clave simétrica.

---

### 6. Intercambio de Claves a Distancia
- **Problema**: dos hosts sin información previa quieren comunicarse de forma segura.
- **Solución conceptual**:
  1. Implementar **Diffie–Hellman** para acordar una clave secreta sin enviarla directamente.
  2. Validar identidades con certificados o intercambio de huellas digitales (fingerprints).
  3. Usar la clave DH para cifrar datos con AES y asegurar integridad (GCM, HMAC).

---

### 7. Resumen de Conceptos Clave
| Tema                 | Conceptos Principales                               |
|----------------------|------------------------------------------------------|
| TCP                  | Conexión, fiabilidad, control de flujo/congestión     |
| UDP                  | Datagramas, sin conexión, baja sobrecarga            |
| Captura de paquetes  | Wireshark, capas, payload, hexa‑ASCII                |
| Métricas             | RTT (avg/min/max), jitter, timestamps                |
| Networking Sockets   | APIs `send()`/`recv()`, configuración de intervalos   |
| Encriptación         | Simétrica (AES), Asimétrica (RSA, ECC), híbrida      |
| Intercambio de clave | Diffie–Hellman, certificados, HMAC                   |

---
