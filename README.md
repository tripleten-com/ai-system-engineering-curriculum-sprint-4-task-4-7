# Coldline Task 4.7 — Project Defense

This checkpoint is the complete, settled Coldline platform. Everything Tasks 1 through 6
assessed now ships supplied in its reference version: the threat model from Task 4.1, the token
verification and access rule from Task 4.2, the output guardrail and audit events from Task
4.3, the PII redaction from Task 4.4, the secret read and security gate from Task 4.5, and the
corrections, risk register and decision record from Task 4.6. This Task adds no code. What you
do instead is assemble the pull request record you built across Tasks 1 through 6 into one
evidence index and a three-part defense structure in this Task's pull request description,
open a pull request that touches only `submission.yaml`, and then deliver a live Project
Defense of at most 10 minutes to your instructor, from the pull requests, the check runs and
your own records on screen.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tripleten-com/ai-system-engineering-curriculum-sprint-4-task-4-7/tree/main)

## Start the system

Prerequisites are Python 3.12 and Docker with Compose v2. The supplied bootstrap supports macOS
arm64/x86-64, Windows x86-64, and Linux x86-64/aarch64, and installs pinned uv 0.11.8 under
`.tools/bin`. If your computer cannot run the stack locally, use the Codespaces button above.

On macOS and most Linux distributions the interpreter is `python3`; substitute it wherever these
commands say `python`.

```shell
python infra/scripts/bootstrap.py
./.tools/bin/uv sync --frozen
./.tools/bin/uv run --frozen poe preflight
./.tools/bin/uv run --frozen poe start
./.tools/bin/uv run --frozen poe ready
```

PowerShell and POSIX wrappers are available under `infra/scripts/`. After uv is on `PATH`, the
shorter `uv run --frozen poe <task>` form works; in PowerShell on Windows the pinned binary is
`.tools/bin/uv.exe`.

| Service | Local URL | Purpose |
|---|---|---|
| API | `http://localhost:8000` | Submit readings, poll exception summaries, search procedures |
| Token issuer: discovery document | `http://localhost:8180/.well-known/openid-configuration` | The development issuer's OIDC discovery document: its `issuer` and `jwks_uri` |
| Token issuer: key set | `http://localhost:8180/.well-known/jwks.json` | The published key set (JWKS) the settled `config/auth.yaml` names |
| Jaeger | `http://localhost:16686` | Open traces; the trace ids the audit records carry are these |
| Grafana | `http://localhost:3000` | Use the focused diagnostics dashboard |
| Prometheus | `http://localhost:9090` | Query bounded metrics and inspect the deployed alert rule |
| Alertmanager | `http://localhost:9093` | Inspect firing and resolved alerts |
| LocalStack S3/SQS/Secrets Manager | `http://localhost:4566` | The emulated object-storage, queue and secret-store endpoint |

Each of these ports can be overridden by setting the matching `COLDLINE_API_HOST_PORT`,
`COLDLINE_ISSUER_HOST_PORT`, `COLDLINE_JAEGER_HOST_PORT`, `COLDLINE_GRAFANA_HOST_PORT`,
`COLDLINE_PROMETHEUS_HOST_PORT`, `COLDLINE_ALERTMANAGER_HOST_PORT`, or
`COLDLINE_LOCALSTACK_HOST_PORT` environment variable in your shell environment or a local
`.env` file (copy `.env.example`) if a default collides with something already running on your
machine. Keep the override in place for every `poe` command. If you remap the issuer port,
keep `config/auth.yaml` unchanged: it is supplied in this Task and names the default port.
Host-side tools (the carried access and audit tests, `poe token-check`) resolve the API's and
the issuer's origins from `COLDLINE_API_HOST_PORT` and `COLDLINE_ISSUER_HOST_PORT` (the
environment, then `.env`, then the default), the secret tools resolve LocalStack's host port
from `COLDLINE_LOCALSTACK_HOST_PORT` the same way, and the API and the worker use the
Compose-network origins.

This Task runs as its own Compose project, `coldline-task-4-7`. If an earlier Task's stack is
still running, run `poe stop` in that Task's repository first; otherwise `poe start` here fails
because the published ports are already taken.

PostgreSQL, Redis, worker metrics, and OTLP remain inside the Compose network. Codespaces uses the
same `compose.yaml` and keeps every forwarded port private. Redis keeps running only for an
earlier checkpoint's own contract test; no composition root reads it anymore.

## Command path

For this Task, run the supplied commands in this order:

```text
poe answers        # as you prepare the branch: the answer sheet still records answers: {}
poe submission     # before you push: only submission.yaml changed
poe verify
```

The exact public command is `./.tools/bin/uv run --frozen poe verify`, run from the repository
root. Where a Task page shortens a command to `poe <task>`, that is the form it means.

| Command | Use |
|---|---|
| `poe verify` | The public student verification path: this Task's own answer-format and permitted-files checks first, then it starts the stack, ingests the supplied corpus, and reruns the checks on the controls you inherited: the running platform, the end-to-end workflow, and the carried Task 4.2, 4.3 and 4.4 tests |
| `poe answers` | This Task's answer-format check on its own: `submission.yaml` is one plain mapping whose `answers` is present and empty |
| `poe submission` | The same check plus the permitted-files boundary: the diff from your merge base touches only `submission.yaml` |
| `poe integrity-record`, `poe integrity-check` | The first and last steps of `poe verify`: hash the answer sheet and the checks' own files into a snapshot outside the repository, then compare the tree with it, so a file that changed while the run was in progress is named |
| `poe student-tests` | Run the supplied tests under `tests/student/`: the carried Task 4.2 access tests, Task 4.3 guardrail and audit tests and Task 4.4 redaction tests. None is yours in this Task; start the stack first |
| `poe auth-checks`, `poe token-check <fixture>`, `poe auth-config` | Task 2's tools over the settled `config/auth.yaml` and the access rule, still runnable; not this Task's exercise |
| `poe scenario [--response <name>] [--note <id>]`, `poe audit-trail <exception_id>`, `poe pii-scan <exception_id>`, `poe redaction-report`, `poe model-request <exception_id>` | Task 3's and Task 4's tools, still runnable; not this Task's exercise |
| `poe secret-status`, `poe secret-replace`, `poe provider-auth-check`, `poe secret-check-old` | Task 5's secret tools, still runnable; none prints a value; not this Task's exercise |
| `poe security-setup`, `poe security-scan`, `poe seed-secret`, `poe seed-vulnerable` | Task 5's gate tools, kept as supplied; the `security-gate` job still runs `poe security-scan` on every pull request with the settled thresholds and suppression, and the clean tree passes it |
| `poe attack-dev` | Task 6's development attack, still runnable; writes `evidence/attack-dev.json`. Your Task 6 evidence is the stage summary you recorded then, at Task 6's accepted commit; a run here is not that record |
| `poe queue-contract`, `poe slo-contract`, `poe gate-contract`, `poe runbook-contract`, `poe e2e` | Project 3's checks and the inherited platform checks, runnable as supplied |
| `poe contract` | Check interfaces, boundaries, submissions, and repository structure |
| `poe migrate`, `poe migrate-down`, `poe migrate-current` | Step the schema by hand; the initializer brings it to head on every start |
| `poe restart` | Restart the existing API and worker containers **without rebuilding** |
| `poe stop` | Remove containers and the network, keeping named volumes |
| `poe reset` | Remove containers, the network, and local named volumes |

`poe verify` records an integrity snapshot of the answer sheet and the checks' own files, runs
`poe answers` and `poe submission`, runs the unit tests, starts the stack, ingests the supplied
corpus, runs the smoke tests, the end-to-end workflow and the carried student tests, and
finally compares the tree with the snapshot. Nothing in it grades the evidence index or the
defense. If the answer format and the permitted files pass but a later step fails, the
checkpoint needs attention, not your submission: keep the result as it is and contact course
support. The earlier Tasks' tools remain in the table above because they still run, but the
lesson is explicit: point at the record you attached when each Task was accepted, and do not
rerun an exercise now for fresher output.

## Folder map

```text
repository root/
├── .gitleaks.toml       The settled secret-scanner configuration from Task 5
├── .semgrepignore       The paths Semgrep leaves out
├── config/              Retrieval configuration, settled since Sprint 2, and the settled auth.yaml
├── docs/                Student guidance, public contracts, fidelity notes, the security and governance material
│   ├── contracts/       Machine-readable public contracts, including this Task's answer schema
│   ├── fidelity/        Local-runtime boundary notes for each active adapter and the token issuer
│   ├── governance/      The Task 6 analysis, owners, concerns and decision policy, and reference versions of the register and the decision record
│   ├── security/        The supplied workflow, threat catalog, control matrix, access policy, output policy, audit events, redactor, and gate policy
│   ├── architecture/    Supplied vector engine technical profiles, in prose
│   ├── retrieval/       Supplied retrieval pipeline reference
│   └── student/         This Task's contract, the settled threat model, a reference version of the Task 6 corrections, and the Project 3 runbook
├── evidence/            Git-ignored: the evidence file `poe attack-dev` writes, if you run it
├── infra/               Local setup and runtime configuration
│   ├── containers/      The API and worker Dockerfiles, with the build identity arguments
│   ├── issuer/          The development token issuer: its server script and the published key set
│   ├── observability/   Prometheus, Alertmanager, and Grafana configuration
│   ├── release/         The supplied release manifest, unchanged
│   ├── corpus/          Supplied synthetic corpus (one procedure carries the planted instruction), query set, and investigation
│   ├── judge/           Supplied cached judge evidence and its provenance record
│   ├── profiles/        Supplied engine and emulator profiles, and their provenance record
│   └── postgres/        Database initialization and the migration baseline stamp
├── loadtest/            Supplied traffic profile and provider-latency harness
├── migrations/          Alembic environment, revision template, and revisions
├── reports/             Git-ignored: the scan report and the bill of materials `poe security-scan` writes
├── schemas/             The supplied output schema the guardrail enforces
├── security/            The settled gate thresholds, the scanner pins, the supplied Semgrep rules
├── src/
│   ├── api/             HTTP application code, the retrieval and document paths, composition, the initializer, the audit-trail command
│   │   └── security/    The settled TokenVerifier and require_access rule
│   ├── worker/          Background application code, the settled settings module, the procedure lookup, the guardrail, the redaction calls
│   ├── common/          The supplied audit sink and the supplied redactor both services use
│   ├── domain/          Shared domain code, contracts, the failure taxonomy, service and repository contracts
│   ├── ports/           Application interfaces
│   └── adapters/        Technology-specific implementations, including the secret-store adapter, the model emulator with its key check, the audit store, the SQS adapter
└── tests/
    ├── unit/            Isolated behavior checks
    ├── benchmark/       Supplied evaluation harness, metrics, and adoption policy
    ├── contract/        Interface, retrieval, and repository checks, and this Task's answer-sheet and boundary checks
    ├── diagnostics/     Supplied stage inspector
    ├── doubles/         Supplied deterministic test doubles
    ├── failure/         Supplied Project 3 failure-lab and exercise scripts; not this Task's work
    ├── fixtures/        Supplied fixtures: the token fixtures, the credential values, the handling notes under pii/, the development attack under attacks/
    ├── security/        Supplied tooling: the attack procedure, the integrity bookends, the inherited harness, scan, secret and gate tools
    ├── student/         The carried Task 4.2, 4.3 and 4.4 test files; none is yours in this Task
    ├── smoke/           Running-platform checks
    └── e2e/             Supplied workflow tools and checks, including `poe scenario`
```

## Overview

Use the Task 7 lesson (Task 4.7 in this repository) to decide what to do. This README covers
local setup and repository orientation.

1. `README.md` — local setup, commands, and permitted changes.
2. [`docs/student/task-4-7-contract.md`](docs/student/task-4-7-contract.md) — what this Task
   assesses and who assesses it, what belongs in the pull request description, the Check-list
   rows and the checks that read them, and the one permitted path.
3. [`docs/governance/owners.md`](docs/governance/owners.md) — the owner roles; the risk you
   accept at the defense names one of them.
4. [`docs/security/control-matrix.md`](docs/security/control-matrix.md) — the controls and the
   limit each one states.
5. [`docs/fidelity/TokenIssuer.md`](docs/fidelity/TokenIssuer.md) and
   [`docs/fidelity/SecretProvider.md`](docs/fidelity/SecretProvider.md) — what the development
   issuer and LocalStack Secrets Manager do not establish; the limits you bring forward in the
   second part.
6. [`docs/student/threat-model.md`](docs/student/threat-model.md),
   [`docs/student/governance-corrections.md`](docs/student/governance-corrections.md),
   [`docs/governance/risk-register.yaml`](docs/governance/risk-register.yaml) and
   [`docs/governance/decision-record.md`](docs/governance/decision-record.md) — completion/reference
   versions of the Task 1 and Task 6 records, supplied for orientation; not your evidence. At the
   defense, use your own records at their accepted commits.

The application source lives in six flat packages:

| Package | Responsibility |
|---|---|
| `api` | HTTP delivery, API use cases, the retrieval workflow, versioned routes, token verification and the access rule, configuration, composition, the initializer, and the audit-trail command |
| `worker` | Background processing, retries, procedure lookup, the output guardrail, the redaction, the record readers, the settled settings module, and composition |
| `common` | The audit sink and the redactor the API and the worker share, and the event names |
| `domain` | Provider-neutral contracts, state rules, identity, embedding, chunking, fusion, access constraints, failure classification, service and repository contracts |
| `ports` | Exactly five visible application interfaces |
| `adapters` | PostgreSQL (exception records and audit records), pgvector retrieval, LocalStack SQS/DLQ, S3-compatible object storage, LocalStack Secrets Manager, the deterministic model emulator with its supplied responses, request log and key check, the resilient model-provider wrapper, logs, traces |

`src/api/bootstrap.py` and `src/worker/bootstrap.py` compose each process from its settings and
adapters. Process settings live in `src/api/config.py` and `src/worker/config.py`; the token
verification settings live in `config/auth.yaml`.

## The five ports

Find the available interfaces in `src/ports/`. A port describes an application capability; an
adapter provides it using a concrete technology.

| Port | General responsibility |
|---|---|
| `ModelProvider` | Call an AI model service; it returns the provider's raw answer text, which the worker redacts and the guardrail checks, and it authenticates the key the client presents |
| `Retriever` | Look up relevant context or documents; the worker calls it too |
| `ObjectStore` | Store large binary objects or files |
| `JobQueue` | Publish and consume background work |
| `SecretProvider` | Read API keys and credentials; the supplied LocalStack Secrets Manager adapter provides it |

## Test levels

| Level | Requires Compose | Main question |
|---|---|---|
| Unit | No | Does one responsibility behave correctly, including failures? |
| Contract | Some | Do interfaces, schemas, paths, and dependency rules stay compatible? |
| Smoke | Yes | Did the complete local platform initialize and become observable? |
| E2E | Yes | Can an external client complete the supplied workflow, in one trace? |
| Student | Issuer | Do the carried Task 4.2, 4.3 and 4.4 tests still hold over the supplied code? |

Contract checks marked `runtime` need the running stack. `poe contract` skips them; `poe
runtime-contract`, `poe queue-contract`, `poe slo-contract`, and `poe gate-contract` run them.
This Task's own checks, `poe answers` and `poe submission`, are static and need no stack.
Unlike every earlier Task, a fresh Task 4.7 checkout has no expected failures: the checkpoint
is settled, so `poe verify` passes as shipped.

## Submission checks

Run `poe verify` locally before opening your student pull request. Public GitHub CI repeats
the student checks, running `poe submission` first so a boundary violation fails fast, and the
`security-gate` job runs `poe security-scan` with the settled thresholds. This Task records
`answers: {}`: the pull request record from Tasks 1 through 6 and your live defense of it are
the evidence, so there is no protected answer check. There is no protected held-out job in this
Task either; Sprint 4's one held-out scenario belonged to Task 4.6 and left with it. The
evidence index and the three-part structure in your pull request description, and the defense
itself, are read and judged by your instructor, at the Instructor Review and the Project
Defense, not by any automated check. Follow the Task lesson's instructor-review and
progression policy.

## Task boundary

Task 4.7 asks you to assemble the evidence index and the three-part structure into this Task's
pull request description, open a pull request that changes only `submission.yaml`, run
`poe verify`, and deliver the live Project Defense.

The only student-editable path is:

- `submission.yaml`

The supplied `submission.yaml` is already this Task's correct answer sheet. If your branch
needs a change to commit, add one YAML comment above `answers: {}` with the date you prepared
the evidence index. The Task 6 corrections, register and decision record, the threat model, the
carried tests under `tests/student/`, the code, the configuration, `security/gate.yaml`,
`.gitleaks.toml` and the workflows are supplied and settled here; keep them, and every other
file, exactly as supplied. The public check compares the diff from your merge base with this
one permitted file and reports any other change as a boundary violation.

### Student walkthrough

See **Task 7: Project Defense** in your course platform for the full walkthrough. In outline:
read `docs/student/task-4-7-contract.md`, open each of Tasks 1 through 6 on the platform and in
its repository, assemble the six entries and the three-part structure into this Task's pull
request description, check that `git diff --stat` shows only `submission.yaml`, run `poe verify`,
open and merge your pull request, submit on the platform, rehearse the three parts against the
clock, and deliver the defense with the pull requests, the check runs and your own records at
their accepted commits on screen.

## Operational limits

This local system does not authenticate users against a managed identity provider, terminate
TLS, or manage production secrets. The token issuer is a development service: it publishes one
fixed key set over plain HTTP and issues no tokens; the eight fixtures were signed once and
committed. See [TokenIssuer fidelity](docs/fidelity/TokenIssuer.md). The Compose PostgreSQL
password and the LocalStack access keys are development values, listed once more in
`tests/fixtures/credentials/test-values.yaml` so the audit checks can search for them. Never
place real credentials, personal data, or production records in this repository. Every
handling note in this repository, the development attack's included, is synthetic.

The secret store is LocalStack Secrets Manager: it shows the read path and the version check,
not how AWS Secrets Manager, IAM, or KMS would decide who may read the secret. See
[SecretProvider fidelity](docs/fidelity/SecretProvider.md). The emulator's key check is a
property of this emulator. See [ModelProvider fidelity](docs/fidelity/ModelProvider.md).

The tested attack cases show how the controls handled those inputs, not inputs nobody sent.
The scanners find what their rules and their database cover, at the versions pinned in
`security/scanners.yaml`; an absent finding is not an absent weakness, as
`docs/security/gate-policy.md` states. These are the limits the lesson asks you to state in the
second part of the defense; cite them, do not rewrite them.

Alertmanager here is configured with a "default" receiver that has no notification integration:
alerts are queryable through its own API but never sent anywhere real. Never add a webhook, email,
Slack, or paid integration; Sprints 1-4 are emulator-only and never call a hosted endpoint.

LocalStack's SQS emulation is a local reliability primitive, not a managed-service durability,
IAM, availability, or cost claim. See [JobQueue fidelity](docs/fidelity/JobQueue.md) for the
exact boundary.

Named volumes preserve local PostgreSQL, Redis, Prometheus, Alertmanager, Grafana, and Jaeger state
across `poe stop`; the audit table is in the PostgreSQL volume. LocalStack object, queue and
secret contents are deliberately not persisted; the initializer re-uploads the supplied corpus
artifacts, re-provisions the queue and re-creates the secret's first version on every start. The
worker's request records and its authentication record live inside the worker container and are
gone when it is recreated. The `poe reset` command deletes the named volumes. This topology makes
no backup, replication, high-availability, disaster-recovery, capacity, latency-SLO, or
availability claim beyond what Project 3 settled.

See [TokenIssuer fidelity](docs/fidelity/TokenIssuer.md),
[JobQueue fidelity](docs/fidelity/JobQueue.md),
[ModelProvider fidelity](docs/fidelity/ModelProvider.md),
[SecretProvider fidelity](docs/fidelity/SecretProvider.md),
[ObjectStore fidelity](docs/fidelity/ObjectStore.md), and
[Retriever fidelity](docs/fidelity/Retriever.md) for the active adapter boundaries. The
[local runtime evidence](docs/fidelity/local-runtime.md) records the current measurement and its
qualification limits.
