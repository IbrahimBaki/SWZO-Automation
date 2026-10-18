# Tasks

**Every future feature or ServiceNow (or other platform) change starts as a task here, before any work begins.** No feature is designed or built, and no Update Set XML is generated, without an approved task file — see [`../CLAUDE.md`](../CLAUDE.md) §2.

This is a local, Markdown-only task system. No external tracker (Jira, Linear, etc.) is used.

## Structure

```
tasks/
  README.md          this file
  BOARD.md            at-a-glance table of every task
  _template.md        copy this to start a new task
  backlog/            not started yet
  in-progress/        actively being worked
  done/               completed
```

A task's file lives in the folder matching its current status — moving a task between statuses means physically moving the file to the matching folder (and updating `BOARD.md`).

## What "approved" means

A task counts as **approved** only when the user has explicitly said so for that specific task, in that specific conversation — not implied by silence, not inherited from approving a different task, and not satisfied by the task merely existing in `backlog/`. Record the approval in the task file: who approved it, when, and what exactly was approved (the whole task, or a specific next step like "go ahead and write the plan, but not XML yet"). A `Blocked on user decision` task cannot be approved until the blocking decision is made.

## Required fields (every task)

```
Task ID              TASK-0NN, sequential
Title
Status                Backlog | In Progress | Done, plus an optional Blocked flag
Platform              ServiceNow | Zoho Creator | both | N/A — never left unstated
User/business outcome
Scope
Out of scope
Acceptance criteria
Dependencies
Risks
Required ServiceNow components   (N/A if platform isn't ServiceNow, or not yet known)
Expected deployment artifact
Human approval required
Verification steps
Evidence links
```

Use [`_template.md`](_template.md) as the starting point for every new task.

## Status vocabulary

- **Backlog** — captured, not started.
- **In Progress** — actively being worked.
- **Done** — completed and verified.
- **Blocked** (a flag, combinable with any of the above, e.g. "Backlog, Blocked on user decision") — cannot proceed until something named in the task (usually a user decision or a dependency) is resolved.

## Relationship to `changes/`

A task that results in ServiceNow configuration work spawns one or more `changes/<CHANGE-ID>/` packages (see [`../changes/README.md`](../changes/README.md)) once the task — and specifically the ServiceNow work it's requesting — is approved. The change package's `manifest.yaml` and `plan.md` must reference the `task_id` that authorized them. A task can exist, and even be fully scoped, without any change package yet — the change package only appears once XML generation is actually authorized.

Not every task produces ServiceNow work — a decision-only task (like defining demo scope) has "none" as its expected deployment artifact.
