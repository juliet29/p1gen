from replan2eplus.ops.afn.ezobject import AirflowNetwork
from typing import NamedTuple
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from p1gen._03_execute.assemble import ComparisonData, assemble_default_data
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.paths import CampaignNameOptions, get_ezcase_for_path
import polars as pl
from texttable import Texttable
import latextable


class Column(NamedTuple):
    Zones: int
    Windows: int
    Doors: int
    Airboundaries: int

    @property
    def keys(self):
        return list(self._asdict().keys())


class ObjectsData(NamedTuple):
    case_name: str
    zones: list[Zone]
    subsurfaces: list[Subsurface]
    afn: AirflowNetwork

    @property
    def num_zones(self):
        return len(self.zones)

    @property
    def num_zones_in_afn(self):
        return len(self.afn.zones)

    @property
    def num_doors(self):
        res = list(filter(lambda x: x.is_door, self.subsurfaces))
        return len(res)

    @property
    def num_windows(self):
        res = list(filter(lambda x: x.is_window, self.subsurfaces))
        return len(res)

    @property
    def num_res_in_afn(self):
        res = list(filter(lambda x: x.is_door, self.afn.subsurfaces))
        return len(res)

    @property
    def num_windows_in_afn(self):
        res = list(filter(lambda x: x.is_window, self.afn.subsurfaces))
        return len(res)

    @property
    def num_airboundaries(self):
        res = self.afn.airboundaries
        return len(res)

    @property
    def summary(self):
        original = Column(
            self.num_zones, self.num_windows, self.num_doors, self.num_airboundaries
        )

        afn = Column(
            self.num_zones_in_afn,
            self.num_windows_in_afn,
            self.num_windows_in_afn,
            self.num_airboundaries,
        )
        return pl.DataFrame(
            {
                "Keys": original.keys,
                f"Original_{self.case_name}": original,
                f"AFN_{self.case_name}": afn,
            }
        )


def get_basic_data(campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN):
    def get(exp: ComparisonData):
        objs = get_ezcase_for_path(exp.path).objects
        return ObjectsData(
            exp.case_name, objs.zones, objs.subsurfaces, objs.airflow_network
        )

    comparison_data = assemble_default_data(campaign_name)
    return [get(i) for i in comparison_data]


def prep_table():
    A, B, C = [i.summary for i in get_basic_data()]
    df = A.join(B, on="Keys").join(C, on="Keys")
    rows = [row for row in df.iter_rows()]
    headers = df.columns
    t1 = Texttable()
    t1.set_cols_align(["l"] * len(headers))
    t1.add_row(headers)
    t1.add_rows(rows)

    return df, t1


def prep_table_mc():
    A, B, C = [i.summary for i in get_basic_data()]
    df = A.join(B, on="Keys").join(C, on="Keys")
    rows = [list(row) for row in df.iter_rows()]
    top_row = [["Key"] + ["Original", "AFN"] * 3]
    total_rows = top_row + rows

    multi_column_header = [("", 1), ("A", 2), ("B", 2), ("C", 2)]
    t1 = latextable.draw_latex(
        total_rows, use_booktabs=True, multicolumn_header=multi_column_header
    )
    return df, t1


def example_10():
    # Example 10 - Multicolumn header
    rows = [
        ["R", "A", "B", "C", "D"],
        ["1", "a1", "b1", "c1", "d1"],
        ["2", "a2", "b2", "c2", "d2"],
        ["3", "a3", "b3", "c3", "d3"],
    ]
    multicolumn_header = [("", 1), ("AB", 2), ("CD", 2)]
    print("\n-- Example 10: Multicolumn header --")
    print("Latextable Output:")
    print(
        latextable.draw_latex(
            rows, use_booktabs=True, multicolumn_header=multicolumn_header
        )
    )


if __name__ == "__main__":

    res = prep_table_mc()
    _, t1 = res
    print(t1)
