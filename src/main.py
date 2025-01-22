import dash
from dash import Dash, html, dcc

from components.getData.GetData import ReadData
from components.header.header import Header

app = Dash(__name__, assets_folder="assets", use_pages=True)
server = app.server

df = ReadData()



app.layout = html.Div(
    [
        Header(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label("Selected Date Range"),
                        dcc.DatePickerRange(
                            id="date-picker-range",
                            min_date_allowed=df["Date"].min(),
                            max_date_allowed=df["Date"].max(),
                            initial_visible_month=df["Date"].min(),
                            start_date=df["Date"].min(),
                            end_date=df["Date"].max(),
                            display_format="MMMM DD, YYYY",
                        ),
                    ],
                    className="picker-range-section",
                ),
                dash.page_container,
            ],
            className="container",
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
