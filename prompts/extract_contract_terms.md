# Contract Terms Extraction Prompt

Extract key terms from commercial contracts (customer agreements, supplier contracts, leases).

## Input

Provide the contract document text or image.

## Extraction Schema

```json
{
  "document_type": "contract",
  "contract_type": "customer|supplier|lease|employment|credit|other",
  "parties": [],
  "effective_date": "YYYY-MM-DD",
  "expiration_date": "YYYY-MM-DD",
  "auto_renewal": false,
  "financial_terms": {},
  "key_clauses": [],
  "risks": []
}
```

## Instructions

1. **Identify contract type** — Customer, supplier, lease, employment, credit facility
2. **Extract parties** — Full legal names of all parties
3. **Extract dates**:
   - Effective/Start date
   - Expiration/End date
   - Notice periods for termination
   - Renewal terms (auto-renew?)
4. **Extract financial terms**:
   - Contract value (total and annual if applicable)
   - Payment terms (Net 30, etc.)
   - Pricing structure (fixed, variable, tiered)
   - Minimum commitments
   - Penalties or liquidated damages
5. **Flag key clauses**:
   - Change of control provisions
   - Termination for convenience
   - Material adverse change (MAC)
   - Non-compete / exclusivity
   - Indemnification
   - Limitation of liability
6. **Assess risks for RTS context**:
   - Can counterparty terminate on distress?
   - Are there minimum volume commitments we can't meet?
   - Is pricing favorable or unfavorable vs. market?

## Example Output (Customer Contract)

```json
{
  "document_type": "contract",
  "contract_type": "customer",
  "source_file": "acme_customer_xyz_agreement.pdf",
  "confidence": "HIGH",
  "parties": [
    {"role": "supplier", "name": "Acme Corporation"},
    {"role": "customer", "name": "XYZ Industries LLC"}
  ],
  "effective_date": "2023-01-01",
  "expiration_date": "2026-12-31",
  "auto_renewal": true,
  "renewal_terms": "Auto-renews for 1-year periods unless 90-day notice",
  "financial_terms": {
    "total_contract_value": 5000000,
    "annual_value": 1250000,
    "payment_terms": "Net 45",
    "pricing_structure": "Fixed price per unit with annual CPI adjustment",
    "minimum_commitment": "500,000 units per year",
    "penalties": "15% of remaining contract value if terminated early"
  },
  "key_clauses": [
    {
      "clause": "Change of Control",
      "summary": "Customer may terminate within 60 days of change of control",
      "risk_level": "HIGH"
    },
    {
      "clause": "Termination for Convenience",
      "summary": "Either party with 180-day notice",
      "risk_level": "MEDIUM"
    },
    {
      "clause": "Most Favored Customer",
      "summary": "Customer entitled to lowest price offered to any customer",
      "risk_level": "LOW"
    }
  ],
  "risks": [
    {
      "risk": "Change of control trigger",
      "impact": "Customer could terminate on acquisition",
      "mitigation": "Negotiate waiver or carve-out in transaction docs"
    },
    {
      "risk": "Minimum commitment",
      "impact": "May not meet 500k units if demand declines",
      "mitigation": "Model downside scenarios; negotiate amendment if needed"
    }
  ]
}
```

## Example Output (Lease Agreement)

```json
{
  "document_type": "contract",
  "contract_type": "lease",
  "source_file": "headquarters_lease.pdf",
  "confidence": "HIGH",
  "parties": [
    {"role": "tenant", "name": "Acme Corporation"},
    {"role": "landlord", "name": "ABC Properties REIT"}
  ],
  "effective_date": "2020-01-01",
  "expiration_date": "2030-12-31",
  "auto_renewal": false,
  "renewal_terms": "Two 5-year renewal options at 95% of market rate",
  "financial_terms": {
    "monthly_base_rent": 85000,
    "annual_base_rent": 1020000,
    "escalation": "3% annual increase",
    "cam_charges": "Triple net - tenant pays taxes, insurance, maintenance",
    "security_deposit": 255000,
    "tenant_improvement_allowance": "None remaining"
  },
  "key_clauses": [
    {
      "clause": "Assignment",
      "summary": "Landlord consent required; not to be unreasonably withheld",
      "risk_level": "MEDIUM"
    },
    {
      "clause": "Subletting",
      "summary": "Permitted with landlord consent; 50% of profit to landlord",
      "risk_level": "LOW"
    },
    {
      "clause": "Default",
      "summary": "30-day cure period for monetary default",
      "risk_level": "MEDIUM"
    }
  ],
  "risks": [
    {
      "risk": "Above-market rent",
      "impact": "$85k/mo is ~15% above current market for comparable space",
      "mitigation": "Negotiate early termination or sublease excess space"
    },
    {
      "risk": "Long remaining term",
      "impact": "5 years remaining; ~$5M obligation",
      "mitigation": "Include in restructuring discussions with landlord"
    }
  ]
}
```
