import dash
from dash import html, dcc, callback, Output, Input, State
import plotly.express as px
import dash_ag_grid as dag
from dash_iconify import DashIconify

from components.getData.GetData import ReadData

dash.register_page(
    __name__, path="/userAnalytics", title="User Analytics", name="User Analytics"
)

df = ReadData()


def prepare_call_stats_by_name(df):
    newStats_df = df.groupby("ToName").agg(
        Total_Calls=("Direction", "count"),
        Avg_Call_Duration=("TotalCallDuration", "mean"),
        Total_Inbound_Calls=("Direction", lambda x: (x == "Inbound").sum()),
        Total_Outbound_Calls=("Direction", lambda x: (x == "Outbound").sum()),
        Total_Internal_Calls=("Direction", lambda x: (x == "Internal").sum()),
        Total_Answered_Calls=("Answered", lambda x: (x == 1).sum()),
    )
    newStats_df["Avg_Call_Duration"] = newStats_df["Avg_Call_Duration"].round(2)
    newStats_df["Percentage_of_Answered_Calls"] = (
        (newStats_df["Total_Answered_Calls"] / newStats_df["Total_Calls"]) * 100
    ).round(0).astype(int).astype(str) + "%"

    newStats_df.reset_index(inplace=True)

    newStats_df.rename(
        columns={
            "ToName": "User Name",
            "Total_Calls": "Total Calls",
            "Avg_Call_Duration": "Avg Call Duration (sec)",
            "Total_Inbound_Calls": "Total Inbound Calls",
            "Percentage_of_Answered_Calls": "Answered Inbound Calls %",
            "Total_Outbound_Calls": "Total Outbound Calls",
            "Total_Internal_Calls": "Total Internal Calls",
        },
        inplace=True,
    )
    newStats_df.drop(columns=["Total_Answered_Calls"], inplace=True)

    return newStats_df


# ************************* Ag Grid Settings Start *************************

call_stats_by_name = prepare_call_stats_by_name(df)
columnDefs = [{"headerName": col, "field": col} for col in call_stats_by_name.columns]
defaultColDef = {
    "width": 180,
    "editable": True,
    "filter": "agTextColumnFilter",
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
}
# ************************* Ag Grid Settings End *************************


def prepare_dropdown_options(df):
    user_names = df["ToName"].dropna().unique().tolist()
    return [{"label": name, "value": name} for name in user_names]


# ************************* User Internal Calls Network (Section 3) Settings Start *************************

dropdown_options = prepare_dropdown_options(df)

# ************************* User Internal Calls Network (Section 3) Settings End *************************

# -------------------------------------------------------------------------------------------------------------------
# Layout Start
# -------------------------------------------------------------------------------------------------------------------
layout = html.Div(
    [
        # ------------------ Section 1 ------------------
        html.Div(
            [
                html.H2(
                    [
                        DashIconify(
                            icon="solar:user-id-linear", width=24, color="#094546"
                        ),
                        "User Based Stats",
                    ]
                ),
                dag.AgGrid(
                    id="user-based-stats-ag-grid",
                    columnDefs=columnDefs,
                    rowData=call_stats_by_name.to_dict("records"),
                    defaultColDef=defaultColDef,
                    dashGridOptions={"animateRows": False},
                ),
            ],
            className="user-based-stats",
        ),
        # ------------------ Section 2 ------------------
        html.Div(
            [
                html.H2(
                    [
                        DashIconify(
                            icon="ic:baseline-access-time-filled",
                            width=24,
                            color="#094546",
                        ),
                        "Total Calls Duration by User",
                    ]
                ),
                dcc.Loading(
                    id="loading-spinner",
                    children=dcc.Graph(id="total-calls-duration-by-user-bar-chart"),
                ),
            ],
            className="user-based-stats",
        ),
        # ------------------ Section 3 ------------------
        html.Div(
            [
                html.H2(
                    [
                        DashIconify(
                            icon="material-symbols-light:connected-tv-outline",
                            width=24,
                            color="#094546",
                        ),
                        "User Internal Calls Network",
                    ]
                ),
                html.Div(
                    [
                        "User",
                        dcc.Dropdown(
                            options=dropdown_options,
                            value=dropdown_options[0]["value"],
                            id="internal-calls-network-option-dropdown",
                            optionHeight=40,
                            style={"width": "220px", "border-radius": "5px"},
                        ),
                    ],
                    className="internal-calls-network-dropdown",
                ),
                # dcc.Graph(id="internal-call-network-graph"),
            ],
            className="user-based-stats",
        ),
    ],
    className="user-analytics-layout",
)
# -------------------------------------------------------------------------------------------------------------------
# Layout End
# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
# CallBacks Start
# -------------------------------------------------------------------------------------------------------------------
@callback(
    Output("total-calls-duration-by-user-bar-chart", "figure"),
    Output("user-based-stats-ag-grid", "rowData"),
    State("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def update_data(start_date, end_date):
    """Update data according to date range."""
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    call_stats_by_name = prepare_call_stats_by_name(filtered_df)

    # ************************* Bar Chart Settings Start *************************

    users_total_calls = (
        filtered_df.groupby("ToName")
        .agg(Total_Call_Duration=("TotalCallDuration", lambda x: round(x.sum() / 60)))
        .reset_index()
    )

    users_total_calls = users_total_calls.sort_values(
        by="Total_Call_Duration", ascending=False
    )

    # Delete the first row & last 20 rows "unknown_name"
    users_total_calls = users_total_calls.iloc[1:-20]

    users_total_calls.rename(
        columns={
            "ToName": "User Name",
            "Total_Call_Duration": "Total Calls Duration (Minutes)",
        },
        inplace=True,
    )

    fig = px.bar(
        users_total_calls,
        x="User Name",
        y="Total Calls Duration (Minutes)",
        labels={
            "User Name": "User Name",
            "Total Calls Duration (Minutes)": "Total Calls Duration (Minutes)",
        },
        custom_data=["Total Calls Duration (Minutes)"],
    )
    fig.update_traces(
        marker_color="#094546",
        text=None,
        hovertemplate="<b>%{x}</b> (%{customdata[0]} Minutes)",
    )

    fig.update_layout(
        xaxis=dict(
            tickangle=45,
            showline=True,
            linewidth=1,
            linecolor="black",
            # title=dict(text="User Name", font=dict(size=14, color="black")),
            # gridcolor="lightgray",
            # gridwidth=0.5
        ),
        yaxis=dict(
            showline=True,
            linecolor="black",
            linewidth=1,
        ),
        template="plotly_white",
        margin=dict(l=50, r=50, t=50, b=150),
        xaxis_range=[-1, len(users_total_calls)],
    )
    # ************************* Bar Chart Settings End *************************

    return fig, call_stats_by_name.to_dict("records")


# -------------------------------------------------------------------------------------------------------------------
# CallBacks End
# -------------------------------------------------------------------------------------------------------------------
