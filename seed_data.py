import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import LogEntry

db = SessionLocal()

usernames = ["alice", "bob", "carol", "dave", "eve"]
normal_ips = ["192.168.1.10", "192.168.1.11", "10.0.0.5", "10.0.0.6"]
attacker_ip = "203.0.113.99"  # reserved test-documentation IP range

entries = []

# --- Normal traffic: spread over the last 7 days, mostly business hours ---
now = datetime.utcnow()
for _ in range(300):
    user = random.choice(usernames)
    ip = random.choice(normal_ips)
    days_ago = random.uniform(0, 7)
    hour = random.choice(range(8, 19))  # business hours
    ts = now - timedelta(days=days_ago)
    ts = ts.replace(hour=hour, minute=random.randint(0, 59))
    entries.append(LogEntry(
        timestamp=ts,
        username=user,
        source_ip=ip,
        success=True,
        event_type="login"
    ))

# --- Anomaly 1: brute-force burst — one IP, many failed attempts, short window ---
burst_start = now - timedelta(days=2, hours=3)
for i in range(40):
    entries.append(LogEntry(
        timestamp=burst_start + timedelta(seconds=i * 5),
        username=random.choice(usernames),
        source_ip=attacker_ip,
        success=False,
        event_type="failed_login"
    ))

# --- Anomaly 2: unusual login time — legit user, 3 AM login ---
odd_time = now - timedelta(days=1)
odd_time = odd_time.replace(hour=3, minute=17)
entries.append(LogEntry(
    timestamp=odd_time,
    username="carol",
    source_ip="192.168.1.10",
    success=True,
    event_type="login"
))

db.add_all(entries)
db.commit()
db.close()

print(f"Seeded {len(entries)} log entries.")