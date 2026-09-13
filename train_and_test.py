from app.features import load_logs_as_dataframe, build_features
from app.detector import train_model, score_features

df = load_logs_as_dataframe()
features = build_features(df)

model = train_model(features)
scored = score_features(model, features)

anomalies = scored[scored["is_anomaly"]].sort_values("anomaly_score")

print(f"Flagged {len(anomalies)} anomalies out of {len(scored)} windows.\n")
print(anomalies[["source_ip", "timestamp", "attempt_count", "failure_rate", "distinct_usernames", "off_hours_fraction", "anomaly_score"]])