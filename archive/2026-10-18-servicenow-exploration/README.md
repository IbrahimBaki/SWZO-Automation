# Archive: 2026-10-18 ServiceNow Exploration

**Status: archived, exploratory only. Not the EduPulse project baseline. Not a reference artifact. Not an approved feature.**

This directory preserves read-only discovery notes and one directly-UI-built demo, all performed on `dev446072.service-now.com` before the EduPulse XML-first workflow (see [`../../CLAUDE.md`](../../CLAUDE.md)) existed. It is kept for historical record only.

## What's here

| File | What it is |
|---|---|
| `ai-request-hub-discovery.md` | Read-only discovery of the Service Portal/Catalog |
| `change-management-discovery.md` | Read-only discovery of Change Management |
| `ai-request-hub-catalog-v1.md` | A demo Catalog Item ("AI Request Hub") built directly through the UI — **not** via the Update-Set-XML pipeline |
| `ai-request-hub-dynamic-url-field.md` | A follow-up UI-built variable + Catalog UI Policy on the same demo item |
| `demo-change-request-creation.md` | A demo Change Request (CHG0030001) created directly |
| `chg0030001-change-task-discovery.md`, `chg0030001-change-tasks-creation.md` | Discovery and creation of Change Tasks under CHG0030001 |
| `screenshots/` | Screenshots referenced by the files above |
| `project-preparation-report-2026-10-18-SUPERSEDED.md` | An earlier project-preparation report that **incorrectly treated this exploratory work as a reference baseline** for EduPulse. It is archived, not deleted, and its recommendations are withdrawn — see the banner at the top of that file and the current [`../../docs/project-cleanup-report.md`](../../docs/project-cleanup-report.md). |

## What this does NOT mean

- Nothing here was adopted into EduPulse scope.
- The demo Update Set referenced in these files (`[AI DEMO] AI Request Hub - Catalog v1`, still **In Progress** and current for Administrator on the PDI as of 2026-10-18) remains untouched and out of scope — it was **not** exported, previewed, or committed, and still isn't.
- No pattern, sys_id, or structure from this archive should be reused in a real EduPulse change package unless a future approved task explicitly adopts it.

Screenshot paths are relative within this directory (e.g. `./screenshots/x.png`) and were preserved unchanged from the original `serviceNow/` location.
