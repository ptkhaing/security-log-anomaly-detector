# Security Log Anomaly Detector

A backend service that ingests authentication logs and flags suspicious activity (brute-force attempts, unusual login times) using unsupervised machine learning — not rule-based thresholds.

**Live demo:** https://security-log-anomaly-detector-5apx.onrender.com/docs

<img width="1478" height="226" alt="Screenshot 2026-09-17 at 5 34 51 PM" src="https://github.com/user-attachments/assets/05d3df8e-1934-4913-9ccd-835a326bcbfc" />

## Why unsupervised ML

Labeled "attack" data is rarely available in real security contexts. This project uses an **Isolation Forest** (scikit-learn), an unsupervised anomaly detection algorithm, so the system can flag *unusual* behavior without ever being told in advance what an attack looks like.

## How it works

1. Raw login events (timestamp, username, source IP, success/failure) are stored in PostgreSQL.
2. Events are aggregated into **10-minute windows per source IP**, generating features like attempt count, failure rate, distinct usernames targeted, and off-hours login fraction.
3. An Isolation Forest is trained on these feature vectors and flags the most statistically unusual windows as anomalies.
4. Results are served via a FastAPI REST API.

## Deployment

Deployed on Render (Docker-based web service) with Supabase as the managed Postgres provider. The database URL is injected via environment variable; `app/database.py` includes a small compatibility fix for Supabase/Render's `postgres://` URL prefix, which SQLAlchemy 2.x requires as `postgresql://`.

## Tech stack

- Python, FastAPI, Uvicorn
- PostgreSQL (Supabase, production) / PostgreSQL (local, development)
- SQLAlchemy
- scikit-learn (Isolation Forest), pandas
- Docker, deployed on Render

## API

- `POST /train` — retrains the model on current log data
- `GET /anomalies` — returns flagged anomalous time-windows

## Known limitations

- `contamination=0.05` is a manually chosen hyperparameter; it can produce false positives on small or unbalanced datasets (observed: a couple of single-event windows flagged due to limited baseline data).
- Currently trained on synthetic seed data; a production version would need real log volume for reliable thresholds.

## Setup (local development)

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_tables.py
python seed_data.py
uvicorn app.main:app --reload
\`\`\`

Requires a local PostgreSQL instance and a `.env` file with `DATABASE_URL` pointing to it.
