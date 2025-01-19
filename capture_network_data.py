import scapy.all as scapy
import time

log_file_path = "logs_from_sniffer.txt"

with open(log_file_path, 'w') as file:
    pass

PROTOCOL_MAP = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP',
    58: 'ICMPv6',
}

def log_packet(packet):
    try:

        if scapy.IP in packet:

            src_mac = packet.src
            dst_mac = packet.dst

            protocol_num = packet.proto
            protocol = PROTOCOL_MAP.get(protocol_num, 'Unknown') 

            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst

            if scapy.TCP in packet:
                src_port = packet.sport
                dst_port = packet.dport
                flags = packet.sprintf("%TCP.flags%")
            elif scapy.UDP in packet:
                src_port = packet.sport
                dst_port = packet.dport
                flags = 'N/A'
            else:
                src_port = 'N/A'
                dst_port = 'N/A'
                flags = 'N/A'

            timestamp = time.time() 
            length = len(packet)  


            packet_data = f"{src_mac}, {dst_mac}, {protocol}, {src_ip}, {dst_ip}, {src_port}, {dst_port}, {flags}, {timestamp}, {length}"

            with open(log_file_path, 'a') as log_file:
                log_file.write(packet_data + "\n")

            print(f"Packet logged: {packet_data}")

    except Exception as e:
        print(f"Error logging packet: {e}")

def capture_packets():
    print("Starting packet capture...")
    scapy.sniff(prn=log_packet, store=0)  # Capture packets indefinitely

if __name__ == "__main__":
    capture_packets()
