CREATE TABLE IF NOT EXISTS ?
(
    ts_processing TIMESTAMP,
    ts_database TIMESTAMP,
    stage_id TEXT,
    population_id TEXT,
    generation INTEGER,
    min_fitness REAL,
    avg_fitness REAL,
    max_fitness REAL
)