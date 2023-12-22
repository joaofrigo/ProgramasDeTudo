select * from json;
show tables;
UPDATE json SET json = JSON_OBJECT('unicornio', 1) WHERE data = '2020-04-21 13:04:49';

create table dashboard_general (
id INT,
total_requests double,
valid_requests double,
failed_requests double,
not_found double,
unique_visitors double,
unique_referrers double,
generation_time double,
unique_static_files double,
excluded_hits double,
log_size double,
bandwith double,
requested_files double
);

drop table dashboard_general;
delete from dashboard_general;

show tables;
select * from dashboard_general;

alter table dashboard_general
add primary key (id);

alter table dashboard_general
modify id INT AUTO_INCREMENT;

SELECT data FROM json WHERE data = 15-02-2002;

select ID, data 
from json 
where data != 0;

alter table json add data datetime NOT NULL;
alter table json change DATA data datetime NOT NULL;
alter table json change IDJson id INT;
alter table json change ID id INT;
alter table json ADD PRIMARY KEY (id);
alter table json modify id INT AUTO_INCREMENT;

alter table json change Json json json;
alter table json modify json json NOT NULL;
 
alter table json change URL url varchar(45);
alter table json modify url varchar(60) NOT NULL;



