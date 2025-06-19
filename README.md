# Trabajo práctico 5

*Facultad de Ciencias Exactas, Fisicas y Naturales de la U.N.C*

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

### a) 192.168.0.10 Servidor y 192.168.0.11 Cliente

![image](https://github.com/user-attachments/assets/fb0d2301-c60a-4f16-af68-9603cde5cf2c)

### Carga útil

Dentro de la sección TCP en Wireshark, suele haber una subsección llamada `[TCP segment data]` o simplemente `Data` (dependiendo de la versión). Ahí se encuentra la carga útil del paquete.

En la vista hexadecimal + ASCII (panel inferior), los bytes resaltados que aparecen después de todos los encabezados corresponden al **payload**. Wireshark normalmente colorea o marca estos bytes como "Data".

Por ejemplo, en una captura, en el offset destacado con los valores hexadecimales `6b 69 72 69 74 6f 72 6f 20 34`, en ASCII se lee `"kiritoro 4"` (nombre del grupo más número). Esa es la **carga útil** que tu script envió.

![image](https://github.com/user-attachments/assets/4a1d8b04-4b3e-4e45-9b90-1930bc37a318)

### c) Cálculo de latencias y jitter

Para calcular latencias y jitter a partir del archivo de log, primero se definen las métricas involucradas y luego se extraen los datos registrados en los archivos.

#### Definiciones y fórmulas

**RTT (Round-Trip Time):**  
Es el tiempo que transcurre desde que un cliente envía un paquete hasta que recibe la respuesta correspondiente. Se mide con el mismo reloj del cliente y se calcula como:

Para cada paquete `i`:
- `T_send,i`: instante en que se envió el paquete `i`.
- `T_recv,i`: instante en que se recibió la respuesta correspondiente.

**Latencia (round-trip):**
L_i = T_recv,i - T_send,i

markdown
Copiar
Editar

**Latencia promedio:**
L_avg = (1 / N) * ∑ L_i , para i = 1 hasta N

markdown
Copiar
Editar

**Latencia mínima y máxima:**
L_min = min(L_i), L_max = max(L_i)

**Jitter:**
Se define como la variación entre latencias sucesivas. Una forma común de calcularlo es:
J = (1 / (N - 1)) * ∑ |L_i - L_{i-1}| , para i = 2 hasta N


---

#### Resumen RTT (100 paquetes analizados)

- **RTT promedio:** 0.002760 s  
- **RTT mínima:** 0.001000 s  
- **RTT máxima:** 0.006000 s  
- **Jitter promedio:** 0.000612 s


---

### a) Paquete UDP

Se muestra un paquete UDP capturado. En Wireshark, se resalta la sección **User Datagram Protocol**, y dentro de ella se puede observar la subsección **Data**, donde se encuentra la carga útil del paquete.

![image](https://github.com/user-attachments/assets/a3abf1e0-71d5-4b5e-ad41-fb6dcfe02630)

### c) Cálculo de latencias y jitter

#### Resumen RTT (100 paquetes analizados)

- **RTT promedio:** 0.002520 s  
- **RTT mínima:** 0.001000 s  
- **RTT máxima:** 0.004000 s  
- **Jitter promedio:** 0.000531 s  

---

### Comparación entre paquetes UDP y TCP

**Carga útil:**

- **UDP:** La carga útil comienza tras los 8 bytes de encabezado UDP.  
  El campo `Length` indica el total de bytes del segmento UDP, donde una parte corresponde al payload.  
  No hay campos de secuencia ni flags.

- **TCP:** La carga útil comienza tras los 20 bytes (o más, si hay opciones) del encabezado TCP.  
  Se incluyen campos como:
  - `Seq=...`, `Ack=...`
  - `Flags=ACK+PSH`, `Window=...`
  - Si hay opciones, el encabezado puede superar los 20 bytes.

---

#### Qué observar al comparar

**Longitudes de encabezado:**
- **UDP:** Siempre 8 bytes.
- **TCP:** Mínimo 20 bytes, pero puede ser mayor si incluye opciones (por ejemplo, Timestamps).

**Campos exclusivos de TCP:**
- `Sequence Number`
- `Acknowledgment Number`
- `Flags` (SYN, ACK, FIN, RST, PSH, URG, etc.)
- `Window Size`
- `Urgent Pointer`
- `Options`

**Campos de UDP:**
- `Puerto origen`
- `Puerto destino`
- `Longitud`
- `Checksum`

**Cálculo del offset al payload en la trama cruda (raw frame):**
- **UDP:** El payload comienza después de `(Encabezado Ethernet + IP header + 8 bytes UDP)`.
- **TCP:** El payload comienza después de `(Encabezado Ethernet + IP header + longitud del encabezado TCP)`.

![image](https://github.com/user-attachments/assets/81d656db-d808-4db4-aecf-a682102e7b1a)
![image](https://github.com/user-attachments/assets/f099a45b-429e-469d-8c58-62112972f722)

## Comparativa de Métricas TCP vs UDP

| Métrica              | TCP       | UDP       |
|----------------------|-----------|-----------|
| Paquetes considerados| 100       | 100       |
| RTT promedio (s)     | 0.002760  | 0.002520  |
| RTT mínima (s)       | 0.001000  | 0.001000  |
| RTT máxima (s)       | 0.006000  | 0.004000  |
| Jitter promedio (s)  | 0.000612  | 0.000531  |

### Interpretación de resultados

- El **RTT promedio** es ligeramente menor en UDP (0.00252 s vs. 0.00276 s). Esto puede deberse a la menor sobrecarga de control de conexión en UDP.
- La **RTT máxima** es más alta en TCP (0.006 s vs. 0.004 s), probablemente por retransmisiones o control de congestión.
- El **jitter promedio** también es algo mayor en TCP, reflejando mayor variabilidad en la transmisión.
- La **RTT mínima** es igual en ambos protocolos (0.001 s), lo que indica que en condiciones óptimas ambos alcanzan rendimientos similares.

### Consideraciones adicionales

- **Confiabilidad vs. latencia:**  
  UDP ofrece menor latencia pero **sin garantías de entrega ni orden**.  
  TCP asegura la entrega y el orden, pero introduce retransmisiones y control de congestión, lo que puede aumentar RTT y jitter bajo pérdida de paquetes.

---

## 4) Encriptación

### a)  Encriptación Simétrica

**Características:**
- Utiliza una única clave secreta para cifrar y descifrar datos.
- La clave debe ser conocida por emisor y receptor previamente.
- Es mucho más rápida y eficiente, ideal para grandes volúmenes de datos.

**Ventajas:**
- Bajo consumo de recursos.
- Alta velocidad de cifrado/descifrado.
- Sencillez en la implementación.

**Desventajas:**
- El mayor problema es la distribución de la clave: si se intercepta, se compromete toda la comunicación.
- No permite firmas digitales ni autenticación (cualquiera con la clave puede cifrar/descifrar).

**Algoritmos comunes:**
- AES (128, 192, 256 bits), DES, 3DES, Blowfish, ChaCha20.

---

###  Encriptación Asimétrica

**Características:**
- Utiliza un par de claves: una pública (para cifrar) y una privada (para descifrar).
- La clave pública puede compartirse libremente, la privada debe mantenerse en secreto.

**Ventajas:**
- No requiere compartir claves privadas, lo que mejora la seguridad.
- Permite firmas digitales, autenticación y no repudio.
- Escalable para redes grandes y sistemas distribuidos.

**Desventajas:**
- Es mucho más lenta y consume más recursos que la encriptación simétrica.
- Las claves son de gran tamaño (ej. RSA de 2048 bits o más).
- Si se pierde la clave privada, no es posible recuperar la información cifrada.

**Algoritmos comunes:**
- RSA, ECC, DSA, Diffie-Hellman.

---

###  Ejemplo mixto: Modelo híbrido

La mayoría de los sistemas modernos usan un esquema híbrido:
1. Utilizan **encriptación asimétrica (RSA)** para intercambiar de forma segura una clave simétrica.
2. Luego, se usa esa **clave simétrica (AES)** para cifrar los datos de la sesión.

Esto combina:
- La **seguridad de la criptografía asimétrica** para el inicio del canal.
- La **eficiencia de la criptografía simétrica** para el volumen de datos.

---

### Tabla comparativa

| Característica        | Encriptación Simétrica | Encriptación Asimétrica         |
|-----------------------|------------------------|----------------------------------|
| Claves                | Una sola compartida    | Par (pública + privada)          |
| Rendimiento           | Muy rápida y eficiente | Lenta y costosa computacionalmente |
| Distribución          | Difícil y riesgosa     | Clave pública libre              |
| Seguridad             | Depende del secreto    | Alta (clave privada protegida)   |
| Escalabilidad         | Limitada               | Excelente en sistemas distribuidos |
| Funcionalidades extra | Confidencialidad       | Confidencialidad + firma digital |

---

### b)  Librería utilizada: PyCryptodome

Se seleccionó la librería **PyCryptodome**, que permite implementar cifrado **simétrico (AES)** y **asimétrico (RSA)**, junto con otras funcionalidades como MAC, hashing, y más.

#### Modelo híbrido implementado:
1. Se genera una clave simétrica `session_key` (AES).
2. Esta clave se cifra usando RSA (con OAEP).
3. Los mensajes se cifran con AES en modo EAX o GCM (que permite verificar la integridad).

#### Características del enfoque:
- **Híbrido:** combina seguridad (RSA) + eficiencia (AES).
- **Integridad:** los modos AES-EAX o GCM permiten verificar si el mensaje fue alterado.
- **Flexible:** se puede usar sobre TCP o UDP.
- **Completo:** incluye cifrado, firmas digitales, hashing, KDFs, etc.

---

### c) Verificación de encriptación en tráfico

Se ejecutaron los scripts con el modelo híbrido implementado.  
En Wireshark, al analizar un paquete aleatorio de la secuencia:

- La carga útil **no es legible** y aparece como una secuencia de bytes aleatorios.
- Esto confirma que el mensaje está efectivamente cifrado.

Se comparó con capturas obtenidas en los ítems 1.a) y 2.a), donde la carga útil era visible (por ejemplo: `"kiritoro 4"`).  
En contraste, en esta nueva versión la carga útil aparece como datos binarios irreconocibles, lo cual verifica el correcto cifrado del contenido.

![image](https://github.com/user-attachments/assets/637ac0bd-3484-4a84-9932-f842520a1746)

### d) ¿Cómo encriptar la comunicación entre dos computadoras distantes sin contacto previo?

En un escenario donde dos computadoras se encuentran geográficamente separadas y **no han intercambiado información previamente**, se recomienda utilizar **criptografía asimétrica** para establecer un canal seguro inicial. A través de este canal, se intercambia una **clave simétrica**, que luego se usa para cifrar eficientemente toda la comunicación.

####  Pasos conceptuales para implementar este esquema:

1. **Generación de claves asimétricas (RSA):**
   - Cada computadora genera un par de claves: una pública y una privada.
   - La clave pública puede compartirse abiertamente.
   - La clave privada se guarda de forma segura y nunca se transmite.

2. **Intercambio de claves públicas:**
   - Al comenzar la conexión, cliente y servidor intercambian sus claves públicas.

3. **Distribución segura de la clave simétrica:**
   - El cliente genera una clave simétrica aleatoria (por ejemplo, AES-256).
   - Luego cifra esa clave utilizando la **clave pública del servidor**.
   - El servidor la descifra usando su **clave privada**.
   - Ahora ambas partes comparten una clave simétrica segura.

4. **Comunicación cifrada:**
   - Todo el contenido transmitido se cifra utilizando esa clave simétrica (AES).
   - Esto permite mantener **eficiencia y seguridad** en la comunicación continua.

####  Aplicación práctica al proyecto:

En el contexto de los scripts desarrollados (TCP/UDP), se podría implementar este mecanismo de la siguiente forma:

- Incluir una **fase de "handshake" inicial**, donde el cliente obtiene la clave pública del servidor.
- Utilizar una librería como `PyCryptodome` para generar las claves RSA, cifrar la clave AES y realizar el cifrado simétrico.
- Asegurar que la clave simétrica se mantenga solo en memoria durante la sesión.
- Cifrar la carga útil antes de enviar cada paquete, y descifrarla al recibirlo.

Este enfoque se basa en el mismo principio que usan los protocolos modernos como **TLS**, garantizando seguridad incluso sin haber establecido un canal de confianza previamente.

