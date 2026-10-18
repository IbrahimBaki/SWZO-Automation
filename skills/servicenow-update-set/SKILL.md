# Skill: ServiceNow Update Set Workflow (EduPulse)

Read this before starting, continuing, or reviewing any ServiceNow configuration change in this repository. It operationalizes the rules in [`../../CLAUDE.md`](../../CLAUDE.md) — if anything here conflicts with that file, CLAUDE.md wins.

> Note: Claude Code only auto-loads skills from `.claude/skills/<name>/SKILL.md`. This file lives at `skills/servicenow-update-set/SKILL.md` per the project's requested layout, so it must be read deliberately (CLAUDE.md links to it) rather than relying on auto-discovery. Moving or symlinking it under `.claude/skills/` would enable auto-discovery if that's ever wanted.

## Precondition

This entire skill only applies once an **approved task** under `tasks/` (see [`../../tasks/README.md`](../../tasks/README.md)) names ServiceNow as the platform and states the intended action. No change package, XML, or Playwright/instance interaction starts without that — see [`../../CLAUDE.md`](../../CLAUDE.md) §2.

## When to use this

Any approved-task request to add, change, or remove ServiceNow configuration for EduPulse (catalog items, variables, UI policies, portal pages/widgets, tables, roles, ACLs, flows, scripts — anything that would normally travel in an Update Set).

Not for: read-only discovery/inspection (still requires its own task-level authorization per CLAUDE.md §2.3), or working with transactional data (actual submitted requests, change records) which isn't Update-Set-tracked configuration.

## Naming

- Change package directories: `changes/<PREFIX>-<NNN>-<short-slug>/`, e.g. `changes/EDUPULSE-001-<slug-from-the-approved-task>/`.
- `<PREFIX>` is `EDUPULSE` for this project unless the user names a different one.
- `<NNN>` is zero-padded, sequential, assigned at package creation time.
- `<short-slug>` is lowercase-kebab, short, describes the functional change (not the ticket/task).

## Artifact checklist (per change package)

- [ ] `plan.md` — filled from the template, every section addressed (not left as placeholder text)
- [ ] `manifest.yaml` — valid YAML, all required keys present, `lifecycle_state` accurate
- [ ] `update-set.xml` — present only once actually generated; absent (not a placeholder) before that
- [ ] `verification.md` — updated as each pipeline step actually happens, not pre-filled
- [ ] `evidence/` — contains real screenshots/links once verification starts, PII scrubbed

## XML validation checklist (before treating update-set.xml as ready to commit)

- [ ] Well-formed XML (hook checks this automatically; `python3 -c "import xml.etree.ElementTree as ET; ET.parse('update-set.xml')"` as a manual fallback)
- [ ] Every `sys_id` referencing an *existing* record matches a value confirmed from the instance or a real export — not invented
- [ ] No unrelated records/changes bundled in beyond what `plan.md` describes
- [ ] No credentials, session tokens, or personal data embedded in any field value
- [ ] `source_baseline` in `manifest.yaml` names what this was built against

## Playwright safety rules

- Playwright only drives: XML upload (Retrieved Update Sets → Import), Preview, Commit (post-approval only), evidence screenshots, and end-user portal verification.
- Never use Playwright to directly create/edit configuration records as a substitute for the XML pipeline, except an explicitly authorized bootstrap/emergency change — and even then, log it in that package's `verification.md` with the authorization quoted.
- Never click Commit without a specific, current, explicit "yes, commit `<CHANGE-ID>`" from the user. A prior approval for a different package, or a general "looks good," does not count.
- Never proceed past a Preview that shows conflicts without the user explicitly deciding how to handle them.
- Capture a screenshot at Preview and at final portal verification, minimum, for every package.

## Final verification checklist (before marking a package `verified`)

- [ ] Preview was clean, or conflicts were explicitly resolved/accepted by the user (recorded in `verification.md`)
- [ ] Commit was explicitly authorized for this exact package and performed
- [ ] Portal re-checked as an end user, matching `plan.md`'s validation steps
- [ ] `verification.md` fully filled in (import, preview, approval, commit, portal check)
- [ ] `evidence/` has supporting screenshots, PII-free
- [ ] `docs/servicenow/pdi-baseline.md` updated if this package changed what's "known to exist" on the instance
- [ ] `manifest.yaml: lifecycle_state` set to `verified`

## Open questions this skill does not resolve

Platform, portal/table architecture, scope, and access-control decisions for EduPulse are not yet made — see [`../../tasks/backlog/TASK-001-define-edupulse-demo-scope.md`](../../tasks/backlog/TASK-001-define-edupulse-demo-scope.md) and [`../../docs/servicenow/architecture.md`](../../docs/servicenow/architecture.md). Resolve those (as approved tasks) before the first change package that depends on them.
