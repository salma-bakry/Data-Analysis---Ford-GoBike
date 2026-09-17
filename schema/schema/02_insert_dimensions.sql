CREATE TABLE IF NOT EXISTS staging_trips (
    duration_sec INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    start_station_id NUMERIC,
    start_station_name VARCHAR(150),
    start_station_latitude NUMERIC(9,6),
    start_station_longitude NUMERIC(9,6),
    end_station_id NUMERIC,
    end_station_name VARCHAR(150),
    end_station_latitude NUMERIC(9,6),
    end_station_longitude NUMERIC(9,6),
    bike_id INTEGER,
    user_type VARCHAR(20),
    member_birth_year NUMERIC,
    member_gender VARCHAR(20),
    bike_share_for_all_trip VARCHAR(10),
    hour SMALLINT,
    day_of_week VARCHAR(20),
    weekend BOOLEAN,
    age NUMERIC,
    duration_min NUMERIC
);


INSERT INTO gobike.dim_time (
    date,
    hour,
    day,
    day_of_week,
    month,
    year
)
SELECT DISTINCT
    start_time::DATE,
    EXTRACT(HOUR FROM start_time)::SMALLINT,
    EXTRACT(DAY FROM start_time)::SMALLINT,
    TRIM(TO_CHAR(start_time, 'Day')),
    EXTRACT(MONTH FROM start_time)::SMALLINT,
    EXTRACT(YEAR FROM start_time)::SMALLINT
FROM public.staging_trips
WHERE start_time IS NOT NULL;


-- ---------------------------
-- Load Dimension: Station
-- ---------------------------

INSERT INTO gobike.dim_station (
    station_id,
    station_name,
    latitude,
    longitude
)
SELECT DISTINCT
    station_id,
    station_name,
    latitude,
    longitude
FROM (
    SELECT
        start_station_id::INTEGER AS station_id,
        start_station_name AS station_name,
        start_station_latitude AS latitude,
        start_station_longitude AS longitude
    FROM public.staging_trips
    WHERE start_station_id IS NOT NULL

    UNION

    SELECT
        end_station_id::INTEGER AS station_id,
        end_station_name AS station_name,
        end_station_latitude AS latitude,
        end_station_longitude AS longitude
    FROM public.staging_trips
    WHERE end_station_id IS NOT NULL
) AS stations;

-- ---------------------------
-- Load Dimension: User
-- ---------------------------

INSERT INTO gobike.dim_user (
    birth_year,
    age,
    gender,
    user_type
)
SELECT DISTINCT
    member_birth_year::SMALLINT,
    age::SMALLINT,
    member_gender,
    user_type
FROM public.staging_trips
WHERE user_type IS NOT NULL;


-- ---------------------------
-- Load Fact: Trips
-- ---------------------------

INSERT INTO gobike.fact_trips (
    start_time,
    end_time,
    duration_sec,
    bike_id,
    start_station_id,
    end_station_id,
    user_id,
    time_id
)
SELECT
    s.start_time,
    s.end_time,
    s.duration_sec,
    s.bike_id,
    s.start_station_id::INTEGER,
    s.end_station_id::INTEGER,
    u.user_id,
    t.time_id
FROM public.staging_trips s

JOIN gobike.dim_user u
    ON u.birth_year IS NOT DISTINCT FROM s.member_birth_year::SMALLINT
   AND u.age IS NOT DISTINCT FROM s.age::SMALLINT
   AND u.gender IS NOT DISTINCT FROM s.member_gender
   AND u.user_type = s.user_type

JOIN gobike.dim_time t
    ON t.date = s.start_time::DATE
   AND t.hour = EXTRACT(HOUR FROM s.start_time)::SMALLINT
   AND t.day = EXTRACT(DAY FROM s.start_time)::SMALLINT
   AND t.month = EXTRACT(MONTH FROM s.start_time)::SMALLINT
   AND t.year = EXTRACT(YEAR FROM s.start_time)::SMALLINT

WHERE s.start_time IS NOT NULL
  AND s.end_time IS NOT NULL
  AND s.duration_sec > 0
  AND s.start_station_id IS NOT NULL
  AND s.end_station_id IS NOT NULL;


  SELECT setval(
    pg_get_serial_sequence('gobike.dim_station', 'station_id'),
    COALESCE((SELECT MAX(station_id) FROM gobike.dim_station), 1)
);



