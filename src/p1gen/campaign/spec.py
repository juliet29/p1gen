"""Typed, serializable descriptions of a single experiment.

These are the values that flow through the pipeline DAG. Nothing here imports
`p1gen.*` or `plan2eplus.*` so the module can be lifted back into plan2eplus
untouched.

`ExperimentSpec` says *what* to build (case + at most one modification).
`ExperimentResult` records *what was built/run* while carrying the original
spec forward, so downstream code never reconstructs the design from toml.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

# A single design modification: (variable_name, option_name).
# e.g. ("window_dimension", "-30%"). `None` == baseline (all defaults).
Modification = tuple[str, str] | None


@dataclass(frozen=True)
class ExperimentSpec:
    """One point in the experimental design. Hashable → safe as a Redun task arg."""

    id: str
    case_name: str
    modification: Modification = None

    @property
    def is_baseline(self) -> bool:
        return self.modification is None

    @property
    def category(self) -> str:
        """Modification variable name, or "Default" for a baseline."""
        return self.modification[0] if self.modification else "Default"

    @property
    def option(self) -> str:
        """Chosen option, or "Default" for a baseline."""
        return self.modification[1] if self.modification else "Default"

    # --- serialization -----------------------------------------------------

    def to_dict(self) -> dict:
        """Clean JSON-friendly form used by the campaign manifest."""
        return {
            "id": self.id,
            "case_name": self.case_name,
            "modification": list(self.modification) if self.modification else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ExperimentSpec":
        mod = d.get("modification")
        return cls(
            id=d["id"],
            case_name=d["case_name"],
            modification=(mod[0], mod[1]) if mod else None,
        )

    def to_metadata(self) -> dict:
        """Back-compat shape matching the old decorator's `metadata.toml`
        (`ExperimentDef.toml`), so existing readers keep working during the
        migration. This file is now an *artifact*, not the source of truth."""
        return {
            "case": self.case_name,
            "modifications": {self.modification[0]: self.modification[1]}
            if self.modification
            else "",
        }


@dataclass(frozen=True)
class ExperimentResult:
    """A built (and possibly run) experiment. Carries its spec forward.

    Paths are kept thin on purpose: we pass locations across task boundaries,
    never the heavy `EZ` / xarray objects, so the Redun cache stays small.
    """

    spec: ExperimentSpec
    out_path: Path
    idf_path: Path
    sql_path: Path | None = None

    @property
    def has_run(self) -> bool:
        return self.sql_path is not None

    def with_sql(self, sql_path: Path) -> "ExperimentResult":
        return replace(self, sql_path=sql_path)
