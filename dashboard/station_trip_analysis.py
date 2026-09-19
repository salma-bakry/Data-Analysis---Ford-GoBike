import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine


# ==========================================
# 1. DATABASE CONNECTION
# ==========================================

engine = create_engine(
    "postgresql+psycopg://postgres:1234@localhost:5432/gobike_db"
)


# ==========================================
# 2. LOAD DATA FROM POSTGRESQL
# ==========================================

query = """
SELECT *
FROM gobike.dashboard_trips
"""

df = pd.read_sql(query, engine)


# ==========================================
# 3. CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "start_station_name",
    "end_station_name",
    "start_latitude",
    "start_longitude",
    "end_latitude",
    "end_longitude"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in gobike.dashboard_trips: {missing_columns}"
    )


# ==========================================
# 4. DATA PREPARATION
# ==========================================

station_df = df.dropna(
    subset=[
        "start_station_name",
        "end_station_name",
        "start_latitude",
        "start_longitude",
        "end_latitude",
        "end_longitude"
    ]
).copy()


# Create trip route
station_df["trip_route"] = (
    station_df["start_station_name"]
    + " → "
    + station_df["end_station_name"]
)


# ==========================================
# 5. CHART 1: TOP START STATIONS
# ==========================================

def create_top_start_stations_chart(df, top_n=10):

    top_start = (
        df["start_station_name"]
        .value_counts()
        .head(top_n)
        .sort_values(ascending=True)
        .reset_index()
    )

    top_start.columns = [
        "station",
        "trip_count"
    ]

    fig = px.bar(
        top_start,
        x="trip_count",
        y="station",
        orientation="h",
        title=f"Top {top_n} Start Stations",
        labels={
            "station": "Start Station",
            "trip_count": "Number of Trips"
        },
        text="trip_count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Number of Trips",
        yaxis_title="Start Station"
    )

    return fig


# ==========================================
# 6. CHART 2: TOP END STATIONS
# ==========================================

def create_top_end_stations_chart(df, top_n=10):

    top_end = (
        df["end_station_name"]
        .value_counts()
        .head(top_n)
        .sort_values(ascending=True)
        .reset_index()
    )

    top_end.columns = [
        "station",
        "trip_count"
    ]

    fig = px.bar(
        top_end,
        x="trip_count",
        y="station",
        orientation="h",
        title=f"Top {top_n} End Stations",
        labels={
            "station": "End Station",
            "trip_count": "Number of Trips"
        },
        text="trip_count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Number of Trips",
        yaxis_title="End Station"
    )

    return fig


# ==========================================
# 7. CHART 3: MOST COMMON TRIP ROUTES
# ==========================================

def create_top_routes_chart(df, top_n=15):

    top_routes = (
        df["trip_route"]
        .value_counts()
        .head(top_n)
        .sort_values(ascending=True)
        .reset_index()
    )

    top_routes.columns = [
        "route",
        "trip_count"
    ]

    fig = px.bar(
        top_routes,
        x="trip_count",
        y="route",
        orientation="h",
        title=f"Top {top_n} Most Common Trip Routes",
        labels={
            "route": "Trip Route",
            "trip_count": "Number of Trips"
        },
        text="trip_count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Number of Trips",
        yaxis_title="Route",
        height=650
    )

    return fig


# ==========================================
# 8. CHART 4: STATION ACTIVITY
# ==========================================

def create_station_activity_chart(df, top_n=15):

    starts = (
        df["start_station_name"]
        .value_counts()
        .rename("start_trips")
    )

    ends = (
        df["end_station_name"]
        .value_counts()
        .rename("end_trips")
    )

    station_activity = pd.concat(
        [starts, ends],
        axis=1
    ).fillna(0)

    station_activity["total_trips"] = (
        station_activity["start_trips"]
        + station_activity["end_trips"]
    )

    station_activity = (
        station_activity
        .sort_values(
            "total_trips",
            ascending=False
        )
        .head(top_n)
        .sort_values(
            "total_trips",
            ascending=True
        )
        .reset_index()
    )

    station_activity = station_activity.rename(
        columns={
            "index": "station"
        }
    )

    fig = px.bar(
        station_activity,
        x=[
            "start_trips",
            "end_trips"
        ],
        y="station",
        orientation="h",
        barmode="group",
        title=f"Top {top_n} Stations by Total Activity",
        labels={
            "value": "Number of Trips",
            "station": "Station",
            "variable": "Trip Type"
        }
    )

    fig.update_layout(
        xaxis_title="Number of Trips",
        yaxis_title="Station"
    )

    return fig


# ==========================================
# 9. MAP 1: STATION ACTIVITY MAP
# ==========================================

def create_station_map(df):

    # --------------------------------------
    # Start station activity
    # --------------------------------------

    starts = (
        df.groupby(
            [
                "start_station_name",
                "start_latitude",
                "start_longitude"
            ]
        )
        .size()
        .reset_index(name="start_trips")
    )

    starts = starts.rename(
        columns={
            "start_station_name": "station",
            "start_latitude": "latitude",
            "start_longitude": "longitude"
        }
    )


    # --------------------------------------
    # End station activity
    # --------------------------------------

    ends = (
        df.groupby(
            [
                "end_station_name",
                "end_latitude",
                "end_longitude"
            ]
        )
        .size()
        .reset_index(name="end_trips")
    )

    ends = ends.rename(
        columns={
            "end_station_name": "station",
            "end_latitude": "latitude",
            "end_longitude": "longitude"
        }
    )


    # --------------------------------------
    # Combine start and end stations
    # --------------------------------------

    station_activity = pd.concat(
        [
            starts[
                [
                    "station",
                    "latitude",
                    "longitude",
                    "start_trips"
                ]
            ],
            ends[
                [
                    "station",
                    "latitude",
                    "longitude",
                    "end_trips"
                ]
            ]
        ],
        ignore_index=True
    )


    # --------------------------------------
    # Combine duplicate stations
    # --------------------------------------

    station_activity = (
        station_activity
        .groupby(
            [
                "station",
                "latitude",
                "longitude"
            ],
            as_index=False
        )
        .sum()
    )


    # --------------------------------------
    # Calculate total trips
    # --------------------------------------

    station_activity["total_trips"] = (
        station_activity["start_trips"]
        + station_activity["end_trips"]
    )


    # --------------------------------------
    # Calculate center of stations
    # --------------------------------------

    center_lat = station_activity["latitude"].mean()
    center_lon = station_activity["longitude"].mean()


    # --------------------------------------
    # Create map
    # --------------------------------------

    fig = px.scatter_map(
        station_activity,
        lat="latitude",
        lon="longitude",
        size="total_trips",
        color="total_trips",
        hover_name="station",
        hover_data={
            "latitude": False,
            "longitude": False,
            "start_trips": True,
            "end_trips": True,
            "total_trips": True
        },
        center={
            "lat": center_lat,
            "lon": center_lon
        },
        zoom=13,
        height=750,
        title="Station Activity Map"
    )


    # --------------------------------------
    # Map style
    # --------------------------------------

    fig.update_layout(
        map_style="open-street-map",
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    return fig


# ==========================================
# 10. MAP 2: TOP TRIP ROUTES
# ==========================================

def create_route_map(df, top_n=30):

    # --------------------------------------
    # Find most common routes
    # --------------------------------------

    top_routes = (
        df["trip_route"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    top_routes.columns = [
        "trip_route",
        "trip_count"
    ]


    # --------------------------------------
    # Keep only top routes
    # --------------------------------------

    route_df = df.merge(
        top_routes,
        on="trip_route",
        how="inner"
    )


    # --------------------------------------
    # Get coordinates for each route
    # --------------------------------------

    route_coordinates = (
        route_df[
            [
                "trip_route",
                "trip_count",
                "start_station_name",
                "start_latitude",
                "start_longitude",
                "end_station_name",
                "end_latitude",
                "end_longitude"
            ]
        ]
        .drop_duplicates("trip_route")
        .sort_values(
            "trip_count",
            ascending=False
        )
    )


    # --------------------------------------
    # Create figure
    # --------------------------------------

    fig = go.Figure()


    # --------------------------------------
    # Draw routes
    # --------------------------------------

    for _, row in route_coordinates.iterrows():

        fig.add_trace(
            go.Scattermap(
                lat=[
                    row["start_latitude"],
                    row["end_latitude"]
                ],
                lon=[
                    row["start_longitude"],
                    row["end_longitude"]
                ],
                mode="lines",
                line=dict(
                    width=2
                ),
                hovertemplate=(
                    f"<b>{row['trip_route']}</b><br>"
                    f"Trips: {row['trip_count']}"
                    "<extra></extra>"
                ),
                showlegend=False
            )
        )


    # --------------------------------------
    # Start station points
    # --------------------------------------

    start_points = route_coordinates[
        [
            "start_station_name",
            "start_latitude",
            "start_longitude"
        ]
    ].drop_duplicates()


    # --------------------------------------
    # End station points
    # --------------------------------------

    end_points = route_coordinates[
        [
            "end_station_name",
            "end_latitude",
            "end_longitude"
        ]
    ].drop_duplicates()


    # --------------------------------------
    # Add start markers
    # --------------------------------------

    fig.add_trace(
        go.Scattermap(
            lat=start_points["start_latitude"],
            lon=start_points["start_longitude"],
            mode="markers",
            marker=dict(
                size=8
            ),
            text=start_points["start_station_name"],
            hovertemplate=(
                "<b>Start Station:</b> %{text}"
                "<extra></extra>"
            ),
            name="Start Stations"
        )
    )


    # --------------------------------------
    # Add end markers
    # --------------------------------------

    fig.add_trace(
        go.Scattermap(
            lat=end_points["end_latitude"],
            lon=end_points["end_longitude"],
            mode="markers",
            marker=dict(
                size=8
            ),
            text=end_points["end_station_name"],
            hovertemplate=(
                "<b>End Station:</b> %{text}"
                "<extra></extra>"
            ),
            name="End Stations"
        )
    )


    # --------------------------------------
    # Calculate map center
    # --------------------------------------

    all_latitudes = pd.concat(
        [
            route_coordinates["start_latitude"],
            route_coordinates["end_latitude"]
        ],
        ignore_index=True
    )

    all_longitudes = pd.concat(
        [
            route_coordinates["start_longitude"],
            route_coordinates["end_longitude"]
        ],
        ignore_index=True
    )

    center_lat = all_latitudes.mean()
    center_lon = all_longitudes.mean()


    # --------------------------------------
    # Map layout
    # --------------------------------------

    fig.update_layout(
        map=dict(
            style="open-street-map",
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            zoom=13
        ),
        title=f"Top {top_n} Trip Routes",
        height=400,
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    return fig


# ==========================================
# 11. RUN ALL VISUALIZATIONS
# ==========================================

if __name__ == "__main__":

    # --------------------------------------
    # Figure 1
    # --------------------------------------

    fig1 = create_top_start_stations_chart(df)
    fig1.show()


    # --------------------------------------
    # Figure 2
    # --------------------------------------

    fig2 = create_top_end_stations_chart(df)
    fig2.show()


    # --------------------------------------
    # Figure 3
    # --------------------------------------

    fig3 = create_top_routes_chart(station_df)
    fig3.show()


    # --------------------------------------
    # Figure 4
    # --------------------------------------

    fig4 = create_station_activity_chart(station_df)
    fig4.show()


    # --------------------------------------
    # Figure 5
    # --------------------------------------

    fig5 = create_station_map(station_df)
    fig5.show()


    # --------------------------------------
    # Figure 6
    # --------------------------------------

    fig6 = create_route_map(station_df)
    fig6.show()