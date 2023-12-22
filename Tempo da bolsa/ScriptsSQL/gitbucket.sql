CREATE TABLE IF NOT EXISTS items_status_codes(
	id INT AUTO_INCREMENT, PRIMARY KEY (id),
    json_id INT, FOREIGN KEY (json_id) REFERENCES json (id),
    hits_count DOUBLE,
	hits_percent varchar(30),
    visitors_count DOUBLE,
    visitors_percent  varchar(30),
    bytes_count DOUBLE,
    bytes_percent  varchar(30),
    data  varchar(2000)
);