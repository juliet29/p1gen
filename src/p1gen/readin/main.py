# from replan2eplus.ezcase.ez import EZ
# from replan2eplus.visuals.base.base_plot import BasePlot

# from p1gen.readin.read import  read_plan
# from p1gen.paths import (
#     PlanPaths,
#     path_to_test_plan, DynamicPaths
# )
# from replan2eplus.ex.make import make_base_plot


# # TODO: need to update this replan2eplus for the IndexPair update to work..


# # TODO use replan2eplus to plot base case..
# # def plot_base_case(case: EZ):
# #     bp = (
# #         BasePlot(case.zones, cardinal_expansion_factor=1.4)
# #         .plot_zones()
# #         .plot_zone_names()
# #         .plot_cardinal_names()
# #         .plot_subsurfaces_and_surfaces(
# #             case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
# #         )
# #         .plot_connections(
# #             case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
# #         )
# #     )
# #     bp.show()


# def prep_case(path_to_plan: PlanPaths, output_path=THROWAWAY_PATH):
#     rooms = read_plan(path_to_plan)
#     airboundary_edges, subsurface_details = prep_subsurface_inputs(path_to_plan)

#     case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
#     case.initialize_idf()
#     case.add_zones(rooms)
#     case.add_airboundaries(airboundary_edges)
#     case.add_subsurfaces(subsurface_details)

#     case.add_constructions_from_other_idf(
#         [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
#         material_idfs,
#         SAMPLE_CONSTRUCTION_SET,
#     )
#     case.add_airflownetwork()
#     case.idf.add_output_variables(default_variables)

#     case.save_and_run_case(output_path)

#     return case


# if __name__ == "__main__":
#     prep_case(path_to_test_plan)
#     # read_details()
#     # prep_subsurface_inputs()
