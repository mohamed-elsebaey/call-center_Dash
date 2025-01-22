import dash
from dash import html, dcc


def Header():
    """
    Reusable header component for your Dash app.
    """
    return html.Section(
        className="headerSection",
        children=[
            html.Div(
                className="header",
                children=[
                    dcc.Link(
                        href="/",
                        children=[
                            html.Img(src="assets/images/center1.png"),
                            html.H2("Void Analytics Dashboard"),
                        ],
                        className="logo",
                    ),
                    html.Nav(
                        children=[
                            html.Div(
                                className="menu",
                                children=[
                                    html.Span(),
                                    html.Span(),
                                    html.Span(),
                                ],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        children=[
                                            dcc.Link(
                                                href=page["relative_path"],
                                                children=f"{page['name']}",
                                            )
                                        ]
                                    )
                                    for page in dash.page_registry.values()
                                ],
                                className="small",
                            ),
                        ]
                    ),
                ],
            )
        ],
    )
