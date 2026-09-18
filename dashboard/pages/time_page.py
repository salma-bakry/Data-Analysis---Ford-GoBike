from dash import register_page, html, dcc

from time_analysis import (
    df,
    create_trips_by_day_chart,
    create_trips_by_hour_chart,
    create_weekday_weekend_chart,
    create_duration_by_day_chart,
    create_average_duration_by_hour_chart,
    create_average_duration_by_day_type_chart,
    create_day_hour_heatmap,
    create_duration_by_hour_user_type_chart
)

register_page(
    __name__,
    path="/time-analysis",
    name="Time Analysis"
)


layout = html.Div(
    children=[
        html.H2(
            "Time Analysis",
            className="page-heading"
        ),

        html.Div(
            children=[
                dcc.Graph(
                    figure=create_trips_by_day_chart(df)
                ),

                dcc.Graph(
                    figure=create_trips_by_hour_chart(df)
                ),

                dcc.Graph(
                    figure=create_weekday_weekend_chart(df)
                ),

                dcc.Graph(
                    figure=create_duration_by_day_chart(df)
                ),

                dcc.Graph(
                    figure=create_average_duration_by_hour_chart(df)
                ),

                dcc.Graph(
                    figure=create_average_duration_by_day_type_chart(df)
                ),

                dcc.Graph(
                    figure=create_day_hour_heatmap(df)
                ),

                dcc.Graph(
                    figure=create_duration_by_hour_user_type_chart(df)
                )
            ],
            className="charts-container"
        )
    ]
)