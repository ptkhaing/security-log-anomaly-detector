# Security Log Anomaly Detector

A backend service that ingests authentication logs and flags suspicious activity (brute-force attempts, unusual login times) using unsupervised machine learning — not rule-based thresholds.

## Why unsupervised ML

Labeled "attack" data is rarely available in real security contexts. This project uses an **Isolation Forest** (scikit-learn), an unsupervised anomaly detection algorithm, so the system can flag *unusual* behavior without ever being told in advance what an attack looks like.

## How it works

1. Raw login events (timestamp, username, source IP, success/failure) are stored in PostgreSQL.
2. Events are aggregated into **10-minute windows per source IP**, generating features like attempt count, failure rate, distinct usernames targeted, and off-hours login fraction.
3. An Isolation Forest is trained on these feature vectors and flags the most statistically unusual windows as anomalies.
4. Results are served via a FastAPI REST API.

## Tech stack

- Python, FastAPI, Uvicorn
- PostgreSQL, SQLAlchemy
- scikit-learn (Isolation Forest), pandas

## API

- `POST /train` — retrains the model on current log data
- `GET /anomalies` — returns flagged anomalous time-windows

## Known limitations

- `contamination=0.05` is a manually chosen hyperparameter; it can produce false positives on small or unbalanced datasets (observed: a couple of single-event windows flagged due to limited baseline data).
- Currently trained on synthetic seed data; a production version would need real log volume for reliable thresholds.

## Setup

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_tables.py
python seed_data.py
uvicorn app.main:app --reload
\`\`\`