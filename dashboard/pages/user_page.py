from dash import register_page, html, dcc, Input, Output, callback

from data_loader import df, filter_data

from user_analysis import (
    create_user_type_chart,
    create_gender_distribution_chart,
    create_age_group_chart,
    create_user_type_gender_chart,
    create_user_type_age_group_chart
)


# ==========================================
# REGISTER PAGE
# ==========================================

register_page(
    __name__,
    path="/user-analysis",
    name="User Analysis"
)


# ==========================================
# PAGE LAYOUT
# ==========================================

layout = html.Div(
    children=[
        html.H2(
            "User Analysis",
            className="page-heading"
        ),

        html.Div(
            className="charts-container",
            children=[
                dcc.Graph(id="user-type-chart"),

                dcc.Graph(id="gender-distribution-chart"),

                dcc.Graph(id="age-group-chart"),

                dcc.Graph(id="user-type-gender-chart"),

                dcc.Graph(id="user-type-age-group-chart")
            ]
        )
    ]
)


# ==========================================
# UPDATE CHARTS
# ==========================================

@callback(
    Output("user-type-chart", "figure"),
    Output("gender-distribution-chart", "figure"),
    Output("age-group-chart", "figure"),
    Output("user-type-gender-chart", "figure"),
    Output("user-type-age-group-chart", "figure"),

    Input("start-date-filter", "date"),
    Input("end-date-filter", "date"),
    Input("user-type-filter", "value"),
    Input("gender-filter", "value"),
    Input("age-group-filter", "value"),
    Input("duration-filter", "value")
)
def update_user_charts(
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
        create_user_type_chart(filtered_df),
        create_gender_distribution_chart(filtered_df),
        create_age_group_chart(filtered_df),
        create_user_type_gender_chart(filtered_df),
        create_user_type_age_group_chart(filtered_df)
    )