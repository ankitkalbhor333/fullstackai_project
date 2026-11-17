import pandas as pd

def detect_time_bursts(posts, interval="1h"):
    if not posts:
        return {}

    df = pd.DataFrame(posts)

    if "createdAt" not in df.columns:
        return {}

    # Convert to datetime safely
    df["timestamp"] = pd.to_datetime(df["createdAt"], errors="coerce")

    # Drop rows with invalid timestamps
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        return {}

    # Group by time interval
    counts = df.groupby(pd.Grouper(key="timestamp", freq=interval)).size()

    # Return with ISO string keys and standard int counts for JSON compatibility
    return {str(k): int(v) for k, v in counts.items()}

