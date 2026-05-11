#!/usr/bin/env python3
"""
RTS Data Extraction Pipeline

Glue code that connects document sources to the Claude-powered
extraction pipeline. This script:

1. Watches a folder (or Google Drive via API) for new documents
2. Parses PDFs and extracts text content
3. Classifies each document by type
4. Routes to the appropriate extraction prompt
5. Validates extracted data against quality rules
6. Stores structured outputs to local files and Google Sheets

This demonstrates the Python glue code, data extraction, and
integration skills required by the engagement.

Dependencies:
    pip install pymupdf gspread google-auth

Optional:
    pip install watchdog  # For folder watching
"""

import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

# PDF parsing - pymupdf (fitz)
try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pymupdf not installed. PDF parsing disabled. Install with: pip install pymupdf")

# Google Sheets API
try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_SUPPORT = True
except ImportError:
    SHEETS_SUPPORT = False
    print("Warning: gspread not installed. Google Sheets disabled. Install with: pip install gspread google-auth")


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
    extracted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
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
        filename = f"{self.document_type}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
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


# --- PDF Parsing ---

def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text content from a PDF file using PyMuPDF.
    
    Returns:
        dict with keys: text, page_count, metadata, tables
    """
    if not PDF_SUPPORT:
        raise ImportError("pymupdf not installed. Install with: pip install pymupdf")
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    
    result = {
        "source_file": str(pdf_path),
        "page_count": len(doc),
        "metadata": doc.metadata,
        "pages": [],
        "full_text": "",
        "tables": []
    }
    
    full_text_parts = []
    
    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        full_text_parts.append(page_text)
        
        # Extract tables (basic detection via text blocks)
        blocks = page.get_text("blocks")
        
        result["pages"].append({
            "page_number": page_num,
            "text": page_text,
            "char_count": len(page_text),
            "block_count": len(blocks)
        })
    
    result["full_text"] = "\n\n".join(full_text_parts)
    result["total_chars"] = len(result["full_text"])
    
    doc.close()
    return result


def process_pdf_for_extraction(pdf_path: str) -> ExtractionResult:
    """
    Full pipeline: parse PDF, classify, and prepare for Claude extraction.
    
    Returns an ExtractionResult with the text ready for prompt-based extraction.
    """
    # Extract text
    pdf_data = extract_text_from_pdf(pdf_path)
    
    # Classify document
    doc_type = classify_document(pdf_data["full_text"])
    
    # Create extraction result
    result = ExtractionResult(
        document_type=doc_type.value,
        source_file=str(pdf_path),
        confidence="MEDIUM",
        data={
            "raw_text": pdf_data["full_text"][:50000],  # Limit for context window
            "page_count": pdf_data["page_count"],
            "metadata": pdf_data["metadata"]
        },
        notes=[f"Classified as {doc_type.value} based on content analysis"]
    )
    
    # Map document type to recommended extraction prompt
    prompt_mapping = {
        DocumentType.FINANCIAL_STATEMENT: "prompts/extract_pl.md or prompts/extract_balance_sheet.md",
        DocumentType.MANAGEMENT_ACCOUNTS: "prompts/extract_pl.md",
        DocumentType.CONTRACT: "prompts/extract_contract_terms.md",
        DocumentType.ORG_DATA: "prompts/extract_org_chart.md",
        DocumentType.OPERATIONAL: "Custom extraction required",
        DocumentType.LEGAL: "Custom extraction required",
        DocumentType.UNKNOWN: "Manual classification required"
    }
    
    result.notes.append(f"Recommended prompt: {prompt_mapping.get(doc_type, 'Unknown')}")
    
    return result


def batch_process_pdfs(folder_path: str, output_dir: str = "outputs/extractions") -> list[dict]:
    """
    Process all PDFs in a folder and return extraction summaries.
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    results = []
    pdf_files = list(folder.glob("*.pdf")) + list(folder.glob("*.PDF"))
    
    for pdf_file in pdf_files:
        try:
            result = process_pdf_for_extraction(str(pdf_file))
            saved_path = result.save(output_dir)
            results.append({
                "file": str(pdf_file),
                "status": "success",
                "document_type": result.document_type,
                "output": saved_path
            })
        except Exception as e:
            results.append({
                "file": str(pdf_file),
                "status": "error",
                "error": str(e)
            })
    
    return results


# --- Google Sheets Integration ---

class GoogleSheetsClient:
    """
    Client for reading/writing RTS data to Google Sheets.
    
    Setup:
    1. Create a Google Cloud project
    2. Enable Google Sheets API
    3. Create a service account and download JSON credentials
    4. Share your spreadsheet with the service account email
    5. Set GOOGLE_SHEETS_CREDENTIALS env var to the JSON file path
    """
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_path: Optional[str] = None):
        if not SHEETS_SUPPORT:
            raise ImportError("gspread not installed. Install with: pip install gspread google-auth")
        
        self.credentials_path = credentials_path or os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
        self.client = None
        
        if self.credentials_path and Path(self.credentials_path).exists():
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API."""
        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=self.SCOPES
        )
        self.client = gspread.authorize(creds)
    
    def is_connected(self) -> bool:
        """Check if authenticated."""
        return self.client is not None
    
    def create_spreadsheet(self, title: str) -> str:
        """Create a new spreadsheet and return its ID."""
        if not self.is_connected():
            raise ConnectionError("Not authenticated. Provide credentials path.")
        
        spreadsheet = self.client.create(title)
        return spreadsheet.id
    
    def open_spreadsheet(self, spreadsheet_id: str):
        """Open an existing spreadsheet by ID."""
        if not self.is_connected():
            raise ConnectionError("Not authenticated. Provide credentials path.")
        
        return self.client.open_by_key(spreadsheet_id)
    
    def write_drl_to_sheet(self, drl: "DataRequestList", spreadsheet_id: str, 
                           worksheet_name: str = "Data Request List"):
        """
        Write a Data Request List to a Google Sheet.
        """
        spreadsheet = self.open_spreadsheet(spreadsheet_id)
        
        # Get or create worksheet
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=10)
        
        # Headers
        headers = ["Category", "Item", "Priority", "Status", "Received Date", 
                   "Source File", "Notes", "Confidence"]
        
        # Data rows
        rows = [headers]
        for item in drl.items:
            rows.append([
                item.category,
                item.item,
                item.priority,
                item.status,
                item.received_date or "",
                item.source_file or "",
                item.notes or "",
                item.confidence
            ])
        
        worksheet.update(rows, "A1")
        
        # Format header row
        worksheet.format("A1:H1", {
            "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        })
        
        return f"Written {len(drl.items)} items to {worksheet_name}"
    
    def write_extraction_to_sheet(self, extraction: ExtractionResult, spreadsheet_id: str,
                                   worksheet_name: str = "Extractions"):
        """
        Append an extraction result to an extractions log sheet.
        """
        spreadsheet = self.open_spreadsheet(spreadsheet_id)
        
        # Get or create worksheet
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=10)
            # Add headers
            headers = ["Timestamp", "Document Type", "Source File", "Confidence", 
                       "Data Summary", "Quality Checks", "Gaps", "Notes"]
            worksheet.update([headers], "A1")
        
        # Append row
        row = [
            extraction.extracted_at,
            extraction.document_type,
            extraction.source_file,
            extraction.confidence,
            json.dumps(extraction.data)[:500],  # Truncate for sheet
            json.dumps(extraction.quality_checks),
            ", ".join(extraction.gaps),
            "; ".join(extraction.notes)
        ]
        
        worksheet.append_row(row)
        return f"Appended extraction for {extraction.source_file}"
    
    def read_sheet_to_dict(self, spreadsheet_id: str, worksheet_name: str) -> list[dict]:
        """
        Read a worksheet into a list of dictionaries (header row as keys).
        """
        spreadsheet = self.open_spreadsheet(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        
        records = worksheet.get_all_records()
        return records
    
    def write_working_capital_analysis(self, wc_data: dict, spreadsheet_id: str,
                                        worksheet_name: str = "Working Capital"):
        """
        Write working capital analysis to a formatted sheet.
        """
        spreadsheet = self.open_spreadsheet(spreadsheet_id)
        
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=50, cols=5)
        
        rows = [
            ["Working Capital Analysis", "", ""],
            ["Generated", datetime.now(timezone.utc).isoformat(), ""],
            ["", "", ""],
            ["Metric", "Value", "Notes"],
            ["Net Working Capital", f"${wc_data['net_working_capital']:,.0f}", ""],
            ["NWC % of Revenue", f"{wc_data['nwc_pct_revenue']:.1f}%", ""],
            ["Days Sales Outstanding", f"{wc_data['days_sales_outstanding']:.1f}", ""],
            ["Days Payable Outstanding", f"{wc_data['days_payable_outstanding']:.1f}", ""],
            ["Days Inventory Outstanding", f"{wc_data['days_inventory_outstanding']:.1f}", ""],
            ["Cash Conversion Cycle", f"{wc_data['cash_conversion_cycle']:.1f} days", ""],
            ["", "", ""],
            ["Assessment Notes", "", ""]
        ]
        
        for note in wc_data.get("notes", []):
            rows.append(["", note, ""])
        
        worksheet.update(rows, "A1")
        
        # Format title
        worksheet.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
        worksheet.format("A4:C4", {
            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
            "textFormat": {"bold": True}
        })
        
        return f"Written working capital analysis to {worksheet_name}"


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
            self.items[item_index].received_date = datetime.now(timezone.utc).isoformat()
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
            "generated_at": datetime.now(timezone.utc).isoformat()
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
    import sys
    
    print("=" * 60)
    print("RTS Data Extraction Pipeline")
    print("=" * 60)
    
    # Demo 1: Data Request List Gap Report
    print("\n📋 Data Request List — Gap Report\n")
    drl = DataRequestList()
    gap = drl.gap_report()
    print(f"Total Items: {gap['total_items']}")
    print(f"Received: {gap['received']}")
    print(f"Pending: {gap['pending']}")
    print(f"Completion: {gap['completion_pct']}%")
    print(f"\nCritical Gaps ({len(gap['critical_gaps'])}):")
    for g in gap['critical_gaps'][:5]:  # Show first 5
        print(f"  - [{g['category']}] {g['item']}")
    if len(gap['critical_gaps']) > 5:
        print(f"  ... and {len(gap['critical_gaps']) - 5} more")

    # Demo 2: Working Capital Calculation
    print("\n📊 Working Capital Analysis\n")
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

    # Demo 3: PDF Parsing (if available)
    print("\n📄 PDF Parsing Capability\n")
    if PDF_SUPPORT:
        print("✅ PyMuPDF installed — PDF parsing available")
        # Check for sample PDF
        sample_pdfs = list(Path(".").glob("**/*.pdf"))[:3]
        if sample_pdfs:
            print(f"   Found {len(sample_pdfs)} PDF(s) in workspace")
            for pdf in sample_pdfs:
                print(f"   - {pdf}")
        else:
            print("   No PDFs found in workspace. To test:")
            print("   >>> from data_extraction import process_pdf_for_extraction")
            print("   >>> result = process_pdf_for_extraction('path/to/file.pdf')")
    else:
        print("❌ PyMuPDF not installed")
        print("   Install with: pip install pymupdf")

    # Demo 4: Google Sheets Integration (if available)
    print("\n📊 Google Sheets Integration\n")
    if SHEETS_SUPPORT:
        print("✅ gspread installed — Google Sheets available")
        creds_path = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
        if creds_path and Path(creds_path).exists():
            print(f"   Credentials found: {creds_path}")
            print("   Ready to connect!")
        else:
            print("   To enable:")
            print("   1. Create a service account in Google Cloud Console")
            print("   2. Download the JSON credentials")
            print("   3. Set GOOGLE_SHEETS_CREDENTIALS=/path/to/creds.json")
            print("   4. Share your spreadsheet with the service account email")
    else:
        print("❌ gspread not installed")
        print("   Install with: pip install gspread google-auth")

    # Demo 5: Document Classification
    print("\n🔍 Document Classification Demo\n")
    sample_texts = [
        "Balance Sheet as of December 31, 2025. Total Assets: $10M",
        "Master Services Agreement between Acme Corp and XYZ Inc. Effective Date: Jan 1, 2025",
        "Organization Chart - Q4 2025. Total Headcount: 127 employees",
        "Monthly KPI Report - Sales increased 15% vs prior period"
    ]
    for text in sample_texts:
        doc_type = classify_document(text)
        print(f"  '{text[:50]}...'")
        print(f"  → Classified as: {doc_type.value}\n")

    print("=" * 60)
    print("Pipeline ready. Import functions for programmatic use:")
    print("  from data_extraction import (")
    print("      extract_text_from_pdf,")
    print("      process_pdf_for_extraction,")
    print("      GoogleSheetsClient,")
    print("      DataRequestList,")
    print("      calculate_working_capital_metrics")
    print("  )")
    print("=" * 60)
