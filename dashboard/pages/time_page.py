from dash import register_page, html, dcc, Input, Output, callback

from data_loader import df, filter_data

from time_analysis import (
    create_trips_by_day_chart,
    create_trips_by_hour_chart,
    create_weekday_weekend_chart,
    create_duration_by_day_chart,
    create_average_duration_by_hour_chart,
    create_average_duration_by_day_type_chart,
    create_day_hour_heatmap,
    create_duration_by_hour_user_type_chart
)


# Register the page
register_page(
    __name__,
    path="/time-analysis",
    name="Time Analysis"
)

# PAGE LAYOUT
layout = html.Div(
    children=[
        html.H2(
            "Time Analysis",
            className="page-heading"
        ),

        html.Div(
            className="charts-container",
            children=[
                dcc.Graph(id="trips-by-day-chart"),
                dcc.Graph(id="trips-by-hour-chart"),
                dcc.Graph(id="weekday-weekend-chart"),
                dcc.Graph(id="duration-by-day-chart"),
                dcc.Graph(id="average-duration-by-hour-chart"),
                dcc.Graph(id="average-duration-by-day-type-chart"),
                dcc.Graph(id="day-hour-heatmap"),
                dcc.Graph(id="duration-by-hour-user-type-chart")
            ]
        )
    ]
)

# UPDATE CHARTS WHEN FILTERS CHANGE
@callback(
    Output("trips-by-day-chart", "figure"),
    Output("trips-by-hour-chart", "figure"),
    Output("weekday-weekend-chart", "figure"),
    Output("duration-by-day-chart", "figure"),
    Output("average-duration-by-hour-chart", "figure"),
    Output("average-duration-by-day-type-chart", "figure"),
    Output("day-hour-heatmap", "figure"),
    Output("duration-by-hour-user-type-chart", "figure"),

    Input("start-date-filter", "date"),
    Input("end-date-filter", "date"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("duration-filter", "value")
)
def update_time_charts(
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

    return (
        create_trips_by_day_chart(filtered_df),
        create_trips_by_hour_chart(filtered_df),
        create_weekday_weekend_chart(filtered_df),
        create_duration_by_day_chart(filtered_df),
        create_average_duration_by_hour_chart(filtered_df),
        create_average_duration_by_day_type_chart(filtered_df),
        create_day_hour_heatmap(filtered_df),
        create_duration_by_hour_user_type_chart(filtered_df)
    )