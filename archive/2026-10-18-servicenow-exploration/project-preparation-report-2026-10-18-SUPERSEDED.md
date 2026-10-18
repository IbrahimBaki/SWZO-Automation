> **⚠ SUPERSEDED — archived 2026-10-18.** This report incorrectly treated the exploratory "AI Request Hub" / Change Management work as a reference baseline for EduPulse and recommended exporting its Update Set (§4) and starting an `EDUPULSE-001-landing-page` package (§5). Both are **withdrawn**. The prior exploratory work is exploratory only — not a baseline, not a reference artifact, not an approved feature. See [`../../CLAUDE.md`](../../CLAUDE.md), [`../../docs/project-cleanup-report.md`](../../docs/project-cleanup-report.md), and [`../../tasks/backlog/TASK-001-define-edupulse-demo-scope.md`](../../tasks/backlog/TASK-001-define-edupulse-demo-scope.md) for current status. Kept below unedited, for historical record only.

---

# EduPulse / ServiceNow — Project Preparation Report

Date: 2026-10-18
Scope: preparation only. **No ServiceNow create/edit/import/export/preview/commit/delete was performed as part of this report.** All Playwright/instance activity referenced below is from prior sessions (see §2).

## 1. Files created or updated

```
.gitignore                                          (new)
CLAUDE.md                                           (new — mandatory workflow + safety rules)
docs/servicenow/architecture.md                     (new)
docs/servicenow/deployment-workflow.md              (new)
docs/servicenow/pdi-baseline.md                     (new)
docs/servicenow/glossary.md                         (new)
docs/servicenow/project-preparation-report.md       (new — this file)
changes/README.md                                   (new — package contract, naming, manifest schema)
changes/_template/plan.md                           (new — reusable scaffold)
changes/_template/manifest.yaml                      (new)
changes/_template/verification.md                    (new)
changes/_template/evidence/.gitkeep                  (new)
skills/servicenow-update-set/SKILL.md                (new)
.claude/settings.json                                (new — PreToolUse hook wiring)
.claude/hooks/git_commit_gate.py                     (new — dispatches the two checks below on `git commit`)
.claude/hooks/check_secrets.py                       (new — blocks committing likely credentials/tokens)
.claude/hooks/validate_change_packages.py            (new — manifest/XML/approval-gate validation)
```

Also: `git init` was run (no commits). Nothing is staged. The first commit is left to the user.

No files under the existing `serviceNow/` folder (prior discovery/demo reports and screenshots) were moved, renamed, or edited — they're linked from `docs/servicenow/pdi-baseline.md` as historical evidence instead, to avoid breaking their relative screenshot paths.

No `update-set.xml` or other placeholder XML was created anywhere, per instructions — `changes/_template/` and `changes/README.md` both state explicitly that the file must not exist until a real export happens.

## 2. What already exists on the PDI (from prior sessions, read via existing reports — not re-verified today)

- **Instance:** `dev446072.service-now.com`.
- An Update Set `[AI DEMO] AI Request Hub - Catalog v1` (`sys_id 6654e7f493041b1075d9f9fbdd03d637`) is **In Progress and is the current Update Set for the Administrator user**. It contains a demo catalog category/item built directly through the UI, before this workflow existed. **This needs a decision before any EduPulse UI work begins** — see §3.
- A demo Change Request `CHG0030001` + 2 Change Tasks exist (transactional data, not Update-Set-tracked, unrelated to EduPulse).
- Service Catalog, Service Portal (`/sp`), and Change Management are active with substantial pre-existing seed data (197 catalog items, 45 categories, 105 change requests).

Full detail: [`pdi-baseline.md`](../../docs/servicenow/pdi-baseline.md) (current version — this archived report originally linked a sibling file that has since moved), which also links the original reports now archived alongside this file.

## 3. Missing information needed before generating the first real XML change package

These are genuine open decisions — please answer or point me at where to find the answer:

1. **The "AI Demo" Update Set hazard.** It's in-progress and current right now. Should I: (a) leave it alone and just make sure EduPulse work uses a brand-new Update Set instead (requires explicitly switching "current" before each EduPulse session), (b) ask you to complete/export it first so it's out of the way, or (c) something else? I will not touch it without your direction.
2. **Scope:** Global application, or a dedicated scoped app (`x_<vendor>_edupulse`)? This affects every sys_id/table name in every future package.
3. **Portal/page architecture for the landing page:** a Service Portal page on the existing `/sp` portal, or a dedicated new portal? (Employee Center exists as an option but isn't activated — is it in scope?)
4. **Registration data model:** reuse the standard Service Catalog request pipeline (`sc_request`/`sc_req_item`, following the pattern already proven by the AI Request Hub demo), or a dedicated custom table per registration type? This affects reporting/workflow needs I don't know yet (e.g., do registrations need their own approval chain, status tracking, or integration with another system?).
5. **Access control:** should the landing page and registration forms be reachable by unauthenticated/guest users, or only authenticated users? This is a security-relevant decision I won't assume.
6. **Change-ID prefix confirmation:** I've assumed `EDUPULSE` (e.g. `EDUPULSE-001`) — confirm or tell me the preferred prefix.
7. **PDI release version** — not yet captured; useful before relying on any version-specific XML/table behavior. Easy to grab next session (System Diagnostics → Stats) if you'd like that as part of the first discovery pass.
8. **Non-admin test user** for end-user verification — none confirmed to exist yet; verification steps will need one (as data, not shippable via Update Set).

## 4. Recommended first baseline artifact to capture

Before generating any EduPulse XML, I'd recommend exporting the existing **AI Request Hub Update Set** (`6654e7f493041b1075d9f9fbdd03d637`) as a reference baseline — not to ship it, but because it's the closest real, working example on this exact PDI of the mechanism EduPulse forms will likely reuse (Catalog Item + Variables + Catalog UI Policy, including conditional show/hide/mandatory logic with zero scripting). Having its real XML on hand lets the first EduPulse package be modeled on verified structure instead of guessed structure — consistent with CLAUDE.md's "never fabricate XML structure" rule.

Caveats, both unverified on this PDI and requiring your authorization before attempting:
- Exporting to XML may require first marking the Update Set **Complete**, which is itself a state change — flagging this now so it isn't a surprise; to be confirmed on the instance, not assumed.
- This export should happen only with your explicit go-ahead, and ties directly into the open question in §3.1 about what to do with that Update Set.

## 5. Proposed first EduPulse change package

Recommend: **`EDUPULSE-001-landing-page`** — the smallest atomic, foundational piece (a Service Portal landing page introducing EduPulse), ahead of any registration flow, since the three registration packages (`EDUPULSE-002-student-registration`, `-003-parent-registration`, `-004-teacher-registration`) will likely link back to it and can reuse whatever portal/page mechanism it establishes.

This package has **not** been created yet (left at the proposal stage, per "preparation only") — creating its `plan.md` for real requires answering open questions §3.2–3.5 first (scope, portal architecture, data model, access control), otherwise the plan would be built on assumptions rather than decisions.

## 6. ServiceNow mutations performed in this task

None. This report, and every file listed in §1, are local repository changes only.
