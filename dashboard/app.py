import pandas as pd

from dash import Dash, html, dcc, page_container, Input, Output

from data_loader import df, filter_data


# Create the Dash application
app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)


# ==========================================
# TOP NAVIGATION BAR
# ==========================================

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
                )
            ]
        )
    ]
)


# ==========================================
# LEFT SIDEBAR
# ==========================================

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
                {"label": "Customer", "value": "Customer"},
                {"label": "Subscriber", "value": "Subscriber"}
            ],
            value=["Customer", "Subscriber"],
            multi=True,
            clearable=True,
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
                {"label": "Female", "value": "Female"},
                {"label": "Male", "value": "Male"},
                {"label": "Unknown", "value": "Unknown"}
            ],
            value=["Female", "Male", "Unknown"],
            multi=True,
            clearable=True,
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
                {"label": "Under 20", "value": "Under 20"},
                {"label": "20-29", "value": "20-29"},
                {"label": "30-39", "value": "30-39"},
                {"label": "40-49", "value": "40-49"},
                {"label": "50-59", "value": "50-59"},
                {"label": "60+", "value": "60+"},
                {"label": "Unknown", "value": "Unknown"}
            ],
            value=[
                "Under 20",
                "20-29",
                "30-39",
                "40-49",
                "50-59",
                "60+",
                "Unknown"
            ]
        ),

        html.Br(),

        # Duration
        html.Label(
            "Duration (minutes)",
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
        )
    ]
)


# ==========================================
# MAIN LAYOUT
# ==========================================

app.layout = html.Div(
    children=[
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
                )
            ]
        )
    ]
)


# ==========================================
# OVERVIEW KPI CALLBACK
# ==========================================

@app.callback(
    Output("total-trips-kpi", "children"),
    Output("total-users-kpi", "children"),
    Output("average-duration-kpi", "children"),
    Output("total-stations-kpi", "children"),

    Input("start-date-filter", "date"),
    Input("end-date-filter", "date"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("duration-filter", "value")
)
def update_overview_kpis(
    start_date,
    end_date,
    user_types,
    genders,
    age_groups,
    duration_range
):
    filtered_df = filter_data(
        df,
        start_date,
        end_date,
        user_types,
        genders,
        age_groups,
        duration_range
    )

    total_trips = len(filtered_df)

    total_users = (
        filtered_df["user_id"].nunique()
        if "user_id" in filtered_df.columns
        else 0
    )

    if not filtered_df.empty:
        average_duration = (
            filtered_df["duration_sec"].mean() / 60
        )
    else:
        average_duration = 0

    station_columns = []

    if "start_station_id" in filtered_df.columns:
        station_columns.append(filtered_df["start_station_id"])

    if "end_station_id" in filtered_df.columns:
        station_columns.append(filtered_df["end_station_id"])

    if station_columns:
        total_stations = pd.concat(station_columns).nunique()
    else:
        total_stations = 0

    return (
        f"{total_trips:,}",
        f"{total_users:,}",
        f"{average_duration:.2f} min",
        f"{total_stations:,}"
    )


# ==========================================
# RUN THE APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)