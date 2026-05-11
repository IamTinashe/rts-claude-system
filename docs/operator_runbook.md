# RTS Automation — Operator Runbook

## Who This Is For

You are a junior analyst running the RTS diligence system day-to-day. You don't need
to understand how the AI works — just how to use it. This guide walks you through
every step of a typical engagement.

## Prerequisites

Before starting, make sure you have:
- Claude Code installed and authenticated (Claude Max or Enterprise account)
- Access to the client's Google Drive data room (shared with your Google account)
- The engagement scoping document from the engagement lead

## Starting a New Engagement

### Step 1: Initialize the Project

Open your terminal in the `rts-claude-system` directory and start Claude Code:

```bash
cd rts-claude-system
claude
```

Claude will automatically load the CLAUDE.md playbook and all skills.

### Step 2: Run the Kick-off

Tell Claude what engagement you're starting:

```
Start a new RTS engagement for [Company Name].
Here's the scoping document: [paste or upload the engagement letter]
The distress trigger is [liquidity/operational/strategic/covenant].
Key stakeholders: [list names and roles]
```

Claude will:
- Generate a scoping memo
- Create a customized Data Request List
- Produce a stakeholder map
- Set up the project timeline

Review these outputs in the `outputs/` directory before sending to the client.

### Step 3: Send the Data Request

Claude will draft a data request email. Review it, then:

```
Draft the data request email for [client contact name] covering all Priority 1 items
```

Copy the email and send it via your normal email client, or ask Claude to draft it
through the Gmail MCP integration.

## Running Data Collection

### When Documents Arrive

Upload or point Claude to new documents:

```
New documents arrived. Process the files in Google Drive folder "[folder name]"
```

Or upload directly:

```
Process this document: [upload file]
```

Claude will:
1. Classify the document type
2. Extract structured data
3. Run quality checks
4. Update the Data Request List status
5. Flag any gaps or anomalies

### Checking Collection Progress

```
Show me the current DRL gap report
```

This shows what's been received, what's missing, and what's critical.

### Following Up on Gaps

```
Draft follow-up requests for all critical gaps that are still pending after 3 days
```

## Running Financial Analysis

### Phase 3 Trigger

Once Priority 1 financial data is mostly collected (>80% received):

```
Run the financial analysis phase.
Start with Adjusted EBITDA, then Working Capital, then Debt & Liquidity.
```

Claude will work through each analysis systematically, using the financial-analysis
skill. It will:
- Build the EBITDA bridge
- Calculate working capital metrics
- Map the debt structure
- Build scenario models

### Review Checkpoints

After each analysis, Claude presents findings for your review. Check:
- Do the numbers trace back to source documents?
- Are assumptions reasonable?
- Do cross-references match?

If something looks wrong:
```
The EBITDA adjustment for restructuring charges looks too high.
The source document shows $2.1M, not $3.4M. Correct this.
```

## Generating the Report

### When Analysis Is Complete

```
Generate the RTS report for [Company Name].
Use the standard report template.
Include all findings from the analysis phase.
```

Claude uses the report-generation skill to produce a consulting-grade deliverable.

### Review the Report

The draft appears in `outputs/reports/`. Review it against the quality checklist:

```
Run the pre-delivery quality checklist on the draft report
```

Claude will flag any issues (unsourced claims, missing confidence levels, etc).

### Finalize

```
Finalize the report. Address the quality checklist items and generate the final PDF.
```

## Troubleshooting

### "Claude doesn't know about the RTS methodology"
Make sure you're in the `rts-claude-system` directory. The skills load from `.claude/skills/`.

### "MCP connection to Google Drive failed"
Run `claude mcp list` to check connections. Re-authenticate if needed.

### "The financial model has errors"
Ask Claude to show its work: `Show me the calculation for [specific number] with source references`

### "I need to override an AI decision"
Always possible. Just tell Claude: `Override the classification for [document] — it's actually a [correct type]`

## Daily Workflow Summary

| Time | Activity |
|------|----------|
| Morning | Check for new documents, run data collection |
| Mid-day | Review extraction results, follow up on gaps |
| Afternoon | Run or review analysis for active phases |
| End of day | Update engagement status, flag blockers |

## Getting Help

- Technical issues with Claude Code: Check `claude doctor`
- Methodology questions: Ask Claude — the rts-methodology skill has the answer
- System issues: Contact the technical team (see Maintenance Guide)
