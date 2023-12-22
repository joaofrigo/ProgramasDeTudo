SELECT * FROM dashboard_visitors;
SELECT * FROM dashboard_general;
SELECT * FROM dashboard_requests;
SELECT * FROM dashboard_status_codes;
SELECT * FROM items_status_codes;
select id from dashboard_requests where id<0;
SELECT * FROM json;
SELECT id FROM dashboard_requests;
SELECT id FROM dashboard_general WHERE id > 0;
SELECT sum(hits_count), sum(hits_percent), sum(visitors_count), sum(visitors_percent), 
    sum(bytes_count) , sum(bytes_percent), data, method, protocol
    FROM ntelogs.dashboard_requests GROUP BY data, method, protocol;
SELECT * FROM json;
-- LIMIT 10;
SHOW TABLES;

SELECT hits_percent from dashboard_requests;
SELECT id from json;
ALTER TABLE dashboard_visitors AUTO_INCREMENT = 1;
DELETE FROM dashboard_visitors WHERE id != -1;