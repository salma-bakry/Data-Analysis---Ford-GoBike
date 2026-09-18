import pandas as pd
from sqlalchemy import create_engine
from dash import register_page, html

register_page(
    __name__,
    path="/",
    name="Overview"
)

# Database connection
engine = create_engine(
    "postgresql+psycopg://postgres:1234@localhost:5432/gobike_db"
)

# Load data
df = pd.read_sql(
    "SELECT * FROM gobike.dashboard_trips",
    engine
)

# Calculate KPIs
total_trips = len(df)

total_users = df["user_id"].nunique()

average_duration = round(
    df["duration_sec"].mean() / 60,
    2
)

total_stations = pd.concat(
    [
        df["start_station_id"],
        df["end_station_id"]
    ]
).nunique()


def create_kpi_card(title, value):
    return html.Div(
        children=[
            html.H4(title, className="kpi-title"),
            html.H2(value, className="kpi-value")
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
                    f"{total_trips:,}"
                ),

                create_kpi_card(
                    "Total Users",
                    f"{total_users:,}"
                ),

                create_kpi_card(
                    "Average Trip Duration",
                    f"{average_duration} min"
                ),

                create_kpi_card(
                    "Total Stations",
                    f"{total_stations:,}"
                )
            ],
            className="kpi-container"
        )
    ]
)