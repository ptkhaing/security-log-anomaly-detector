from fastapi import FastAPI
from app.features import load_logs_as_dataframe, build_features
from app.detector import train_model, load_model, score_features

app = FastAPI(title="Security Log Anomaly Detector")


@app.post("/train")
def train():
    df = load_logs_as_dataframe()
    features = build_features(df)
    train_model(features)
    return {"status": "trained", "windows_used": len(features)}


@app.get("/anomalies")
def get_anomalies():
    df = load_logs_as_dataframe()
    features = build_features(df)
    model = load_model()
    scored = score_features(model, features)

    anomalies = scored[scored["is_anomaly"]].sort_values("anomaly_score")

    return anomalies[[
        "source_ip", "timestamp", "attempt_count",
        "failure_rate", "distinct_usernames",
        "off_hours_fraction", "anomaly_score"
    ]].to_dict(orient="records")