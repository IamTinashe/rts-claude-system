# Balance Sheet Extraction Prompt

Extract structured data from a Balance Sheet.

## Input

Provide the Balance Sheet document text or image.

## Extraction Schema

```json
{
  "document_type": "balance_sheet",
  "as_of_date": "YYYY-MM-DD",
  "currency": "USD",
  "assets": {
    "current": [],
    "non_current": [],
    "total": 0.00
  },
  "liabilities": {
    "current": [],
    "non_current": [],
    "total": 0.00
  },
  "equity": {
    "items": [],
    "total": 0.00
  }
}
```

## Instructions

1. **Identify the as-of date** — Usually in header "As of December 31, 2025"
2. **Classify each line item** into the correct category:
   - Current Assets: Cash, AR, Inventory, Prepaid (< 12 months)
   - Non-Current Assets: PP&E, Intangibles, Investments
   - Current Liabilities: AP, Accrued, Short-term debt (< 12 months)
   - Non-Current Liabilities: Long-term debt, Deferred tax
   - Equity: Common stock, Retained earnings, APIC
3. **Verify the accounting equation**: Assets = Liabilities + Equity
4. **Extract key working capital items** for NWC calculation:
   - Accounts Receivable
   - Inventory
   - Prepaid Expenses
   - Accounts Payable
   - Accrued Liabilities
   - Deferred Revenue
5. **Flag anomalies**:
   - Negative cash balance
   - AR > 25% of annual revenue (if known)
   - Negative equity
   - Assets ≠ Liabilities + Equity

## Example Output

```json
{
  "document_type": "balance_sheet",
  "as_of_date": "2025-12-31",
  "currency": "USD",
  "source_file": "acme_bs_2025.pdf",
  "confidence": "HIGH",
  "assets": {
    "current": [
      {"account": "Cash and Cash Equivalents", "amount": 1500000},
      {"account": "Accounts Receivable", "amount": 2500000},
      {"account": "Inventory", "amount": 1800000},
      {"account": "Prepaid Expenses", "amount": 200000}
    ],
    "non_current": [
      {"account": "Property, Plant & Equipment", "amount": 4500000},
      {"account": "Intangible Assets", "amount": 800000}
    ],
    "total": 11300000
  },
  "liabilities": {
    "current": [
      {"account": "Accounts Payable", "amount": 1500000},
      {"account": "Accrued Liabilities", "amount": 400000},
      {"account": "Current Portion of Debt", "amount": 500000},
      {"account": "Deferred Revenue", "amount": 300000}
    ],
    "non_current": [
      {"account": "Long-term Debt", "amount": 3000000},
      {"account": "Deferred Tax Liability", "amount": 200000}
    ],
    "total": 5900000
  },
  "equity": {
    "items": [
      {"account": "Common Stock", "amount": 1000000},
      {"account": "Additional Paid-in Capital", "amount": 2000000},
      {"account": "Retained Earnings", "amount": 2400000}
    ],
    "total": 5400000
  },
  "integrity_checks": {
    "assets_equals_liabilities_plus_equity": true,
    "current_assets_subtotal_verified": true,
    "current_liabilities_subtotal_verified": true
  },
  "working_capital_inputs": {
    "accounts_receivable": 2500000,
    "inventory": 1800000,
    "prepaid": 200000,
    "accounts_payable": 1500000,
    "accrued_liabilities": 400000,
    "deferred_revenue": 300000
  },
  "anomalies": []
}
```
