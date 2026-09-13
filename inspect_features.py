from app.features import load_logs_as_dataframe, build_features

df = load_logs_as_dataframe()
features = build_features(df)

print(f"Generated {len(features)} time-windows across all IPs.\n")
print(features.sort_values("attempt_count", ascending=False).head(10))