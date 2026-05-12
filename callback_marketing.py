"""FR-297: Marketing campaign questionnaire — graph-specific tool nodes.

Schema-driven field extraction and gap detection for marketing
questionnaire (3 fields: name, organization, quote).
Shared handlers (message management, corrections, etc.) live in
graphs._common.handlers (NC-228).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent / "schema.yaml"


def load_schema(state: dict[str, Any]) -> dict[str, Any]:
    """Load schema.yaml. Graph runs once — no re-entry guard needed."""
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    return {"schema": schema}


def normalize_extracted(state: dict[str, Any]) -> dict[str, Any]:
    """Coerce non-dict race output to {} at the boundary."""
    extracted = state.get("extracted")
    if isinstance(extracted, dict):
        return {}
    if extracted is not None:
        logger.warning(
            "normalize_extracted: coercing non-dict %s to {}",
            type(extracted).__name__,
        )
    return {"extracted": {}}


def detect_gaps(state: dict[str, Any]) -> dict[str, Any]:
    """Compute missing required fields. Outputs {gaps, has_gaps}."""
    extracted_raw = state.get("extracted")
    if isinstance(extracted_raw, dict):
        extracted = extracted_raw
    else:
        if extracted_raw is not None:
            logger.warning(
                "detect_gaps: extracted has unexpected type %s",
                type(extracted_raw).__name__,
            )
        extracted = {}
    schema = state.get("schema", {})
    fields = schema.get("fields", [])

    required_ids = [f["id"] for f in fields if f.get("required", False)]
    gaps = [fid for fid in required_ids if not extracted.get(fid)]

    logger.info("detect_gaps: gaps=%s extracted=%s", gaps, extracted)

    return {"gaps": gaps, "has_gaps": bool(gaps)}
