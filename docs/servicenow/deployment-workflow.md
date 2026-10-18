# Deployment Workflow

This applies **only once a task under `tasks/` has been approved** and specifies ServiceNow as (part of) its platform — see [../../tasks/README.md](../../tasks/README.md) and [../../CLAUDE.md](../../CLAUDE.md) §2. CLAUDE.md is authoritative if this file ever drifts.

```
Approved task (tasks/)
  → plan.md (implementation plan, developer-readable)
  → update-set.xml (ServiceNow Update Set XML artifact)
  → Git review/versioning
  → Playwright: upload XML to the authorized PDI
  → Playwright: Preview Update Set
  → explicit human approval  ← hard stop, every time
  → Playwright: Commit Update Set
  → Playwright: verify the portal UI
```

## Step-by-step detail

### 0. Approved task
No plan, no XML, no instance interaction starts without an approved task file under `tasks/` naming this work and its platform. See `tasks/README.md` for what "approved" means.

### 1. Approved task → plan.md
Write `plan.md` from the task (template: see `changes/_template/plan.md`). The plan must state: what's changing, affected portal/form behavior, implementation approach, rollback approach, validation steps, risks, and current approval status. No XML is generated yet — state `pending`.

### 2. plan.md → update-set.xml
Only after the plan is written, and only against a real baseline:
- If the change extends/depends on existing configuration, obtain a fresh export or authoritative metadata for that configuration first (never guess field names, sys_ids, or table structure).
- Generate the Update Set XML so it reflects exactly what `plan.md` describes — no extra, unrelated changes bundled in.
- Mark the package `xml-generated` in `manifest.yaml`.

### 3. Git review/versioning
Commit `plan.md`, `manifest.yaml`, and `update-set.xml` together so a human can review the actual payload before it ever touches the PDI. This is the review gate that exists *before* any instance interaction — treat it as seriously as the in-product preview/approval gate.

### 4. Playwright: upload XML
Navigate to **Retrieved Update Sets** (`sys_remote_update_set_list.do` or the equivalent nav path) → **Import Update Set from XML** → upload `update-set.xml`. Record the resulting Retrieved Update Set's sys_id in `verification.md`. Mark `imported`.

### 5. Playwright: Preview
Open the imported/retrieved set → **Preview Update Set**. Capture the full result (clean, or list of conflicts) — screenshot to `evidence/`, summary in `verification.md`. Mark `previewed`.

### 6. Human approval — hard stop
If preview is clean: present it to the user and wait for explicit go-ahead naming this exact change package. If there are conflicts: do **not** proceed; surface them and let the user decide (resolve, abandon, or accept with an explicit override). Mark `awaiting-human-approval` only once preview is clean or conflicts are explicitly accepted by the user. **Never commit an Update Set with unresolved conflicts** (see CLAUDE.md §7.3).

### 7. Playwright: Commit
Only after the approval above, for this exact package. Click **Commit Update Set**. Record the committed set's final sys_id/state in `verification.md`. Mark `committed`.

### 8. Playwright: verify the portal UI
Navigate the live portal as an end user would, confirm the expected behavior (new field visible, form renders, conditional logic fires, etc.), capture screenshots to `evidence/` (scrub any real PII first). Mark `verified`.

## If something goes wrong

- Preview conflicts → stop, do not commit, document in `verification.md`, decide with the user.
- Post-commit verification fails → do not silently retry with more UI changes; write up the failure, propose either a fix-forward change package or a rollback, and get the user's direction. Mark `rolled-back` only once an actual back-out has been performed and confirmed.

## Playwright usage boundary

Playwright only touches the PDI for: import, preview, approved commit, evidence screenshots, and end-user verification navigation. It must never be used to directly author configuration (creating catalog items/variables/policies/etc. by clicking through forms) as a substitute for the XML pipeline above — that bypasses Git review entirely. The one exception is an explicitly authorized bootstrap/emergency change, which must still be logged in `verification.md` with the authorization noted.
