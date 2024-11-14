import scapy.all as scapy
import time

# Define the log file path
log_file_path = "logs_from_sniffer.txt"

# Clear previous log file data
with open(log_file_path, 'w') as file:
    pass

# Protocol mapping dictionary for common protocol numbers
PROTOCOL_MAP = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP',
    58: 'ICMPv6',
    # Add more protocols as needed
}

# Function to process and log packet data
def log_packet(packet):
    try:
        # Check if it's a valid IP packet
        if scapy.IP in packet:
            # Ethernet details
            src_mac = packet.src
            dst_mac = packet.dst

            # Protocol details (mapped to readable names)
            protocol_num = packet.proto
            protocol = PROTOCOL_MAP.get(protocol_num, 'Unknown')  # Get protocol name or 'Unknown'

            # IP details
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst

            # Transport layer details
            if scapy.TCP in packet:
                src_port = packet.sport
                dst_port = packet.dport
                flags = packet.sprintf("%TCP.flags%")  # TCP flags
            elif scapy.UDP in packet:
                src_port = packet.sport
                dst_port = packet.dport
                flags = 'N/A'
            else:
                src_port = 'N/A'
                dst_port = 'N/A'
                flags = 'N/A'

            # Additional packet details
            timestamp = time.time()  # Timestamp in seconds
            length = len(packet)  # Length of the packet

            # Log data without labels for streamlined processing
            packet_data = f"{src_mac}, {dst_mac}, {protocol}, {src_ip}, {dst_ip}, {src_port}, {dst_port}, {flags}, {timestamp}, {length}"

            # Write to the log file in real-time
            with open(log_file_path, 'a') as log_file:
                log_file.write(packet_data + "\n")

            print(f"Packet logged: {packet_data}")

    except Exception as e:
        print(f"Error logging packet: {e}")

# Function to capture packets
def capture_packets():
    print("Starting packet capture...")
    scapy.sniff(prn=log_packet, store=0)  # Capture packets indefinitely

# Start capturing packets
if __name__ == "__main__":
    capture_packets()
