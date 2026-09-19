from dash import register_page, html, dcc, Input, Output, callback

from data_loader import df, filter_data

from station_trip_analysis import (
    create_top_start_stations_chart,
    create_top_end_stations_chart,
    create_top_routes_chart,
    create_station_activity_chart,
    create_station_map,
    create_route_map
)


# ==========================================
# REGISTER PAGE
# ==========================================

register_page(
    __name__,
    path="/station-analysis",
    name="Station Analysis"
)


# ==========================================
# PREPARE STATION DATA
# ==========================================

def prepare_station_data(data):
    station_df = data.dropna(
        subset=[
            "start_station_name",
            "end_station_name",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude"
        ]
    ).copy()

    station_df["trip_route"] = (
        station_df["start_station_name"]
        + " → "
        + station_df["end_station_name"]
    )

    return station_df


# ==========================================
# PAGE LAYOUT
# ==========================================

layout = html.Div(
    children=[
        html.H2(
            "Station Analysis",
            className="page-heading"
        ),

        html.Div(
            className="station-charts-container",
            children=[
                dcc.Graph(id="top-start-stations-chart"),

                dcc.Graph(id="top-end-stations-chart"),

                dcc.Graph(id="top-routes-chart"),

                dcc.Graph(id="station-activity-chart"),

                html.Div(
                    className="station-map-frame",
                    children=[
                        dcc.Graph(
                            id="station-activity-map",
                            style={
                                "width": "100%",
                                "height": "100%"
                            },
                            config={"responsive": True}
                        )
                    ]
                ),

                html.Div(
                    className="station-map-frame",
                    children=[
                        dcc.Graph(
                            id="route-map",
                            style={
                                "width": "100%",
                                "height": "100%"
                            },
                            config={"responsive": True}
                        )
                    ]
                ),
            ]
        )
    ]
)


# ==========================================
# UPDATE STATION CHARTS
# ==========================================

@callback(
    Output("top-start-stations-chart", "figure"),
    Output("top-end-stations-chart", "figure"),
    Output("top-routes-chart", "figure"),
    Output("station-activity-chart", "figure"),
    Output("station-activity-map", "figure"),
    Output("route-map", "figure"),

    Input("start-date-filter", "date"),
    Input("end-date-filter", "date"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("duration-filter", "value")
)
def update_station_charts(
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

    station_df = prepare_station_data(filtered_df)

    return (
        create_top_start_stations_chart(station_df),
        create_top_end_stations_chart(station_df),
        create_top_routes_chart(station_df),
        create_station_activity_chart(station_df),
        create_station_map(station_df),
        create_route_map(station_df)
    )