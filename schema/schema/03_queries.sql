SET search_path TO gobike;

-- =========================================================
-- Ford GoBike Dashboard - SQL Queries
-- =========================================================


-- =========================================================
-- 0. DASHBOARD BASE VIEW
-- =========================================================
-- This view combines fact and dimension tables.
-- It makes the dashboard queries easier and keeps the ERD clean.

CREATE OR REPLACE VIEW dashboard_trips AS
SELECT
    f.trip_id,
    f.start_time,
    f.end_time,
    f.duration_sec,

    -- Processed duration used by the dashboard
    LEAST(f.duration_sec / 60.0, 57.62633333333312)
        AS duration_min,

    f.bike_id,

    -- Start station
    ss.station_id AS start_station_id,
    ss.station_name AS start_station_name,
    ss.latitude AS start_latitude,
    ss.longitude AS start_longitude,

    -- End station
    es.station_id AS end_station_id,
    es.station_name AS end_station_name,
    es.latitude AS end_latitude,
    es.longitude AS end_longitude,

    -- User information
    u.user_id,
    u.birth_year,
    u.age,
    u.gender,
    u.user_type,

    -- Age group for dashboard filtering
    CASE
        WHEN u.age < 20 THEN 'Under 20'
        WHEN u.age BETWEEN 20 AND 29 THEN '20-29'
        WHEN u.age BETWEEN 30 AND 39 THEN '30-39'
        WHEN u.age BETWEEN 40 AND 49 THEN '40-49'
        WHEN u.age BETWEEN 50 AND 59 THEN '50-59'
        ELSE '60+'
    END AS age_group,

    -- Time information
    t.time_id,
    t.date,
    t.hour,
    t.day,
    t.day_of_week,
    t.month,
    t.year

FROM fact_trips f

JOIN dim_station ss
    ON f.start_station_id = ss.station_id

JOIN dim_station es
    ON f.end_station_id = es.station_id

JOIN dim_user u
    ON f.user_id = u.user_id

JOIN dim_time t
    ON f.time_id = t.time_id;


-- =========================================================
-- 1. OVERVIEW KPI - TOTAL TRIPS
-- =========================================================

SELECT
    COUNT(*) AS total_trips
FROM dashboard_trips;


-- =========================================================
-- 2. OVERVIEW KPI - AVERAGE TRIP DURATION
-- =========================================================

SELECT
    ROUND(AVG(duration_min), 2) AS avg_duration_minutes
FROM dashboard_trips;


-- =========================================================
-- 3. OVERVIEW KPI - ACTIVE USERS
-- =========================================================
-- Active users = users who made at least one trip.

SELECT
    COUNT(DISTINCT user_id) AS active_users
FROM dashboard_trips;


-- =========================================================
-- 4. OVERVIEW KPI - MOST POPULAR START STATION
-- =========================================================

SELECT
    start_station_id,
    start_station_name,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    start_station_id,
    start_station_name
ORDER BY total_trips DESC
LIMIT 1;


-- =========================================================
-- 5. TIME ANALYSIS - TRIPS BY DAY OF WEEK
-- =========================================================

SELECT
    day_of_week,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY day_of_week
ORDER BY
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- =========================================================
-- 6. TIME ANALYSIS - TRIPS BY HOUR
-- =========================================================

SELECT
    hour,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY hour
ORDER BY hour;


-- =========================================================
-- 7. TIME ANALYSIS - TRIPS BY DATE
-- =========================================================

SELECT
    date,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY date
ORDER BY date;


-- =========================================================
-- 8. TIME ANALYSIS - TRIPS BY MONTH
-- =========================================================

SELECT
    year,
    month,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    year,
    month
ORDER BY
    year,
    month;


-- =========================================================
-- 9. TIME ANALYSIS - AVERAGE DURATION BY HOUR
-- =========================================================

SELECT
    hour,
    ROUND(AVG(duration_min), 2) AS avg_duration_minutes
FROM dashboard_trips
GROUP BY hour
ORDER BY hour;


-- =========================================================
-- 10. USER ANALYSIS - SUBSCRIBER VS CUSTOMER
-- =========================================================

SELECT
    user_type,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY user_type
ORDER BY total_trips DESC;


-- =========================================================
-- 11. USER ANALYSIS - GENDER
-- =========================================================

SELECT
    gender,
    COUNT(*) AS total_trips
FROM dashboard_trips
WHERE gender IS NOT NULL
GROUP BY gender
ORDER BY total_trips DESC;


-- =========================================================
-- 12. USER ANALYSIS - AGE GROUP
-- =========================================================

SELECT
    age_group,
    COUNT(*) AS total_trips
FROM dashboard_trips
WHERE age IS NOT NULL
GROUP BY age_group
ORDER BY
    CASE age_group
        WHEN 'Under 20' THEN 1
        WHEN '20-29' THEN 2
        WHEN '30-39' THEN 3
        WHEN '40-49' THEN 4
        WHEN '50-59' THEN 5
        WHEN '60+' THEN 6
    END;


-- =========================================================
-- 13. USER ANALYSIS - AVERAGE DURATION BY USER TYPE
-- =========================================================

SELECT
    user_type,
    ROUND(AVG(duration_min), 2) AS avg_duration_minutes
FROM dashboard_trips
GROUP BY user_type
ORDER BY avg_duration_minutes DESC;


-- =========================================================
-- 14. USER ANALYSIS - USER TYPE BY WEEKDAY
-- =========================================================

SELECT
    day_of_week,
    user_type,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    day_of_week,
    user_type
ORDER BY
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END,
    user_type;


-- =========================================================
-- 15. USER ANALYSIS - GENDER BY USER TYPE
-- =========================================================

SELECT
    user_type,
    gender,
    COUNT(*) AS total_trips
FROM dashboard_trips
WHERE gender IS NOT NULL
GROUP BY
    user_type,
    gender
ORDER BY
    user_type,
    total_trips DESC;


-- =========================================================
-- 16. STATION ANALYSIS - TOP 10 START STATIONS
-- =========================================================

SELECT
    start_station_id AS station_id,
    start_station_name AS station_name,
    start_latitude AS latitude,
    start_longitude AS longitude,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    start_station_id,
    start_station_name,
    start_latitude,
    start_longitude
ORDER BY total_trips DESC
LIMIT 10;


-- =========================================================
-- 17. STATION ANALYSIS - TOP 10 END STATIONS
-- =========================================================

SELECT
    end_station_id AS station_id,
    end_station_name AS station_name,
    end_latitude AS latitude,
    end_longitude AS longitude,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    end_station_id,
    end_station_name,
    end_latitude,
    end_longitude
ORDER BY total_trips DESC
LIMIT 10;


-- =========================================================
-- 18. STATION ANALYSIS - STATION USAGE
-- =========================================================
-- Useful for the map.
-- Shows how many trips started and ended at each station.

SELECT
    station_id,
    station_name,
    latitude,
    longitude,
    SUM(departures) AS departures,
    SUM(arrivals) AS arrivals,
    SUM(departures + arrivals) AS total_activity
FROM (

    SELECT
        start_station_id AS station_id,
        start_station_name AS station_name,
        start_latitude AS latitude,
        start_longitude AS longitude,
        COUNT(*) AS departures,
        0::BIGINT AS arrivals
    FROM dashboard_trips
    GROUP BY
        start_station_id,
        start_station_name,
        start_latitude,
        start_longitude

    UNION ALL

    SELECT
        end_station_id AS station_id,
        end_station_name AS station_name,
        end_latitude AS latitude,
        end_longitude AS longitude,
        0::BIGINT AS departures,
        COUNT(*) AS arrivals
    FROM dashboard_trips
    GROUP BY
        end_station_id,
        end_station_name,
        end_latitude,
        end_longitude

) station_activity

GROUP BY
    station_id,
    station_name,
    latitude,
    longitude

ORDER BY total_activity DESC;


-- =========================================================
-- 19. ROUTE ANALYSIS - TOP 10 POPULAR ROUTES
-- =========================================================

SELECT
    start_station_id,
    start_station_name,
    end_station_id,
    end_station_name,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    start_station_id,
    start_station_name,
    end_station_id,
    end_station_name
ORDER BY total_trips DESC
LIMIT 10;


-- =========================================================
-- 20. ROUTE ANALYSIS - TOP 10 ROUTES WITH COORDINATES
-- =========================================================
-- This query can be used later for a map showing trip flows.

SELECT
    start_station_name,
    start_latitude,
    start_longitude,
    end_station_name,
    end_latitude,
    end_longitude,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    start_station_name,
    start_latitude,
    start_longitude,
    end_station_name,
    end_latitude,
    end_longitude
ORDER BY total_trips DESC
LIMIT 10;


-- =========================================================
-- 21. TRIP DURATION DISTRIBUTION
-- =========================================================

SELECT
    CASE
        WHEN duration_min < 5 THEN 'Under 5 min'
        WHEN duration_min < 10 THEN '5-10 min'
        WHEN duration_min < 20 THEN '10-20 min'
        WHEN duration_min < 30 THEN '20-30 min'
        WHEN duration_min < 45 THEN '30-45 min'
        ELSE '45+ min'
    END AS duration_group,

    COUNT(*) AS total_trips

FROM dashboard_trips

GROUP BY duration_group

ORDER BY
    CASE duration_group
        WHEN 'Under 5 min' THEN 1
        WHEN '5-10 min' THEN 2
        WHEN '10-20 min' THEN 3
        WHEN '20-30 min' THEN 4
        WHEN '30-45 min' THEN 5
        WHEN '45+ min' THEN 6
    END;


-- =========================================================
-- 22. TRIP DURATION BY USER TYPE
-- =========================================================

SELECT
    user_type,
    CASE
        WHEN duration_min < 5 THEN 'Under 5 min'
        WHEN duration_min < 10 THEN '5-10 min'
        WHEN duration_min < 20 THEN '10-20 min'
        WHEN duration_min < 30 THEN '20-30 min'
        WHEN duration_min < 45 THEN '30-45 min'
        ELSE '45+ min'
    END AS duration_group,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY
    user_type,
    duration_group
ORDER BY
    user_type,
    MIN(duration_min);


-- =========================================================
-- 23. BIKE USAGE - TOP 10 MOST USED BIKES
-- =========================================================

SELECT
    bike_id,
    COUNT(*) AS total_trips
FROM dashboard_trips
GROUP BY bike_id
ORDER BY total_trips DESC
LIMIT 10;


-- =========================================================
-- 24. MAP DATA - ALL STATIONS
-- =========================================================
-- Main query for the interactive station map.

SELECT
    station_id,
    station_name,
    latitude,
    longitude
FROM dim_station
ORDER BY station_id;


-- =========================================================
-- 25. MAP DATA - STATION ACTIVITY
-- =========================================================
-- Recommended query for a bubble/scatter map.
-- Bubble size can represent total_activity.

SELECT
    station_id,
    station_name,
    latitude,
    longitude,
    SUM(departures) AS departures,
    SUM(arrivals) AS arrivals,
    SUM(departures + arrivals) AS total_activity
FROM (

    SELECT
        start_station_id AS station_id,
        start_station_name AS station_name,
        start_latitude AS latitude,
        start_longitude AS longitude,
        COUNT(*) AS departures,
        0::BIGINT AS arrivals
    FROM dashboard_trips
    GROUP BY
        start_station_id,
        start_station_name,
        start_latitude,
        start_longitude

    UNION ALL

    SELECT
        end_station_id AS station_id,
        end_station_name AS station_name,
        end_latitude AS latitude,
        end_longitude AS longitude,
        0::BIGINT AS departures,
        COUNT(*) AS arrivals
    FROM dashboard_trips
    GROUP BY
        end_station_id,
        end_station_name,
        end_latitude,
        end_longitude

) station_activity

GROUP BY
    station_id,
    station_name,
    latitude,
    longitude

ORDER BY total_activity DESC;


-- =========================================================
-- 26. DASHBOARD FILTER OPTIONS - USER TYPES
-- =========================================================

SELECT DISTINCT
    user_type
FROM dashboard_trips
ORDER BY user_type;


-- =========================================================
-- 27. DASHBOARD FILTER OPTIONS - GENDER
-- =========================================================

SELECT DISTINCT
    gender
FROM dashboard_trips
WHERE gender IS NOT NULL
ORDER BY gender;


-- =========================================================
-- 28. DASHBOARD FILTER OPTIONS - AGE GROUP
-- =========================================================

SELECT DISTINCT
    age_group
FROM dashboard_trips
WHERE age IS NOT NULL
ORDER BY
    CASE age_group
        WHEN 'Under 20' THEN 1
        WHEN '20-29' THEN 2
        WHEN '30-39' THEN 3
        WHEN '40-49' THEN 4
        WHEN '50-59' THEN 5
        WHEN '60+' THEN 6
    END;


-- =========================================================
-- 29. DASHBOARD DATE RANGE
-- =========================================================

SELECT
    MIN(date) AS min_date,
    MAX(date) AS max_date
FROM dashboard_trips;


-- =========================================================
-- 30. DATASET SUMMARY
-- =========================================================

SELECT
    COUNT(*) AS total_trips,
    COUNT(DISTINCT user_id) AS active_users,
    COUNT(DISTINCT bike_id) AS unique_bikes,
    COUNT(DISTINCT start_station_id) AS start_stations,
    COUNT(DISTINCT end_station_id) AS end_stations,
    ROUND(AVG(duration_min), 2) AS avg_duration_minutes
FROM dashboard_trips;