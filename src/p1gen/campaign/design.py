"""The experimental design: variables, options, and the enumeration of specs.

Ported from plan2eplus `decorator2.py` (the pure, generic parts only — no
side effects, no build loop). The one behavioural change: experiments get a
*stable slug id* derived from (case, modification) instead of the positional
`enumerate(ix)` folder number, which shifted whenever the design was reordered.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p1gen.campaign.spec import ExperimentSpec


def slugify(text: str) -> str:
    """Deterministic, human-readable id fragment. "-30%" -> "minus30pct"."""
    replacements = {"%": "pct", "+": "plus", "-": "minus", " ": "_", "/": "_"}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return "".join(c for c in text.lower() if c.isalnum() or c == "_")


class Option:
    def __init__(self, name: str, IS_DEFAULT: bool = False) -> None:
        self.name = name
        self.IS_DEFAULT = IS_DEFAULT

    @property
    def toml(self) -> dict:
        d = {"name": self.name}
        if self.IS_DEFAULT:
            d["DEFAULT"] = self.IS_DEFAULT
        return d


@dataclass
class Variable:
    name: str
    options: list[Option]

    def __post_init__(self) -> None:
        defaults = [o for o in self.options if o.IS_DEFAULT]
        assert len(defaults) == 1, f"{self.name}: need exactly one default option"
        names = [o.name for o in self.options]
        assert len(set(names)) == len(names), f"{self.name}: option names not unique"

    @property
    def default_option(self) -> str:
        return next(o.name for o in self.options if o.IS_DEFAULT)

    @property
    def non_default_options(self) -> list[str]:
        return [o.name for o in self.options if not o.IS_DEFAULT]

    @property
    def toml(self) -> dict:
        return {"name": self.name, "options": [o.toml for o in self.options]}


@dataclass
class DefinitionDict:
    case_names: list[str]          # e.g. ["A", "B", "C"]
    case_variables: list[str]      # e.g. ["rooms", "edge_groups", "airboundary_edges"]
    modifications: list[Variable]

    @property
    def toml(self) -> dict:
        return {
            "case_names": self.case_names,
            "case_variables": self.case_variables,
            "modifications": [v.toml for v in self.modifications],
        }


def _spec_id(case_name: str, modification: tuple[str, str] | None) -> str:
    if modification is None:
        return f"{case_name}__default"
    var, opt = modification
    return f"{case_name}__{slugify(var)}__{slugify(opt)}"


def enumerate_specs(defn: DefinitionDict) -> list[ExperimentSpec]:
    """Baseline cases (all defaults) + one-at-a-time modifications.

    Mirrors `DefinitionDict.experiments` from the old decorator, emitting
    typed `ExperimentSpec`s with stable ids. Ids are unique because each
    (case, variable, non-default-option) triple is unique and baselines are
    one-per-case.
    """
    baseline = [
        ExperimentSpec(id=_spec_id(case, None), case_name=case, modification=None)
        for case in defn.case_names
    ]

    modified = [
        ExperimentSpec(
            id=_spec_id(case, (var.name, option)),
            case_name=case,
            modification=(var.name, option),
        )
        for var in defn.modifications
        for case, option in product(defn.case_names, var.non_default_options)
    ]

    return baseline + modified
