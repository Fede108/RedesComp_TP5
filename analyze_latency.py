#!/usr/bin/env python3
import re
from datetime import datetime
import sys
import os

# Ruta de log del cliente
CLIENT_LOG_PATH = "client.log"

def parse_client_log(file_path):
    send_times = {}
    recv_times = {}
    # Regex según formato exacto del log de cliente
    send_pattern = re.compile(
        r'^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+Enviando: \S+ (?P<id>\d+)$'
    )
    recv_pattern = re.compile(
        r'^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+Recibido del servidor: \S+ (?P<id>\d+)$'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            m_send = send_pattern.match(line)
            if m_send:
                ts = datetime.strptime(m_send.group('ts'), "%Y-%m-%d %H:%M:%S.%f")
                pkt_id = int(m_send.group('id'))
                send_times[pkt_id] = ts
                continue
            m_recv = recv_pattern.match(line)
            if m_recv:
                ts = datetime.strptime(m_recv.group('ts'), "%Y-%m-%d %H:%M:%S.%f")
                pkt_id = int(m_recv.group('id'))
                recv_times[pkt_id] = ts
    return send_times, recv_times

def compute_rtt(client_send, client_recv):
    rtts = {}
    for req_id, t_send in client_send.items():
        resp_id = req_id + 1
        if resp_id in client_recv:
            t_recv = client_recv[resp_id]
            delta = (t_recv - t_send).total_seconds()
            if delta >= 0:
                rtts[req_id] = delta
            else:
                # registro negativo: ajustar a 0 o ignorar
                print(f"Advertencia: RTT negativo para ID {req_id}: {delta}s. Se ignora.", file=sys.stderr)
    return rtts

def summarize_delays(name, delays):
    if not delays:
        print(f"No se encontraron {name} válidos.")
        return
    values = list(delays.values())
    ids = sorted(delays.keys())
    n = len(values)
    avg = sum(values) / n
    minimum = min(values)
    maximum = max(values)
    diffs = [abs(delays[ids[i]] - delays[ids[i-1]]) for i in range(1, len(ids))]
    jitter = sum(diffs) / len(diffs) if diffs else 0.0

    print(f"--- Resumen {name} ---")
    print(f"Paquetes considerados: {n}")
    print(f"RTT promedio (s): {avg:.6f}")
    print(f"RTT mínima (s): {minimum:.6f}")
    print(f"RTT máxima (s): {maximum:.6f}")
    print(f"Jitter RTT promedio (s): {jitter:.6f}")
    print()

def main():
    client_log = CLIENT_LOG_PATH
    if not os.path.isfile(client_log):
        print(f"Error: no se encuentra el log del cliente: {client_log}", file=sys.stderr)
        sys.exit(1)

    client_send, client_recv = parse_client_log(client_log)
    rtts = compute_rtt(client_send, client_recv)

    # Detalle RTT
    print("RTT por paquete (ID petición):")
    for pkt_id in sorted(rtts.keys()):
        print(f"ID {pkt_id}: RTT = {rtts[pkt_id]:.6f}s")
    print()

    # Resumen
    summarize_delays("RTT", rtts)

if __name__ == "__main__":
    main()