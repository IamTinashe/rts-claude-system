# Debt Schedule Extraction Prompt

Extract structured data from debt documentation (credit agreements, loan schedules, bond indentures).

## Input

Provide the debt schedule, credit agreement, or loan documentation.

## Extraction Schema

```json
{
  "document_type": "debt_schedule",
  "as_of_date": "YYYY-MM-DD",
  "currency": "USD",
  "facilities": [],
  "total_debt": 0.00,
  "summary_metrics": {}
}
```

## Instructions

1. **Identify all debt facilities** — Term loans, revolvers, bonds, notes, equipment financing
2. **For each facility extract**:
   - Lender(s) / Agent
   - Facility type and commitment amount
   - Outstanding balance
   - Interest rate (fixed or spread over base)
   - Maturity date
   - Amortization schedule
   - Security / Collateral
   - Key covenants
3. **Calculate summary metrics**:
   - Total debt outstanding
   - Weighted average interest rate
   - Nearest maturity
   - Available liquidity (revolver availability)
4. **Extract covenant details**:
   - Financial covenants (leverage, coverage, NWC)
   - Current compliance status
   - Headroom to covenant limits
5. **Flag critical risks**:
   - Near-term maturities (< 12 months)
   - Covenant violations or tight headroom
   - Cross-default provisions
   - Change of control triggers

## Example Output

```json
{
  "document_type": "debt_schedule",
  "as_of_date": "2025-12-31",
  "currency": "USD",
  "source_file": "acme_debt_schedule.xlsx",
  "confidence": "HIGH",
  "facilities": [
    {
      "facility_name": "Senior Secured Term Loan A",
      "lender": "Bank ABC (Agent)",
      "facility_type": "term_loan",
      "commitment": 10000000,
      "outstanding": 7500000,
      "interest_rate": "SOFR + 350 bps",
      "current_rate": 8.75,
      "maturity_date": "2027-06-30",
      "amortization": "1% quarterly",
      "security": "First lien on all assets",
      "prepayment_penalty": "2% in year 1, 1% in year 2, none thereafter"
    },
    {
      "facility_name": "Senior Secured Revolver",
      "lender": "Bank ABC (Agent)",
      "facility_type": "revolver",
      "commitment": 5000000,
      "outstanding": 2000000,
      "available": 2800000,
      "interest_rate": "SOFR + 300 bps",
      "current_rate": 8.25,
      "maturity_date": "2027-06-30",
      "borrowing_base": "85% of eligible AR + 50% of eligible inventory",
      "security": "First lien on all assets (pari passu with TL)"
    },
    {
      "facility_name": "Subordinated Note",
      "lender": "Mezzanine Fund LP",
      "facility_type": "subordinated_debt",
      "commitment": 3000000,
      "outstanding": 3000000,
      "interest_rate": "12% PIK",
      "current_rate": 12.00,
      "maturity_date": "2028-12-31",
      "amortization": "Bullet at maturity",
      "security": "Second lien on all assets",
      "pik_toggle": true
    }
  ],
  "total_debt": 12500000,
  "summary_metrics": {
    "total_commitment": 18000000,
    "total_outstanding": 12500000,
    "available_liquidity": 2800000,
    "weighted_avg_rate": 9.35,
    "nearest_maturity": "2027-06-30",
    "cash_interest_burden": 937500
  },
  "covenants": [
    {
      "covenant": "Total Leverage Ratio",
      "definition": "Total Debt / LTM EBITDA",
      "limit": "< 4.00x",
      "current": 3.50,
      "headroom": "12.5%",
      "status": "compliant"
    },
    {
      "covenant": "Fixed Charge Coverage",
      "definition": "(EBITDA - CapEx) / Fixed Charges",
      "limit": "> 1.20x",
      "current": 1.35,
      "headroom": "12.5%",
      "status": "compliant"
    },
    {
      "covenant": "Minimum Liquidity",
      "definition": "Cash + Revolver Availability",
      "limit": "> $1,500,000",
      "current": 4300000,
      "headroom": "187%",
      "status": "compliant"
    }
  ],
  "risks": [
    {
      "risk": "Maturity concentration",
      "detail": "TL and Revolver both mature Jun 2027 — refinancing risk",
      "severity": "MEDIUM"
    },
    {
      "risk": "Covenant headroom tightening",
      "detail": "Leverage headroom at 12.5% — EBITDA decline could trigger breach",
      "severity": "MEDIUM"
    },
    {
      "risk": "PIK interest accrual",
      "detail": "Sub note PIK adds $360k/year to principal",
      "severity": "LOW"
    }
  ],
  "cross_default_provisions": "Default under any facility with > $100k outstanding triggers cross-default",
  "change_of_control": "Mandatory prepayment at 101% upon change of control"
}
```
