from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd

FEATURE_COLUMNS = [
    "attempt_count",
    "failure_count",
    "distinct_usernames",
    "off_hours_fraction",
    "failure_rate",
]

MODEL_PATH = "isolation_forest.joblib"


def train_model(features: pd.DataFrame, contamination: float = 0.05):
    X = features[FEATURE_COLUMNS]

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
    )
    model.fit(X)

    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    return joblib.load(MODEL_PATH)


def score_features(model, features: pd.DataFrame) -> pd.DataFrame:
    X = features[FEATURE_COLUMNS]

    features = features.copy()
    features["anomaly_score"] = model.decision_function(X)  # higher = more normal
    features["is_anomaly"] = model.predict(X) == -1          # -1 = anomaly, 1 = normal

    return features