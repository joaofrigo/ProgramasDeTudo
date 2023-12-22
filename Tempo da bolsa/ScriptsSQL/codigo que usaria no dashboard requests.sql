SELECT sum(hits_count), sum(hits_percent), sum(visitors_count), sum(visitors_percent), 
sum(bytes_count) , sum(bytes_percent), method, protocol, data
FROM ntelogs.dashboard_requests GROUP BY data, method, protocol;

Select * from dashboard_general;

SELECT count(data), data from ntelogs.dashboard_requests GROUP BY data;

SELECT bytes_count, bytes_percent FROM ntelogs.dashboard_requests;

SELECT * FROM ntelogs.dashboard_requests;
