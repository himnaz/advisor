CREATE TABLE pre_prod_20_silver.silver.address (
address_id string,
address_line_1 varchar(35),
address_line_2 varchar(35),
address_line_3 varchar(35),
address_line_4 varchar(35),
address_line_5 varchar(35),
country varchar(35),
postcode varchar(10),
PRIMARY KEY (address_id)
);


CREATE TABLE pre_prod_20_silver.silver.business (
business_id varchar(7),
business_legal_name varchar(255),
business_segment varchar(100),
business_trading_name varchar(255),
PRIMARY KEY (business_id)
);


CREATE TABLE pre_prod_20_silver.silver.staff (
agent_category_code varchar(8),
agent_type_code tinyint,
channel varchar(7),
date_joined_partnership datetime,
date_left_partnership datetime,
dob datetime,
email varchar(50),
first_name varchar(60),
gender varchar(1),
last_name varchar(60),
licence_number varchar(50),
mobile_telephone varchar(20),
nationality varchar(50),
ni_number varchar(15),
notice_given datetime,
pdm varchar(100),
pdm_area varchar(100),
portal_code varchar(20),
region varchar(100),
salutation varchar(35),
staff_fullname varchar(255),
staff_id varchar(7),
telephone_number varchar(30),
title varchar(35)
);


CREATE TABLE pre_prod_20_silver.silver.staff_address (
address_id string,
staff_address_id string,
staff_address_source string,
staff_address_type string,
staff_id string,
PRIMARY KEY (staff_address_id)
);


CREATE TABLE pre_prod_20_silver.silver.staff_network_hierarchy (
parent_staff_id int,
parent_staff_id string,
parent_staff_role string,
staff_id string,
staff_network_hierarchy_id string,
staff_role string,
PRIMARY KEY (staff_network_hierarchy_id,staff_id)
);


CREATE TABLE pre_prod_20_silver.silver.staff_position (
business_id varchar(50),
date_joined_firm datetime,
date_left_firm datetime,
employment_status varchar(50),
firm_supervisor_id varchar(50),
firm_supervisor_name varchar(50),
insight_contract_status varchar(50),
is_seller_role varchar(1),
job_title varchar(255),
principal_role_start_date datetime,
reason_for_leaving varchar100),
seller_type int,
staff_position_id string,
PRIMARY KEY (staff_position_id,business_id)
);


CREATE TABLE pre_prod_20_silver.silver.staff_transformations (
agent_category_description varchar(50),
ar_agent_type varchar(50),
business_area varchar(12),
business_development_manager varchar(50),
cf30_status varchar(100),
competency_achieved_date datetime,
gives_advice varchar(1),
is_asm varchar(50),
is_esm varchar(50),
is_principle varchar(50),
is_supervisor varchar(50),
months_active int,
new_experienced varchar(11),
panel varchar(100),
recruitment_source varchar(14),
staff_id string,
swift_status varchar(20),
PRIMARY KEY (staff_id)
);



ALTER TABLE pre_prod_20_silver.silver.staff_address ADD CONSTRAINT sa1_staff_address_address FOREIGN KEY (address_id) REFERENCES pre_prod_20_silver.silver.address(address_id);

ALTER TABLE pre_prod_20_silver.silver.staff_address ADD CONSTRAINT ss1_staff_address_staff FOREIGN KEY (staff_id) REFERENCES pre_prod_20_silver.silver.staff(staff_id);

ALTER TABLE pre_prod_20_silver.silver.staff_network_hierarchy ADD CONSTRAINT ss3_staff_network_hierarchy_staff FOREIGN KEY (staff_id) REFERENCES pre_prod_20_silver.silver.staff(staff_id);

ALTER TABLE pre_prod_20_silver.silver.staff_position ADD CONSTRAINT sb1_staff_position_business FOREIGN KEY (business_id) REFERENCES pre_prod_20_silver.silver.business(business_id);

ALTER TABLE pre_prod_20_silver.silver.staff_position ADD CONSTRAINT ss2_staff_position_staff FOREIGN KEY (staff_id) REFERENCES pre_prod_20_silver.silver.staff(staff_id);

ALTER TABLE pre_prod_20_silver.silver.staff_transformations ADD CONSTRAINT ss4_staff_transformations_staff FOREIGN KEY (staff_id) REFERENCES pre_prod_20_silver.silver.staff(staff_id);
