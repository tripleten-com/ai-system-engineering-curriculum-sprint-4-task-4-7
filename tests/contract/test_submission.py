"""Coldline.

===================

File:              tests/contract/test_submission.py
Component:         Contract tests — Test Submission
Purpose:           Tests for the public answer and path checks for this Task's submission.
Interacts With:    Published interfaces and repository boundaries
Sprint/Task:       Sprint 4 — Project 4 / Task 4.7
Concepts:          Compatibility, ownership, export safety
Tools:             Python 3.12, pytest
"""

import json
from pathlib import Path

import pytest
import yaml

from tests.contract.submission_validation import (
    ALLOWED_PATHS,
    SubmissionError,
    _load_one_document,
    main,
    validate_changed_paths,
    validate_submission,
)

ROOT = Path(__file__).parents[2]
SCHEMA = ROOT / "docs/contracts/submission.schema.json"
TEMPLATE = ROOT / "tests/fixtures/submission-template.yaml"


def _task_root(tmp_path: Path, submission_text: str) -> Path:
    """Stage a minimal Task root the public verifier can validate."""
    (tmp_path / "docs/contracts").mkdir(parents=True)
    (tmp_path / "submission.yaml").write_text(submission_text, encoding="utf-8")
    (tmp_path / "submission-sample.yaml").write_text(
        (ROOT / "submission-sample.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "docs/contracts/submission.schema.json").write_text(
        SCHEMA.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return tmp_path


def test_shipped_answer_sheet_passes_as_it_stands(tmp_path: Path) -> None:
    """Accept the shipped empty mapping, which is this Task's correct answer sheet."""
    root = _task_root(tmp_path, TEMPLATE.read_text(encoding="utf-8"))

    validate_submission(root / "submission.yaml", SCHEMA)


def test_a_dated_comment_above_the_mapping_is_accepted(tmp_path: Path) -> None:
    """The lesson's committable change, one dated comment, leaves the sheet correct."""
    text = "# Evidence index prepared 2026-01-15.\nanswers: {}\n"
    root = _task_root(tmp_path, text)

    validate_submission(root / "submission.yaml", SCHEMA)
    assert main(root, changed_paths=["submission.yaml"]) == 0


def test_public_entrypoint_accepts_the_shipped_sheet_and_the_sample(tmp_path: Path) -> None:
    """The public verifier must not require an answer this Task does not ask for.

    The sample shows the same empty mapping, so a sheet equal to it is correct here and
    there is no sample-copy rejection.
    """
    shipped = _task_root(tmp_path / "shipped", TEMPLATE.read_text(encoding="utf-8"))
    assert main(shipped, changed_paths=[], format_only=True) == 0
    assert main(shipped, changed_paths=["submission.yaml"]) == 0

    sample = _task_root(
        tmp_path / "sample", (ROOT / "submission-sample.yaml").read_text(encoding="utf-8")
    )
    assert main(sample, changed_paths=[], format_only=True) == 0


@pytest.mark.parametrize(
    "answers",
    [
        {"defense_delivered": True},
        {"evidence_index": "Task 1: https://example.invalid/pull/1"},
        {"instructor_approved": True},
        {"decision": "conditional_go"},
        {"accepted_risk": "R-80"},
    ],
    ids=["status", "pasted-index", "self-approval", "task-6-decision", "task-6-risk"],
)
def test_any_answer_field_is_rejected(tmp_path: Path, answers: dict[str, object]) -> None:
    """A status, a pasted index or a Task 6 answer recorded again is not evidence."""
    root = _task_root(tmp_path, yaml.safe_dump({"answers": answers}))

    with pytest.raises(SubmissionError, match="answers must stay an empty mapping"):
        validate_submission(root / "submission.yaml", SCHEMA)


def test_missing_answers_mapping_is_rejected(tmp_path: Path) -> None:
    """An empty mapping is required, not merely tolerated."""
    root = _task_root(tmp_path, "task: 4.7\n")

    with pytest.raises(SubmissionError, match="answers must be one mapping"):
        validate_submission(root / "submission.yaml", SCHEMA)


def test_a_key_beside_answers_is_rejected(tmp_path: Path) -> None:
    """The schema allows `answers` and nothing beside it."""
    root = _task_root(tmp_path, "answers: {}\nnotes: prepared on time\n")

    with pytest.raises(SubmissionError, match="Additional properties"):
        validate_submission(root / "submission.yaml", SCHEMA)


def test_public_entrypoint_reports_an_answer_field(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Catch a verifier entrypoint that skips the real submission contract."""
    root = _task_root(tmp_path, yaml.safe_dump({"answers": {"defense_delivered": True}}))

    assert main(root, changed_paths=[], format_only=True) == 1
    assert "answers must stay an empty mapping" in capsys.readouterr().err


def test_public_entrypoint_reports_a_protected_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A change to a supplied Task 6 document is named, not silently accepted."""
    root = _task_root(tmp_path, TEMPLATE.read_text(encoding="utf-8"))

    assert main(root, changed_paths=["docs/governance/decision-record.md"]) == 1
    assert "protected path changed: docs/governance/decision-record.md" in capsys.readouterr().err
    assert main(root, changed_paths=["docs/governance/decision-record.md"], format_only=True) == 0


def test_only_the_answer_sheet_is_permitted() -> None:
    """The path gate must accept `submission.yaml` alone and reject every other path.

    Task 4.6's three governance documents are supplied and settled here, and so is every
    test under `tests/student/`. The gate configuration, the workflows, the application
    code and the evidence directory are protected as earlier Tasks settled them. This
    Task's pull request may modify only `submission.yaml`.
    """
    assert frozenset({"submission.yaml"}) == ALLOWED_PATHS
    validate_changed_paths(["submission.yaml"])

    for protected in (
        "docs/governance/decision-record.md",
        "docs/governance/risk-register.yaml",
        "docs/student/governance-corrections.md",
        "docs/student/threat-model.md",
        "docs/student/evidence-index.md",
        "tests/student/test_exception_access.py",
        "tests/student/test_my_evidence.py",
        "tests/fixtures/attacks/development.json",
        "evidence/attack-dev.json",
        "security/gate.yaml",
        ".gitleaks.toml",
        ".github/workflows/task.yml",
        ".github/workflows/security.yml",
        "src/worker/config.py",
        "config/auth.yaml",
        "compose.yaml",
        "pyproject.toml",
        "uv.lock",
        "README.md",
        "submission-sample.yaml",
    ):
        with pytest.raises(SubmissionError, match="protected path changed"):
            validate_changed_paths([protected])


@pytest.mark.parametrize(
    "unsafe_text",
    [
        "answers: {value: first, value: second}\n",
        "answers: &answer {}\n",
        "answers: *missing\n",
        "answers: {<<: {value: fictional}}\n",
        "answers: {value: 2026-09-04}\n",
        "answers: {value: !custom fictional}\n",
        "answers: {1: fictional}\n",
    ],
    ids=["duplicate-key", "anchor", "alias", "merge-key", "date", "custom-tag", "non-string-key"],
)
def test_non_json_yaml_constructs_are_rejected(tmp_path: Path, unsafe_text: str) -> None:
    """Reject restricted syntax before schema validation can mask a parser defect."""
    submission = tmp_path / "submission.yaml"
    submission.write_text(unsafe_text, encoding="utf-8")

    with pytest.raises(SubmissionError, match="restricted YAML"):
        _load_one_document(submission)


def test_multiple_yaml_documents_are_rejected(tmp_path: Path) -> None:
    """A second document cannot supply or replace the answer mapping."""
    submission = tmp_path / "submission.yaml"
    submission.write_text("answers: {}\n---\nanswers: {}\n", encoding="utf-8")

    with pytest.raises(SubmissionError, match="exactly one YAML mapping"):
        _load_one_document(submission)


def test_a_sheet_that_is_not_utf_8_is_a_submission_error(tmp_path: Path) -> None:
    """A sheet saved in another encoding gets the public error, not a Python traceback."""
    submission = tmp_path / "submission.yaml"
    submission.write_bytes("answers: {}\n".encode("utf-16"))

    with pytest.raises(SubmissionError, match="restricted YAML"):
        _load_one_document(submission)


def test_the_schema_requires_one_empty_answers_mapping() -> None:
    """The schema names one required `answers` mapping that admits no property."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert schema["required"] == ["answers"]
    assert schema["additionalProperties"] is False
    answers = schema["properties"]["answers"]
    assert answers["type"] == "object"
    assert answers["additionalProperties"] is False
    assert answers["maxProperties"] == 0
    assert "Task 4.7" in schema["title"]


def test_the_template_and_the_sample_record_the_empty_mapping() -> None:
    """The fixture, the sample and the shipped sheet all parse to `answers: {}`."""
    for relative in ("tests/fixtures/submission-template.yaml", "submission-sample.yaml"):
        assert yaml.safe_load((ROOT / relative).read_text(encoding="utf-8")) == {"answers": {}}
