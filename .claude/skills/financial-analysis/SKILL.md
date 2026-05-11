---
name: financial-analysis
description: Use this skill when performing financial modelling, ratio analysis, EBITDA adjustments, working capital analysis, debt analysis, scenario modelling, or any quantitative financial work within the RTS engagement. Trigger on mentions of P&L, balance sheet, cash flow, EBITDA, working capital, debt, covenants, projections, or financial model.
---

# Financial Analysis Skill

## Purpose

Execute the financial analysis phase of the RTS methodology with rigour.
This skill provides the formulas, frameworks, and validation checks for
every standard financial analysis performed during diligence.

## Adjusted EBITDA Bridge

### Step-by-step Process

1. Start with reported Net Income
2. Add back: Interest, Tax, Depreciation, Amortisation = Reported EBITDA
3. Identify and categorize adjustments:

| Category | Direction | Examples |
|----------|-----------|---------|
| Non-recurring charges | Add back | Restructuring, litigation settlements, one-time consulting |
| Non-recurring income | Remove | Asset sale gains, insurance recoveries, PPP forgiveness |
| Owner add-backs | Add back | Above-market owner compensation, personal expenses |
| Related party | Adjust | Below-market rent to related entity, management fees |
| Run-rate adjustments | Adjust | Full-year impact of mid-year events (hires, contracts, price changes) |
| Accounting corrections | Adjust | Misclassified items, policy changes |

4. Document every adjustment with:
   - Amount
   - Source document and page
   - Rationale (1-2 sentences)
   - Confidence level
   - Whether recurring or one-time

### Validation Checks
- Total adjustments should rarely exceed 30% of reported EBITDA (flag if so)
- Each adjustment should be independently verifiable
- Compare adjusted EBITDA margin to industry benchmarks
- Check year-over-year trends for consistency

## Working Capital Analysis

### Formulas
```
NWC = Accounts Receivable + Inventory + Prepaid Expenses
      - Accounts Payable - Accrued Liabilities - Deferred Revenue
      (excluding cash, debt, and tax-related items)

DSO = (Accounts Receivable / Revenue) × 365
DPO = (Accounts Payable / COGS) × 365
DIO = (Inventory / COGS) × 365
CCC = DSO + DIO - DPO  (Cash Conversion Cycle)

NWC % Revenue = NWC / LTM Revenue × 100
```

### Analysis Approach
1. Calculate monthly NWC for trailing 24 months
2. Plot trend line — is NWC growing faster than revenue?
3. Calculate DSO, DPO, DIO monthly — identify deterioration
4. Benchmark against industry (if data available)
5. Identify seasonality — what's the normalized NWC level?
6. Estimate NWC release opportunity = (Current DSO - Target DSO) × Daily Revenue

## 13-Week Cash Flow Model

### Structure
```
Week 1 | Week 2 | ... | Week 13
───────────────────────────────
Opening Cash Balance
+ Cash Receipts
  - Collections from AR
  - Other receipts
- Cash Disbursements
  - Payroll
  - Rent / Occupancy
  - Supplier payments
  - Debt service (interest + principal)
  - Tax payments
  - Capex
  - Other
= Net Cash Flow
= Closing Cash Balance
- Minimum Cash Requirement
= Available Liquidity
+ Undrawn Facilities
= Total Liquidity Headroom
```

### Key Principles
- Use collection patterns, not revenue recognition, for receipts
- Payroll is the most predictable line — get exact dates and amounts
- Map debt service from the debt schedule exactly
- Flag any week where liquidity headroom < 0

## Scenario Analysis

### Standard Scenarios
1. **Base Case**: Management plan with moderate haircuts on optimistic assumptions
2. **Downside**: Revenue -10-15%, delayed collections, no new initiatives
3. **Severe Downside**: Revenue -20-25%, customer losses, covenant breach triggers
4. **Upside**: Quick wins deliver early, revenue holds, working capital improves

### Sensitivity Table
Vary the 3-5 most impactful assumptions independently:
- Revenue growth rate: -5%, 0%, +5%, +10%
- Gross margin: -200bps, flat, +200bps
- DSO change: +10 days, flat, -10 days
- Cost savings realization: 50%, 75%, 100%

Show impact on: EBITDA, Free Cash Flow, Covenant Compliance, Liquidity Runway

## Output Format

All financial analysis outputs should be:
1. Structured data (JSON or CSV) for programmatic use
2. Summary narrative (2-3 paragraphs) for the report
3. Key metrics table for executive summary
4. Charts/visualizations where they add clarity
5. Source citations for every input data point
