---
name: data-collection
description: Use this skill when extracting, classifying, or structuring data from uploaded documents, connected data sources (Google Drive, email, spreadsheets), or interview transcripts. Covers document parsing, entity extraction, data classification, quality checks, and gap analysis. Trigger on uploads, data requests, document review, or when populating the data room.
---

# Data Collection Skill

## Purpose

Automate the extraction and structuring of data from diverse sources into the
standardized formats required by the RTS methodology. This replaces the manual
process of analysts reading documents and typing findings into spreadsheets.

## Document Classification

When a document is uploaded or accessed via MCP, classify it first:

| Category | Examples | Extraction Approach |
|----------|----------|-------------------|
| Financial Statements | P&L, Balance Sheet, Cash Flow | Extract line items into structured table |
| Management Accounts | Monthly P&L, departmental reports | Map to standard chart of accounts |
| Contracts | Customer agreements, leases, debt docs | Extract key terms, dates, amounts |
| Org Data | Org charts, headcount lists, payroll | Extract hierarchy, counts, costs |
| Operational | KPI reports, sales data, inventory | Extract metrics into time series |
| Legal | Litigation summaries, compliance docs | Extract status, exposure, timelines |

## Extraction Patterns

### Financial Statement Extraction
When processing a P&L, Balance Sheet, or Cash Flow statement:

1. Identify the reporting period and currency
2. Extract every line item with its amount
3. Verify mathematical integrity (subtotals sum correctly)
4. Map to the standard chart of accounts (see rts-methodology skill)
5. Flag any unusual items or reclassifications
6. Output as structured JSON:

```json
{
  "document_type": "profit_and_loss",
  "period": "2025-01-01/2025-12-31",
  "currency": "USD",
  "source_file": "client_pl_2025.pdf",
  "confidence": "HIGH",
  "line_items": [
    {"account": "Revenue", "amount": 15000000, "notes": null},
    {"account": "COGS", "amount": -9000000, "notes": null}
  ],
  "integrity_checks": {
    "subtotals_verified": true,
    "anomalies": []
  }
}
```

### Contract Key Terms Extraction
For any contract or agreement:

```json
{
  "document_type": "contract",
  "parties": ["Company A", "Company B"],
  "effective_date": "2024-01-15",
  "expiry_date": "2027-01-14",
  "auto_renewal": true,
  "termination_notice_days": 90,
  "annual_value": 500000,
  "key_terms": ["Exclusivity clause in Section 4.2", "Change of control trigger in Section 8"],
  "risks": ["No force majeure clause", "Uncapped liability"],
  "confidence": "MEDIUM",
  "notes": "Missing Schedule B referenced in Section 3"
}
```

### Interview/Meeting Notes Structuring
When processing interview transcripts or meeting notes:

1. Extract factual claims (with speaker attribution)
2. Separate opinions from facts
3. Identify action items and data requests
4. Flag contradictions with other sources
5. Map insights to the relevant RTS phase/lever

## Data Quality Framework

For every data point extracted, assign:

- **Source**: Exact document, page, section
- **Confidence**: HIGH (verified/audited), MEDIUM (management-provided), LOW (estimated/verbal)
- **Freshness**: Date of the underlying data
- **Cross-reference**: Does it match other sources? Flag conflicts.

## Gap Analysis

After each collection round, run the Data Request List (from rts-methodology)
as a checklist. For each missing item:

1. Flag it as a gap
2. Assess criticality (blocking analysis? or nice-to-have?)
3. Draft a specific follow-up request to the client
4. Suggest alternative data sources or estimation methods

## MCP Integration

Use connected MCP servers to:

- **Google Drive**: Search for and read documents from the client data room
- **Gmail**: Monitor for incoming data deliveries, parse attachments
- **Google Sheets**: Write extracted data into structured worksheets

Always verify that MCP-sourced data matches what was expected in the DRL.
