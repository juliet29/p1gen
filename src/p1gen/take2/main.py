from p1gen.take2.interfaces import Plan
from p1gen.paths import test_plan_paths
from pydantic import ValidationError


def read_plan():
    json_data = test_plan_paths.plan[0] # TODO STOP DOUBLE NESTING PLAN.JSON IN SVG TO PLAN!
    try:
        plan_data = Plan.model_validate({"rooms": json_data})
    except ValidationError as e:
        raise Exception(f"Plan at {test_plan_paths.path_to_case} has invalid data: {e}")

    print(plan_data)
    return plan_data.replan2eplus_rooms



if __name__ == "__main__":
    read_plan()
