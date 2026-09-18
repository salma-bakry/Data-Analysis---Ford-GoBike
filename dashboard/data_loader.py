import pandas as pd
from sqlalchemy import create_engine


# ==========================================
# DATABASE CONNECTION
# ==========================================

engine = create_engine(
    "postgresql+psycopg://postgres:1234@localhost:5432/gobike_db"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_sql(
    "SELECT * FROM gobike.dashboard_trips",
    engine
)


# ==========================================
# DATA PREPARATION
# ==========================================

# Convert date column
df["date"] = pd.to_datetime(df["date"])


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


# Create duration columns
df["duration_min_original"] = df["duration_sec"] / 60

duration_cap = df["duration_min_original"].quantile(0.995)

df["duration_min_clean"] = df["duration_min_original"].clip(
    upper=duration_cap
)


# Create weekend information
df["weekend"] = df["day_of_week"].isin(
    ["Saturday", "Sunday"]
)

df["day_type"] = df["weekend"].map(
    {
        True: "Weekend",
        False: "Weekday"
    }
)


# ==========================================
# FILTER FUNCTION
# ==========================================

def filter_data(
    data,
    start_date,
    end_date,
    user_types,
    genders,
    age_groups,
    duration_range
):
    filtered_df = data.copy()

    # Date filter
    if start_date:
        filtered_df = filtered_df[
            filtered_df["date"] >= pd.to_datetime(start_date)
        ]

    if end_date:
        end_datetime = (
            pd.to_datetime(end_date) + pd.Timedelta(days=1)
        )

        filtered_df = filtered_df[
            filtered_df["date"] < end_datetime
        ]

    # User type filter
    if user_types:
        filtered_df = filtered_df[
            filtered_df["user_type"].isin(user_types)
        ]

    # Gender filter
    if genders:
        filtered_df = filtered_df[
            filtered_df["gender"].isin(genders)
        ]

    # Age group filter
    if age_groups:
        filtered_df = filtered_df[
            filtered_df["age_group"].isin(age_groups)
        ]

    # Duration filter
    if duration_range:
        duration_minutes = filtered_df["duration_sec"] / 60

        filtered_df = filtered_df[
            duration_minutes.between(
                duration_range[0],
                duration_range[1]
            )
        ]

    return filtered_df