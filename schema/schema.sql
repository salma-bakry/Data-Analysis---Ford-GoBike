CREATE SCHEMA IF NOT EXISTS gobike;
SET search_path TO gobike;

CREATE TABLE dim_station (
    station_id   SERIAL PRIMARY KEY,
    station_name VARCHAR(150) NOT NULL,
    latitude     NUMERIC(9,6) NOT NULL,
    longitude    NUMERIC(9,6) NOT NULL
);

CREATE TABLE dim_user (
    user_id      SERIAL PRIMARY KEY,
    birth_year   SMALLINT,
    age          SMALLINT,
    gender       VARCHAR(20),
    user_type    VARCHAR(20) NOT NULL
);


CREATE TABLE dim_time (
    time_id      SERIAL PRIMARY KEY,
    date         DATE NOT NULL,
    hour         SMALLINT NOT NULL CHECK (hour BETWEEN 0 AND 23),
    day          SMALLINT NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_of_week  VARCHAR(10) NOT NULL,
    month        SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    year         SMALLINT NOT NULL
);




CREATE TABLE fact_trips (
    trip_id          BIGSERIAL PRIMARY KEY,
    start_time       TIMESTAMP NOT NULL,
    end_time         TIMESTAMP NOT NULL,
    duration_sec     INTEGER NOT NULL CHECK (duration_sec > 0),
    bike_id          INTEGER NOT NULL,
    start_station_id INTEGER NOT NULL,
    end_station_id   INTEGER NOT NULL,
    user_id          INTEGER NOT NULL,
    time_id          INTEGER NOT NULL,

    CONSTRAINT fk_start_station
        FOREIGN KEY (start_station_id) REFERENCES dim_station(station_id),

    CONSTRAINT fk_end_station
        FOREIGN KEY (end_station_id) REFERENCES dim_station(station_id),

    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES dim_user(user_id),

    CONSTRAINT fk_time
        FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);

CREATE INDEX idx_fact_trips_start_station
    ON fact_trips(start_station_id);

CREATE INDEX idx_fact_trips_end_station
    ON fact_trips(end_station_id);

CREATE INDEX idx_fact_trips_user
    ON fact_trips(user_id);

CREATE INDEX idx_fact_trips_time
    ON fact_trips(time_id);