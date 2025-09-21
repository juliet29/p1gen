import pytest
from p1gen.paths import PlanPaths, SVG2PLANS
from p1gen.take2.main import prep_case


@pytest.mark.parametrize("case", ["case_bol_5", "case_red_b1", "case_amb_b1"])
def test_run_case(case, tmp_path):
    plan = PlanPaths(SVG2PLANS / case)
    prep_case(plan, output_path=tmp_path)
    assert 1
