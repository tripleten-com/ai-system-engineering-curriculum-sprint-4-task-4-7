"""Coldline.

===================

File:              tests/contract/submission_validation.py
Component:         Contract tests — Submission Validation
Purpose:           Validate the Task 4.7 answer sheet (an empty `answers` mapping) and the
                    permitted path: the answer sheet alone.
Interacts With:    Published interfaces and repository boundaries, tests/security/repository.py
Sprint/Task:       Sprint 4 — Project 4 / Task 4.7
Concepts:          Compatibility, ownership, export safety
Tools:             Python 3.12, pytest

Two entrypoints share this module. ``poe answers`` runs it with ``--format-only`` and checks
the answer sheet alone: one plain YAML mapping whose ``answers`` is present and empty.
``poe submission`` (inside ``poe verify``) runs it in full, which adds the permitted-path
boundary: the diff from the merge base touches only ``submission.yaml``. Task 4.7's
checkpoint is settled. Everything Tasks 4.1 to 4.6 assessed ships supplied, the Task 4.6
corrections, register and decision record among it, so a change to any of those, or to any
application, configuration, test or workflow file, is a boundary violation. The evidence
index lives in the pull request description, which is not a file in this repository.
"""

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from tests.security import repository

# The one file a Task 4.7 pull request may change: the answer sheet the pull request
# carries alongside its evidence index. Task 4.6's three governance documents were that
# Task's editable surface and are supplied, settled, here.
ALLOWED_PATHS = frozenset({"submission.yaml"})
# Task 4.7 grants no directory prefix. An empty tuple is deliberate and correct:
# str.startswith(()) is always False, so nothing outside ALLOWED_PATHS is ever permitted.
ALLOWED_PREFIXES: tuple[str, ...] = ()


_JSON_YAML_TAGS = frozenset(
    {
        "tag:yaml.org,2002:map",
        "tag:yaml.org,2002:seq",
        "tag:yaml.org,2002:str",
        "tag:yaml.org,2002:null",
        "tag:yaml.org,2002:bool",
        "tag:yaml.org,2002:int",
        "tag:yaml.org,2002:float",
    }
)


class RestrictedYamlLoader(yaml.SafeLoader):  # type: ignore[misc]
    """Load the Task's small YAML profile without YAML-only conveniences."""

    def compose_node(self, parent: object, index: object) -> yaml.Node:
        """Compose one node, refusing an alias or an anchor where it appears."""
        # A prior anchor is already rejected below, but deny aliases directly too.
        if self.check_event(yaml.AliasEvent):
            event = self.get_event()
            raise yaml.composer.ComposerError(
                None,
                None,
                "YAML aliases are not permitted",
                event.start_mark,
            )
        event = self.peek_event()
        if getattr(event, "anchor", None) is not None:
            raise yaml.composer.ComposerError(
                None,
                None,
                "YAML anchors are not permitted",
                event.start_mark,
            )
        return super().compose_node(parent, index)

    def construct_object(self, node: yaml.Node, deep: bool = False) -> object:
        """Construct one value, refusing any tag outside the JSON-compatible set."""
        if node.tag not in _JSON_YAML_TAGS:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "non-JSON YAML tags are not permitted",
                node.start_mark,
            )
        return super().construct_object(node, deep=deep)

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[str, object]:
        """Construct one mapping with string keys, refusing merge keys and repeated keys."""
        mapping: dict[str, object] = {}
        for key_node, value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise yaml.constructor.ConstructorError(
                    None,
                    None,
                    "YAML merge keys are not permitted",
                    key_node.start_mark,
                )
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise yaml.constructor.ConstructorError(
                    None,
                    None,
                    "YAML mapping keys must be strings",
                    key_node.start_mark,
                )
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    None,
                    None,
                    f"duplicate YAML key: {key}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


class SubmissionError(ValueError):
    """Report one actionable public-verification failure."""


def main(
    root: Path | None = None,
    *,
    changed_paths: list[str] | None = None,
    format_only: bool = False,
) -> int:
    """Validate the answer sheet, and unless ``format_only``, the permitted-path boundary.

    The optional arguments keep this entrypoint testable without changing the
    process working directory or creating a temporary Git repository.
    """
    task_root = Path.cwd() if root is None else root
    try:
        validate_submission(
            task_root / "submission.yaml",
            task_root / "docs/contracts/submission.schema.json",
            # No sample comparison for this Task. The accepted answer sheet IS the empty
            # mapping the sample shows, so a copy check would reject every correct sheet.
            sample_path=None,
            task_root=task_root,
        )
        if not format_only:
            changed = _changed_paths(task_root) if changed_paths is None else changed_paths
            validate_changed_paths(changed)
    except (SubmissionError, RuntimeError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1
    if format_only:
        print("Task 4.7 answer format check passed.")
    else:
        print("Task 4.7 answer and permitted-path verification passed.")
    return 0


def validate_submission(
    submission_path: Path,
    schema_path: Path,
    *,
    sample_path: Path | None = None,
    task_root: Path | None = None,
) -> None:
    """Validate YAML shape, the empty mapping, the schema, and sample-copy behavior.

    ``task_root`` names the repository that owns the published contracts. It defaults
    to the answer sheet's own directory, which is correct for a student checkout. A
    curriculum-owned evaluator validating a sheet stored elsewhere passes the trusted
    Task root explicitly.
    """
    submission = _load_one_document(submission_path)
    answers = submission.get("answers") if isinstance(submission, dict) else None
    if not isinstance(answers, dict):
        raise SubmissionError("answers must be one mapping")

    # Task 4.7 has no useful direct answer: the evidence is the pull request record from
    # Tasks 1 through 6, the index assembled into this Task's own pull request description,
    # and the live defense of it, none of which a recorded claim could stand in for. The
    # mapping is therefore required to be present and empty, which is a real check: it
    # rejects an invented status field, or a Task 6 answer recorded again, as firmly as a
    # missing mapping.
    if answers:
        raise SubmissionError(
            "answers must stay an empty mapping for this Task; the pull request record from "
            "Tasks 1 to 6 and your defense of it are the evidence, not a recorded claim "
            f"(found: {', '.join(sorted(answers))})"
        )

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(submission), key=lambda error: list(error.path)
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "submission"
        raise SubmissionError(f"{location}: {error.message}")

    if sample_path is not None and submission == _load_one_document(sample_path):
        raise SubmissionError("submission must not copy the fictional sample answers")


def validate_changed_paths(paths: list[str], permitted: frozenset[str] = ALLOWED_PATHS) -> None:
    """Reject changed paths outside the permitted surfaces."""
    normalized = {PurePosixPath(path.replace("\\", "/")).as_posix() for path in paths}
    protected = sorted(
        path for path in normalized - permitted if not path.startswith(ALLOWED_PREFIXES)
    )
    if protected:
        raise SubmissionError(f"protected path changed: {', '.join(protected)}")


def _changed_paths(root: Path) -> list[str]:
    """Return changes since the commit this checkout branched from."""
    try:
        return repository.changed_paths(root)
    except repository.RepositoryError as exc:
        raise RuntimeError("Git history is unavailable for protected-path validation") from exc


def _load_one_document(path: Path) -> dict[str, Any]:
    """Load exactly one plain JSON-compatible YAML mapping.

    A file that is not UTF-8 is reported the same way as one that is not the
    restricted YAML profile: as a public verification failure, not a traceback.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SubmissionError(
            f"{path.name} is missing; restore it from the starting checkpoint"
        ) from exc
    except UnicodeDecodeError as exc:
        raise SubmissionError(f"{path.name} must contain UTF-8 restricted YAML") from exc
    try:
        documents = list(yaml.load_all(text, Loader=RestrictedYamlLoader))
    except yaml.YAMLError as exc:
        raise SubmissionError(f"{path.name} must contain UTF-8 restricted YAML") from exc
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise SubmissionError(f"{path.name} must contain exactly one YAML mapping")
    return documents[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate the Task 4.7 submission.")
    parser.add_argument(
        "--format-only",
        action="store_true",
        help="check the answer sheet's format only (what `poe answers` runs)",
    )
    arguments = parser.parse_args()
    raise SystemExit(main(format_only=arguments.format_only))
