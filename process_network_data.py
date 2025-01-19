import csv
import os
import time


log_file_path = "logs_from_sniffer.txt" 
csv_file_path = "network_data.csv"

with open(csv_file_path, 'w') as file:
    pass

def process_log_file():
    try:
        if not os.path.exists(log_file_path):
            print(f"Log file not found: {log_file_path}")
            return

        with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
            log_reader = log_file.readlines()
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(["Source MAC", "Destination MAC", "Protocol", "Source IP", "Destination IP", 
                                 "Source Port", "Destination Port", "TCP Flags", "Timestamp", "Packet Length"])

            for line in log_reader:
                if line.strip():
                    fields = [field.strip() for field in line.split(",")]  # Split by commas and trim whitespace

                    # Only write rows with exactly 10 fields to the CSV
                    if len(fields) == 10:
                        print(f"Processing line: {fields}") 
                        csv_writer.writerow(fields)
                    else:
                        print(f"Invalid line format: {line}")

    except Exception as e:
        print(f"Error processing log file: {e}")

def monitor_log_file():
    while True:
        process_log_file()
        time.sleep(3)

if __name__ == "__main__":
    print("Monitoring log file and processing network data...")
    monitor_log_file()
