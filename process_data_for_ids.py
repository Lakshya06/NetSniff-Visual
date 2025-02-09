import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# loading the logs
df = pd.read_csv("network_data.csv")
df.columns = ["src_mac", "dst_mac", "protocol", "src_ip", "dst_ip", "src_port", "dst_port", "tcp_flags", "timestamp", "packet_size"]

# converting timestamp into float
df["timestamp"] = df["timestamp"].astype(float)

# converting src port and dest port into numeric
df["src_port"] = pd.to_numeric(df["src_port"], errors="coerce")
df["dst_port"] = pd.to_numeric(df["dst_port"], errors="coerce")

# computing inter arrival time - time gap b/w packets
df["inter_arrival_time"] = df.groupby("src_ip")["timestamp"].diff().fillna(0)

#computing packet rate - packets per second/source IP
df['packet_rate'] = df.groupby("src_ip")["src_ip"].transform("count") / (df["timestamp"].max() - df["timestamp"].min())

# One-hot encode protocol (ICMP, TCP, UDP)
encoder = OneHotEncoder(sparse_output=False)
protocol_encoded = encoder.fit_transform(df[["protocol"]])
protocol_df = pd.DataFrame(protocol_encoded, columns=encoder.get_feature_names_out(["protocol"]))

# Merge encoded protocol and drop unnecessary columns
df = pd.concat([df, protocol_df], axis=1)
df.drop(columns=["src_mac", "dst_mac", "protocol", "src_ip", "dst_ip", "tcp_flags"], inplace=True)

# Fill NaN values
df.fillna(0, inplace=True)

# Standardize numerical features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

print(df_scaled.head())
