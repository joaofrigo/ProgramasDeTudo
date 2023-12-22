SELECT SUM(d.total_requests) AS soma_valores
FROM (
    SELECT dg.total_requests
    FROM dashboard_general AS dg
    INNER JOIN json AS j ON dg.json_id = j.id
    WHERE j.data BETWEEN '2022-01-01' AND '2023-08-14' 
    ORDER BY dg.id
) AS d;


