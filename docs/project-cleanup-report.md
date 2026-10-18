# Project Cleanup Report — 2026-10-18

Scope: local repository cleanup and task-management preparation only. **No ServiceNow create, edit, import, preview, commit, complete, export, or delete action was performed as part of this cleanup.** No EduPulse feature, XML package, portal page, catalog item, form, or workflow was created.

## 1. Why this correction happened

The previous preparation pass treated prior exploratory ServiceNow work (the "AI Request Hub" demo and Change Management discovery) as a reference baseline for EduPulse, and its report recommended exporting that work's Update Set and starting a `EDUPULSE-001-landing-page` package. Both were premature: that work was exploratory only, not an approved EduPulse baseline. This cleanup corrects that by archiving the exploratory material, stripping speculative feature/architecture content from the reusable docs, and adding a task-first gate so nothing gets designed or built without an explicit, approved task.

## 2. Files archived

Moved from `serviceNow/` (deleted after the move; nothing was deleted *in content*) into [`archive/2026-10-18-servicenow-exploration/`](../archive/2026-10-18-servicenow-exploration/), structure and relative screenshot paths preserved exactly:

```
ai-request-hub-catalog-v1.md
ai-request-hub-discovery.md
ai-request-hub-dynamic-url-field.md
change-management-discovery.md
chg0030001-change-task-discovery.md
chg0030001-change-tasks-creation.md
demo-change-request-creation.md
screenshots/ (12 PNG files, unchanged)
```

Also moved into the same archive directory, as a superseded document (not original exploratory evidence, but built entirely on the now-rejected premise):

```
project-preparation-report-2026-10-18-SUPERSEDED.md   (was docs/servicenow/project-preparation-report.md)
```

A banner was added to the top of that file stating its export/XML-package recommendations are withdrawn. A new [`archive/2026-10-18-servicenow-exploration/README.md`](../archive/2026-10-18-servicenow-exploration/README.md) explains what's archived and, explicitly, that none of it is a baseline, reference artifact, or approved feature.

Nothing was deleted. `git status` / `find` confirm the file count moved matches the file count archived (20 files + 1 superseded report = 21).

## 3. Reusable workflow foundation kept at the project root

```
CLAUDE.md                               — rewritten: task-first gate added, project framed as "scope not yet defined," prior exploration explicitly marked out of scope
docs/servicenow/
  architecture.md                       — rewritten: no speculative design; defers to tasks/
  deployment-workflow.md                — updated: pipeline now starts from "approved task," not "natural-language request"
  pdi-baseline.md                       — rewritten: factual record only, explicitly marked "not a baseline, not a recommendation"
  glossary.md                           — updated: removed "repurposed as a registration form" framing, softened PDI/portal claims
changes/
  README.md                             — updated: states the task-approval precondition, added task_id to the manifest schema, genericized naming examples
  _template/                            — unchanged in structure; manifest.yaml and plan.md now require a task_id
skills/servicenow-update-set/SKILL.md   — updated: states its own precondition (approved task required), removed dangling link to the now-archived prep report
```

`changes/` contains **only** `README.md` and `_template/` — confirmed via directory listing. No `update-set.xml` exists anywhere in the repository (confirmed via `find . -name "*.xml"`, excluding `node_modules`). No proposed EduPulse change package exists.

## 4. New local task system

```
tasks/
  README.md              task-first rule, required fields, status vocabulary, what "approved" means
  BOARD.md                table of all tasks (currently TASK-000, TASK-001)
  _template.md            copy-to-start template with all 14 required fields
  backlog/
    TASK-001-define-edupulse-demo-scope.md
  in-progress/            empty (.gitkeep)
  done/
    TASK-000-project-workflow-setup.md
```

- **TASK-000** (`Done`) describes exactly this local preparation work (the original setup session plus this correction) — no feature, no ServiceNow mutation.
- **TASK-001** (`Backlog, Blocked on user decision`) invents nothing. It contains seven genuinely empty decision sections — purpose, target end users, first visible screen, first form/workflow, what the AI should change live, platform (ServiceNow / Zoho Creator / both), and success criteria — each marked "_Decision needed_," with no suggested answers.

`CLAUDE.md` §2 now states plainly: no feature is designed or built without an approved task; no XML is generated without an approved task and a `plan.md`; no ServiceNow action occurs without explicit authorization; existing PDI artifacts are out of scope unless explicitly adopted by a future task; Playwright is used only after a task specifies the intended action and its verification.

## 5. Verification performed

- **Link check:** wrote and ran a script that extracts every Markdown link repo-wide (archive included), resolves it relative to its containing file, and reports anything missing. Found and fixed one broken sibling link inside the archived superseded report (it had pointed to a file that moved); all links now resolve, including the three that pointed forward to this report before it existed.
- **No XML anywhere:** `find . -name "*.xml" -not -path "./node_modules/*"` returns nothing.
- **`changes/` is templates-only:** directory listing shows only `README.md` and `_template/`.
- **`serviceNow/` no longer exists** at the old path; its contents are confirmed present, unchanged, under the archive path.
- **Grep sweep** for leftover design-assumption language (`landing page`, `registration`, `AI Request Hub`, `EDUPULSE-00N-<slug>`, `serviceNow/`, `precedent`, `hypothesis`, the Service Catalog sys_id) outside `archive/`: every remaining hit is a deliberately neutral, factual reference (e.g. a hazard note pointing at the archive, or a task description of what was done) — none proposes or assumes a feature.
- **Local hooks still pass:** `.claude/hooks/check_secrets.py` and `.claude/hooks/validate_change_packages.py` were re-run after all moves/edits and both report clean (no change packages exist to validate; no secrets staged). These hooks were not modified in this cleanup, only the documentation around them.
- **No ServiceNow mutation:** no instance was navigated, read, or modified during this cleanup — it was entirely local file moves and edits, verified by reviewing every tool call made during this task.

## 6. Carried-over note (not actioned)

`.claude/settings.local.json` still pre-allows the `mcp__playwright__browser_navigate` tool without a prompt. This predates the new task-first rule and sits awkwardly next to it (CLAUDE.md §2.4 now requires a task to specify intended action before Playwright is used at all). Left untouched — flagged in `CLAUDE.md` §8 as the user's call, not changed unilaterally here.

## 7. What's next

Nothing ServiceNow-related can proceed until [`tasks/backlog/TASK-001-define-edupulse-demo-scope.md`](../tasks/backlog/TASK-001-define-edupulse-demo-scope.md) is answered by the user.
