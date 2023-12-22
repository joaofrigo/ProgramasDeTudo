create table if not exists dashboard_general (
json_id INT, FOREIGN KEY(id) REFERENCES json (id), 
id INT AUTO_INCREMENT, PRIMARY KEY (id),
start_date varchar(120),
end_date varchar(120),
date_time varchar(120),
total_requests double,
valid_requests double,
failed_requests double,
generation_time double,
unique_visitors double,
unique_files double, -- Requested Files
excluded_hits double,
unique_referrers double,
not_found double,
unique_static_files double,
log_size double,
bandwidth double,
log_path varchar(120)
);

insert into dashboard_general (total_requests, valid_requests, failed_requests, not_found, unique_visitors,
unique_referrers, generation_time, unique_static_files, excluded_hits, log_size, bandwidth, unique_files,
start_date, end_date, date_time, log_path)
SELECT
    JSON_EXTRACT(json.json, '$.general.total_requests'),
    JSON_EXTRACT(json.json, '$.general.valid_requests'),
	JSON_EXTRACT(json.json, '$.general.failed_requests'),
    JSON_EXTRACT(json.json, '$.general.unique_not_found'),
    JSON_EXTRACT(json.json, '$.general.unique_visitors'),
    JSON_EXTRACT(json.json, '$.general.unique_referrers'),
    JSON_EXTRACT(json.json, '$.general.generation_time'),
    JSON_EXTRACT(json.json, '$.general.unique_static_files'),
    JSON_EXTRACT(json.json, '$.general.excluded_hits'),
    JSON_EXTRACT(json.json, '$.general.log_size'),
    JSON_EXTRACT(json.json, '$.general.bandwidth'),
    JSON_EXTRACT(json.json, '$.general.unique_files'),
    JSON_EXTRACT(json.json, '$.general.start_date'),
    JSON_EXTRACT(json.json, '$.general.end_date'),
    JSON_EXTRACT(json.json, '$.general.date_time'),
    JSON_EXTRACT(json.json, '$.general.log_path')
FROM json;

UPDATE dashboard_general
SET json_id = (SELECT id FROM json WHERE dashboard_general.id = json.id);
