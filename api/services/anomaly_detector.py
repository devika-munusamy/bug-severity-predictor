"""
Anomaly Detector
----------------
Uses a rolling window of prediction timestamps stored in the DB to detect
unusual spikes in error volume.

Strategy:
  - Bucket timestamps into 1-minute slots.
  - Keep the last 60 buckets (1 hour of history).
  - Use IsolationForest for anomaly scoring.
  - Fall back to μ + 2σ (simple statistical) if there is not enough data
    for the model (< 10 data points).
"""

from __future__ import annotations

import sqlite3
import os
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "predictions.db")

# How many 1-minute buckets to look at
_WINDOW_MINUTES = 60
# Minimum buckets needed before switching to IsolationForest
_MIN_SAMPLES_FOR_ISO = 10


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _fetch_timestamps(window_minutes: int = _WINDOW_MINUTES) -> list[str]:
    """Return all prediction timestamps within the last *window_minutes*."""
    since = (datetime.utcnow() - timedelta(minutes=window_minutes)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM predictions WHERE timestamp >= ? ORDER BY timestamp",
            (since,),
        )
        rows = [r[0] for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception:
        return []


def _bucket_counts(timestamps: list[str]) -> dict[str, int]:
    """
    Group timestamps into 1-minute buckets.
    Returns {bucket_str: count}.
    """
    counts: dict[str, int] = defaultdict(int)
    for ts in timestamps:
        try:
            dt = datetime.strptime(ts[:16], "%Y-%m-%d %H:%M")
            bucket = dt.strftime("%Y-%m-%d %H:%M")
            counts[bucket] += 1
        except ValueError:
            pass
    return dict(counts)


def _fill_zero_buckets(
    counts: dict[str, int], window_minutes: int = _WINDOW_MINUTES
) -> list[int]:
    """
    Produce a dense list (oldest → newest) of per-minute counts,
    filling minutes with no predictions as 0.
    """
    now = datetime.utcnow().replace(second=0, microsecond=0)
    series = []
    for i in range(window_minutes, -1, -1):
        bucket = (now - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        series.append(counts.get(bucket, 0))
    return series


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_anomaly_status() -> dict:
    """
    Return:
      {
        "is_anomaly":      bool,
        "current_count":   int,   # errors in the *last* minute
        "expected_range":  [lo, hi],
        "method":          "IsolationForest" | "statistical",
        "time_series":     [{"bucket": str, "count": int}, ...],   # last 30 mins
      }
    """
    timestamps = _fetch_timestamps()
    counts_map = _bucket_counts(timestamps)
    series = _fill_zero_buckets(counts_map)

    current_count = series[-1]  # most recent minute

    # Build time-series payload for the chart (last 30 minutes)
    now = datetime.utcnow().replace(second=0, microsecond=0)
    time_series = []
    for i in range(30, -1, -1):
        bucket = (now - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        time_series.append({"bucket": bucket, "count": counts_map.get(bucket, 0)})

    # ── Choose detection method ──────────────────────────────────────────
    arr = np.array(series, dtype=float)
    non_zero = arr[arr > 0]

    if len(arr) >= _MIN_SAMPLES_FOR_ISO and len(non_zero) >= 3:
        method, is_anomaly, lo, hi = _iso_forest_detect(arr, current_count)
    else:
        method, is_anomaly, lo, hi = _statistical_detect(arr, current_count)

    return {
        "is_anomaly": bool(is_anomaly),
        "current_count": int(current_count),
        "expected_range": [round(float(lo), 2), round(float(hi), 2)],
        "method": method,
        "time_series": time_series,
    }


def _statistical_detect(
    series: np.ndarray, current: float
) -> tuple[str, bool, float, float]:
    """μ ± 2σ threshold."""
    mu = float(np.mean(series))
    sigma = float(np.std(series))
    lo = max(0.0, mu - 2 * sigma)
    hi = mu + 2 * sigma
    is_anomaly = current > hi and current > 0
    return "statistical", is_anomaly, lo, hi


def _iso_forest_detect(
    series: np.ndarray, current: float
) -> tuple[str, bool, float, float]:
    """IsolationForest anomaly detection."""
    try:
        from sklearn.ensemble import IsolationForest

        X = series.reshape(-1, 1)
        clf = IsolationForest(contamination=0.05, random_state=42)
        clf.fit(X)
        pred = clf.predict([[current]])[0]  # -1 = anomaly, 1 = normal
        is_anomaly = pred == -1 and current > 0

        # Derive an approximate expected range from the training data
        scores = clf.score_samples(X)
        normal_vals = series[scores > np.percentile(scores, 10)]
        lo = float(np.percentile(normal_vals, 5)) if len(normal_vals) else 0.0
        hi = float(np.percentile(normal_vals, 95)) if len(normal_vals) else float(np.max(series))

        return "IsolationForest", is_anomaly, max(0.0, lo), hi
    except Exception:
        # Graceful fallback
        return _statistical_detect(series, current)
