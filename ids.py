import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import IsolationForest
import logging

class IDS:
    def __init__(self, file):
        self.file = file
        self.df_scaled = None
        self.iso_forest = IsolationForest(contamination=0.05, random_state=42)
        logging.basicConfig(filename="anomalies.log", level=logging.INFO, format="%(asctime)s - %(message)s")


    def preprocess_data(self):
        df = pd.read_csv("network_data.csv")
        df.columns = ["src_mac", "dst_mac", "protocol", "src_ip", "dst_ip", "src_port", "dst_port", "tcp_flags", "timestamp", "packet_size"]

        # converting timestamp into float
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")

        df["packet_size"] = pd.to_numeric(df["packet_size"], errors="coerce")

        # converting src port and dest port into numeric
        df["src_port"] = pd.to_numeric(df["src_port"], errors="coerce").fillna(-1)
        df["dst_port"] = pd.to_numeric(df["dst_port"], errors="coerce").fillna(-1)

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
        self.df_scaled = scaler.fit_transform(df)

        self.df_scaled = pd.DataFrame(self.df_scaled, columns=df.columns)

        # print(df_scaled.head())
        print("Data preprocessing completed")

    def train_model(self):
        if self.df_scaled is None:
            raise ValueError("Data not preprocessed!")

        self.df_scaled["anomaly"] = self.iso_forest.fit_predict(self.df_scaled)

        # marking anomalies
        self.df_scaled["anomaly"] = self.df_scaled["anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal")

        print(self.df_scaled[["packet_size", "inter_arrival_time", "packet_rate", "anomaly"]])

    def detect(self):
        self.preprocess_data()
        self.train_model()
        predictions = self.iso_forest.predict(self.df_scaled.drop(columns=["anomaly"]))

        for i, pred in enumerate(predictions):
            if pred == -1:
                print(f"Alert: Anomaly detected! in row {i}")
                print(self.df_scaled.iloc[i])
        
        self.save_logs()

    def save_logs(self):
        # Configure logging to write anomalies to a log file
        detected_anomalies = self.df_scaled[self.df_scaled["anomaly"] == "Anomaly"]
        if not detected_anomalies.empty:
            for index, row in detected_anomalies.iterrows():
                log_message = f"Alert: Anomaly detected at row {index} - {row.to_dict()}"
                logging.info(log_message)