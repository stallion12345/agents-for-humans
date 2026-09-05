# O.C. Manjos Restock & Qualification Agent

Built for the AWS "Agents for Humans" Hackathon (Strands Agents SDK) — **Professional Agents** track.

## The Problem

O.C. Manjos is a 300+ product electrical merchant at Dei Dei International Market, Abuja. Like most small merchants, it has no digital stock-tracking system — inventory knowledge lives with the owner, not in a database. Meanwhile, customer enquiries come in constantly via WhatsApp, and busy stock lines can run out unnoticed between manual checks, costing sales.

This project builds a small multi-agent system that:
1. Qualifies incoming customer enquiries against real pricing and value thresholds
2. Recommends restocking based on enquiry demand — since stock-level data doesn't exist yet, the signal used is enquiry *volume*, not inventory count

## Who It's For

Small electrical/hardware merchants who track customer interest informally (WhatsApp, phone calls) and don't have digital inventory systems — a common reality for small businesses in this market, not an edge case.

## Why It Matters

Manually noticing "we're getting a lot of enquiries about X" and connecting that to a restock decision is exactly the kind of repetitive, judgment-adjacent task a small business owner doesn't have time to do consistently. This agent does it automatically and only escalates orders that need a human decision — everything else it handles or reports quietly.

## Architecture

Three agents, each doing one clear job:

**Agent 1 + 2 — Intake & Qualification** (`qualify_full_enquiry` tool)
- Extracts the product, size, and phase from raw enquiry text
- Looks up price against the current worksheet
- Maps the product to its qualification tier and threshold
- Returns whether the enquiry is high-value enough to qualify for follow-up

**Agent 3 — Restock Recommendation**
- Pulls the last 7 days of enquiries from Supabase
- Counts enquiries per product category
- **Two-tier check:** looks for real stock-level data first; since none exists yet, falls back to enquiry-volume analysis
- If enquiry volume for a category crosses the weekly threshold, recommends a restock

**Restock approval logic**
- Recommended orders under ₦100,000 are treated as auto-approvable
- Orders at or above ₦100,000 are flagged for the owner's approval — no purchase is ever placed autonomously

See `architecture.png` (or `.md` diagram) for the full data flow.

## Current Scope

This is a working, honestly-scoped v1, not a finished commercial product:

- **Pricing and qualification currently support A&B brand Distribution Boards specifically.** The price sheet includes multiple other brands (ABB, HAVEL, A&Itech, A&Btech); the agent correctly identifies when a different brand is asked about and reports that pricing isn't available yet, rather than guessing.
- **No stock-level data source exists yet.** Restock recommendations are based on enquiry volume, a proxy for demand, not actual inventory shortage. The code is structured so that real stock data can be plugged in later without changing the agent's logic.
- **Several other product categories** (cable, ELCB, sockets, switches, bulbs) are recognized by the intake agent but don't yet have qualification tier thresholds defined — a deliberate, flagged gap rather than a guessed number.

## Tech Stack

- **Strands Agents SDK** (Python) — agent orchestration and tool-calling
- **Groq** (via LiteLLM) — LLM inference
- **Supabase** — enquiry data storage
- **pandas / openpyxl** — price worksheet parsing

## Setup

```bash
pip install strands-agents[litellm] groq supabase pandas openpyxl python-dotenv
```

Create a `.env` file with:
```
GROQ_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

Run the full pipeline:
```bash
python main.py
```

## What's Next (Post-Hackathon)

This build intentionally stayed scoped to one business for the hackathon submission. Planned next steps:
- Generalize the architecture so any small merchant can configure their own product categories, brands, and thresholds
- Add real stock-level tracking as a first-class data source
- Multi-agent handoff refinement using Strands' built-in orchestration patterns

## License

MIT
