# Glossary

**PDI (Personal Developer Instance)** — A free, personal ServiceNow instance for development/demo use. No PDI is yet confirmed as EduPulse's target — `dev446072.service-now.com` was used for prior exploration only (see [pdi-baseline.md](pdi-baseline.md) and [../../CLAUDE.md](../../CLAUDE.md) §1/§6).

**Update Set** — A ServiceNow container that records configuration changes (not data) made while it is the "current" set, so they can be exported, moved between instances, previewed, and committed as a unit.

**Retrieved Update Set** — The record created on a *target* instance after importing an Update Set's XML, prior to preview/commit.

**Preview** — The step where ServiceNow compares a retrieved Update Set's changes against the target instance's current state and reports conflicts (same record changed both places) before anything is actually applied.

**Commit** — Applying a previewed Update Set's changes to the target instance for real. Irreversible without a deliberate back-out.

**Back Out** — ServiceNow's built-in attempt to reverse a committed Update Set. Not yet verified as reliable on this PDI — treat as untested until a change package explicitly confirms it works.

**Service Catalog** — The OOB request-catalog app (categories, items, variables) that renders catalog items as forms in the Service Portal.

**Catalog Item / Variable / Catalog UI Policy** — A catalog item is a requestable "product"; variables are its form fields; a Catalog UI Policy conditionally shows/hides/requires variables based on other variables' values — no scripting required for simple conditions. Whether EduPulse ends up using this mechanism is undecided (see [architecture.md](architecture.md)).

**Service Portal (`/sp`)** — ServiceNow's OOB end-user-facing portal theme (as opposed to Employee Center, the newer alternative). Observed active on the exploratory PDI (`dev446072`); not confirmed as part of EduPulse's architecture.

**sys_id** — ServiceNow's internal 32-character hex primary key for every record. Never invent one for an existing record; only freshly-created records get freshly-generated ones (and those come from the platform, not from guessing).

**Scope / Application scope** — Whether configuration lives in the shared `Global` scope or an isolated scoped application (`x_<vendor>_<app>`). Not yet decided for EduPulse — see [architecture.md](architecture.md).

**Change package** — This repo's unit of work: one directory under `changes/` per atomic functional change, carrying its plan, manifest, XML (once generated), verification evidence, and lifecycle state. See [../../changes/README.md](../../changes/README.md).

**Lifecycle state** — The `manifest.yaml` field tracking a change package's progress through the pipeline (`draft` → … → `verified`/`rolled-back`). Full list in [../../CLAUDE.md](../../CLAUDE.md) §5.

**Task** — This repo's unit of authorization: nothing is designed or built without an approved task file under `tasks/`. See [../../tasks/README.md](../../tasks/README.md).
