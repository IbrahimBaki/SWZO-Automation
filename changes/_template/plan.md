# <CHANGE-ID> — <Title>

> Template. Copy this directory, rename it, and fill in every section below. Delete this blockquote.

## Approving task

`task_id`: the `tasks/` file that authorized this package (must match `manifest.yaml`). No package exists without one.

## Request

Verbatim or faithfully summarized request this package implements, as scoped by the approving task.

## Affected portal/form behavior

What an end user (or admin) will see differently after this change. Be specific — field names, forms, pages.

## Implementation approach

What ServiceNow mechanism this uses (Catalog Item/Variables/UI Policy, Service Portal widget, Flow, custom table, etc.) and why. Name every table/record type touched. If this depends on existing configuration, name the baseline/export it was built against (must match `manifest.yaml: source_baseline`).

## Rollback approach

How this gets backed out if committed in error. Name the specific mechanism (Update Set Back Out, or a compensating Update Set) and note whether it has been verified to work on this PDI — if untested, say so rather than assuming.

## Validation steps

The exact steps that will be performed post-commit to confirm the change works (what to click, what to expect). These become the checklist in `verification.md`.

## Risks

Anything that could go wrong: conflicts with existing config, scope issues, data migration concerns, access-control implications, etc.

## Approval status

- [ ] Plan reviewed by a human
- [ ] XML reviewed by a human
- [ ] Preview clean / conflicts explicitly accepted
- [ ] Commit explicitly authorized for this exact package

Approver, date, and scope of approval go in `verification.md`, not here.
