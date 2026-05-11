---
name: rts-methodology
description: Use this skill when working on any phase of the RTS (Recovery and Transformation Services) diligence process. Covers the full methodology from kick-off through final deliverable, including phase checklists, data requirements, analysis frameworks, and quality standards. Trigger on any mention of RTS, diligence, transformation, recovery, turnaround, restructuring, or when executing any phase of the engagement workflow.
---

# RTS Methodology — Codified Framework

## What This Skill Does

This skill encodes the complete Recovery and Transformation Services methodology into
structured, repeatable steps that Claude can execute. It was built by interviewing
senior consultants and extracting their decision-making patterns.

## Phase 1: Kick-off & Scoping (Day 1-2)

### Objectives
- Define engagement scope and boundaries
- Identify key stakeholders and data owners
- Establish timeline and milestone dates
- Agree on deliverable format and audience

### Required Inputs
- Engagement letter or mandate description
- Target company name, industry, geography
- Reason for engagement (distress trigger: liquidity, covenant breach, operational decline)
- Key stakeholders list (management, creditors, board, advisors)

### Outputs
- Scoping memo (1-2 pages)
- Data request list (DRL) — comprehensive checklist of documents needed
- Stakeholder map with communication plan
- Project timeline with phase gates

### Decision Framework
When scoping, classify the engagement:
- **Liquidity Crisis**: Focus on cash flow, working capital, immediate cost cuts
- **Operational Underperformance**: Focus on revenue drivers, cost structure, benchmarking
- **Strategic Restructuring**: Focus on business unit analysis, divestiture candidates, growth levers
- **Covenant/Compliance**: Focus on debt structure, covenant calculations, lender negotiations

## Phase 2: Data Collection (Day 2-5)

### Standard Data Request List

#### Financial Data (Priority 1)
- [ ] 3-year audited financial statements (P&L, Balance Sheet, Cash Flow)
- [ ] Monthly management accounts (trailing 12-24 months)
- [ ] Budget vs actual for current and prior year
- [ ] Aged receivables and payables
- [ ] Debt schedule (all facilities, rates, maturities, covenants)
- [ ] Cash flow forecast (13-week if available)
- [ ] Tax returns (3 years)
- [ ] Intercompany balances and transactions

#### Operational Data (Priority 2)
- [ ] Org chart with headcount by department
- [ ] Revenue by customer/product/geography (trailing 24 months)
- [ ] Cost breakdown by category (fixed vs variable)
- [ ] Key contracts (top 10 customers, top 10 suppliers, leases)
- [ ] Technology systems inventory
- [ ] Capital expenditure schedule (historical and planned)

#### Legal & Compliance (Priority 3)
- [ ] Corporate structure chart
- [ ] Material litigation summary
- [ ] Regulatory filings and compliance status
- [ ] Insurance coverage summary
- [ ] Key employee contracts and retention arrangements

### Data Quality Checks
For every document received:
1. Verify the period covered matches the request
2. Check for internal consistency (e.g., P&L net income = BS retained earnings movement)
3. Flag gaps or anomalies with specific questions
4. Cross-reference against other sources where possible
5. Assign confidence level: HIGH / MEDIUM / LOW

## Phase 3: Financial Analysis (Day 3-8)

### Core Analyses

#### 3.1 Earnings Quality (Adjusted EBITDA)
Start from reported EBITDA and adjust for:
- One-time/non-recurring items (restructuring charges, litigation, asset sales)
- Related party transactions at non-market rates
- Owner/management add-backs (excess compensation, personal expenses)
- Accounting policy changes or errors
- Run-rate impact of recent events (new contracts, lost customers, price changes)

Output: Bridge from reported to adjusted EBITDA with supporting notes.

#### 3.2 Working Capital Analysis
- Calculate Net Working Capital (NWC) = Current Assets - Current Liabilities - Cash - Current Debt
- Trend analysis: NWC as % of revenue over 24 months
- Days Sales Outstanding (DSO), Days Payable Outstanding (DPO), Days Inventory Outstanding (DIO)
- Identify seasonality and normalize
- Flag anomalies (sudden DSO spikes, aging concentration)

#### 3.3 Debt & Liquidity
- Map all debt facilities: principal, rate, maturity, covenants, security
- Calculate covenant compliance (current and projected)
- Build 13-week cash flow if not provided
- Identify liquidity runway (weeks of cash at current burn)
- Model scenarios: base case, downside, severe downside

#### 3.4 Cost Structure
- Classify all costs as fixed, variable, or semi-variable
- Benchmark against industry comparables (use public data)
- Identify cost reduction opportunities with estimated savings
- Rank by implementation speed: Quick Win (<30 days), Medium (30-90), Long-term (90+)

### Financial Model Structure
```
Inputs Tab     → Assumptions, scenarios, toggles
Historical Tab → 3-year actuals mapped to standard chart of accounts
Adjustments    → EBITDA bridge, NWC normalization
Projections    → 3-year forecast (monthly Y1, quarterly Y2-Y3)
Scenarios      → Base, Upside, Downside with key driver sensitivities
Outputs        → Summary dashboard, covenant compliance, cash flow waterfall
```

## Phase 4: Operational Assessment (Day 5-10)

### Framework: The 7 Levers
1. **Revenue Enhancement** — Pricing, mix, new channels, customer retention
2. **Cost Optimization** — Headcount, procurement, overhead, facilities
3. **Working Capital** — Receivables, payables, inventory management
4. **Asset Optimization** — Underutilized assets, sale-leaseback, disposals
5. **Organizational Design** — Structure, spans of control, capability gaps
6. **Technology & Process** — Automation opportunities, system rationalization
7. **Strategic Options** — Divestitures, partnerships, market repositioning

### For Each Lever
- Current state assessment (what exists today)
- Gap analysis (vs best practice or comparable benchmarks)
- Opportunity sizing ($ impact, confidence level)
- Implementation requirements (cost, time, dependencies, risks)
- Quick win identification (can it start in <30 days?)

## Phase 5: Synthesis (Day 8-12)

### Transformation Value Bridge
```
Current EBITDA (adjusted)
  + Revenue enhancement opportunities
  - Implementation costs (one-time)
  + Cost optimization savings
  + Working capital release (one-time cash impact)
  + Asset optimization proceeds
  ─────────────────────────────
  = Projected Transformed EBITDA (Year 2)
```

### Risk Assessment Matrix
Rate each initiative on:
- **Impact**: Low ($) / Medium ($$) / High ($$$)
- **Feasibility**: Low / Medium / High
- **Speed**: Quick Win / Medium / Long-term
- **Risk**: Execution risk, stakeholder resistance, dependency risk

### Prioritization
Plot on 2x2: Impact vs Feasibility. Recommend in this order:
1. High Impact + High Feasibility (do first)
2. High Impact + Low Feasibility (plan carefully)
3. Low Impact + High Feasibility (delegate/quick wins)
4. Low Impact + Low Feasibility (deprioritize)

## Phase 6: Deliverable (Day 10-14)

### Report Structure
1. Executive Summary (2 pages max)
2. Situation Overview & Engagement Scope
3. Financial Analysis & Adjusted EBITDA
4. Operational Assessment by Lever
5. Transformation Opportunities (ranked)
6. Implementation Roadmap (30/60/90-day plan)
7. Risk Factors & Mitigants
8. Appendices (detailed models, data sources, assumptions)

### Quality Standards
- Every finding sourced to specific data
- All financial figures independently verified or flagged
- Assumptions clearly stated and stress-tested
- Recommendations actionable with specific next steps
- Executive summary readable as standalone document
