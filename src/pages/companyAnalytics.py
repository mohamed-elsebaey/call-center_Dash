from dash import html, dcc, register_page, Output, Input, callback, State
from components.getData.GetData import ReadData

import plotly.express as px

from dash_iconify import DashIconify


# Convert seconds to hh:mm:ss
def convert_seconds(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Read data
df = ReadData()

# Convert DataTypes
# df["Date"] = pd.to_datetime(df["Date"])
# df["StartTime"] = pd.to_datetime(df["StartTime"])
# df["BillingDate"] = pd.to_datetime(df["BillingDate"])
df["TotalCallDuration"] = df["TotalCallDuration"].astype(float)
df["Charge"] = df["Charge"].astype(float)
df["Tax"] = df["Tax"].astype(float)
df["FromNumber"] = df["FromNumber"].astype(str)


# Page Data
register_page(
    __name__,
    path="/",
    name="Company Analytics",
    title="Company Analytics",
    description="Company Analytics Description",
    image="logo.png",
)

# -------------------------------------------------------------------------------------------------------------------
# Layout Start
# -------------------------------------------------------------------------------------------------------------------

layout = html.Div(
    [
        # Picker Range Section
        html.Div(
            [
                html.Div(
                    children=[
                        html.H2(
                            [
                                DashIconify(
                                    icon="lucide:phone-incoming",
                                    width=20,
                                    color="#094546",
                                ),
                                "Inbound Calls",
                            ],
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Total Calls"),
                                        html.P("0", id="inbound_calls"),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Total Time"),
                                        html.P(
                                            "00:00:00",
                                            id="inbound_time",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Average Time"),
                                        html.P(
                                            "00:00:00",
                                            id="inbound_time_avg",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Answered Calls"),
                                        html.P(
                                            "00.00 %",
                                            id="Inbound_answered",
                                        ),
                                    ]
                                ),
                            ],
                            className="data",
                        ),
                    ],
                    className="call-row",
                ),
                html.Div(
                    children=[
                        html.H2(
                            [
                                DashIconify(
                                    icon="lucide:phone-outgoing",
                                    width=20,
                                    color="#094546",
                                ),
                                "Outbound Calls",
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Total Calls"),
                                        html.P(
                                            "0",
                                            id="outbound_calls",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Total Time"),
                                        html.P(
                                            "00:00:00",
                                            id="outbound_time",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Average Time"),
                                        html.P(
                                            "00:00:00",
                                            id="outbound_time_avg",
                                        ),
                                    ]
                                ),
                            ],
                            className="data",
                        ),
                    ],
                    className="call-row",
                ),
                html.Div(
                    children=[
                        html.H2(
                            [
                                DashIconify(
                                    icon="carbon:phone-ip",
                                    width=25,
                                    color="#094546",
                                ),
                                "Internal Calls",
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Total Calls"),
                                        html.P(
                                            "0",
                                            id="internal_calls",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Total Time"),
                                        html.P(
                                            "00:00:00",
                                            id="internal_time",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Average Time"),
                                        html.P(
                                            "00:00:00",
                                            id="internal_time_avg",
                                        ),
                                    ]
                                ),
                            ],
                            className="data",
                        ),
                    ],
                    className="call-row",
                ),
            ],
            className="calls-row",
        ),
        # US Map Section
        html.Div(
            [
                dcc.Graph(id="us-map"),
                html.Div(
                    [
                        html.H2(
                            [
                                DashIconify(
                                    icon="game-icons:trophy-cup",
                                    width=25,
                                    color="white",
                                ),
                                "Top 3 Inbound Callers",
                            ],
                        ),
                        html.Hr(style={"margin-top": "15px", "margin-bottom": "15px"}),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        DashIconify(
                                            icon="fluent-emoji-high-contrast:1st-place-medal",
                                            width=20,
                                            color="gold",
                                        ),
                                        "Top Inbound Caller",
                                    ]
                                ),
                                html.Ul(
                                    [
                                        html.Li(["Name : ", html.P(id="top1-name")]),
                                        html.Li(
                                            ["Number : ", html.P(id="top1-number")]
                                        ),
                                        html.Li(
                                            [
                                                "Total Calls :",
                                                html.P(id="top1-totalCalls"),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                "Average Calls Length :",
                                                html.P(id="top1-averageCallsLength"),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Hr(style={"margin-top": "15px", "margin-bottom": "15px"}),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        DashIconify(
                                            icon="fluent-emoji-high-contrast:2nd-place-medal",
                                            width=20,
                                            color="silver",
                                        ),
                                        " 2nd Top Inbound Caller",
                                    ]
                                ),
                                html.Ul(
                                    [
                                        html.Li(["Name : ", html.P(id="top2-name")]),
                                        html.Li(
                                            ["Number : ", html.P(id="top2-number")]
                                        ),
                                        html.Li(
                                            [
                                                "Total Calls :",
                                                html.P(id="top2-totalCalls"),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                "Average Calls Length :",
                                                html.P(id="top2-averageCallsLength"),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Hr(style={"margin-top": "15px", "margin-bottom": "15px"}),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        DashIconify(
                                            icon="fluent-emoji-high-contrast:3rd-place-medal",
                                            width=20,
                                            color="#CD7F32",
                                        ),
                                        "3rd Top Inbound Caller",
                                    ]
                                ),
                                html.Ul(
                                    [
                                        html.Li(["Name : ", html.P(id="top3-name")]),
                                        html.Li(
                                            ["Number : ", html.P(id="top3-number")]
                                        ),
                                        html.Li(
                                            [
                                                "Total Calls :",
                                                html.P(id="top3-totalCalls"),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                "Average Calls Length :",
                                                html.P(id="top3-averageCallsLength"),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    id="top3",
                ),
            ],
            className="container graph-section",
        ),
        html.Div(
            [
                html.H2(
                    [
                        DashIconify(
                            icon="icon-park:chart-line",
                            width=20,
                            color="#094546",
                        ),
                        "Numbers of Calls Over Time",
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                "Resolution",
                                dcc.Dropdown(
                                    [
                                        "Monthly Calls",
                                        "Daily Calls",
                                        "hourly Calls",
                                    ],
                                    value="Monthly Calls",
                                    id="option-dropdown",
                                    optionHeight=50,
                                    style={
                                        "width": "220px",
                                        "border-radius": "5px",
                                    },
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                "Chart Type",
                                dcc.RadioItems(
                                    ["Line Chart", "Area Chart"],
                                    "Line Chart",
                                    id="option-radioItems",
                                    inline=True,
                                    style={"display": "flex", "gap": "10px"},
                                ),
                            ]
                        ),
                    ],
                    style={"display": "flex", "gap": "50px", "alignItems": "center"},
                ),
                dcc.Loading(
                    [
                        dcc.Graph(
                            id="chart",
                            # figure=px.line(
                            #     df, y="TotalCallDuration", x="Date", color="Direction"
                            # ),
                        ),
                    ],
                    overlay_style={
                        "visibility": "visible",
                        "opacity": 0.2,
                        "backgroundColor": "white",
                    },
                ),
            ],
            className="container lineChart-section",
        ),
    ],
    className="company-analytics-layout",
)
# -------------------------------------------------------------------------------------------------------------------
# Layout End
# -------------------------------------------------------------------------------------------------------------------


# **************************************************************************************
# section 1


@callback(
    Output("inbound_calls", "children"),
    Output("inbound_time", "children"),
    Output("inbound_time_avg", "children"),
    Output("Inbound_answered", "children"),
    Output("outbound_calls", "children"),
    Output("outbound_time", "children"),
    Output("outbound_time_avg", "children"),
    Output("internal_calls", "children"),
    Output("internal_time", "children"),
    Output("internal_time_avg", "children"),
    State("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def update_calls_row(start_date, end_date):
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    def calculate_stats(direction):
        calls = filtered_df[filtered_df["Direction"] == direction]
        total_calls = len(calls)
        total_time = calls["TotalCallDuration"].sum()
        avg_time = calls["TotalCallDuration"].mean()
        if direction == "Inbound":
            answered_calls = len(calls[calls["Answered"] == 1])
            answer_rate = (answered_calls / total_calls) * 100 if total_calls > 0 else 0
            return (
                total_calls,
                convert_seconds(total_time),
                convert_seconds(avg_time),
                f"{answer_rate:.2f} %",
            )
        else:
            return total_calls, convert_seconds(total_time), convert_seconds(avg_time)

    inbound_stats = calculate_stats("Inbound")
    outbound_stats = calculate_stats("Outbound")
    internal_stats = calculate_stats("Internal")

    return (*inbound_stats, *outbound_stats, *internal_stats)


# **************************************************************************************

# **************************************************************************************
# section 2 A


@callback(
    Output("us-map", "figure"),
    State("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def update_map(start_date, end_date):
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    inbound_calls = filtered_df[filtered_df["Direction"] == "Inbound"]

    # Set a new dataframe
    state_counts = inbound_calls["StateCode"].value_counts().reset_index()
    # change column names
    state_counts.columns = ["State Code", "Inbound Calls"]

    # ?????????? Show State Name when hover

    fig = px.choropleth(
        state_counts,
        locations="State Code",
        locationmode="USA-states",
        color="Inbound Calls",
        scope="usa",
        title="📊 Inbound Calls by State",
        hover_data={"State Code": True, "Inbound Calls": True},
        color_continuous_scale=px.colors.sequential.Blues,
    )
    return fig


# **************************************************************************************

# **************************************************************************************
# Section 2 B


@callback(
    Output("top1-name", "children"),
    Output("top1-number", "children"),
    Output("top1-totalCalls", "children"),
    Output("top1-averageCallsLength", "children"),
    Output("top2-name", "children"),
    Output("top2-number", "children"),
    Output("top2-totalCalls", "children"),
    Output("top2-averageCallsLength", "children"),
    Output("top3-name", "children"),
    Output("top3-number", "children"),
    Output("top3-totalCalls", "children"),
    Output("top3-averageCallsLength", "children"),
    State("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def Top_Inbound_Callers(start_date, end_date):
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    Inbound = filtered_df[filtered_df["Direction"] == "Inbound"]

    grouped_data = Inbound.groupby("FromNumber").agg(
        TotalCalls=("FromNumber", "count"),
        AverageCallLength=("TotalCallDuration", "mean"),
    )
    sorted_data = grouped_data.sort_values(by="TotalCalls", ascending=False)

    def get_caller_details(rank):
        caller_number = sorted_data.index[rank - 1]
        caller_row = Inbound[Inbound["FromNumber"] == caller_number]
        caller_name = caller_row["FromName"].iloc[0]
        total_calls = sorted_data.loc[caller_number, "TotalCalls"]
        avg_call_length = convert_seconds(
            sorted_data.loc[caller_number, "AverageCallLength"]
        )
        return caller_name, caller_number, total_calls, avg_call_length

    top1_details = get_caller_details(1)
    top2_details = get_caller_details(2)
    top3_details = get_caller_details(3)

    return (*top1_details, *top2_details, *top3_details)


# **************************************************************************************


# # **************************************************************************************
# # section 3


@callback(
    Output(component_id="chart", component_property="figure"),
    State("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input(component_id="option-dropdown", component_property="value"),
    Input(component_id="option-radioItems", component_property="value"),
)
def update_graph(start_date, end_date, dropdownValue, radioItemsValue):
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    # Group by 'Date' and count the number of calls
    call_counts = (
        filtered_df.groupby(["Date", "Direction"]).size().unstack(fill_value=0)
    )
    # Sort the data by Date
    call_counts_melted = call_counts.reset_index().melt(
        id_vars="Date", var_name="Direction", value_name="Call_Count"
    )

    chart_types = {"Line Chart": px.line, "Area Chart": px.area}

    fig = chart_types[radioItemsValue](
        call_counts_melted,
        x="Date",
        y="Call_Count",
        color="Direction",
        hover_data=["Direction", "Call_Count"],
        labels={"Call_Count": "Number of Calls"},
        # color_discrete_sequence=["#094546","#aec7e8", "#2171b5"],
    )
    fig.update_xaxes(tickangle=45)

    # Customize grid lines: only horizontal grid lines in gray
    fig.update_xaxes(
        showgrid=False,  # Disable vertical grid lines
        showline=True,  # Show the x-axis line
        linecolor="black",  # Set x-axis line color to black
    )
    fig.update_yaxes(
        showgrid=True,  # Enable horizontal grid lines
        gridcolor="lightgray",  # Set grid line color to light gray
        showline=True,  # Show the y-axis line
        linecolor="black",  # Set y-axis line color to black
    )

    # Set background color to white
    fig.update_layout(
        plot_bgcolor="white",  # Background color of the plotting area
        paper_bgcolor="white",  # Background color of the entire chart
    )

    # fig.update_traces(
    #     line=dict(color="#1f77b4"),  # لون الخطوط
    #     fillcolor="rgba(31, 119, 180, 0.2)",  # لون المناطق مع شفافية
    #     fillgradient=dict(type="vertical", colorscale="Blues"),  # تدرج لوني
    # )

    return fig
