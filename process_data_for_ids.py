import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# loading the logs
df = pd.read_csv("network_data.csv", header=None)
df.columns = ["src_mac", "dst_mac", "protocol", "src_ip", "dst_ip", "src_port", "dst_port", "tcp_flags", "timestamp", "packet_size"]

# converting timestamp into float
df["timestamp"] = df["timestamp"].astype(float)

# converting src port and dest port into numeric
df["src_port"] = pd.to_numeric(df["src_port"], errors="coerce")
df["dst_port"] = pd.to_numeric(df["dst_port"], errors="coerce")

# computing inter arrival time - time gap b/w packets
df["inter_arrival_time"] = df.groupby("src_ip")["timestamp"].diff().fillna(0)