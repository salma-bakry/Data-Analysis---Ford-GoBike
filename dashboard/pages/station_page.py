from dash import register_page, html


register_page(
    __name__,
    path="/station-analysis",
    name="Station Analysis"
)


layout = html.Div(
    children=[

        html.H2("Station Analysis Page"),

        html.P(
            "The Station Analysis page is working successfully!"
        )
    ]
)