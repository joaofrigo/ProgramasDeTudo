-- DROP TABLE dashboard_general;
DROP TABLE SUAMAE;
DROP TABLE dashboard_visitors;
DROP TABLE dashboard_requests;
DROP TABLE dashboard_general;
DROP TABLE dashboard_static_requests;
DELETE FROM dashboard_requests WHERE id != 0;
DELETE FROM dashboard_general WHERE id != 0;
DELETE FROM json WHERE id != 0; -- isso vai deletar todos os valores do json
DROP TABLE json;

DROP PROCEDURE loop_json;
DROP PROCEDURE loop_json_dashboard_requests;
DROP PROCEDURE loop_json_dashboard_visitors;
DROP PROCEDURE loop_json_dashboard_static_requests;
DROP PROCEDURE loop_json_dashboard_not_found;
DROP PROCEDURE loop_json_dashboard_hosts;
DROP PROCEDURE loop_json_dashboard_os;
DROP PROCEDURE loop_json_dashboard_browsers;
DROP PROCEDURE loop_json_dashboard_visit_time;
DROP PROCEDURE loop_json_dashboard_referring_sites;
DROP PROCEDURE loop_json_dashboard_status_codes;
DROP PROCEDURE loop_json_dashboard_geolocation;


SET GLOBAL innodb_lock_wait_timeout = 180;