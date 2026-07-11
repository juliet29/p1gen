"""Read/write the campaign manifest — the one file downstream reads instead of
globbing the campaign directory and reparsing every `metadata.toml`.
"""

from __future__ import annotations

import json
from pathlib import Path

from p1gen.campaign.spec import ExperimentSpec

MANIFEST_NAME = "campaign_manifest.json"


def write_manifest(
    campaign_dir: Path,
    campaign_name: str,
    specs: list[ExperimentSpec],
) -> Path:
    path = campaign_dir / MANIFEST_NAME
    payload = {
        "campaign_name": campaign_name,
        "specs": [s.to_dict() for s in specs],
    }
    path.write_text(json.dumps(payload, indent=2))
    return path


def read_manifest(campaign_dir: Path) -> list[ExperimentSpec]:
    path = campaign_dir / MANIFEST_NAME
    payload = json.loads(path.read_text())
    return [ExperimentSpec.from_dict(d) for d in payload["specs"]]
