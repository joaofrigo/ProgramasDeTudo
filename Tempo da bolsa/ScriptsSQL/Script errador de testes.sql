-- Script para fazer erros ocorrerem e testa-los
SELECT * FROM dashboard_general;
SELECT * FROM json;
INSERT INTO dashboard_general (json_id, start_date, end_date, date_time, total_requests, valid_requests, failed_requests, generation_time, unique_visitors, unique_files, excluded_hits, unique_referrers, not_found, unique_static_files, log_size, bandwidth, log_path)
VALUES (1, '2023-10-01', '2023-10-31', '2023-10-01 12:00:00', 1000, 800, 200, 0.5, 500, 300, 50, 200, 10, 200, 1024.5, 512, '/var/log/access.log');

