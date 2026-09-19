import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

#  DATABASE CONNECTION

engine = create_engine(
    "postgresql+psycopg://postgres:1234@localhost:5432/gobike_db"
)
# LOAD DATA FROM POSTGRESQL

query = """
SELECT *
FROM gobike.dashboard_trips
"""
df = pd.read_sql(query, engine)

#  DATA PREPARATION
# Create age groups
def create_age_group(age):
    if pd.isna(age):
        return "Unknown"
    elif age < 20:
        return "Under 20"
    elif age < 30:
        return "20-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    else:
        return "60+"


df["age_group"] = df["age"].apply(create_age_group)


# Define the correct age group order
age_order = [
    "Under 20",
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60+",
    "Unknown"
]

#  CHART 1: USER TYPE DISTRIBUTION

def create_user_type_chart(df):

    users_by_type = (
        df["user_type"]
        .value_counts()
        .reset_index()
    )

    users_by_type.columns = [
        "user_type",
        "trip_count"
    ]

    fig = px.pie(
        users_by_type,
        names="user_type",
        values="trip_count",
        title="User Type Distribution",
        hole=0.4
    )

    fig.update_traces(
        textinfo="percent+label",
         marker_colors=[
        "#fbb4ae",
        "#b3cde3",
        "#ccebc5",
        "#decbe4",
        "#fed9a6",
        "#ffffcc",
        "#e5d8bd",
        "#fddaec"
    ],
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Trips: %{value}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    return fig
#  CHART 2: GENDER DISTRIBUTION

def create_gender_distribution_chart(df):

    trips_by_gender = (
        df["gender"]
        .value_counts()
        .reset_index()
    )

    trips_by_gender.columns = [
        "gender",
        "trip_count"
    ]

    fig = px.bar(
        trips_by_gender,
        x="gender",
        y="trip_count",
        title="Number of Trips by Gender",
        labels={
            "gender": "Gender",
            "trip_count": "Number of Trips"
        },
        text="trip_count",
        color="gender", 
        color_discrete_sequence=[ "#b3cde3",
        "#fbb4ae"] ,#blue and pink
    )

    fig.update_traces(
        textposition="outside",
        
    )

    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Number of Trips",
        showlegend=False
    )

    return fig

#  CHART 3: AGE GROUP DISTRIBUTION

def create_age_group_chart(df):

    trips_by_age_group = (
        df["age_group"]
        .value_counts()
        .reindex(age_order, fill_value=0)
        .reset_index()
    )

    trips_by_age_group.columns = [
        "age_group",
        "trip_count"
    ]

    fig = px.bar(
        trips_by_age_group,
        x="age_group",
        y="trip_count",
        title="Number of Trips by Age Group",
        labels={
            "age_group": "Age Group",
            "trip_count": "Number of Trips"
        },
        text="trip_count",
        color="age_group", color_discrete_sequence=[ "#b3cde3", 
         "#ccebc5",  "#decbe4", "#fed9a6", "#fbb4ae"  ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Number of Trips"
    )

    return fig

# CHART 4: USER TYPE BY GENDER

def create_user_type_gender_chart(df):

    trips_by_type_gender = (
        df.groupby(
            ["gender", "user_type"],
            as_index=False
        )
        .size()
    )

    trips_by_type_gender.columns = [
        "gender",
        "user_type",
        "trip_count"
    ]

    fig = px.bar(
        trips_by_type_gender,
        x="gender",
        y="trip_count",
        color="user_type",
        barmode="group",
        title="Number of Trips by Gender and User Type",
        labels={
            "gender": "Gender",
            "trip_count": "Number of Trips",
            "user_type": "User Type"
        },
        text="trip_count",
        color_discrete_sequence=[
            "#b3cde3",  #blue
            "#decbe4",  #purple
            "#ccebc5"   #green
        ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Number of Trips"
    )

    return fig

# CHART 5: USER TYPE BY AGE GROUP


def create_user_type_age_group_chart(df):

    trips_by_type_age = (
        df.groupby(
            ["age_group", "user_type"],
            as_index=False
        )
        .size()
    )

    trips_by_type_age.columns = [
        "age_group",
        "user_type",
        "trip_count"
    ]

    trips_by_type_age["age_group"] = pd.Categorical(
        trips_by_type_age["age_group"],
        categories=age_order,
        ordered=True
    )

    trips_by_type_age = trips_by_type_age.sort_values(
        "age_group"
    )

    fig = px.bar(
        trips_by_type_age,
        x="age_group",
        y="trip_count",
        color="user_type",
        barmode="group",
        title="Number of Trips by Age Group and User Type",
        labels={
            "age_group": "Age Group",
            "trip_count": "Number of Trips",
            "user_type": "User Type"
        },
        text="trip_count",
        color_discrete_sequence=[
            "#b3cde3",  # pastel blue
            "#decbe4",  # pastel purple
            "#ccebc5"   # pastel green
        ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Number of Trips"
    )

    return fig

# TEST ALL CHART FUNCTIONS

if __name__ == "__main__":

    fig1 = create_user_type_chart(df)
    fig1.show()

    fig2 = create_gender_distribution_chart(df)
    fig2.show()

    fig3 = create_age_group_chart(df)
    fig3.show()

    fig4 = create_user_type_gender_chart(df)
    fig4.show()

    fig5 = create_user_type_age_group_chart(df)
    fig5.show()