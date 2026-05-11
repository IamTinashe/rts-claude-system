# Org Chart / Headcount Extraction Prompt

Extract organizational structure and headcount data from org charts, HR reports, or payroll summaries.

## Input

Provide the org chart, headcount report, or payroll summary.

## Extraction Schema

```json
{
  "document_type": "org_data",
  "as_of_date": "YYYY-MM-DD",
  "total_headcount": 0,
  "total_payroll_cost": 0.00,
  "departments": [],
  "leadership_team": [],
  "insights": []
}
```

## Instructions

1. **Extract hierarchy** — CEO → VPs → Directors → Managers → Staff
2. **Count headcount by department** — Group into standard categories
3. **Extract compensation data** if available:
   - Base salary
   - Bonus / incentive
   - Benefits cost
   - Fully-loaded cost
4. **Identify leadership team** — C-suite and direct reports
5. **Calculate key metrics**:
   - Revenue per employee (if revenue known)
   - Payroll as % of revenue
   - Span of control ratios
   - Management layers
6. **Flag anomalies for RTS**:
   - High management-to-staff ratios
   - Redundant positions
   - Below-market or above-market compensation
   - Key person dependencies

## Example Output

```json
{
  "document_type": "org_data",
  "as_of_date": "2025-12-31",
  "source_file": "acme_org_chart_dec2025.pdf",
  "confidence": "HIGH",
  "total_headcount": 127,
  "total_payroll_cost": 12500000,
  "average_cost_per_employee": 98425,
  "departments": [
    {
      "department": "Sales",
      "headcount": 25,
      "payroll_cost": 3200000,
      "avg_cost": 128000,
      "manager_count": 4,
      "span_of_control": 5.25
    },
    {
      "department": "Operations",
      "headcount": 45,
      "payroll_cost": 3600000,
      "avg_cost": 80000,
      "manager_count": 5,
      "span_of_control": 8.0
    },
    {
      "department": "Engineering",
      "headcount": 22,
      "payroll_cost": 3300000,
      "avg_cost": 150000,
      "manager_count": 3,
      "span_of_control": 6.33
    },
    {
      "department": "Finance",
      "headcount": 12,
      "payroll_cost": 1400000,
      "avg_cost": 116667,
      "manager_count": 2,
      "span_of_control": 5.0
    },
    {
      "department": "HR",
      "headcount": 8,
      "payroll_cost": 640000,
      "avg_cost": 80000,
      "manager_count": 1,
      "span_of_control": 7.0
    },
    {
      "department": "Executive",
      "headcount": 5,
      "payroll_cost": 1800000,
      "avg_cost": 360000,
      "manager_count": 0,
      "notes": "C-suite"
    },
    {
      "department": "Admin/Other",
      "headcount": 10,
      "payroll_cost": 560000,
      "avg_cost": 56000,
      "manager_count": 1,
      "span_of_control": 9.0
    }
  ],
  "leadership_team": [
    {"name": "John Doe", "title": "CEO", "tenure_years": 5, "compensation": 450000},
    {"name": "Jane Smith", "title": "CFO", "tenure_years": 3, "compensation": 350000},
    {"name": "Bob Johnson", "title": "COO", "tenure_years": 7, "compensation": 325000},
    {"name": "Sarah Williams", "title": "CTO", "tenure_years": 2, "compensation": 375000},
    {"name": "Mike Brown", "title": "VP Sales", "tenure_years": 4, "compensation": 300000}
  ],
  "metrics": {
    "management_layers": 4,
    "avg_span_of_control": 6.5,
    "manager_to_ic_ratio": "1:7",
    "revenue_per_employee": 118110,
    "payroll_pct_of_revenue": 83.3
  },
  "insights": [
    {
      "finding": "Low span of control in Sales",
      "detail": "4 managers for 21 ICs (5.25:1) vs. benchmark 8:1",
      "opportunity": "Consolidate to 3 managers — save ~$130k",
      "confidence": "MEDIUM"
    },
    {
      "finding": "High executive compensation",
      "detail": "C-suite at $360k avg vs. $280k benchmark for company size",
      "opportunity": "May indicate over-investment in leadership",
      "confidence": "LOW"
    },
    {
      "finding": "Engineering costs elevated",
      "detail": "$150k avg vs. $130k market rate for region",
      "opportunity": "Review for market adjustment or offshore mix",
      "confidence": "MEDIUM"
    }
  ],
  "rts_flags": [
    {
      "flag": "Key person risk",
      "detail": "COO Bob Johnson owns critical vendor relationships",
      "mitigation": "Document processes; cross-train"
    },
    {
      "flag": "Recent leadership turnover",
      "detail": "CTO joined 2 years ago; 3rd CTO in 5 years",
      "mitigation": "Assess stability of tech strategy"
    }
  ]
}
```
