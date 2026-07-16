# 📊 Use Case 1: Earnings Comp and Consensus Analysis

This use case automates the synthesis of corporate performance during earnings season, benchmarking actual financial results against consensus analyst targets and measuring immediate market sentiment/price responses.

---

## 🎯 Rogo.ai Problem Framings Solved
* **Earnings Season Comp Benchmarking:** Having analysts manually pull earnings filings, track beat/miss statuses, compile EPS actuals vs. consensus estimates, and write summaries.
* **Sentiment Synthesis & Market Reaction:** Combining analyst notes, post-earnings news, and daily price volatility to assess corporate sentiment trends.
* **Audit-Ready Financial Data (Daloopa/Quartr Style):** Hyperlinking each extracted data point to the original source (filing tables, transcript text) to verify accuracy.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Routes routine earnings-date lookups and basic sentiment screening.
2. **Frontier Routing (Sol @ $1.26):** Reserves heavy reasoning (e.g., assessing why a company hit revenue targets but missed operating margins, or comparing quarterly earnings commentary differences) for the frontier model.
3. **Reasoning Reductions:** Instead of sifting through raw text files, pre-constructed search inputs index exact dates, filtering out non-earnings press releases to minimize token consumption.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/earnings_estimates/](file:///home/maxdemarzi/rogue/data/earnings_estimates/)**: Consensus EPS estimates, beat/miss indicators, streak counts, and average surprise rates.
2. **[data/simfin/](file:///home/maxdemarzi/rogue/data/simfin/)**: Public company metadata, financial sheet snapshots, and historical statements.
3. **[data/sec_financials/](file:///home/maxdemarzi/rogue/data/sec_financials/)**: Pre-cleaned structural summaries of SEC reports.
4. **[data/financial_news/](file:///home/maxdemarzi/rogue/data/financial_news/)**: Labeled headlines, articles, and sell-side recommendation changes.
5. **[data/financial_phrasebank/](file:///home/maxdemarzi/rogue/data/financial_phrasebank/)**: Sentiment annotations for corporate announcements.
6. **[data/ohlcv/](file:///home/maxdemarzi/rogue/data/ohlcv/)**: Daily price and volume timelines to track post-earnings market response.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. The Earnings Comp Link
Establish a relationship between corporate profiles and their quarterly consensus figures:
```
(:Company {ticker: $TICKER}) -[:HAS_EARNINGS_ESTIMATE]-> (:EarningsEstimate {
  date: earnings_date,
  beat: beat,
  beat_streak: beat_streak,
  avg_surprise: avg_surprise_4q
})
```

### 2. Market Reaction Loop
Align the earnings release timeline with short-term price variations:
```
(:Company {ticker: $TICKER}) -[:HAS_PRICE_SERIES]-> (:OHLCV {date: earnings_date})
```
Compare price changes on `earnings_date + 1` and `earnings_date + 5` to gauge the magnitude of the surprise.

### 3. Sentiment Integration
Connect news coverage and sentiment scores to the earnings window:
```
(:SentimentEvent {date: earnings_date, score: sentiment}) -[:REFERS_TO]-> (:Company {ticker: $TICKER})
```

---

## 💻 Technical Solution Steps

### Step 1: Benchmark EPS Beats and Misses
Load target company details alongside consensus EPS parameters to identify earnings surprises:
```python
import pandas as pd

estimates_df = pd.read_csv('data/earnings_estimates/earnings_features_clean (1).csv')
company_estimates = estimates_df[estimates_df['ticker'] == 'AAPL'].sort_values('earnings_date')
print(company_estimates[['earnings_date', 'beat', 'beat_streak', 'avg_surprise_4q']].tail(4))
```

### Step 2: Correlate with Daily Stock Performance
Calculate the stock return on the day of and the day following the announcement:
```python
price_df = pd.read_csv('data/ohlcv/stocks_us/1d/AAPL.csv')
price_df['Date'] = pd.to_datetime(price_df['Date'])
estimates_df['earnings_date'] = pd.to_datetime(estimates_df['earnings_date'])

for _, row in company_estimates.iterrows():
    announcement_date = row['earnings_date']
    # Fetch 5-day window around announcement
    window = price_df[(price_df['Date'] >= announcement_date - pd.Timedelta(days=1)) & 
                      (price_df['Date'] <= announcement_date + pd.Timedelta(days=3))]
    print(f"Announcement Date: {announcement_date.date()} | Beat: {row['beat']}")
    print(window[['Date', 'Open', 'Close', 'Volume']])
```

### Step 3: Parse News Sentiment Windows
Scan the financial headlines matching the announcement date to extract thematic drivers behind the performance:
```python
news_df = pd.read_csv('data/financial_news/analyst_ratings_processed.csv')
news_df['date'] = pd.to_datetime(news_df['date'])

earnings_day_news = news_df[
    (news_df['stock'] == 'AAPL') & 
    (news_df['date'].dt.date == announcement_date.date())
]
print(earnings_day_news['title'].tolist())
```
