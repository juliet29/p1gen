from replan2eplus.campaigns.decorator2 import DefinitionDict, Variable, Option

defn = DefinitionDict(
    case_names=["A", "B", "C"],
    case_variables=["path_to_rooms", "path_to_edges"],
    modifications=[
        Variable(
            name="window_dim",
            options=[
                Option("-50%"),
                Option("Default", IS_DEFAULT=True),
                Option("+50%"),
            ],
        ),
        Variable(
            name="door_vent_schedule",
            options=[
                Option("Always Closed"),
                Option("Dynamic"),
                Option("Always Open", IS_DEFAULT=True),
            ],
        ),
        Variable(
            name="construction",
            options=[
                Option("Light"),
                Option("Medium", IS_DEFAULT=True),
                Option("Heavy"),
            ],
        ),
    ],
)
