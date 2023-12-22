CREATE TABLE IF NOT EXISTS items_status_codes(
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    id_status_codes INT, FOREIGN KEY (id_status_codes) REFERENCES dashboard_status_codes (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  longtext
);

SELECT count(*), b.data FROM items_status_codes as a inner join dashboard_status_codes as b on a.id_status_codes = b.id GROUP BY b.data;

