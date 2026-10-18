# TASK-000 — Project workflow setup

**Task ID:** TASK-000
**Title:** Project workflow setup
**Status:** Done
**Platform:** N/A — this is local repository/process tooling, not a ServiceNow (or any platform) change.

## User/business outcome

The user/developer can request EduPulse features with confidence that: every change is reviewable in Git before it touches any instance, nothing gets built without an explicit task and approval, and local safety checks (secrets, required files, approval-before-commit) run automatically. This task does not deliver any EduPulse-facing feature.

## Scope

- Establish `CLAUDE.md` as the mandatory, task-gated workflow definition for all future ServiceNow (or other platform) configuration work.
- Establish `docs/servicenow/` as living reference docs (architecture placeholder, deployment workflow, PDI baseline facts, glossary) — no speculative feature design.
- Establish `changes/` as the change-package convention (template + docs only).
- Establish `skills/servicenow-update-set/SKILL.md` as the detailed ServiceNow pipeline procedure.
- Establish this `tasks/` system (README, BOARD, template, status folders) as the mandatory starting point for all future feature work.
- Archive prior exploratory ServiceNow work (read-only discovery + one directly-UI-built demo) into `archive/2026-10-18-servicenow-exploration/`, explicitly marked as not a baseline, not a reference, not approved.
- Add local Claude Code hooks (`.claude/hooks/`) that: block `git commit` if staged files look like they contain credentials/tokens, and validate that any `changes/*/manifest.yaml` is well-formed, has required files for its lifecycle state, and cannot be marked `committed` without recorded approval evidence.
- Initialize this directory as a Git repository (`git init`, no commits made — left for the user).

## Out of scope

- Any EduPulse feature, screen, form, workflow, or data model.
- Any ServiceNow create/edit/import/preview/commit/export/delete action.
- Any proposal, recommendation, or adoption of the archived exploratory work as a baseline.
- Any external task-tracking service.

## Acceptance criteria

- [x] `CLAUDE.md` exists at the project root and states the task-first rule, the mandatory pipeline, lifecycle states, and safety rules.
- [x] `docs/servicenow/{architecture,deployment-workflow,pdi-baseline,glossary}.md` exist and contain no speculative EduPulse feature design.
- [x] `changes/` contains only `README.md` and `_template/` (no real change package, no XML).
- [x] `skills/servicenow-update-set/SKILL.md` exists and states its own precondition (approved task required).
- [x] `tasks/{README.md,BOARD.md,_template.md}` exist; `backlog/`, `in-progress/`, `done/` folders exist.
- [x] Prior exploratory ServiceNow material is preserved (not deleted) under `archive/2026-10-18-servicenow-exploration/`, with its own README clarifying its non-baseline status.
- [x] Local hooks exist, are wired via `.claude/settings.json`, and were tested locally against both a passing and a deliberately failing case.
- [x] No ServiceNow mutation occurred during this task or the correction that followed it — see `docs/project-cleanup-report.md`.

## Dependencies

None.

## Risks

None — local-only, reversible (plain files, no destructive action taken). The one live risk this task surfaces (not caused by it): an existing ServiceNow Update Set on the exploratory PDI was left "In Progress" and current by a prior session — tracked as a known hazard in `CLAUDE.md` §6 and `docs/servicenow/pdi-baseline.md`, not resolved by this task.

## Required ServiceNow components

None.

## Expected deployment artifact

None — no `update-set.xml`, no ServiceNow change of any kind.

## Human approval required

None for the setup/structure itself (process tooling, fully reversible). Every subsequent *feature* task still requires explicit human approval per `tasks/README.md`.

## Verification steps

- Confirmed `changes/` contains no files besides `README.md` and `_template/` (no stray `update-set.xml` anywhere in the repo: `find . -name "*.xml"` outside `node_modules` returns nothing).
- Ran `.claude/hooks/check_secrets.py` against a deliberately staged fake credential — confirmed it blocks (exit 1) and against a clean stage — confirmed it passes (exit 0).
- Ran `.claude/hooks/validate_change_packages.py` against a deliberately invalid `committed` package (no approval evidence) — confirmed it blocks (exit 1); fixed the test package and confirmed it then passes (exit 0).
- Confirmed `git status` shows no commits and nothing destructive was done to the pre-existing `serviceNow/` content (moved, not deleted).
- Verified internal Markdown links across the repo resolve to real files (see `docs/project-cleanup-report.md` for the method and result).

## Evidence links

- [`../../docs/project-cleanup-report.md`](../../docs/project-cleanup-report.md) — the correction/cleanup report covering this task's final state.
- [`../../archive/2026-10-18-servicenow-exploration/README.md`](../../archive/2026-10-18-servicenow-exploration/README.md) — archive contents and disposition.
