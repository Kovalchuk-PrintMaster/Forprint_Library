from __future__ import annotations

import copy
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.coordination.validate_completion_packet import (
    CompletionPacketValidationError,
    validate_packet,
)

ROOT = Path(__file__).resolve().parents[2]
PACKET = (
    ROOT
    / "coordination"
    / "completion_packets"
    / "records"
    / "2026-07-29__forprint_library__calculator_input_contract_v0_1_completion.yaml"
)


def _packet_data() -> dict[str, Any]:
    loaded = yaml.safe_load(PACKET.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_packet(tmp_path: Path, data: dict[str, Any], name: str = "packet.yaml") -> Path:
    path = tmp_path / name
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _invalid_packet(tmp_path: Path, field: str, value: Any = None) -> Path:
    data = copy.deepcopy(_packet_data())
    if value is None:
        data.pop(field, None)
    else:
        data[field] = value
    return _write_packet(tmp_path, data)


def test_valid_library_completion_packet_passes() -> None:
    packet = validate_packet(PACKET, root=ROOT)

    assert packet["module_id"] == "forprint_library"
    assert packet["prompt_id"] == "forprint_library_calculator_input_contract_v0_1"
    assert packet["implementation_commit"] == "0b8cbce"
    assert packet["completion_commit"] == "89c4ec6"


@pytest.mark.parametrize("value", [None, ""])
def test_implementation_commit_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "implementation_commit", value)

    with pytest.raises(CompletionPacketValidationError, match="implementation_commit"):
        validate_packet(packet, root=ROOT)


@pytest.mark.parametrize("value", [None, ""])
def test_completion_commit_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "completion_commit", value)

    with pytest.raises(CompletionPacketValidationError, match="completion_commit"):
        validate_packet(packet, root=ROOT)


def test_wrong_prompt_id_fails(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "prompt_id", "wrong_prompt")

    with pytest.raises(CompletionPacketValidationError, match="prompt_id"):
        validate_packet(packet, root=ROOT)


def test_wrong_module_id_fails(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "module_id", "wrong_module")

    with pytest.raises(CompletionPacketValidationError, match="module_id"):
        validate_packet(packet, root=ROOT)


@pytest.mark.parametrize("value", [None, ""])
def test_report_path_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "report_path", value)

    with pytest.raises(CompletionPacketValidationError, match="report_path"):
        validate_packet(packet, root=ROOT)


def test_invalid_yaml_fails(tmp_path: Path) -> None:
    packet = tmp_path / "invalid.yaml"
    packet.write_text("module_id: [\n", encoding="utf-8")

    with pytest.raises(CompletionPacketValidationError, match="invalid YAML"):
        validate_packet(packet, root=ROOT)


def test_make_target_respects_packet_path(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "implementation_commit", "")

    result = subprocess.run(
        ["make", "completion-packet-validate", f"PACKET={packet}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "implementation_commit" in result.stderr
