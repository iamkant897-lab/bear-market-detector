#!/usr/bin/env python3
"""
FRED 데이터 자동 수집 스크립트
GitHub Actions에서 매일 실행됨
"""
import json, os, urllib.request, datetime

API_KEY = os.environ['FRED_API_KEY']
BASE = 'https://api.stlouisfed.org/fred/series/observations'

def fetch(series_id, start='1985-01-01'):
    url = f"{BASE}?series_id={series_id}&api_key={API_KEY}&file_type=json&observation_start={start}&sort_order=asc"
    print(f"  Fetching {series_id}...")
    with urllib.request.urlopen(url, timeout=30) as r:
        obs = json.loads(r.read())['observations']
    obs = [{'date': o['date'], 'value': float(o['value'])} for o in obs if o['value'] != '.']
    print(f"  {series_id}: {len(obs)} observations")
    return obs

def fetch_spx():
    """Yahoo Finance에서 S&P500 40년치 주간 데이터 수집 (CORS 없이 서버에서 직접 호출)"""
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1wk&range=40y&includePrePost=false'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; GitHub-Actions)'})
    print("  Fetching SPX from Yahoo Finance...")
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read())
    res = j['chart']['result'][0]
    obs = [
        {'date': datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc).strftime('%Y-%m-%d'), 'value': v}
        for t, v in zip(res['timestamp'], res['indicators']['quote'][0]['close'])
        if v is not None
    ]
    print(f"  SPX: {len(obs)} observations")
    return obs

print("FRED 데이터 수집 시작...")
data = {
    'updated': datetime.datetime.utcnow().isoformat() + 'Z',
    'd10':      fetch('DGS10'),
    'd2':       fetch('DGS2'),
    'd3m':      fetch('DGS3MO'),
    'sp':       fetch_spx(),
    'usrec':    fetch('USREC'),
    'fedfunds': fetch('FEDFUNDS'),
}

os.makedirs('data', exist_ok=True)
with open('data/cache.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))

total = sum(len(v) for v in data.values() if isinstance(v, list))
print(f"완료! 총 {total}개 데이터 포인트 → data/cache.json")
