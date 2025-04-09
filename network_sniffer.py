import psutil
import time
import sys
import socket
from datetime import datetime

# Ensure UTF-8 encoding for Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

def get_protocol_name(conn_type):
    """Map socket types to actual protocol numbers (TCP=6, UDP=17)."""
    if conn_type == socket.SOCK_STREAM:
        return "6 (TCP)"
    elif conn_type == socket.SOCK_DGRAM:
        return "17 (UDP)"
    return f"{conn_type} (Unknown)"  # Handle unexpected protocol types

def capture_network_activity():
    seen_connections = set()

    while True:
        connections = psutil.net_connections(kind="inet")

        for conn in connections:
            # Capture only established TCP connections and active UDP connections
            if conn.status == psutil.CONN_ESTABLISHED or conn.type == socket.SOCK_DGRAM:
                src_ip, src_port = conn.laddr
                dst_ip, dst_port = conn.raddr if conn.raddr else ("N/A", "N/A")
                protocol = get_protocol_name(conn.type)
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

                conn_tuple = (src_ip, dst_ip, protocol)
                if conn_tuple not in seen_connections:
                    seen_connections.add(conn_tuple)

                    print(f"{timestamp} 📡 Packet Captured")
                    print(f"◆ Source IP: {src_ip}")
                    print(f"◆ Destination IP: {dst_ip}")
                    print(f"◆ Protocol: {protocol}")
                    print("-" * 50)

        time.sleep(2)

print("Starting network activity monitor...\n")
capture_network_activity()
