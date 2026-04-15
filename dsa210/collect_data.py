"""
DSA 210 Project - Data Collection Script
Author: Omer
Description: Fetches weather (Open-Meteo), Brent oil price and USD/TRY (Yahoo Finance),
             merges them with weekly plastic bucket sales data on ISO weeks.

How to run:
    pip install -r requirements.txt
    python collect_data.py

Output:
    data/raw/weather_daily.csv
    data/raw/brent_daily.csv
    data/raw/usdtry_daily.csv
    data/processed/merged_weekly.csv
"""
import os
import pandas as pd
import numpy as np
import requests
import yfinance as yf

# ---------- Config ----------
START = "2023-01-01"
END   = "2025-12-31"

SALES_FILE = "data/raw/haftalik_satis_2023_2025.xlsx"  # put your sales file here
RAW_DIR    = "data/raw"
PROC_DIR   = "data/processed"

os.makedirs(RAW_DIR,  exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

# Major Turkish cities for demand-side temperature (population in millions, ~2023)
# Osmaniye is the factory location and is fetched separately.
CITIES = {
    "Istanbul":  {"lat": 41.0082, "lon": 28.9784, "pop": 15.8},
    "Ankara":    {"lat": 39.9334, "lon": 32.8597, "pop":  5.7},
    "Izmir":     {"lat": 38.4192, "lon": 27.1287, "pop":  4.4},
    "Bursa":     {"lat": 40.1885, "lon": 29.0610, "pop":  3.2},
    "Antalya":   {"lat": 36.8969, "lon": 30.7133, "pop":  2.7},
    "Konya":     {"lat": 37.8746, "lon": 32.4932, "pop":  2.3},
    "Adana":     {"lat": 37.0000, "lon": 35.3213, "pop":  2.3},
    "Gaziantep": {"lat": 37.0662, "lon": 37.3833, "pop":  2.1},
    "Kayseri":   {"lat": 38.7312, "lon": 35.4787, "pop":  1.4},
    "Osmaniye":  {"lat": 37.0742, "lon": 36.2467, "pop":  0.6},  # factory
}

# ---------- 1. Weather ----------
print("Fetching weather data from Open-Meteo Historical API...")
weather = {}
for city, info in CITIES.items():
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={info['lat']}&longitude={info['lon']}"
        f"&start_date={START}&end_date={END}"
        "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Europe/Istanbul"
    )
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    j = r.json()
    df = pd.DataFrame({
        "date": pd.to_datetime(j["daily"]["time"]),
        "temp_mean": j["daily"]["temperature_2m_mean"],
        "temp_max":  j["daily"]["temperature_2m_max"],
        "temp_min":  j["daily"]["temperature_2m_min"],
        "precip":    j["daily"]["precipitation_sum"],
    })
    weather[city] = df
    print(f"  {city}: {len(df)} days")

# Save raw weather (long format, all cities stacked)
all_w = []
for city, df in weather.items():
    d = df.copy()
    d["city"] = city
    all_w.append(d)
pd.concat(all_w, ignore_index=True).to_csv(f"{RAW_DIR}/weather_daily.csv", index=False)

# Population-weighted Turkey average (excluding Osmaniye to keep it as a separate signal)
demand_cities = {k: v for k, v in CITIES.items() if k != "Osmaniye"}
total_pop = sum(c["pop"] for c in demand_cities.values())

tr_daily = pd.DataFrame({"date": weather["Istanbul"]["date"]})
tr_daily["temp_tr_mean"] = 0.0
tr_daily["temp_tr_max"]  = 0.0
tr_daily["precip_tr"]    = 0.0
for city, info in demand_cities.items():
    w = info["pop"] / total_pop
    tr_daily["temp_tr_mean"] += weather[city]["temp_mean"].values * w
    tr_daily["temp_tr_max"]  += weather[city]["temp_max"].values  * w
    tr_daily["precip_tr"]    += weather[city]["precip"].values    * w

tr_daily["temp_osmaniye"] = weather["Osmaniye"]["temp_mean"].values

# ---------- 2. Brent oil ----------
print("\nFetching Brent crude oil (BZ=F) from Yahoo Finance...")
brent = yf.download("BZ=F", start=START, end="2026-01-01", progress=False, auto_adjust=True)
brent = brent[["Close"]].reset_index()
brent.columns = ["date", "brent_usd"]
brent["date"] = pd.to_datetime(brent["date"]).dt.tz_localize(None)
brent.to_csv(f"{RAW_DIR}/brent_daily.csv", index=False)
print(f"  Brent: {len(brent)} trading days")

# ---------- 3. USD/TRY ----------
print("\nFetching USD/TRY from Yahoo Finance...")
usdtry = yf.download("TRY=X", start=START, end="2026-01-01", progress=False, auto_adjust=True)
usdtry = usdtry[["Close"]].reset_index()
usdtry.columns = ["date", "usd_try"]
usdtry["date"] = pd.to_datetime(usdtry["date"]).dt.tz_localize(None)
usdtry.to_csv(f"{RAW_DIR}/usdtry_daily.csv", index=False)
print(f"  USD/TRY: {len(usdtry)} trading days")

# ---------- 4. Aggregate to weekly (ISO Mon-Sun) ----------
print("\nAggregating to weekly (ISO weeks)...")

def add_iso(df, date_col="date"):
    d = df.copy()
    d[date_col] = pd.to_datetime(d[date_col])
    iso = d[date_col].dt.isocalendar()
    d["year"] = iso.year.astype(int)
    d["week"] = iso.week.astype(int)
    return d

# Weather weekly
tr_w = add_iso(tr_daily)
weather_weekly = tr_w.groupby(["year", "week"]).agg(
    temp_tr_mean=("temp_tr_mean", "mean"),
    temp_tr_max=("temp_tr_max", "mean"),
    precip_tr=("precip_tr", "sum"),
    temp_osmaniye=("temp_osmaniye", "mean"),
).reset_index()

# Forward-fill financial series across weekends, then weekly mean
def fill_and_weekly(df, value_col):
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    d = d.set_index("date").asfreq("D").ffill().reset_index()
    d = add_iso(d)
    return d.groupby(["year", "week"])[value_col].mean().reset_index()

brent_weekly  = fill_and_weekly(brent,  "brent_usd")
usdtry_weekly = fill_and_weekly(usdtry, "usd_try")

# ---------- 5. Load sales and merge ----------
print(f"\nLoading sales data from {SALES_FILE}...")
sales = pd.read_excel(SALES_FILE, sheet_name="Haftalık Satış")
sales = sales[sales["Hafta No"] != "TOPLAM"].copy()
sales = sales.rename(columns={
    "Yıl": "year",
    "Hafta No": "week",
    "Hafta Başlangıç (Pzt)": "week_start",
    "Hafta Bitiş (Paz)": "week_end",
    "Haftalık Satış (ton)": "sales_tons",
})
sales["year"] = sales["year"].astype(int)
sales["week"] = sales["week"].astype(int)
sales["sales_tons"] = sales["sales_tons"].astype(float)
print(f"  Sales: {len(sales)} weeks")

merged = (sales
    .merge(weather_weekly, on=["year", "week"], how="left")
    .merge(brent_weekly,   on=["year", "week"], how="left")
    .merge(usdtry_weekly,  on=["year", "week"], how="left"))

merged["week_start"] = pd.to_datetime(merged["week_start"], format="%d.%m.%Y")
merged["week_end"]   = pd.to_datetime(merged["week_end"],   format="%d.%m.%Y")
merged["month"]   = merged["week_start"].dt.month
merged["quarter"] = merged["week_start"].dt.quarter

def season(m):
    if m in (12, 1, 2): return "Winter"
    if m in (3, 4, 5):  return "Spring"
    if m in (6, 7, 8):  return "Summer"
    return "Autumn"
merged["season"] = merged["month"].apply(season)

merged = merged.sort_values("week_start").reset_index(drop=True)

print("\nMissing values per column:")
print(merged.isnull().sum())

out_path = f"{PROC_DIR}/merged_weekly.csv"
merged.to_csv(out_path, index=False)
print(f"\n✓ Saved: {out_path}")
print(f"  Shape: {merged.shape}")
print("\nFirst 3 rows:")
print(merged.head(3).to_string())
print("\nSummary:")
print(merged[["sales_tons","temp_tr_mean","temp_osmaniye","brent_usd","usd_try"]].describe().round(2))
