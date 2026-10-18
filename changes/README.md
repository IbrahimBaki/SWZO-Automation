# Change Packages

**Precondition: a change package only gets created for an approved task.** See [`../tasks/README.md`](../tasks/README.md) and [`../CLAUDE.md`](../CLAUDE.md) §2 — no feature is designed or built, and no XML is generated, without an approved task and a `plan.md` referencing it. This directory currently contains only the template and this documentation — no real change package exists yet.

One directory per atomic functional change, named `<CHANGE-ID>-<short-slug>`, e.g. `changes/EDUPULSE-001-<slug-from-the-approved-task>/`.

IDs are sequential per project prefix (`EDUPULSE-00N`), assigned in the order the change is started, not necessarily the order it ships. The slug describes the functional change decided by its task — don't pre-guess feature names here.

To start a new one (only once a task approves it): copy [`_template/`](_template/) to a new `<CHANGE-ID>-<slug>` directory and fill it in. `_template/` itself is never deployed and is skipped by the validation hook.

## Required contents

| File | Purpose | Required from state |
|---|---|---|
| `plan.md` | Developer-readable: what's changing, affected portal/form behavior, implementation approach, rollback approach, validation steps, risks, approval status. Must reference the approving `task_id`. | `planned` |
| `manifest.yaml` | Structured metadata — see schema below | `draft` (all states) |
| `update-set.xml` | The exact Update Set XML, only once generated/exported from a verified baseline. **Never create a placeholder/fake XML file** — if it doesn't exist yet, `manifest.yaml`'s `xml_artifact` stays `pending` and the file is simply absent. | `xml-generated` |
| `verification.md` | Import, preview, conflict, commit, and portal-test evidence/log | `imported` onward |
| `evidence/` | Screenshots or links captured during verification (scrub PII first) | `previewed` onward |

## manifest.yaml schema

```yaml
change_id: EDUPULSE-00N
task_id: TASK-0NN             # the approved task that authorized this package — required
title: Short human title
pdi_target: "<instance explicitly named by the approving task>"
source_baseline: "<what export/instance-state this was built against, or 'none (net-new)'>"
affected_components:
  - table_or_component_1
  - table_or_component_2
dependencies: []            # other change_ids this one requires, if any
xml_artifact: pending       # pending | changes/<id>/update-set.xml
lifecycle_state: draft      # see CLAUDE.md §5 for the full ordered list
approval:
  required: true
  approved_by: null         # set only once a human has actually approved THIS package
  approved_at: null
```

## Lifecycle states

Defined in [`../CLAUDE.md`](../CLAUDE.md) §5: `draft → planned → xml-generated → peer-reviewed → imported → previewed → awaiting-human-approval → committed → verified` (or `rolled-back` at any point after `committed`). States cannot be skipped.

A local hook blocks setting `lifecycle_state: committed` unless `verification.md` already contains approval evidence (who approved, when, for this exact package) — see [`../skills/servicenow-update-set/SKILL.md`](../skills/servicenow-update-set/SKILL.md).
