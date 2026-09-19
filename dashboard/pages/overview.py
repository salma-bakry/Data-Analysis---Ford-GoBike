from dash import register_page, html, dcc

register_page(__name__, path="/", name="Overview")


def create_kpi_card(title, component_id):
    return html.Div(
        [
            html.H4(title, className="kpi-title"),
            html.H2(
                id=component_id,
                children="Loading...",
                className="kpi-value"
            ),
        ],
        className="kpi-card",
    )


layout = html.Div(
    [
        html.H2("Overview", className="page-heading"),

        # KPI cards
        html.Div(
            [
                create_kpi_card("Total Trips", "total-trips-kpi"),
                create_kpi_card("Total Users", "total-users-kpi"),
                create_kpi_card(
                    "Average Trip Duration",
                    "average-duration-kpi"
                ),
                create_kpi_card("Total Stations", "total-stations-kpi"),
            ],
            className="kpi-container",
        ),

        # Project description
        html.Div(
            [
                html.H3("About the GoBike Dataset"),
                html.P(
                    """
                    This dashboard analyzes the Ford GoBike bike-sharing
                    dataset. The database contains information about bike
                    trips, users, stations, dates, trip durations, and
                    user characteristics.
                    """
                ),
                html.P(
                    """
                    The purpose of this analysis is to understand how people
                    use the bike-sharing service, identify travel patterns
                    over time, compare different user groups, and discover
                    the most frequently used stations and routes.
                    """
                ),
                html.P(
                    """
                    Use the filters on the left to explore the data and
                    update the KPIs and charts dynamically.
                    """
                ),
            ],
            className="overview-description",
        ),

        # Important charts
        html.H3(
            "Key Insights",
            className="overview-section-title"
        ),

        # First row: two charts
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Trips by Day"),
                        dcc.Graph(id="overview-trips-by-day"),
                    ],
                    className="overview-chart-card",
                ),

                html.Div(
                    [
                        html.H4("User Type Distribution"),
                        dcc.Graph(id="overview-user-type"),
                    ],
                    className="overview-chart-card",
                ),
            ],
            className="overview-charts-row",
        ),

        # Second row: one chart
        html.Div(
            [
                html.H4("Top Starting Stations"),
                dcc.Graph(id="overview-top-start-stations"),
            ],
            className="overview-chart-card overview-single-chart",
        ),
    ]
)