# PDI Baseline

**No ServiceNow PDI has been confirmed as EduPulse's target.** This file records, factually, what prior exploration observed on `dev446072.service-now.com` — kept in case a future task adopts this (or another) instance. It is a factual record, not a recommendation, not a baseline, and not a reference to design against. See [`../../CLAUDE.md`](../../CLAUDE.md) §1 and §6, and [`../../archive/2026-10-18-servicenow-exploration/`](../../archive/2026-10-18-servicenow-exploration/) for the full original reports this is drawn from.

| | |
|---|---|
| **Instance observed** | `dev446072.service-now.com` (Personal Developer Instance) — exploratory use only, not confirmed as EduPulse's target |
| **Default portal observed** | Service Portal (`/sp`), OOB theme. Employee Center was offered but not activated. |
| **Default catalog observed** | Service Catalog, `sys_id e0d08b13c3330100c8b837659bba8fb4` |
| **Release version** | Not captured. |
| **Scope / vendor prefix** | Not applicable — no EduPulse scope decision has been made. |

## Known existing data/config on that instance (as of 2026-10-18, from archived exploration)

| Item | sys_id | State | Notes |
|---|---|---|---|
| Update Set `[AI DEMO] AI Request Hub - Catalog v1` | `6654e7f493041b1075d9f9fbdd03d637` | **In Progress, current for Administrator** | Built directly through the UI, exploratory, unrelated to EduPulse. **Not exported, previewed, or committed** — must stay that way absent explicit user authorization. If a future task targets this instance, this must be resolved deliberately with the user first (see CLAUDE.md §6) — not silently added to, completed, or switched. |
| Change Request CHG0030001 `[AI DEMO] Release Payment API v2.4` | `8900b0fc9300d71075d9f9fbdd03d699` | New | Demo data, not configuration, unrelated to EduPulse. Has 2 Change Tasks. |
| Change Management application | — | Active | 105 pre-existing Change Request records (PDI seed/demo data). |
| Service Catalog | — | Active | 197 catalog items, 45 categories (pre-existing PDI seed data + the 1 AI Demo item above). |

Full detail and screenshots: [`../../archive/2026-10-18-servicenow-exploration/`](../../archive/2026-10-18-servicenow-exploration/).

## What this does NOT establish

- That EduPulse will use this PDI, ServiceNow at all, or any particular mechanism (Catalog Items, custom tables, etc.) observed here.
- That Update Set export/preview/commit works a particular way on this instance — that part of the pipeline has never been exercised by this project.
- Whether Update Set **Back Out** is reliable here — never tested.

Update this file only with newly confirmed facts (from an authorized, logged task), never with proposed design.
