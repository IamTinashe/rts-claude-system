# P&L Extraction Prompt

Extract structured data from a Profit & Loss statement.

## Input

Provide the P&L document text or image.

## Extraction Schema

```json
{
  "document_type": "profit_and_loss",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD",
  "currency": "USD",
  "line_items": [
    {
      "account": "Account Name",
      "category": "revenue|cogs|operating_expense|other_income|other_expense|tax",
      "amount": 0.00,
      "notes": "Any adjustments or footnotes"
    }
  ],
  "totals": {
    "revenue": 0.00,
    "gross_profit": 0.00,
    "operating_income": 0.00,
    "net_income": 0.00
  }
}
```

## Instructions

1. **Identify the reporting period** — Look for headers like "For the year ended" or "Q1 2025"
2. **Identify currency** — Default to USD if not specified; flag if ambiguous
3. **Extract every line item** with its amount
4. **Categorize each line item** into the appropriate category
5. **Verify mathematical integrity**:
   - Revenue - COGS = Gross Profit
   - Gross Profit - Operating Expenses = Operating Income
   - Sum of all items = Net Income
6. **Flag anomalies**:
   - Negative revenue
   - Unusual expense ratios (SG&A > 50% of revenue)
   - Missing standard line items
7. **Assign confidence level**:
   - HIGH: Audited financials with clear formatting
   - MEDIUM: Management accounts or unclear formatting
   - LOW: Partial data or significant assumptions required

## Example Output

```json
{
  "document_type": "profit_and_loss",
  "period_start": "2025-01-01",
  "period_end": "2025-12-31",
  "currency": "USD",
  "source_file": "acme_pl_2025.pdf",
  "confidence": "HIGH",
  "line_items": [
    {"account": "Product Revenue", "category": "revenue", "amount": 12000000, "notes": null},
    {"account": "Service Revenue", "category": "revenue", "amount": 3000000, "notes": null},
    {"account": "Cost of Goods Sold", "category": "cogs", "amount": -9000000, "notes": null},
    {"account": "Salaries & Wages", "category": "operating_expense", "amount": -2500000, "notes": null},
    {"account": "Rent & Utilities", "category": "operating_expense", "amount": -500000, "notes": null},
    {"account": "Depreciation", "category": "operating_expense", "amount": -300000, "notes": null},
    {"account": "Interest Expense", "category": "other_expense", "amount": -200000, "notes": null},
    {"account": "Income Tax", "category": "tax", "amount": -600000, "notes": "Effective rate 24%"}
  ],
  "totals": {
    "revenue": 15000000,
    "gross_profit": 6000000,
    "operating_income": 2700000,
    "net_income": 1900000
  },
  "integrity_checks": {
    "revenue_subtotal_verified": true,
    "gross_profit_verified": true,
    "net_income_verified": true
  },
  "anomalies": []
}
```
