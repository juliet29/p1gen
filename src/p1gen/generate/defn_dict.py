from replan2eplus.campaigns.decorator2 import DefinitionDict, Variable, Option

defn = DefinitionDict(
    case_names=["A", "B", "C"],
    case_variables=["rooms", "edge_groups"],
    modifications=[
        Variable(
            name="window_dimension",
            options=[
                Option("-30%"),
                Option("Default", IS_DEFAULT=True),
                Option("+30%"),
            ],
        ),
        # Variable(
        #     name="door_vent_schedule",
        #     options=[
        #         Option("Always Closed"),
        #         Option("Dynamic"),
        #         Option("Always Open", IS_DEFAULT=True),
        #     ],
        # ),
        Variable(
            name="construction_set",
            options=[
                Option("Light"),
                Option("Medium", IS_DEFAULT=True),
                Option("Heavy"),
            ],
        ),
    ],
)
