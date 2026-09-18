from dash import register_page, html


register_page(
    __name__,
    path="/user-analysis",
    name="User Analysis"
)


layout = html.Div(
    children=[

        html.H2("User Analysis Page"),

        html.P(
            "The User Analysis page is working successfully!"
        )
    ]
)