from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.visuals.calcs import domain_to_mpl_patch,  subsurface_connection
from typing import Any, NamedTuple
from p1gen.axtest import flow_colorbar, pressure_colorbar
from p1gen.geom_plot import get_afn_opening_names, organize_subsurfaces
from p1gen.utils import read_idf
from p1gen.paths import test_case
from p1gen.read_sql import create_collections_for_variable, get_sql_results
from p1gen.data_helpers import create_dataframe_for_case, DFC
from p1gen.volume import QOI, CalcQOI
import polars as pl 
from replan2eplus.ezobjects.subsurface import Subsurface

edge_color = "black"
alpha = 0.9

class GeomDataPair(NamedTuple):
    value: float
    geom: Any 

    @property
    def is_neg(self):
        return self.value < 0
    
    @property
    def abs_(self):
        return abs(self.value)
    

class DataPlot(BasePlot):
    def plot_zones_with_values(self, values:dict[str, float], edge_color=edge_color, alpha=alpha):
        assert len(values.keys()) == len(self.zones)
        bar, cmap, norm = pressure_colorbar(list(values.values()), self.axes)

        pairs = [GeomDataPair(
                    values[i.zone_name.upper()], 
                    domain_to_mpl_patch(i.domain)
                ) for i in self.zones]

        for pair in pairs:
            color = cmap(norm(pair.value))
            pair.geom.set(edgecolor=edge_color, alpha=alpha, facecolor=color, fill=True)
            self.axes.add_artist(pair.geom)
        
        # TODO can change in future -> maybe pass all values? 
        # bar = plt.colorbar()
        return self
    
    def plot_connections_with_values(self, values:dict[str, float], subsurfaces: list[Subsurface]):
        bar, cmap, norm = flow_colorbar([abs(i) for i in values.values()], self.axes)
        valid_subsurfaces = [i for i in subsurfaces if i.subsurface_name.upper() in values.keys()]
        pairs = [GeomDataPair(
            values[i.subsurface_name.upper()], 
            subsurface_connection(i, self.zones, self.cardinal_domain.cardinal)
            ) for i in valid_subsurfaces]
        
        for pair in pairs:
            width = norm(pair.abs_)*7
            color = cmap(norm(pair.abs_))
            pair.geom.set(linewidth=width, color=color)
            self.axes.add_artist(pair.geom)
        
        # maybe plot as greyed out if no flow? 
        # for ss in subsurfaces:
        #     line = subsurface_connection(ss, self.zones, self.cardinal_domain.cardinal)
        #     self.axes.add_artist(line)
    
        return self
    # get the subsurfaces with values in the dict.. 
    # lets do the width and color first.. 
    # then do the direction (maybe even not tn.. )
    
def prep_flow_data():
    case = read_idf(test_case)
    sql = get_sql_results(test_case)
    flow_data = (create_dataframe_for_case(sql, 
                [QOI.FLOW_12, QOI.FLOW_21], case)
                .with_columns(pl.col(DFC.DATETIMES).dt.time().alias(DFC.TIME))
                .filter(pl.col(DFC.TIME)==pl.time(12,0))
                .filter(pl.col(DFC.SPACE_NAMES).is_in(case.subsurface_names))
                .with_columns((pl.col(QOI.FLOW_12) - pl.col(QOI.FLOW_21)).alias(CalcQOI.NET_FLOW))
                .select([DFC.SPACE_NAMES,CalcQOI.NET_FLOW]).to_dicts()
                )
    flow_dict = {i[DFC.SPACE_NAMES]: i[CalcQOI.NET_FLOW] for i  in flow_data}
    # non_zero_zones = [i[DFC.SPACE_NAMES] for i in flow_data]
    
    # for z in case.subsurface_names:
    #     subsurface = z.upper()
    #     if subsurface not in flow_dict.keys():
    #         flow_dict[subsurface] = 0
    
    print(flow_dict)
    return flow_dict


def prep_pressure_data():
    case = read_idf(test_case)
    sql = get_sql_results(test_case)
    pressure_data = (create_dataframe_for_case(sql, 
                [QOI.NODE_PRESSURE], case)
                .with_columns(pl.col(DFC.DATETIMES).dt.time().alias(DFC.TIME))
                .filter(pl.col(DFC.TIME)==pl.time(12,0)).select([DFC.SPACE_NAMES, QOI.NODE_PRESSURE]).to_dicts()
                )
    
    pressure_dict = {i[DFC.SPACE_NAMES]: i[QOI.NODE_PRESSURE] for i  in pressure_data}
    # non_zero_zones = [i[DFC.SPACE_NAMES] for i in pressure_data]

    for z in case.zone_names:
        zone = z.upper()
        if zone not in pressure_dict.keys():
            pressure_dict[zone] = 0
    
    return pressure_dict


def plot_data():
    case = read_idf(test_case)
    pressure_data = prep_pressure_data()
    flow_data = prep_flow_data()
    bp = (
        DataPlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones_with_values(pressure_data)
        .plot_connections_with_values(flow_data, case.subsurfaces))
    
    assert case.idf
    afn_openings = get_afn_opening_names(case.idf.idf)
    surface_lines = organize_subsurfaces(case.subsurfaces, case.surfaces, afn_openings)

    bp.plot_cardinal() #.plot_connections(surface_lines.afn_surfaces)

    for line in surface_lines.all_lines:
            bp.axes.add_artist(line)

    bp.axes.legend()
    bp.show()


if __name__ == "__main__":
    plot_data()
    #prep_flow_data()
