from dash import Dash, html, dcc, page_container


# ==========================================
# 1. CREATE DASH APPLICATION
# ==========================================

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)

app.title = "Ford GoBike Dashboard"


# ==========================================
# 2. TOP NAVIGATION BAR
# ==========================================

navbar = html.Div(
    children=[

        html.Div(
            "GoBike",
            className="brand"
        ),

        html.Div(
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

            ],
            className="nav-buttons"
        )

    ],
    className="navbar"
)


# ==========================================
# 3. LEFT SIDEBAR
# ==========================================

sidebar = html.Div(
    children=[
        html.H2("Filters", className="sidebar-title"),

        html.P(
            "Every chart updates instantly.",
            className="sidebar-subtitle"
        ),

        html.Hr(),

        # Date range
        # Start date
        html.Label("Start Date", className="filter-label"),

        dcc.DatePickerSingle(
        id="start-date-filter",
        date="2019-02-01",
        display_format="YYYY-MM-DD",
        className="compact-date-picker"
        ),
        html.Br(),

        # End date
        html.Label("End Date", className="filter-label"),

        dcc.DatePickerSingle(
        id="end-date-filter",
        date="2019-02-28",
        display_format="YYYY-MM-DD",
        className="compact-date-picker"
        ),

        html.Br(),

        # User type
        html.Label("User Type", className="filter-label"),

        dcc.Dropdown(
            id="user-type-filter",
            options=[
                {"label": "Customer", "value": "Customer"},
                {"label": "Subscriber", "value": "Subscriber"}
            ],
            value=["Customer", "Subscriber"],
            multi=True,
            placeholder="Select user type..."
        ),

        html.Br(),

        # Gender
        html.Label("Gender", className="filter-label"),

        dcc.Dropdown(
            id="gender-filter",
            options=[
                {"label": "Female", "value": "Female"},
                {"label": "Male", "value": "Male"},
                {"label": "Unknown", "value": "Unknown"}
            ],
            value=["Female", "Male", "Unknown"],
            multi=True,
            placeholder="Select gender..."
        ),

        html.Br(),

        # Age group
        html.Label("Age Group", className="filter-label"),

        dcc.Checklist(
            id="age-group-filter",
            options=[
                {"label": "Under 20", "value": "Under 20"},
                {"label": "20-29", "value": "20-29"},
                {"label": "30-39", "value": "30-39"},
                {"label": "40-49", "value": "40-49"},
                {"label": "50-59", "value": "50-59"},
                {"label": "60+", "value": "60+"}
            ],
            value=[
                "Under 20",
                "20-29",
                "30-39",
                "40-49",
                "50-59",
                "60+"
            ],
            labelStyle={
                "display": "block",
                "marginBottom": "12px"
            }
        ),

        html.Br(),

        # Trip duration
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
                1: "1m",
                40: "40m",
                80: "80m"
            },
            tooltip={
                "placement": "bottom",
                "always_visible": False
            }
        ),

        html.Br(),
    ],
    className="sidebar"
)

# ==========================================
# 4. MAIN APPLICATION LAYOUT
# ==========================================

app.layout = html.Div(
    children=[

        navbar,

        sidebar,

        html.Main(
            children=[

                html.H1(
                    "Ford GoBike Data Analysis Dashboard",
                    className="main-title"
                ),

                html.Div(
                    page_container,
                    className="page-content"
                )

            ],
            className="main-content"
        )

    ]
)


# ==========================================
# 5. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)