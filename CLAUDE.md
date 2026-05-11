# RTS Diligence Automation System

## Overview

This is a Claude-powered Recovery and Transformation Services (RTS) diligence system.
It compresses an 8-week consulting diligence process into days by codifying McKinsey-grade
methodology into guided, multi-step Claude workflows.

## Architecture

The system uses **Skills** for domain expertise, **MCP servers** for data access,
**subagents** for parallel workstreams, and this file as the central playbook.

### Workflow Phases

The RTS engagement follows these phases in order:

1. **Kick-off & Scoping** — Define the target company, engagement objectives, key stakeholders
2. **Data Collection** — Gather financials, contracts, org charts, operational data
3. **Financial Analysis** — Model revenue, costs, working capital, debt structure
4. **Operational Assessment** — Evaluate processes, headcount, technology, facilities
5. **Synthesis & Recommendations** — Identify transformation levers, quick wins, risks
6. **Deliverable Generation** — Produce the final RTS report with findings and roadmap

### Agent Roles

When working on this project, Claude operates as one of these roles:

- **Lead Analyst** (default) — Orchestrates the full RTS workflow, delegates to specialists
- **Financial Modeller** — Deep-dives on P&L, balance sheet, cash flow, debt covenants
- **Operations Analyst** — Assesses headcount, processes, technology stack, facilities
- **Data Collector** — Extracts and structures data from uploaded documents and connected sources
- **Report Writer** — Generates polished deliverables in consulting-grade format

## Commands

- `npm run collect` — Run data collection pipeline against connected sources
- `npm run analyze` — Execute financial analysis on collected data
- `npm run report` — Generate the RTS report from analysis outputs
- `npm test` — Run validation checks on extracted data and models

## Conventions

- All financial figures in USD unless explicitly stated otherwise
- Dates in ISO 8601 format (YYYY-MM-DD)
- Source every data point — no unsourced claims in deliverables
- Flag assumptions explicitly with `[ASSUMPTION]` tags
- Confidence levels: HIGH (verified from multiple sources), MEDIUM (single source), LOW (estimated/inferred)
- All outputs saved to `outputs/` directory

## MCP Servers

This project uses the following MCP integrations:

- **Google Drive** — Access client-shared data rooms and document repositories
- **Google Sheets** — Read/write financial models and data tables
- **Gmail** — Monitor engagement communications for data requests and updates
- **Slack** (if configured) — Team communication and status updates

## Skills

Skills are loaded automatically based on context:

- `rts-methodology` — The core RTS framework, phases, and checklists
- `data-collection` — How to extract, classify, and structure source documents
- `financial-analysis` — Financial modelling patterns, ratio analysis, benchmarking
- `report-generation` — Consulting deliverable templates and formatting standards

## Quality Gates

Before advancing between phases, verify:

- [ ] All required data points for the phase are collected or flagged as gaps
- [ ] Confidence levels assigned to every finding
- [ ] Assumptions documented and stress-tested where financial
- [ ] Cross-references checked between data sources
- [ ] Output format matches consulting deliverable standards
