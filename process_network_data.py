import csv
import os
import time

# Define the log file path (ensure this matches where capture_network_data.py is writing)
log_file_path = "logs_from_sniffer.txt"  # Update to the actual path of your log file
csv_file_path = "network_data.csv"

with open(csv_file_path, 'w') as file:
    pass

# Function to process the log file
def process_log_file():
    try:
        # Check if the log file exists
        if not os.path.exists(log_file_path):
            print(f"Log file not found: {log_file_path}")
            return

        # Open the log file in read mode and the CSV in write mode (clear the CSV file)
        with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
            log_reader = log_file.readlines()
            csv_writer = csv.writer(csv_file)

            # Write the header for the CSV file
            csv_writer.writerow(["Source MAC", "Destination MAC", "Protocol", "Source IP", "Destination IP", 
                                 "Source Port", "Destination Port", "TCP Flags", "Timestamp", "Packet Length"])

            for line in log_reader:
                if line.strip():  # Ignore empty lines
                    fields = line.strip().split(",")  # Assuming comma-delimited data

                    # If the line has the correct number of fields, write it to the CSV
                    if len(fields) == 10:
                        print(f"Processing line: {fields}")  # Debugging
                        csv_writer.writerow(fields)
                    else:
                        print(f"Invalid line format: {line}")  # Debugging

    except Exception as e:
        print(f"Error processing log file: {e}")

# Run the function to process the log file periodically
def monitor_log_file():
    while True:
        process_log_file()  # Process the log file
        time.sleep(5)  # Wait before processing again (adjust time as necessary)

# Start monitoring the log file for new entries
if __name__ == "__main__":
    print("Monitoring log file and processing network data...")
    monitor_log_file()
