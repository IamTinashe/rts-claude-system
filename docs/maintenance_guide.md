# RTS Automation — Maintenance & Extension Guide

## For the Client's Technical Team

This guide explains how to maintain, customize, and extend the RTS automation
system after handover. It covers the system architecture, how to add new skills,
configure MCP integrations, and troubleshoot common issues.

## System Architecture Overview

```
rts-claude-system/
├── CLAUDE.md                    # Central playbook (Claude reads this first)
├── .mcp.json                    # MCP server connections
├── .claude/
│   └── skills/
│       ├── rts-methodology/     # Core RTS framework
│       │   └── SKILL.md
│       ├── data-collection/     # Document extraction patterns
│       │   └── SKILL.md
│       ├── financial-analysis/  # Financial modelling frameworks
│       │   └── SKILL.md
│       └── report-generation/   # Deliverable templates and standards
│           └── SKILL.md
├── scripts/
│   └── data_extraction.py       # Python glue code for data pipeline
├── prompts/                     # Reusable prompt templates (optional)
├── outputs/                     # All generated outputs land here
│   ├── extractions/
│   ├── analysis/
│   └── reports/
└── docs/
    ├── operator_runbook.md
    └── maintenance_guide.md     # This file
```

## How Skills Work

Skills are the core of the system. Each skill is a folder containing a `SKILL.md`
file with two parts:

1. **YAML Frontmatter** — `name` and `description` that tell Claude when to load it
2. **Markdown Body** — Instructions, frameworks, templates that Claude follows

Claude Code scans skill descriptions at the start of every session. When your prompt
matches a skill's description, Claude loads that skill's full content into context.

### Adding a New Skill

Example: Adding an industry-specific benchmarking skill.

1. Create the directory:
```bash
mkdir -p .claude/skills/industry-benchmarks
```

2. Create `SKILL.md`:
```markdown
---
name: industry-benchmarks
description: Use this skill when benchmarking financial or operational
metrics against industry comparables. Covers manufacturing, retail,
healthcare, and technology sectors. Trigger when comparing client
metrics to peers or industry averages.
---

# Industry Benchmarking

## Manufacturing Benchmarks
- Gross margin: 25-35% (mid-market)
- EBITDA margin: 10-18%
- DSO: 40-55 days
...
```

3. Test it by starting Claude Code and asking a benchmarking question.

### Modifying an Existing Skill

Edit the `SKILL.md` file directly. Changes take effect on the next Claude Code session.

Key principles:
- Keep descriptions specific — vague descriptions cause false triggers
- Keep skill content focused — one skill, one domain
- Use structured formats (tables, checklists) that Claude can follow precisely
- Include examples of good output

### Skill Triggering Tips

If a skill isn't activating when expected:
- Check the `description` field — does it contain the keywords from your prompt?
- Make descriptions action-oriented ("Use when extracting financial data")
- Avoid overlap between skill descriptions
- Test with: "What skills are loaded for this task?"

## MCP Server Configuration

MCP servers in `.mcp.json` give Claude access to external tools. The current setup
connects Google Workspace (Drive, Sheets, Gmail, Calendar).

### Adding a New MCP Server

1. Find the MCP server URL (check the MCP registry or provider docs)
2. Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "existing-server": { ... },
    "new-server-name": {
      "type": "url",
      "url": "https://example-mcp-server.com/sse",
      "description": "What this server provides"
    }
  }
}
```

3. Restart Claude Code
4. Run `claude mcp list` to verify the connection
5. Run `claude mcp test new-server-name` to verify it works

### Useful MCP Servers for RTS

| Server | Purpose | URL |
|--------|---------|-----|
| Google Drive | Client data rooms | `https://drivemcp.googleapis.com/mcp/v1` |
| Gmail | Email monitoring | `https://gmailmcp.googleapis.com/mcp/v1` |
| Slack | Team comms | Configure via Slack MCP app |
| Linear/Jira | Task tracking | Check MCP registry |
| Notion | Knowledge base | Check MCP registry |

## Modifying CLAUDE.md

`CLAUDE.md` is the master playbook. Claude reads it at the start of every session.

### What to Put in CLAUDE.md
- Project context and objectives
- Agent roles and their responsibilities
- Commands and conventions
- Quality gates between phases
- Links to skills and MCP servers

### What NOT to Put in CLAUDE.md
- Detailed methodology (that goes in skills)
- One-time instructions (just type those in the session)
- Very long content (keep CLAUDE.md under 500 lines; use skills for depth)

## Multi-Agent Patterns

### Subagents for Parallel Work

For tasks that can run in parallel (e.g., analyzing multiple business units):

```
Spawn a subagent to analyze the North America revenue segment.
Use the financial-analysis skill.
Meanwhile, I'll work on the EMEA segment.
```

### Agent Teams for Complex Engagements

For larger engagements, use Claude Code's Agent Teams feature:

```
Spawn a team of 3 analysts:
- "financial-analyst" to work on EBITDA and working capital
- "operations-analyst" to assess cost structure and headcount
- "data-collector" to process remaining documents from Drive

Each should use the relevant skill and report findings to me.
```

## Python Scripts

### data_extraction.py

The main glue script. Extend it by:

- Adding new `DocumentType` enum values for new document categories
- Adding classification patterns to `CLASSIFICATION_PATTERNS`
- Adding new validation functions for domain-specific checks
- Extending `DataRequestList._load_standard_drl()` with industry-specific items

### Running Scripts

```bash
python scripts/data_extraction.py           # Demo mode
python scripts/data_extraction.py --watch   # Watch mode (if implemented)
```

## Troubleshooting

### Claude Not Following the Methodology
- Verify CLAUDE.md is in the project root
- Check that skills are in `.claude/skills/` (not a different path)
- Start a fresh session — skills load at session start

### MCP Server Errors
```bash
claude mcp list       # See all registered servers
claude mcp test <name> # Test a specific server
claude doctor         # Full diagnostic
```

### Slow Performance
- Skills add to context — only keep skills you actively need
- Large files should be processed via scripts, not pasted into chat
- Use subagents for parallel work to stay within context limits

### Data Quality Issues
- Check source document quality (scanned PDFs may need OCR first)
- Verify extraction against the original manually for the first few documents
- Adjust confidence thresholds in the data-collection skill as needed

## Extending for New Engagement Types

The current system is built for RTS diligence. To extend for other engagement types:

1. Create a new skill (e.g., `.claude/skills/ma-diligence/SKILL.md`)
2. Define the phases, data requirements, and analysis frameworks
3. Update CLAUDE.md to reference the new engagement type
4. Add any new Python tooling to `scripts/`
5. Create a new operator runbook in `docs/`

The architecture is designed to be modular — new engagement types are just new skills
with a different playbook.
