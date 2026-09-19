import pandas as pd

from dash import (
    Dash,
    html,
    dcc,
    page_container,
    Input,
    Output,
)

from data_loader import df, filter_data

from time_analysis import create_trips_by_day_chart
from user_analysis import create_user_type_chart
from station_trip_analysis import create_top_start_stations_chart

# Create Dash application
app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)
# Navbar
navbar = html.Nav(
    className="navbar",
    children=[
        html.Div(
            "GoBike",
            className="brand"
        ),

        html.Div(
            className="nav-buttons",
            children=[
                dcc.Link(
                    "Overview",
                    href="/",
                    className="nav-button"
                ),

                dcc.Link(
                    "Time Analysis",
                    href="/time-analysis",
                    className="nav-button"
                ),

                dcc.Link(
                    "User Analysis",
                    href="/user-analysis",
                    className="nav-button"
                ),

                dcc.Link(
                    "Station Analysis",
                    href="/station-analysis",
                    className="nav-button"
                ),
            ]
        ),
    ]
)

# Sidebar filters
sidebar = html.Aside(
    className="sidebar",
    children=[
        html.H3(
            "Filters",
            className="sidebar-title"
        ),

        # Start date
        html.Label(
            "Start Date",
            className="filter-label"
        ),

        dcc.DatePickerSingle(
            id="start-date-filter",
            date="2019-02-01",
            display_format="YYYY-MM-DD",
            className="compact-date-picker"
        ),

        html.Br(),

        # End date
        html.Label(
            "End Date",
            className="filter-label"
        ),

        dcc.DatePickerSingle(
            id="end-date-filter",
            date="2019-02-28",
            display_format="YYYY-MM-DD",
            className="compact-date-picker"
        ),

        html.Br(),

        # User type
        html.Label(
            "User Type",
            className="filter-label"
        ),

        dcc.Dropdown(
            id="user-type-filter",
            options=[
                {
                    "label": "Customer",
                    "value": "Customer"
                },
                {
                    "label": "Subscriber",
                    "value": "Subscriber"
                },
            ],
            value=[
                "Customer",
                "Subscriber"
            ],
            multi=True,
            placeholder="Select user type"
        ),

        html.Br(),

        # Gender
        html.Label(
            "Gender",
            className="filter-label"
        ),

        dcc.Dropdown(
            id="gender-filter",
            options=[
                {
                    "label": "Female",
                    "value": "Female"
                },
                {
                    "label": "Male",
                    "value": "Male"
                },
                {
                    "label": "Unknown",
                    "value": "Unknown"
                },
            ],
            value=[
                "Female",
                "Male",
                "Unknown"
            ],
            multi=True,
            placeholder="Select gender"
        ),

        html.Br(),

        # Age group
        html.Label(
            "Age Group",
            className="filter-label"
        ),

        dcc.Checklist(
            id="age-group-filter",
            options=[
                {
                    "label": "Under 20",
                    "value": "Under 20"
                },
                {
                    "label": "20-29",
                    "value": "20-29"
                },
                {
                    "label": "30-39",
                    "value": "30-39"
                },
                {
                    "label": "40-49",
                    "value": "40-49"
                },
                {
                    "label": "50-59",
                    "value": "50-59"
                },
                {
                    "label": "60+",
                    "value": "60+"
                },
                {
                    "label": "Unknown",
                    "value": "Unknown"
                },
            ],
            value=[
                "Under 20",
                "20-29",
                "30-39",
                "40-49",
                "50-59",
                "60+",
                "Unknown"
            ],
            inline=False
        ),

        html.Br(),

        # Duration
        html.Label(
            "Trip Duration (minutes)",
            className="filter-label"
        ),

        dcc.RangeSlider(
            id="duration-filter",
            min=1,
            max=80,
            step=1,
            value=[1, 80],
            marks={
                1: "1",
                20: "20",
                40: "40",
                60: "60",
                80: "80"
            },
            tooltip={
                "placement": "bottom",
                "always_visible": False
            }
        ),
    ]
)

# Main application layout
app.layout = html.Div(
    [
        navbar,

        sidebar,

        html.Main(
            className="main-content",
            children=[
                html.H1(
                    "Ford GoBike Dashboard",
                    className="main-title"
                ),

                html.Div(
                    page_container,
                    className="page-content"
                ),
            ]
        ),
    ]
)
# Overview KPIs and charts callback
@app.callback(
    [
        Output("total-trips-kpi", "children"),
        Output("total-users-kpi", "children"),
        Output("average-duration-kpi", "children"),
        Output("total-stations-kpi", "children"),

        Output("overview-trips-by-day", "figure"),
        Output("overview-user-type", "figure"),
        Output("overview-top-start-stations", "figure"),
    ],
    [
        Input("start-date-filter", "date"),
        Input("end-date-filter", "date"),
        Input("user-type-filter", "value"),
        Input("gender-filter", "value"),
        Input("age-group-filter", "value"),
        Input("duration-filter", "value"),
    ]
)
def update_overview(
    start_date,
    end_date,
    user_types,
    genders,
    age_groups,
    duration_range
):
    # Apply filters
    filtered_df = filter_data(
        df,
        start_date,
        end_date,
        user_types,
        genders,
        age_groups,
        duration_range
    )
    # Calculate KPIs
    total_trips = len(filtered_df)

    total_users = filtered_df["user_id"].nunique()

    if len(filtered_df) > 0:
        average_duration = (
            filtered_df["duration_sec"].mean() / 60
        )
    else:
        average_duration = 0

    station_columns = []

    if "start_station_id" in filtered_df.columns:
        station_columns.append("start_station_id")

    if "end_station_id" in filtered_df.columns:
        station_columns.append("end_station_id")

    if station_columns and len(filtered_df) > 0:
        unique_stations = pd.concat(
            [
                filtered_df[column]
                for column in station_columns
            ]
        ).nunique()

    else:
        unique_stations = 0

    # Format KPI values
    total_trips_display = f"{total_trips:,}"

    total_users_display = f"{total_users:,}"

    average_duration_display = (
        f"{average_duration:.2f} min"
    )

    total_stations_display = f"{unique_stations:,}"

    # Create overview charts
    # Chart 1: Trips by day
    if len(filtered_df) > 0:
        trips_by_day_figure = create_trips_by_day_chart(
            filtered_df
        )
    else:
        trips_by_day_figure = {
            "data": [],
            "layout": {
                "title": "No data available"
            }
        }

    # Chart 2: User type distribution
    if len(filtered_df) > 0:
        user_type_figure = create_user_type_chart(
            filtered_df
        )
    else:
        user_type_figure = {
            "data": [],
            "layout": {
                "title": "No data available"
            }
        }

    # Chart 3: Top starting stations
    station_df = filtered_df.dropna(
        subset=["start_station_name"]
    ).copy()

    if len(station_df) > 0:
        top_start_stations_figure = (
            create_top_start_stations_chart(station_df)
        )
    else:
        top_start_stations_figure = {
            "data": [],
            "layout": {
                "title": "No data available"
            }
        }

    # Make overview charts smaller
    trips_by_day_figure.update_layout(
        height=350,
        margin=dict(
            l=30,
            r=20,
            t=50,
            b=40
        )
    )

    user_type_figure.update_layout(
        height=350,
        margin=dict(
            l=30,
            r=20,
            t=50,
            b=40
        )
    )

    top_start_stations_figure.update_layout(
        height=350,
        margin=dict(
            l=30,
            r=20,
            t=50,
            b=40
        )
    )

    # Return KPIs and charts
    return (
        total_trips_display,
        total_users_display,
        average_duration_display,
        total_stations_display,

        trips_by_day_figure,
        user_type_figure,
        top_start_stations_figure,
    )


# Run application
if __name__ == "__main__":
    app.run(debug=True)