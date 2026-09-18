from dash import register_page, html

register_page(
    __name__,
    path="/",
    name="Overview"
)


def create_kpi_card(title, component_id):
    return html.Div(
        children=[
            html.H4(title, className="kpi-title"),
            html.H2(
                id=component_id,
                children="Loading...",
                className="kpi-value"
            )
        ],
        className="kpi-card"
    )


layout = html.Div(
    children=[
        html.H2(
            "Overview",
            className="page-heading"
        ),

        html.Div(
            children=[
                create_kpi_card(
                    "Total Trips",
                    "total-trips-kpi"
                ),

                create_kpi_card(
                    "Total Users",
                    "total-users-kpi"
                ),

                create_kpi_card(
                    "Average Trip Duration",
                    "average-duration-kpi"
                ),

                create_kpi_card(
                    "Total Stations",
                    "total-stations-kpi"
                )
            ],
            className="kpi-container"
        )
    ]
)