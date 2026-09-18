import pandas as pd
import plotly.express as px
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
# 3. DATA PREPARATION
# ==========================================

# Reconstruct the original duration in minutes
df["duration_min_original"] = df["duration_sec"] / 60

# Remove the influence of extreme duration values
duration_cap = df["duration_min_original"].quantile(0.995)

df["duration_min_clean"] = df["duration_min_original"].clip(
    upper=duration_cap
)

# Identify weekends
df["weekend"] = df["day_of_week"].isin(
    ["Saturday", "Sunday"]
)

# Create weekday/weekend classification
df["day_type"] = df["weekend"].map(
    {
        True: "Weekend",
        False: "Weekday"
    }
)


# ==========================================
# 4. CHART 1: TRIPS BY DAY OF WEEK
# ==========================================

def create_trips_by_day_chart(df):

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    trips_by_day = (
        df["day_of_week"]
        .value_counts()
        .reindex(day_order, fill_value=0)
        .reset_index()
    )

    trips_by_day.columns = [
        "day_of_week",
        "trip_count"
    ]

    fig = px.bar(
        trips_by_day,
        x="day_of_week",
        y="trip_count",
        title="Number of Trips by Day of Week",
        labels={
            "day_of_week": "Day of Week",
            "trip_count": "Number of Trips"
        },
        text="trip_count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Number of Trips"
    )

    return fig


# ==========================================
# 5. CHART 2: TRIPS BY HOUR OF DAY
# ==========================================

def create_trips_by_hour_chart(df):

    trips_by_hour = (
        df["hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    trips_by_hour.columns = [
        "hour",
        "trip_count"
    ]

    fig = px.line(
        trips_by_hour,
        x="hour",
        y="trip_count",
        title="Number of Trips by Hour of Day",
        markers=True,
        labels={
            "hour": "Hour of Day",
            "trip_count": "Number of Trips"
        }
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        xaxis_title="Hour of Day",
        yaxis_title="Number of Trips"
    )

    return fig


# ==========================================
# 6. CHART 3: WEEKDAY VS WEEKEND TRIPS
# ==========================================

def create_weekday_weekend_chart(df):

    trips_by_day_type = (
        df["day_type"]
        .value_counts()
        .reindex(["Weekday", "Weekend"], fill_value=0)
        .reset_index()
    )

    trips_by_day_type.columns = [
        "day_type",
        "trip_count"
    ]

    fig = px.pie(
        trips_by_day_type,
        names="day_type",
        values="trip_count",
        title="Weekday vs. Weekend Trips",
        hole=0.4
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Trips: %{value}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    return fig


# ==========================================
# 7. CHART 4: TRIP DURATION BY DAY OF WEEK
# ==========================================

def create_duration_by_day_chart(df):

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    fig = px.box(
        df,
        x="day_of_week",
        y="duration_min_clean",
        category_orders={
            "day_of_week": day_order
        },
        title="Trip Duration by Day of Week",
        labels={
            "day_of_week": "Day of Week",
            "duration_min_clean": "Trip Duration (Minutes)"
        },
        points=False
    )

    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Trip Duration (Minutes)"
    )

    return fig


# ==========================================
# 8. CHART 5: AVERAGE TRIP DURATION BY HOUR
# ==========================================

def create_average_duration_by_hour_chart(df):

    average_duration_by_hour = (
        df.groupby("hour", as_index=False)["duration_min_clean"]
        .mean()
        .sort_values("hour")
    )

    average_duration_by_hour.columns = [
        "hour",
        "average_duration"
    ]

    fig = px.line(
        average_duration_by_hour,
        x="hour",
        y="average_duration",
        title="Average Trip Duration by Hour of Day",
        markers=True,
        labels={
            "hour": "Hour of Day",
            "average_duration": "Average Duration (Minutes)"
        }
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        xaxis_title="Hour of Day",
        yaxis_title="Average Duration (Minutes)"
    )

    return fig


# ==========================================
# 9. CHART 6: TRIP DURATION: WEEKDAY VS WEEKEND
# ==========================================

def create_average_duration_by_day_type_chart(df):

    average_duration_by_day_type = (
        df.groupby("day_type", as_index=False)["duration_min_clean"]
        .mean()
        .set_index("day_type")
        .reindex(["Weekday", "Weekend"])
        .reset_index()
    )

    average_duration_by_day_type.columns = [
        "day_type",
        "average_duration"
    ]

    fig = px.bar(
        average_duration_by_day_type,
        x="day_type",
        y="average_duration",
        title="Average Trip Duration: Weekday vs. Weekend",
        labels={
            "day_type": "Day Type",
            "average_duration": "Average Duration (Minutes)"
        },
        text="average_duration"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Day Type",
        yaxis_title="Average Duration (Minutes)"
    )

    return fig


# ==========================================
# 10. CHART 7: TRIP VOLUME BY DAY AND HOUR
# ==========================================

def create_day_hour_heatmap(df):

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    trips_by_day_hour = (
        df.groupby(["day_of_week", "hour"])
        .size()
        .reset_index(name="trip_count")
    )

    heatmap_data = trips_by_day_hour.pivot(
        index="day_of_week",
        columns="hour",
        values="trip_count"
    )

    heatmap_data = heatmap_data.reindex(day_order)
    heatmap_data = heatmap_data.reindex(
        columns=range(24),
        fill_value=0
    )

    heatmap_data = heatmap_data.fillna(0)

    fig = px.imshow(
        heatmap_data,
        labels={
            "x": "Hour of Day",
            "y": "Day of Week",
            "color": "Number of Trips"
        },
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title="Trip Volume by Day of Week and Hour",
        aspect="auto"
    )

    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week"
    )

    return fig


# ==========================================
# 11. CHART 8: AVERAGE DURATION BY HOUR SPLIT BY USER TYPE
# ==========================================

def create_duration_by_hour_user_type_chart(df):

    average_duration = (
        df.groupby(["hour", "user_type"], as_index=False)
        ["duration_min_clean"]
        .mean()
    )

    average_duration.columns = [
        "hour",
        "user_type",
        "average_duration"
    ]

    average_duration = average_duration.sort_values(
        ["user_type", "hour"]
    )

    fig = px.line(
        average_duration,
        x="hour",
        y="average_duration",
        color="user_type",
        markers=True,
        title="Average Trip Duration by Hour and User Type",
        labels={
            "hour": "Hour of Day",
            "average_duration": "Average Duration (Minutes)",
            "user_type": "User Type"
        }
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        xaxis_title="Hour of Day",
        yaxis_title="Average Duration (Minutes)"
    )

    return fig


# ==========================================
# 12. TEST ALL CHART FUNCTIONS
# ==========================================

if __name__ == "__main__":

    fig1 = create_trips_by_day_chart(df)
    fig1.show()

    fig2 = create_trips_by_hour_chart(df)
    fig2.show()

    fig3 = create_weekday_weekend_chart(df)
    fig3.show()

    fig4 = create_duration_by_day_chart(df)
    fig4.show()

    fig5 = create_average_duration_by_hour_chart(df)
    fig5.show()

    fig6 = create_average_duration_by_day_type_chart(df)
    fig6.show()

    fig7 = create_day_hour_heatmap(df)
    fig7.show()

    fig8 = create_duration_by_hour_user_type_chart(df)
    fig8.show()