# RTS Diligence Automation System

> A Claude-powered system that codifies McKinsey-grade Recovery and Transformation
> Services (RTS) methodology into guided, multi-step AI workflows — compressing
> an 8-week diligence process into days.

## What This Is

This is a **production-ready Claude Code project** demonstrating:

- **CLAUDE.md Playbook** — Central orchestration file that defines agent roles, workflow phases, quality gates, and conventions
- **4 Custom Skills** — Domain-specific instruction packs for RTS methodology, data collection, financial analysis, and report generation
- **MCP Integration** — Google Drive, Gmail, Sheets, and Calendar connections for real-time data access
- **Multi-Agent Patterns** — Subagent delegation and Agent Teams for parallel workstreams
- **Python Tooling** — Data extraction pipeline with document classification, financial validation, and gap analysis
- **Operator Documentation** — Runbook for junior analysts and maintenance guide for technical teams

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE.md PLAYBOOK                     │
│         (Roles, Phases, Quality Gates, Conventions)      │
└──────────────┬──────────────────────┬────────────────────┘
               │                      │
    ┌──────────▼──────────┐  ┌───────▼─────────┐
    │      4 SKILLS        │  │   MCP SERVERS    │
    │                      │  │                  │
    │  rts-methodology     │  │  Google Drive    │
    │  data-collection     │  │  Gmail           │
    │  financial-analysis  │  │  Google Sheets   │
    │  report-generation   │  │  Google Calendar │
    └──────────┬───────────┘  └───────┬──────────┘
               │                      │
    ┌──────────▼──────────────────────▼──────────┐
    │           CLAUDE CODE SESSION                │
    │                                              │
    │  Lead Analyst (orchestrator)                 │
    │    ├── Financial Modeller (subagent)         │
    │    ├── Operations Analyst (subagent)         │
    │    ├── Data Collector (subagent)             │
    │    └── Report Writer (subagent)              │
    └──────────────────┬───────────────────────────┘
                       │
    ┌──────────────────▼───────────────────────────┐
    │           PYTHON TOOLING                      │
    │                                               │
    │  data_extraction.py                           │
    │    ├── Document classification                │
    │    ├── Financial validation                   │
    │    ├── Working capital calculations            │
    │    └── Data Request List tracking             │
    └───────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Claude Code installed (Claude Max or Enterprise account)
- Node.js 18+ (for npm install method) or native installer
- Python 3.10+ (for data extraction scripts)
- Google Workspace account (for MCP integrations)

### Setup
```bash
# Clone this repository
git clone https://github.com/IamTinashe/rts-claude-system.git
cd rts-claude-system

# Start Claude Code — it automatically loads CLAUDE.md and skills
claude

# Verify skills are loaded
> What skills are available for this project?

# Verify MCP connections
> claude mcp list
```

### Run a Demo Engagement
```bash
# In Claude Code session:
> Start a new RTS engagement for Acme Corp.
> The distress trigger is liquidity — they have 8 weeks of cash runway.
> Key stakeholders: CFO (Jane Smith), CEO (John Doe), Lead Creditor (Bank ABC)
```

## Project Structure

```
rts-claude-system/
├── CLAUDE.md                          # Master playbook
├── .mcp.json                          # MCP server configuration
├── requirements.txt                   # Python dependencies
├── .claude/
│   ├── skills/
│   │   ├── rts-methodology/SKILL.md   # Core RTS framework
│   │   ├── data-collection/SKILL.md   # Document extraction patterns
│   │   ├── financial-analysis/SKILL.md # Financial modelling
│   │   └── report-generation/SKILL.md # Deliverable templates
│   └── agents/
│       ├── lead-analyst.agent.md      # Orchestrator agent
│       ├── financial-modeller.agent.md # Financial specialist
│       ├── operations-analyst.agent.md # Operations specialist
│       ├── data-collector.agent.md    # Data extraction specialist
│       └── report-writer.agent.md     # Deliverables specialist
├── prompts/
│   ├── extract_pl.md                  # P&L extraction template
│   ├── extract_balance_sheet.md       # Balance sheet extraction
│   ├── extract_contract_terms.md      # Contract terms extraction
│   ├── extract_debt_schedule.md       # Debt analysis extraction
│   └── extract_org_chart.md           # Org/headcount extraction
├── scripts/
│   └── data_extraction.py             # Python data pipeline
│       # Includes: PDF parsing, Google Sheets API, document
│       # classification, working capital calcs, DRL tracking
├── docs/
│   ├── operator_runbook.md            # For junior analysts
│   └── maintenance_guide.md           # For technical team
└── README.md                          # This file
```

## Python Pipeline Setup

```bash
# Install dependencies (optional - core features work without them)
pip install -r requirements.txt

# Or install specific features:
pip install pymupdf          # PDF parsing
pip install gspread google-auth  # Google Sheets integration

# Run the demo
python scripts/data_extraction.py

# Use programmatically
python -c "
from scripts.data_extraction import (
    process_pdf_for_extraction,
    GoogleSheetsClient,
    calculate_working_capital_metrics
)
"
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Skills over monolithic CLAUDE.md | Modular, context-efficient, only loaded when needed |
| MCP for data access | Real-time access to client data rooms without manual uploads |
| Subagents for parallel work | Financial and operational analysis can run simultaneously |
| Python glue code | Structured validation and calculation that benefits from typing |
| Human-in-the-loop | No financial finding published without analyst review |

## Deliverables Mapping

This system produces all deliverables expected from an RTS engagement:

| Deliverable | Generated By | Quality Gate |
|------------|--------------|-------------|
| Scoping Memo | rts-methodology skill | Engagement lead review |
| Data Request List | data-collection skill | Standard DRL + customization |
| Adjusted EBITDA Bridge | financial-analysis skill | Source verification |
| Working Capital Analysis | financial-analysis skill + Python calcs | Cross-reference check |
| Operational Assessment | rts-methodology (7 Levers) | Benchmark validation |
| Transformation Roadmap | rts-methodology + financial-analysis | Impact sizing review |
| Final RTS Report | report-generation skill | Pre-delivery quality checklist |

## Built By

**Tinashe Zvihwati** — Senior Software Engineer specializing in AI system design,
enterprise integration, and digital transformation.

- Designed and built AI-powered AR automation system using Amazon Bedrock (Claude Sonnet,
  Nova Pro) with multi-model routing, RAG pipeline, and human-in-the-loop approval workflows
- 8+ years production software development across fintech, BPO, and enterprise platforms
- Anthropic certified: Claude 101, Claude Code in Action, Introduction to Responsible AI
- Award-winning engineer: 2022 Old Mutual ICT Stars of Africa

[GitHub](https://github.com/IamTinashe) | [LinkedIn](https://linkedin.com/in/tinashepride)
