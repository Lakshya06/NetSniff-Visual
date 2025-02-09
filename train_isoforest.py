
from sklearn.ensemble import IsolationForest

# training isolation forest
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df_scaled["anomaly"] = iso_forest.fit_predict(df_scaled)

# marking anomalies
df_scaled["anomaly"] = df_scaled["anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal")

print(df_scaled[["packet_size", "inter_arrival_time", "packet_rate", "anomaly"]])