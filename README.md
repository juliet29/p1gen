# p1gen

This repository accompanies the paper "AURA: Automated Universal floor plan Replication for Airflow and thermal analysis". It showcases a methodology for transforming SVGs drawn on images of floorplans into EnergyPlus models and running a sensitivity analysis. [`svg2plan`](https://github.com/juliet29/svg2plan) is used to transform SVGs into vectorized data, while [`plan2eplus`](https://github.com/juliet29/plan2eplus) transforms vectorized data into energy models. This repository shows how to generate multiple energy models, perform a sensitivity analysis, and generate figures.

## Source Files

In `src/p1gen`, the source files for executing this code are present.

`_01_readin/read.py` contains code that transforms vectorized data into `Rooms`, `Edges`, and `Details` that can be converted into EnergyPlus models.

`_02_generate/main.py` contains the code used to generate the cases for the sensitivity analysis. The `generate_experiments` function relies on the `make_experimental_campaign` decorator from `plan2eplus` to create cases with varying layouts, window dimension, constructions, and door operation schedules. When this script is run, cases with IDF files are written.

`_03_execute/run.py` runs an experimental campaign. This separation of concerns makes it possible change the parameters affecting a run even after the cases have been generated. For instance, the analysis period (the period of time over which the case is run) and the weather file can be changed independently of the rest of the IDF.

The remaining folders are used to generate plots: `geom/geom.py` creates the pressure floor plan visualizations, `time_period/plot.py` makes the plots that compare the statistical performance across cases, `sensitivity/plot.py` makes the sensitivity plots that compare temperature and airflow for different variables

## Static Files

In `static`, inputs and outputs needed for the analysis are stored.

The weather data used to run the case are in `_01_inputs/pa2024`.

The outcomes from generating vector data from SVGs using `svg2plan` are in `_02_plans/svg2plan_outputs_p1gen`.

The EnergyPlus models that correspond to the experimental campaign shown in the sensitivity analysis are in `03_models/20251116_summer_update_dv`.

Intermediate data used in generating plots can be found in `_04_temp`, while `_05_figures` contains figures.
