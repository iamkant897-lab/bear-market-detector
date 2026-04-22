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
    # "." 값 필터링 + 프론트엔드가 기대하는 {date, value} 형식으로 변환
    obs = [{'date': o['date'], 'value': float(o['value'])} for o in obs if o['value'] != '.']
    print(f"  {series_id}: {len(obs)} observations")
    return obs

print("FRED 데이터 수집 시작...")
data = {
    'updated': datetime.datetime.utcnow().isoformat() + 'Z',
    'd10':      fetch('DGS10'),
    'd2':       fetch('DGS2'),
    'd3m':      fetch('DGS3MO'),
    'sp':       fetch('SP500', '1990-01-01'),
    'usrec':    fetch('USREC'),
    'fedfunds': fetch('FEDFUNDS'),
}

os.makedirs('data', exist_ok=True)
with open('data/cache.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))

total = sum(len(v) for v in data.values() if isinstance(v, list))
print(f"완료! 총 {total}개 데이터 포인트 → data/cache.json")
