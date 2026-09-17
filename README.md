# Ford-GoBike-February-2019---DataSet
# Ford GoBike Data Analysis

## Project Overview

This project analyzes the Ford GoBike February 2019 dataset.

It includes:

- Data preprocessing and cleaning
- Exploratory Data Analysis (EDA)
- PostgreSQL database
- Star-schema design
- SQL queries for dashboard development

---

## Project Structure

```text
Data-Analysis---Ford-GoBike/
│
├── preprocessing/
│   └── ford_gobike_cleaned.csv
│
├── schema/
│   └── schema/
│       ├── schema.sql
│       ├── 02_insert_dimensions.sql
│       └── 03_queries.sql
│
├── dashboard/
│   └── ...
│
└── README.md
```

---

## PostgreSQL Database

Database name:

```text
gobike_db
```

Schema:

```text
gobike
```

The database contains:

- `dim_time`
- `dim_station`
- `dim_user`
- `fact_trips`
- `dashboard_trips` (view)

### Data Summary

| Table | Rows |
|---|---:|
| dim_time | 672 |
| dim_station | 329 |
| dim_user | 311 |
| fact_trips | 183,138 |

---

# Database Setup

## 1. Download the Database Dump

Download:

```text
gobike_db.dump
```

from the following link:

**Database Dump:**  
<https://drive.google.com/file/d/1-C2nKn3wjoXzYkrTSXO0tJKuWLRKQYSV/view?usp=sharing>

After downloading, place the file somewhere accessible, for example:

```text
/tmp/gobike_db.dump
```

---

## 2. Create the Database

Make sure PostgreSQL is installed and running.

Create the database:

```bash
createdb gobike_db
```

If needed:

```bash
sudo -u postgres createdb gobike_db
```

---

## 3. Restore the Database

Run:

```bash
pg_restore -d gobike_db /tmp/gobike_db.dump
```

If needed:

```bash
sudo -u postgres pg_restore -d gobike_db /tmp/gobike_db.dump
```

---

## 4. Verify the Database

Connect:

```bash
psql -d gobike_db
```

Check the tables:

```sql
\dt gobike.*
```

Check the number of trips:

```sql
SELECT COUNT(*) 
FROM gobike.fact_trips;
```

Expected result:

```text
183138
```

---

# Dashboard

The dashboard can connect to the PostgreSQL database using:

```text
Host: localhost
Port: 5432
Database: gobike_db
Schema: gobike
```

The dashboard should use the prepared view:

```sql
gobike.dashboard_trips
```

Example:

```sql
SELECT *
FROM gobike.dashboard_trips
LIMIT 10;
```

---

## Dashboard Queries

Dashboard-related SQL queries are available in:

```text
schema/schema/03_queries.sql
```

The queries support:

- Total trips
- Average trip duration
- Active users
- Trips by weekday
- Trips by hour
- Trips by month/date
- User type analysis
- Gender analysis
- Age groups
- Top start/end stations
- Popular routes
- Station activity
- Map data
- Dashboard filters

---

## Running the Dashboard

### Streamlit

```bash
streamlit run dashboard/app.py
```

### Plotly Dash

```bash
python dashboard/app.py
```

Use the URL displayed in the terminal to open the dashboard.

---

## Important

The PostgreSQL dump is shared separately from the GitHub repository.

Do not store database passwords in GitHub.

---

## Authors

DEPI AI – Data Analysis Team

Project: Ford GoBike Data Analysis
