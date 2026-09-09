<<<<<<< HEAD
# Local-Business-Growth-Lead-Intelligence-Platform
Local Business Growth &amp; Lead Intelligence Platform
=======
# GrowthPilot — Business Growth & Lead Intelligence Dashboard

A mini growth team dashboard built for local businesses, growth generalists, and operations leaders. It transforms raw lead inquiries into actionable business intelligence by identifying where leads originate, which marketing channels drive conversions, why prospects drop off, competitor benchmark gaps, and automated next actions.

---

## 🎯 The Business Problem Solved

Local businesses frequently struggle with:
1. **Lead Attribution Blindspots**: Not knowing where their best leads originate (Instagram, Google Search, WhatsApp, Referrals, Website).
2. **Channel Efficiency Disconnect**: Spending heavily on channels with high vanity volume but dismal conversion rates.
3. **Funnel Leaks**: Inability to identify where prospects drop off in the conversion journey (*Visitors → Leads → Contacted → Qualified → Converted*).
4. **Sales Operations Decay**: Stalling follow-ups and uncontacted leads decay in value within 48 hours.
5. **Competitor Blindness**: Lack of structured intelligence on local competitor pricing, ratings, and digital presence gaps.
6. **Lack of Actionable Strategy**: Generic dashboards display graphs without prescribing what operational steps to take next.

**GrowthPilot** bridges the gap from *"Here is some data"* to *"Here is the business problem, here is the evidence, and here is what you should do next."*

---

## 🚀 Key Features

### 1. Lead Management (Mini CRM)
- Track leads with: **Name, Phone, Email, Source, Product/Service, Lead Status, Created Date, Follow-up Date, Conversion Status, Revenue (₹), Loss Reason, and Notes**.
- Explicit support for sample leads:
  - *Rahul*: Instagram, Converted, ₹8,000
  - *Sneha*: Google, Follow-up
  - *Amit*: Referral, Converted, ₹12,000
  - *Priya*: Website, Lost
- Inline status and conversion updater.
- Overdue follow-up alert banner.
- CSV Export and Import for batch operations.

### 2. Executive Growth Scorecard (KPIs)
- **Total Leads & Converted Leads**
- **Overall Conversion Rate (%)**
- **Total Revenue Generated (₹)** with Average Order Value (AOV)
- **Cost Per Lead (CPL)**
- **Customer Acquisition Cost (CAC)** & Blended ROAS
- **Top Performing Channel** (Attribution & efficiency winner)
- **Lost Leads** (Volume & pipeline drop-off rate)
- **Follow-up Pending** (Count with real-time overdue alerts)

### 3. Marketing Channel Analysis
- Multi-channel comparison across **Instagram, Google, WhatsApp, Referral, and Website**.
- Comparison of **Volume vs Conversion Rate** (Dual-axis interactive chart).
- **Unit Economics**: Side-by-side CPL vs CAC benchmark.
- **Revenue Share Donut**: Revenue contribution per marketing channel in ₹.
- Interactive Monthly Spend Editor to adjust budgets and instantly recalculate unit economics.
- Automated channel insights (e.g., highlighting Instagram's 120 leads @ 8% vs Referrals' 40 leads @ 30%).

### 4. 5-Stage Customer Conversion Funnel
- Stages: **Visitors → Leads → Contacted → Qualified → Converted**.
- Step-by-step drop-off calculation: Transition volume, drop-off count, and drop-off %.
- **Automatic Bottleneck Detection**: Isolates the single largest drop-off stage (e.g. *Contacted → Qualified*) and displays diagnostic checklists.
- Lost reason breakdown chart (Price, Competitor, Timing, No response).

### 5. Competitor Intelligence & Benchmarking
- Competitor tracking matrix: Price, Google Rating, Active Website, Social Presence, Strengths, Weaknesses, Notes.
- **Competitor Quadrant Chart**: Visualizes Price vs Google Rating (4.0 - 5.0★) with bubble sizing by social presence and color by website existence.
- **Automated Opportunity Engine**: Detects gaps like *Competitor C (High rating 4.7★, but No website / low social presence)* to capitalize on search ad capture.
- Form to add new competitors to the database.

### 6. Rule-Based Growth Recommendation Engine 🤖
Applies data science business heuristics to generate prioritized action cards:
- `IF conversion_rate < 5%`: Review lead quality and landing page friction.
- `IF Instagram leads > Google leads AND Instagram conversion rate < Google`: Improve Instagram lead qualification and reallocate ad budget to Google Search intent.
- `IF referral conversion rate > other channels`: Systematize customer referral incentives.
- `IF follow-up pending > 20 OR overdue > 0`: Prioritize sales follow-up sprint and WhatsApp templates.
- Funnel drop-off intervention playbooks (e.g. speed-to-lead scripts).
- Competitor digital arbitrage plays.

### 7. "Ask GrowthPilot" (Interactive Growth Simulator)
- **Conversion Rate Simulator**: Test what happens if conversion increases from 8% to 15% (calculates extra customers, added revenue in ₹, and CAC reduction).
- **Budget Reallocation Simulator**: Model shifting ad spend from Instagram into Google/Referrals.
- **Instant Business Q&A**: Data-backed answers to key growth questions (*Why are we losing leads? Where is the biggest bottleneck? What should we focus on this week?*).

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend / Dashboard** | Streamlit |
| **Data Processing** | Python 3.11, Pandas, NumPy |
| **Database** | SQLite (`growthpilot.db`) with auto-seeding |
| **Visualizations** | Plotly Express & Plotly Graph Objects |
| **File Formats** | CSV Import & Export |

---

## 📂 Project Structure

```
Local Business Growth & Lead Intelligence Platform/
├── app.py                      # Main Streamlit application
├── database.py                 # SQLite database schema, connections, and CRUD
├── seed_data.py                # Prompt-accurate seed generator & CSV exporter
├── analytics.py                # KPI calculations, CAC, CPL, funnel drop-offs
├── recommendations.py          # Rule-based Growth Intelligence engine
├── requirements.txt            # Python dependencies
├── components/
│   ├── styles.py               # Custom modern CSS styling and cards
│   ├── kpi_cards.py            # Responsive KPI metric cards
│   └── charts.py               # Interactive Plotly chart builders
├── data/
│   └── sample_leads.csv        # Pre-packaged sample CSV for testing import
└── README.md                   # Project documentation
```

---

## ⚡ Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Seeding (Optional - auto-seeds on first run)
```bash
python seed_data.py
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.
>>>>>>> 2036b5f (Initial commit: GrowthPilot Business Growth & Lead Intelligence Platform)
