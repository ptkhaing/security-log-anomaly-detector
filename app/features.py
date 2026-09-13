import pandas as pd
from app.database import SessionLocal
from app.models import LogEntry

def load_logs_as_dataframe():
    db = SessionLocal()
    logs = db.query(LogEntry).all()
    db.close()

    data = [{
        "timestamp": log.timestamp,
        "username": log.username,
        "source_ip": log.source_ip,
        "success": log.success,
    } for log in logs]

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def build_features(df, window="10min"):
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour
    df["is_off_hours"] = ((df["hour"] < 8) | (df["hour"] >= 19)).astype(int)
    df["is_failure"] = (~df["success"]).astype(int)

    df = df.set_index("timestamp").sort_index()
    grouped = df.groupby("source_ip").resample(window)

    features = grouped.agg(
        attempt_count=("username", "count"),
        failure_count=("is_failure", "sum"),
        distinct_usernames=("username", "nunique"),
        off_hours_fraction=("is_off_hours", "mean"),
    )

    features["failure_rate"] = (features["failure_count"] / features["attempt_count"]).fillna(0)
    features = features[features["attempt_count"] > 0].reset_index()

    return features