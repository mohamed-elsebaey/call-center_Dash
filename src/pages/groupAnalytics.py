import dash
from dash import html, dash_table, dcc
from dash_iconify import DashIconify

import plotly.graph_objects as go
import plotly.express as px

dash.register_page(
    __name__, path="/GroupAnalytics", title="Group Analytics", name="Group Analytics"
)

data = [
    {
        "GroupName": "Customer Success",
        "Total Inbound Calls": 848,
        "Answered %": "71.11 %",
    },
    {
        "GroupName": "Customer Support",
        "Total Inbound Calls": 500,
        "Answered %": "72.8 %",
    },
    {
        "GroupName": "Technical Support",
        "Total Inbound Calls": 349,
        "Answered %": "66.76 %",
    },
]

data2 = {
    "Name": ["Emilio Rangel", "Makenna Pugh", "Olivia Villa"],
    "Percentage": [41.1, 45.1, 13.8],
}

fig = px.pie(data_frame=data2, names="Name", values="Percentage", hole=0.0)
fig.update_traces(
    texttemplate="<b>%{label}</b><br>%{percent}",
    textposition="inside",
    insidetextorientation="horizontal",
)
# ++++

data3 = {
    "source": [
        "Technical Support",
        "Technical Support",
        "Technical Support",
        "Customer Success",
        "Customer Success",
        "Customer Support",
        "Customer Support",
    ],
    "target": [
        "Edward Lester",
        "Cruz Melendez",
        "Ezra Merritt",
        "Makena Pugh",
        "Emilio Rangel",
        "Elvis Conrad",
        "Gerardo Villegas",
    ],
    "value": [100, 150, 50, 200, 100, 120, 80],
}

fig2 = go.Figure(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Technical Support", "Customer Success", "Customer Support"]
            + [
                "Edward Lester",
                "Cruz Melendez",
                "Ezra Merritt",
                "Makena Pugh",
                "Emilio Rangel",
                "Elvis Conrad",
                "Gerardo Villegas",
            ],
            color=[
                "#003f5c",
                "#2f4b7c",
                "#665191",
                "#a05195",
                "#d45087",
                "#f95d6a",
                "#ff7c43",
                "#ffa600",
                "#003f5c",
            ],
        ),
        link=dict(
            source=[0, 0, 0, 1, 1, 2, 2],
            target=[3, 4, 5, 6, 7, 8, 9],
            value=data3["value"],
        ),
    )
)

layout = html.Div(
    [
        # ------------------------------------- Right Section -------------------------------------
        html.Div(
            [
                # ------------------------------------- Right (1) Section -------------------------------------
                html.Div(
                    [
                        html.H2("Inbound Calls by Group"),
                        dash_table.DataTable(
                            data=data,
                            columns=[
                                {"name": "GroupName", "id": "GroupName"},
                                {
                                    "name": "Total Inbound Calls",
                                    "id": "Total Inbound Calls",
                                },
                                {"name": "Answered %", "id": "Answered %"},
                            ],
                            style_header={
                                "backgroundColor": "lightblue",
                                "fontWeight": "bold",
                                "textAlign": "center",
                            },
                            style_data={"textAlign": "center"},
                        ),
                    ],
                    className="inbound-calls",
                ),
                # ------------------------------------- Right (2) Section -------------------------------------
                html.Div(
                    [
                        html.H2(
                            [
                                DashIconify(
                                    icon="material-symbols-light:connected-tv-outline",
                                    width=24,
                                    color="#094546",
                                ),
                                "Calls Answered by WorkGroup",
                            ]
                        ),
                        html.Div(
                            [
                                "Group",
                                dcc.Dropdown(
                                    options=[
                                        "Customer Success",
                                        "Customer Support",
                                        "Technical Support",
                                    ],
                                    value="Customer Success",
                                    id="internal-calls-network-option-dropdown",
                                    optionHeight=40,
                                    style={"width": "220px", "border-radius": "5px"},
                                ),
                            ],
                            className="calls-answered-dropdown",
                        ),
                        dcc.Graph(figure=fig),
                    ],
                    className="calls-answered",
                ),
            ],
            className="right-section",
        ),
        # ------------------------------------- Left Section -------------------------------------
        html.Div(
            [
                html.H2(
                    [
                        DashIconify(
                            icon="material-symbols-light:connected-tv-outline",
                            width=24,
                            color="#094546",
                        ),
                        "Answered Inbound Calls Flow",
                    ]
                ),
                dcc.Graph(figure=fig2),
            ],
            className="calls-flow-section",
        ),
    ],
    className="group-analytics-layout",
)
