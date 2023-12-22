SELECT data,
       SUM(hits_count) AS total_hits_count,
       SUM(visitors_count) AS total_visitors_count,
       SUM(bytes_count) AS total_bytes_count
FROM dashboard_status_codes
GROUP BY data;

    SELECT
        dsc.data,
        SUM(dsc.hits_count) AS total_dashboard_hits,
        SUM(dsc.hits_percent) AS total_hits_percent,
        SUM(dsc.bytes_count) AS total_dashboard_bytes,
        SUM(dsc.bytes_percent) AS total_dashboard_bytes_percent,
        SUM(dsc.visitors_count) AS total_dashboard_visitors,
        SUM(dsc.visitors_percent) AS total_dashboard_visitors_percent,
		isc.data AS items_data,
        SUM(isc.hits_count) AS total_items_hits,
        SUM(isc.hits_percent) AS total_items_hits_percent,
        SUM(isc.bytes_count) AS total_items_bytes,
        SUM(isc.bytes_percent) AS total_items_bytes_percent,
        SUM(isc.visitors_count) AS total_items_visitors_hits,
        SUM(isc.visitors_percent) AS total_items_visitors_percent
    FROM
        dashboard_status_codes dsc
    JOIN
        items_status_codes isc ON dsc.id = isc.id_status_codes
    GROUP BY
        dsc.data;
        
SELECT
    dsc.data AS dashboard_data,
    isc.data AS items_data,
    SUM(isc.hits_count) AS total_items_hits,
    SUM(isc.hits_percent) AS total_items_hits_percent,
    SUM(isc.bytes_count) AS total_items_bytes,
    SUM(isc.bytes_percent) AS total_items_bytes_percent,
    SUM(isc.visitors_count) AS total_items_visitors,
    SUM(isc.visitors_percent) AS total_items_visitors_percent
FROM
    dashboard_status_codes dsc
JOIN
    items_status_codes isc ON dsc.id = isc.id_status_codes
GROUP BY
    dsc.data, isc.data;
    
SELECT
    dsc.data AS dashboard_data,
    SUM(dsc.hits_count) AS total_dashboard_hits,
    SUM(dsc.hits_percent) AS total_dashboard_hits_percent,
    SUM(dsc.bytes_count) AS total_dashboard_bytes,
    SUM(dsc.bytes_percent) AS total_dashboard_bytes_percent,
    SUM(dsc.visitors_count) AS total_dashboard_visitors,
    SUM(dsc.visitors_percent) AS total_dashboard_visitors_percent,
    NULL AS items_data,
    NULL AS total_items_hits,
    NULL AS total_items_hits_percent,
    NULL AS total_items_bytes,
    NULL AS total_items_bytes_percent,
    NULL AS total_items_visitors,
    NULL AS total_items_visitors_percent
FROM
    dashboard_status_codes dsc
GROUP BY
    dsc.data

UNION

SELECT
    dsc.data AS dashboard_data,
    NULL AS total_dashboard_hits,
    NULL AS total_dashboard_hits_percent,
    NULL AS total_dashboard_bytes,
    NULL AS total_dashboard_bytes_percent,
    NULL AS total_dashboard_visitors,
    NULL AS total_dashboard_visitors_percent,
    isc.data AS items_data,
    SUM(isc.hits_count) AS total_items_hits,
    SUM(isc.hits_percent) AS total_items_hits_percent,
    SUM(isc.bytes_count) AS total_items_bytes,
    SUM(isc.bytes_percent) AS total_items_bytes_percent,
    SUM(isc.visitors_count) AS total_items_visitors,
    SUM(isc.visitors_percent) AS total_items_visitors_percent
FROM
    dashboard_status_codes dsc
JOIN
    items_status_codes isc ON dsc.id = isc.id_status_codes
GROUP BY
    dsc.data, isc.data;



