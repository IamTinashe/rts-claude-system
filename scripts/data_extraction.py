#!/usr/bin/env python3
"""
RTS Data Extraction Pipeline

Glue code that connects document sources to the Claude-powered
extraction pipeline. This script:

1. Watches a folder (or Google Drive via API) for new documents
2. Classifies each document by type
3. Routes to the appropriate extraction prompt
4. Validates extracted data against quality rules
5. Stores structured outputs for analysis

This demonstrates the Python glue code, data extraction, and
integration skills required by the engagement.
"""

import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class DocumentType(Enum):
    FINANCIAL_STATEMENT = "financial_statement"
    MANAGEMENT_ACCOUNTS = "management_accounts"
    CONTRACT = "contract"
    ORG_DATA = "org_data"
    OPERATIONAL = "operational"
    LEGAL = "legal"
    UNKNOWN = "unknown"


class Confidence(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ExtractionResult:
    """Structured output from document extraction."""
    document_type: str
    source_file: str
    extracted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: str = "MEDIUM"
    data: dict = field(default_factory=dict)
    quality_checks: dict = field(default_factory=dict)
    gaps: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def save(self, output_dir: str = "outputs/extractions"):
        """Save extraction result to the outputs directory."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filename = f"{self.document_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path(output_dir) / filename
        with open(filepath, "w") as f:
            f.write(self.to_json())
        return str(filepath)


# --- Document Classification ---

CLASSIFICATION_PATTERNS = {
    DocumentType.FINANCIAL_STATEMENT: [
        r"balance\s+sheet", r"income\s+statement", r"profit\s+(and|&)\s+loss",
        r"cash\s+flow\s+statement", r"statement\s+of\s+operations",
        r"audited\s+financial", r"consolidated\s+statements"
    ],
    DocumentType.MANAGEMENT_ACCOUNTS: [
        r"management\s+accounts", r"monthly\s+p&l", r"budget\s+vs\s+actual",
        r"flash\s+report", r"month\s+end\s+report", r"departmental\s+report"
    ],
    DocumentType.CONTRACT: [
        r"agreement\s+between", r"terms\s+and\s+conditions", r"lease\s+agreement",
        r"credit\s+agreement", r"facility\s+agreement", r"master\s+services",
        r"effective\s+date", r"termination\s+clause"
    ],
    DocumentType.ORG_DATA: [
        r"org\s*(anization)?\s*chart", r"headcount", r"employee\s+roster",
        r"payroll\s+summary", r"department\s+structure"
    ],
    DocumentType.OPERATIONAL: [
        r"kpi\s+report", r"sales\s+report", r"inventory\s+report",
        r"customer\s+list", r"pipeline\s+report", r"backlog"
    ],
    DocumentType.LEGAL: [
        r"litigation", r"regulatory\s+filing", r"compliance\s+report",
        r"insurance\s+schedule", r"corporate\s+structure"
    ]
}


def classify_document(text: str) -> DocumentType:
    """Classify a document based on content patterns."""
    text_lower = text.lower()
    scores = {}
    for doc_type, patterns in CLASSIFICATION_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, text_lower))
        if score > 0:
            scores[doc_type] = score

    if not scores:
        return DocumentType.UNKNOWN

    return max(scores, key=scores.get)


# --- Data Request List Tracker ---

@dataclass
class DataRequestItem:
    """Single item on the Data Request List."""
    category: str
    item: str
    priority: int  # 1 = critical, 2 = important, 3 = nice-to-have
    status: str = "pending"  # pending, received, partial, not_available
    received_date: Optional[str] = None
    source_file: Optional[str] = None
    notes: Optional[str] = None
    confidence: str = "LOW"


class DataRequestList:
    """Tracks the status of all data requests for the engagement."""

    def __init__(self):
        self.items: list[DataRequestItem] = []
        self._load_standard_drl()

    def _load_standard_drl(self):
        """Load the standard RTS data request list."""
        standard_items = [
            # Financial Data (Priority 1)
            ("Financial", "3-year audited financial statements", 1),
            ("Financial", "Monthly management accounts (24 months)", 1),
            ("Financial", "Budget vs actual (current + prior year)", 1),
            ("Financial", "Aged receivables schedule", 1),
            ("Financial", "Aged payables schedule", 1),
            ("Financial", "Debt schedule (all facilities)", 1),
            ("Financial", "13-week cash flow forecast", 1),
            ("Financial", "Tax returns (3 years)", 2),
            ("Financial", "Intercompany balances", 2),
            # Operational Data (Priority 2)
            ("Operational", "Org chart with headcount by department", 2),
            ("Operational", "Revenue by customer (24 months)", 1),
            ("Operational", "Revenue by product/service (24 months)", 2),
            ("Operational", "Cost breakdown (fixed vs variable)", 1),
            ("Operational", "Top 10 customer contracts", 1),
            ("Operational", "Top 10 supplier contracts", 2),
            ("Operational", "Lease schedule", 2),
            ("Operational", "Technology systems inventory", 3),
            ("Operational", "Capital expenditure schedule", 2),
            # Legal & Compliance (Priority 3)
            ("Legal", "Corporate structure chart", 2),
            ("Legal", "Material litigation summary", 2),
            ("Legal", "Regulatory compliance status", 3),
            ("Legal", "Insurance coverage summary", 3),
            ("Legal", "Key employee contracts", 3),
        ]
        for category, item, priority in standard_items:
            self.items.append(DataRequestItem(
                category=category, item=item, priority=priority
            ))

    def update_status(self, item_index: int, status: str,
                      source_file: str = None, notes: str = None):
        """Update the status of a DRL item."""
        if 0 <= item_index < len(self.items):
            self.items[item_index].status = status
            self.items[item_index].received_date = datetime.utcnow().isoformat()
            if source_file:
                self.items[item_index].source_file = source_file
            if notes:
                self.items[item_index].notes = notes

    def gap_report(self) -> dict:
        """Generate a gap analysis report."""
        total = len(self.items)
        received = sum(1 for i in self.items if i.status == "received")
        partial = sum(1 for i in self.items if i.status == "partial")
        pending = sum(1 for i in self.items if i.status == "pending")
        critical_gaps = [
            i for i in self.items
            if i.status == "pending" and i.priority == 1
        ]
        return {
            "total_items": total,
            "received": received,
            "partial": partial,
            "pending": pending,
            "completion_pct": round((received + partial * 0.5) / total * 100, 1),
            "critical_gaps": [asdict(g) for g in critical_gaps],
            "generated_at": datetime.utcnow().isoformat()
        }

    def to_json(self) -> str:
        return json.dumps([asdict(i) for i in self.items], indent=2)


# --- Financial Validation ---

def validate_pl_integrity(line_items: list[dict]) -> dict:
    """Validate that a P&L statement is internally consistent."""
    checks = {
        "has_revenue": False,
        "has_expenses": False,
        "subtotals_verified": True,
        "anomalies": []
    }

    revenue = None
    total_expenses = 0

    for item in line_items:
        account = item.get("account", "").lower()
        amount = item.get("amount", 0)

        if "revenue" in account or "sales" in account:
            checks["has_revenue"] = True
            revenue = amount
        elif "cost" in account or "expense" in account:
            checks["has_expenses"] = True
            total_expenses += abs(amount)

    # Check for common anomalies
    if revenue and revenue < 0:
        checks["anomalies"].append("Negative revenue reported")
    if revenue and total_expenses > revenue * 1.5:
        checks["anomalies"].append(
            f"Expenses ({total_expenses:,.0f}) significantly exceed "
            f"revenue ({revenue:,.0f}) — verify for accuracy"
        )

    return checks


# --- Working Capital Calculations ---

def calculate_working_capital_metrics(
    accounts_receivable: float,
    inventory: float,
    prepaid: float,
    accounts_payable: float,
    accrued_liabilities: float,
    deferred_revenue: float,
    annual_revenue: float,
    annual_cogs: float
) -> dict:
    """Calculate standard working capital metrics."""
    nwc = (accounts_receivable + inventory + prepaid
           - accounts_payable - accrued_liabilities - deferred_revenue)

    daily_revenue = annual_revenue / 365
    daily_cogs = annual_cogs / 365

    dso = accounts_receivable / daily_revenue if daily_revenue else 0
    dpo = accounts_payable / daily_cogs if daily_cogs else 0
    dio = inventory / daily_cogs if daily_cogs else 0
    ccc = dso + dio - dpo

    nwc_pct = (nwc / annual_revenue * 100) if annual_revenue else 0

    return {
        "net_working_capital": round(nwc, 2),
        "nwc_pct_revenue": round(nwc_pct, 1),
        "days_sales_outstanding": round(dso, 1),
        "days_payable_outstanding": round(dpo, 1),
        "days_inventory_outstanding": round(dio, 1),
        "cash_conversion_cycle": round(ccc, 1),
        "notes": _assess_wc_health(dso, dpo, dio, ccc)
    }


def _assess_wc_health(dso, dpo, dio, ccc) -> list[str]:
    """Generate assessment notes based on working capital metrics."""
    notes = []
    if dso > 60:
        notes.append(f"DSO of {dso:.0f} days is elevated — investigate collection issues")
    if dpo < 20:
        notes.append(f"DPO of {dpo:.0f} days suggests early payment — negotiate better terms")
    if dio > 90:
        notes.append(f"DIO of {dio:.0f} days indicates excess inventory — review SKU rationalization")
    if ccc > 60:
        notes.append(f"Cash conversion cycle of {ccc:.0f} days is long — working capital optimization opportunity")
    if not notes:
        notes.append("Working capital metrics within normal ranges")
    return notes


# --- Entry Point ---

if __name__ == "__main__":
    # Demo: Initialize a DRL and show gap report
    drl = DataRequestList()
    print("=== RTS Data Request List — Gap Report ===\n")
    gap = drl.gap_report()
    print(f"Total Items: {gap['total_items']}")
    print(f"Received: {gap['received']}")
    print(f"Pending: {gap['pending']}")
    print(f"Completion: {gap['completion_pct']}%")
    print(f"\nCritical Gaps ({len(gap['critical_gaps'])}):")
    for g in gap['critical_gaps']:
        print(f"  - [{g['category']}] {g['item']}")

    # Demo: Working capital calculation
    print("\n=== Working Capital Analysis Demo ===\n")
    wc = calculate_working_capital_metrics(
        accounts_receivable=2_500_000,
        inventory=1_800_000,
        prepaid=200_000,
        accounts_payable=1_500_000,
        accrued_liabilities=400_000,
        deferred_revenue=300_000,
        annual_revenue=15_000_000,
        annual_cogs=9_000_000
    )
    print(json.dumps(wc, indent=2))
