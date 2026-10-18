# CLAUDE.md — EduPulse Project Rules

This file governs **all** ServiceNow (and any other platform) configuration work in this repository. It applies to Claude Code and to any human contributor. These rules are **mandatory**, not suggestions — if a request conflicts with them, stop and ask the user rather than improvising a workaround.

## 1. Project status

EduPulse's originally stated goal is a registration portal with Student, Parent, and Teacher flows plus a landing page. **The actual demo scope, target platform, and first deliverable are not yet defined** — they are pending the decisions in [`tasks/backlog/TASK-001-define-edupulse-demo-scope.md`](tasks/backlog/TASK-001-define-edupulse-demo-scope.md), including whether the platform is ServiceNow, Zoho Creator, or both.

Nothing in this repository should be read as a confirmed feature, architecture, or platform choice until that task is resolved and approved by the user.

If/when ServiceNow is adopted (in whole or part) for a task, the target instance must be explicitly named by the user for that task — do not assume `dev446072.service-now.com` or any other instance is in scope just because it was used for prior exploration (see §6).

## 2. Task-first rule — no exceptions

1. **No feature is designed or built without an approved task file** under `tasks/` (see [`tasks/README.md`](tasks/README.md) for what "approved" means and the task lifecycle).
2. **No Update Set XML package is generated without an approved task and a developer-readable `plan.md`** for that exact change package.
3. **No ServiceNow action of any kind occurs without explicit authorization** from the user for that exact action — this includes read-only discovery/navigation. A task specifying "discovery" as its intended action is sufficient authorization for discovery; it does not authorize anything beyond what it specifies.
4. **Playwright is used only after a task specifies the intended action and its verification** — never as an ad hoc way to "just check something" on a live instance outside a task's stated scope.
5. **Existing PDI artifacts are out of scope** (including anything described in [`archive/2026-10-18-servicenow-exploration/`](archive/2026-10-18-servicenow-exploration/)) **unless explicitly adopted by a future task.** Prior exploration is not a baseline and must not be treated as precedent to build on without that explicit adoption.

## 3. Mandatory operating model (once a task authorizes ServiceNow work)

```
Approved task (tasks/)
  → implementation plan (plan.md, developer-readable)
  → ServiceNow Update Set XML artifact (update-set.xml)
  → Git review / versioning (commit the plan + XML for human review)
  → Playwright uploads XML to the authorized PDI (Retrieved Update Sets → Import)
  → Preview Update Set (capture conflicts)
  → STOP — explicit human approval required before commit
  → Commit Update Set (only after approval)
  → Playwright verifies the portal UI (end-user check)
  → verification.md + evidence/ updated
```

Playwright is a **UI driver for the pipeline's edges only** — import, preview, approved commit, evidence capture, and end-user verification as specified by the authorizing task. It is **not** a development mechanism. Do not use Playwright (or manual UI clicks) to author configuration — catalog items, variables, UI policies, workflows, widgets, roles, ACLs, tables, business rules, etc. — outside this pipeline, unless the user explicitly authorizes a one-off UI change for **initial bootstrap or emergency recovery**, and that exception is recorded in the relevant change package's `verification.md`.

## 4. Project structure

```
tasks/                  every feature/change starts here — see tasks/README.md
docs/servicenow/        architecture, workflow, PDI baseline, glossary — living reference docs
changes/<CHANGE-ID>/    one atomic change package per approved, in-flight functional change (templates/docs only until a task authorizes a real one)
skills/servicenow-update-set/SKILL.md   reusable procedure/checklists for the ServiceNow pipeline
archive/                preserved historical/exploratory material — not a baseline, not reference, see §6
```

See [changes/README.md](changes/README.md) for the change-package contract and [skills/servicenow-update-set/SKILL.md](skills/servicenow-update-set/SKILL.md) for the detailed ServiceNow procedure — **read that skill file before starting any ServiceNow change**, and read [tasks/README.md](tasks/README.md) before starting any feature work at all.

## 5. Lifecycle states (change packages, once a task reaches that stage)

Every change package's `manifest.yaml` carries exactly one of these states, in order:

| State | Meaning |
|---|---|
| `draft` | Request captured, plan not yet written |
| `planned` | `plan.md` complete, not yet reviewed |
| `xml-generated` | `update-set.xml` produced from a real baseline/export |
| `peer-reviewed` | Plan + XML reviewed by a human (not just Claude) |
| `imported` | XML imported ("Retrieved Update Sets") on the target PDI, not yet previewed |
| `previewed` | Preview run; conflicts (if any) captured in `verification.md` |
| `awaiting-human-approval` | Preview is clean (or conflicts are explicitly accepted); waiting on explicit go-ahead to commit |
| `committed` | Update Set committed on the PDI |
| `verified` | Post-commit portal/UI verification complete, evidence captured |
| `rolled-back` | Change was backed out; reason and method recorded in `verification.md` |

A package cannot skip states. A package cannot be marked `committed` without approval evidence in `verification.md` (enforced by a local hook — see §8).

## 6. Prior exploration — explicitly out of scope

Earlier sessions performed read-only discovery and one directly-UI-built demo ("AI Request Hub" catalog item, a demo Change Request + tasks) on `dev446072.service-now.com`, before this workflow existed. That material is preserved in [`archive/2026-10-18-servicenow-exploration/`](archive/2026-10-18-servicenow-exploration/).

**It is exploratory only. It is not the EduPulse baseline, not a reference artifact, and not an approved feature.** Do not reuse its patterns, sys_ids, or structure in any real change package unless a future approved task explicitly says to adopt it.

One factual hazard worth knowing regardless of adoption: as of 2026-10-18, the Update Set `[AI DEMO] AI Request Hub - Catalog v1` (`sys_id 6654e7f493041b1075d9f9fbdd03d637`) was left **In Progress and set as the current Update Set** for the Administrator user on that instance. It was not exported, previewed, or committed, and must not be, absent explicit user authorization. If a future task ever targets that same PDI, this needs to be addressed deliberately (ask the user) rather than silently added to or silently completed/switched. See [`docs/servicenow/pdi-baseline.md`](docs/servicenow/pdi-baseline.md) for the full factual record.

## 7. Non-negotiable safety rules

1. Work only against a PDI (or other platform instance) the user has explicitly named for the specific task at hand.
2. Never upload, preview, commit, delete, or overwrite an Update Set without explicit user authorization for that **exact** change package.
3. Never commit an Update Set that has unresolved preview conflicts.
4. Never edit unrelated configuration or existing records outside the scope of the authorized change package.
5. **Never fabricate** unknown `sys_id` values, table metadata, or XML payload structures.
   - New records introduced by a change package get freshly generated sys_ids (standard ServiceNow behavior on create/export).
   - Any reference to an *existing* record, table, or scope must come from authoritative instance metadata or a real export obtained for that task — never invented, and never carried over from unrelated prior exploration without re-verifying it for the task at hand.
   - XML structure must be copied/derived from a real export, never hand-invented.
6. Before generating an executable Update Set XML, obtain and inspect a valid baseline export or authoritative instance metadata for anything the change touches.
7. Update Set XML moves **configuration**. It does not represent, carry, or substitute for submitted requests, user accounts, approvals, or other transactional data.
8. Keep configuration changes small, atomic, versioned, and reversible — one functional change per change package.
9. Preserve original exports (never overwrite a committed `update-set.xml` in place — a new change gets a new package) and write a rollback/back-out plan *before* deployment. Treat ServiceNow's built-in "Back Out" as unverified until tested — call this out explicitly in `plan.md` rather than assuming it works.
10. Do not store credentials, session cookies, tokens, or personal data in Git, XML, screenshots, plans, or reports. Scrub screenshots of any real user PII before adding them to `evidence/`.

## 8. Local validation hooks

This repo uses Claude Code hooks (`.claude/settings.json`) to catch mistakes locally, before they reach Git or any instance:

- XML well-formedness check on any `update-set.xml` touched in a commit.
- Required-files check per change package (varies by lifecycle state — see `changes/README.md`).
- Secret/credential scan on staged files.
- Block on marking a package `committed` in `manifest.yaml` without approval evidence in that package's `verification.md`.

Hooks never open a browser, upload XML, preview, or commit anything on any instance — they only validate local files. See [skills/servicenow-update-set/SKILL.md](skills/servicenow-update-set/SKILL.md) for what the validator checks.

Note: `.claude/settings.local.json` currently pre-allows the `mcp__playwright__browser_navigate` tool without a prompt. That predates the task-first rule in §2 and sits awkwardly with it — it's the user's call whether to tighten it; this file doesn't change it unilaterally.
