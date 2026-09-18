import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://postgres:1234@localhost:5432/gobike_db"
)

# Load data from PostgreSQL
query = """
SELECT *
FROM gobike.dashboard_trips
"""

df = pd.read_sql(query, engine)

print(df.head())
print(df.columns)