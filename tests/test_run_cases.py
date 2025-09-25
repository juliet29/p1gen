import pytest
from p1gen.paths import (
    PlanPaths,
    SVG2PLANS,
    REPLAN2EPLUS_TESTS,
    static_paths,
    PATH_TO_IDD,
)
from p1gen.main import prep_case
from typing import Literal
from utils4plans.io import get_or_make_folder_path
from replan2eplus.visuals.examples import plot_zones_and_connections


def run_cases():
    exps = ["case_bol_5", "case_red_b1", "case_amb_b1"]
    for exp in exps:
        plan_path = PlanPaths(SVG2PLANS / exp)
        out_path = get_or_make_folder_path(REPLAN2EPLUS_TESTS, exp)
        case = prep_case(plan_path, output_path=out_path)


def plot_case_results(exp: Literal["case_bol_5", "case_red_b1", "case_amb_b1"]):
    # plan_path = PlanPaths(SVG2PLANS / exp)
    # case = prep_case(plan_path, output_path=static_paths.models / exp)
    dp = plot_zones_and_connections(
        path_to_idd=PATH_TO_IDD, path=REPLAN2EPLUS_TESTS / exp
    )
    dp.show()


@pytest.mark.parametrize("exp", ["case_bol_5", "case_red_b1", "case_amb_b1"])
def test_run_case(exp, tmp_path):
    plan = PlanPaths(SVG2PLANS / exp)
    prep_case(plan, output_path=tmp_path)
    assert 1


if __name__ == "__main__":
    plot_case_results("case_red_b1")
