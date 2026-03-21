# 📉 하락장 감별기 / Bear Market Detector

미국 국채 금리차(스프레드) 역전 현상을 분석해 **경기침체·조정장 신호**를 감지하는 대시보드.

🔗 **라이브**: [GitHub Pages URL]

---

## 작동 원리

| 신호 | 조건 | 역사적 결과 |
|------|------|------------|
| **3종 역전** | s1(10Y-2Y) + s2(2Y-3M) + s3(10Y-3M) 동시 음수 3개월 → s2·s3 양전환 2개월 | 평균 수개월 내 S&P 500 -20%+ |
| **2종 역전** | s2(2Y-3M) + s3(10Y-3M) 음수 3개월 → s3 양전환 3개월 | S&P 500 -15% 조정 |

> s1(10Y-2Y)은 **깊이 지표** — 진입에만 포함, 해소 판단 제외

---

## 사용 방법

### 1. FRED API 키 발급 (무료, 1분)
1. [fredaccount.stlouisfed.org](https://fredaccount.stlouisfed.org) 접속
2. 무료 계정 생성
3. 로그인 → 우측 상단 **API Keys** → **Request API Key**
4. 발급된 32자리 키를 대시보드에 입력

### 2. GitHub Pages 배포
```bash
git clone https://github.com/YOUR_ID/bear-market-detector
cd bear-market-detector
# bear-market-detector.html 파일을 index.html로 이름 변경
mv bear-market-detector.html index.html
git add .
git commit -m "deploy"
git push
```
Repository Settings → Pages → Source: **main branch** → Save

---

## 데이터 소스

| 지표 | 출처 | 설명 |
|------|------|------|
| DGS10, DGS2, DGS3MO | FRED | 미국 국채 10년/2년/3개월 수익률 |
| USREC | FRED | NBER 공식 경기침체 기간 |
| FEDFUNDS | FRED | 연방기금금리 |
| S&P 500 | Yahoo Finance | 월봉 종가 |

---

## 주요 기능

- 📊 3종·2종 금리차 역전 자동 감지 및 신호 확정
- 📈 S&P 500 오버레이 + 역전/해소 구간 시각화
- 📋 과거 신호 이력 테이블 (수익률 3M/6M/12M/24M, 최대낙폭)
- 🔴 NBER 공식 경기침체 구간 표시 (닷컴버블침체, 서브프라임침체 등)
- 💾 24시간 로컬 캐시 (새로고침 없이 빠른 로딩)

---

## 주의사항

- API 키는 브라우저 localStorage에만 저장. 서버로 전송되지 않음
- 이 대시보드는 **투자 조언이 아닙니다**
- 과거 패턴이 미래를 보장하지 않습니다
