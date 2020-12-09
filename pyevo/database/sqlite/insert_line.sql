INSERT INTO ?
(
    ts_processing,
    ts_database,
    stage_id,
    population_id,
    generation,
    min_fitness,
    avg_fitness,
    max_fitness
)
VALUES
(
    ?,
    strftime('%Y-%m-%d %H:%M:%S', 'now'),
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
)