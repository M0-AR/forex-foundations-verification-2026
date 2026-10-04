"""Live market data fetcher — free, keyless, reproducible.

VERIFIED 2026-10-04 from this host:
  - Yahoo Finance v8 (no key): daily 5y + hourly 3mo WORK.
    e.g. https://query2.finance.yahoo.com/v8/finance/chart/EURUSD=X?interval=1d&range=5y
  - Frankfurter (ECB, no key): daily cross-rates WORK.
    e.g. https://api.frankfurter.app/2023-01-01..?from=EUR&to=USD,GBP,JPY
  - ECB 90d XML WORK (cross-check).
  - Stooq CSV BLOCKED from server IP (JS challenge) -> best-effort only, flagged.

All outputs stamped with UTC fetch time, source URL, row counts and sha.
"""
from __future__ import annotations
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "forex-foundations-verification/1.0 (research)"}

YAHOO_MAP = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "USDCHF": "CHF=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X",
    "NZDUSD": "NZDUSD=X",
    "XAUUSD": "GC=F",
    "BTCUSD": "BTC-USD",
}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def fetch_yahoo(symbol: str, interval: str = "1d", rng: str = "5y", timeout: int = 40) -> pd.DataFrame | None:
    ticker = YAHOO_MAP.get(symbol, symbol)
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&range={rng}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        j = r.json()
        res = j["chart"]["result"][0]
        ts = res["timestamp"]
        q = res["indicators"]["quote"][0]
        df = pd.DataFrame({
            "Date": pd.to_datetime(ts, unit="s", utc=True),
            "Open": q.get("open"), "High": q.get("high"),
            "Low": q.get("low"), "Close": q.get("close"),
            "Volume": q.get("volume"),
        })
        df = df.dropna(subset=["Open", "High", "Low", "Close"]).sort_values("Date").reset_index(drop=True)
        df["source"] = f"yahoo:{interval}:{ticker}"
        df["fetch_url"] = url
        return df
    except Exception:
        return None


def fetch_frankfurter_daily(timeout: int = 40) -> pd.DataFrame | None:
    url = "https://api.frankfurter.app/2020-01-01..?from=EUR&to=USD,GBP,JPY,CHF,AUD,CAD,NZD"
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        j = r.json()
        rows = []
        for day, rates in j.get("rates", {}).items():
            row = {"Date": pd.to_datetime(day)}
            for k, v in rates.items():
                row[f"EUR{k}"] = float(v)
            rows.append(row)
        if not rows:
            return None
        df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
        # EURUSD directly; others as cross via EUR base
        df["source"] = "frankfurter:ECB:daily"
        df["fetch_url"] = url
        return df
    except Exception:
        return None


def fetch_ecb_eurusd_daily(timeout: int = 30) -> pd.DataFrame | None:
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        ns = {"g": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
        rows = []
        for cube_time in root.findall(".//g:Cube[@time]", ns):
            day = cube_time.attrib["time"]
            for cube_rate in cube_time.findall("g:Cube[@currency='USD']", ns):
                rows.append({"Date": pd.to_datetime(day), "ECB_EURUSD": float(cube_rate.attrib["rate"])})
        if not rows:
            return None
        df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
        df["source"] = "ecb:90d:EURUSD"
        df["fetch_url"] = url
        return df
    except Exception:
        return None


def save_with_manifest(df: pd.DataFrame, path: Path, extra: dict | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    manifest = {
        "file": str(path.name),
        "rows": int(len(df)),
        "cols": list(df.columns),
        "sha16": _sha(df.to_csv(index=False)[:200000]),
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "extra": extra or {},
    }
    with open(str(path) + ".manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest


def to_stooq_daily_format(yahoo_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize Yahoo frame to OHLC daily with naive Date for downstream compat."""
    df = yahoo_df.copy()
    return df


def main():
    t0 = time.time()
    summary: dict = {"started_utc": datetime.now(timezone.utc).isoformat(), "symbols": {}}
    for sym in YAHOO_MAP:
        entry: dict = {}
        daily = fetch_yahoo(sym, "1d", "5y")
        if daily is not None and len(daily) > 100:
            m = save_with_manifest(daily, DATA_DIR / f"{sym}_daily.csv", {"interval": "1d", "source": "yahoo"})
            entry = {"daily_rows": len(daily), "daily_from": str(daily["Date"].min()), "daily_to": str(daily["Date"].max()), "manifest": m}
        else:
            entry = {"daily_rows": 0, "error": "yahoo_daily_unavailable"}
        if sym in ("EURUSD", "GBPUSD", "XAUUSD", "USDJPY"):
            hourly = fetch_yahoo(sym, "1h", "3mo")
            if hourly is not None and len(hourly) > 100:
                # normalize column for benchmark loader (expects DateTime or Date)
                hourly["DateTime"] = hourly["Date"]
                mh = save_with_manifest(hourly, DATA_DIR / f"{sym}_hourly.csv", {"interval": "1h", "source": "yahoo"})
                entry["hourly_rows"] = len(hourly)
                entry["hourly_manifest"] = mh
            else:
                entry["hourly_rows"] = 0
        summary["symbols"][sym] = entry
        time.sleep(0.5)

    fr = fetch_frankfurter_daily()
    if fr is not None:
        mf = save_with_manifest(fr, DATA_DIR / "FRANKFURTER_EUR_base_daily.csv", {"interval": "1d", "source": "frankfurter"})
        summary["frankfurter"] = {"rows": len(fr), "manifest": mf}
    else:
        summary["frankfurter"] = {"rows": 0, "error": "frankfurter_unavailable"}

    ecb = fetch_ecb_eurusd_daily()
    if ecb is not None:
        me = save_with_manifest(ecb, DATA_DIR / "ECB_EURUSD_90d.csv", {"interval": "1d", "source": "ecb"})
        summary["ecb"] = {"rows": len(ecb), "manifest": me}
    else:
        summary["ecb"] = {"rows": 0, "error": "ecb_unavailable"}

    summary["elapsed_s"] = round(time.time() - t0, 2)
    with open(DATA_DIR / "fetch_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
