# Task 4.7 — Project Defense contract

Six merged pull requests already record what each control did when it was tested. This Task
asks whether you can say why it is built the way it is, where its evidence stops, and why the
residual risk you accepted is acceptable now. You write no new code, no essay and no slides.
You assemble the pull request record you built across Tasks 1 through 6 into one evidence
index, structure it into a defense of at most 10 minutes, and deliver that defense live to
your instructor with the pull requests, the check runs and your own records on screen.

The evidence index and the three-part structure live in this Task's pull request
**description**, not in a file. The only change this Task's pull request makes to the
repository is `submission.yaml`, which stays `answers: {}`. Everything Tasks 1 through 6
assessed ships supplied and settled in this checkpoint, and you do not touch any of it.

## What is assessed, and by whom

| Assessed | By |
|---|---|
| The pull request changes only `submission.yaml` | Automated, in this repository (`poe submission`, inside `poe verify`, and `test_submission_change_stays_within_the_permitted_diff`) |
| `submission.yaml` still records `answers: {}` | Automated (`poe answers`, repeated by `poe submission` and `poe verify`) |
| The inherited Task 1 to 6 checkpoint still passes as supplied | Automated (`poe verify`: the running platform, the end-to-end workflow and the carried Task 4.2, 4.3 and 4.4 tests); the hosted `security-gate` job runs the settled Task 5 gate on the pull request |
| The evidence index, the three-part structure, the labels and the links | Your instructor, at the Task 7 Instructor Review |
| Your explanation of the decisions, their limits and the accepted risk | Your instructor, at the live Project Defense |

This Task has no held-out check and no protected answer key. Sprint 4's one held-out scenario
belonged to Task 4.6 and left with it; nothing in this repository is graded privately. What
the automated checks do not read (the index, the structure, the reasoning and the limits) is
read by a human.

## What is already supplied

| Supplied | Where | Note |
|---|---|---|
| The settled Task 1 threat model | `docs/student/threat-model.md` | a completion/reference version; cite your own at Task 1's accepted commit |
| The settled Task 2 to 5 controls and their configuration | `config/auth.yaml`, `src/api/`, `src/worker/`, `src/common/`, `security/gate.yaml`, `.gitleaks.toml` | the reference completions, supplied and settled; not this Task's editable surface |
| The carried Task 2 to 4 tests | `tests/student/test_exception_access.py`, `tests/student/test_output_guardrail.py`, `tests/student/test_audit.py`, `tests/student/test_redaction.py` | reference completions; `poe student-tests` and `poe verify` run them as the checks on the controls you inherited |
| The Task 6 corrections, risk register and decision record | `docs/student/governance-corrections.md`, `docs/governance/risk-register.yaml`, `docs/governance/decision-record.md` | completion/reference versions, supplied for orientation; not your evidence: cite your own at Task 6's accepted commit |
| The Task 6 governance material | `docs/governance/ai-governance-analysis.md`, `owners.md`, `concerns.md`, `decision-policy.md` | supplied as in Task 6; the owner roles your accepted risk names are in `owners.md` |
| The security material and fidelity notes | `docs/security/`, `docs/fidelity/TokenIssuer.md`, `docs/fidelity/SecretProvider.md` | the limits you bring forward in the second part; cite them, do not rewrite them |
| The earlier Tasks' tools | `poe auth-checks`, `poe audit-trail`, `poe pii-scan`, `poe provider-auth-check`, `poe secret-check-old`, `poe attack-dev`, `poe security-scan` and the rest in `README.md` | still runnable; not this Task's exercise. Recover missing evidence through the original Task, never by rerunning its exercise here |

None of these is this Task's editable surface. The public check compares the diff from your
merge base with the one permitted file below and reports a change to any of them as a
boundary violation.

## What belongs in the pull request description

The pull request description is where this Task's work lives. It is read by your instructor at
the Instructor Review; no automated check in this repository reads it. It carries:

- **Three named parts**, above the index, named after the three Project Defense questions in
  the same order, each with a time slice, the slices summing to 10 minutes. Under each part,
  the index entries you show on screen (a diff, a check log, a command's closing output, a
  check-run page, a section of a document, never a slide) and what you say about them.
- **Six entries**, one for each of Tasks 1 through 6: the merged pull request link, the
  accepted commit, its required results on the platform, the evidence that Task's lesson asked
  you to attach, and one or two sentences in your own words: what you chose, what the supplied
  starting state did instead, and why your choice suits Coldline.
- **The stated limits**, in the second part: what the development issuer cannot establish about
  a managed identity provider, what LocalStack Secrets Manager cannot establish about AWS
  Secrets Manager, IAM or KMS, and what your tested attack cases cannot establish about the
  ones you did not test. Where your register or your decision record at Task 6's accepted
  commit already states a limit, cite it.

Every run-output excerpt names the command or check that produced it and when it ran. Every
authored document or answer excerpt links to your record at its accepted commit. Supplied
fixtures and reference material are labeled as supplied, apart from your own observations and
decisions. A Task with no link, or with a missing, skipped or errored required result, is not
assembled; resolve it through that Task's own **Resubmit** route first.

## Commands

```shell
poe answers       # the answer sheet's format only: answers: {}
poe submission    # the format plus the permitted-files boundary: only submission.yaml changed
poe verify        # the full public path: both checks above, then the stack and the checks on
                  # the controls you inherited
```

`poe answers` and `poe submission` are static and need no stack. `poe verify` starts the stack
itself and ingests the supplied corpus. Nothing in any of them grades the evidence index or the
defense. A failure in `poe answers` or `poe submission` means the answer sheet is no longer
empty or the diff reached outside `submission.yaml`. If both pass and a later step of
`poe verify` fails, the checkpoint needs attention, not your submission: keep the result as it
is and contact course support.

## Check-list rows and the checks that read them

| Check-list row | Check |
|---|---|
| This Task's pull request description links the merged pull request and accepted commit for each of Tasks 1 to 6 | Instructor-reviewed (the evidence index), at the Task 7 Instructor Review |
| The description groups the evidence into three parts named after the Project Defense questions, with time slices summing to 10 minutes | Instructor-reviewed (the defense structure), at the Task 7 Instructor Review |
| Every linked Task shows passing results for its required platform checks at its accepted commit | Instructor-reviewed (the evidence index): your instructor reads each result on the platform; no check in this repository can read another Task's platform result |
| Task 5's assessed pull request shows that its last `security-gate` run before merge passed | Instructor-reviewed (the evidence index) |
| Each run-output excerpt identifies its command or check and when it ran | Instructor-reviewed (the evidence index) |
| Each authored document or answer excerpt links to your record at its accepted commit | Instructor-reviewed (the evidence index) |
| Supplied fixtures and reference material are labeled apart from your observations and decisions | Instructor-reviewed (the evidence index) |
| `submission.yaml` still records `answers: {}` | `poe answers` (`tests/contract/submission_validation.py --format-only`), repeated by `poe submission` and `poe verify` |
| The pull request modifies only `submission.yaml` | `test_submission_change_stays_within_the_permitted_diff` in `tests/contract/test_authoring_contract.py`, and `poe submission` inside `poe verify` |
| After you submit Task 7 on the platform, its public check runs and passes for this submission | The platform records the public-check result for the submitted commit, which runs `poe verify`. The repository's hosted `verify` job is the same command and gives you a separate check before you submit |

The live Project Defense of at most 10 minutes is instructor-reviewed at the Project Defense;
your instructor records its outcome.

## What the checks verify

| Check | What it looks at |
|---|---|
| `tests/contract/submission_validation.py` (`poe answers`, `poe submission`) | `submission.yaml` is one plain YAML mapping (no duplicate keys, aliases, anchors, merge keys or non-JSON tags) with a required, empty `answers` and nothing beside it; a comment above the mapping is not part of it. With `poe submission`, the diff from the merge base with `main` touches only `submission.yaml`, with no directory prefix exempted |
| `test_submission_change_stays_within_the_permitted_diff` | The same boundary asserted as a pytest case over the repository's own diff: every changed path is `submission.yaml`, and any other path (a supplied Task 6 document, a test under `tests/student/`, a new file, an application, configuration, test or workflow file) fails it |
| `tests/security/integrity.py` (`poe integrity-record`, `poe integrity-check`) | SHA-256 digests of the answer sheet and every trusted file the checks rely on, recorded outside the repository when `poe verify` starts and compared when it ends |
| `poe smoke`, `poe e2e-tests`, `poe student-tests` inside `poe verify` | The settled platform you inherited: the running stack, the end-to-end workflow, and the carried Task 4.2 access tests, Task 4.3 guardrail and audit tests and Task 4.4 redaction tests over the supplied controls. They pass as shipped and assess the checkpoint, not your work |

## Student-editable paths

- `submission.yaml`

That is the whole list. The Task 6 corrections, register and decision record, the threat
model, the carried tests under `tests/student/`, the application code, the configuration,
`compose.yaml`, `pyproject.toml` and the workflows stay as supplied. If your branch needs a
change to commit, add one YAML comment above `answers: {}` with the date you prepared the
evidence index. Before you push, run `git status` and `git diff --stat`: if anything besides
`submission.yaml` changed, the public check reports the boundary violation rather than your
work.

## The defense

After the public check passes and your instructor has accepted the assembled pull request at
the Instructor Review, you deliver the Project Defense live, in at most 10 minutes, part by
part: state the decision, point at the diff or the output that shows it holds, and name its
limit. Have the six pull request pages, the platform results for each Task, and your own
records at their accepted commits open before the session, and share that screen. When the
local evidence cannot answer a question, say so and name the measurement or test that would.
Sprint 4 - Project 4 is complete once everything **Who checks what** lists is recorded,
including your Task 7 Instructor Review acceptance and the outcome of the Project Defense.
