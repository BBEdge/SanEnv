-- DROP TABLE IF EXISTS swtypes;

CREATE TABLE IF NOT EXISTS swtypes(
    sw_type_id int not null primary key,
    sw_type_desc character varying(12) not null,
    sw_type_image text not null
)

-- /static/images/dcx.png


INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (62, 'DCX', '/static/images/dcx.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (83, '7800', '/static/images/7800.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (109, '6510', '/static/images/6510.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (118, '6505', '/static/images/6505.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (120, 'DCX 8510-8', '/static/images/8510-8.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (121, 'DCX 8510-4', '/static/images/8510-4.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (133, '6520', '/static/images/6510.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (148, '7840', '/static/images/7840.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (165, 'X6-4', '/static/images/x6-4.png');
INSERT INTO swtypes (sw_type_id, sw_type_desc, sw_type_image) VALUES (166, 'X6-8', '/static/images/x6-8.png');

SELECT * FROM swtypes;

-- DROP TABLE IF EXISTS switch;
CREATE TABLE IF NOT EXISTS switch(
    switch_id BIGSERIAL not null primary key,
    sw_date date NOT NULL,
    sw_name character varying(16) not null,
    sw_type int not null,
    sw_domain int not null ,
    sw_id character varying(6) UNIQUE not null,
    sw_wwn character varying(24) not null,
    sw_fid character varying(3)
)

-- DROP TABLE IF EXISTS ports_status;
CREATE TABLE IF NOT EXISTS ports_status(
    switch_id int not null references switch(switch_id),
    p_date character varying(16),
    p_index int not null,
    p_slop int not null,
    p_port int not null,
    p_addr character varying(6) not null,
    p_speed int not null,
    p_state character varying(8) not null,
    p_proto character varying(100)
)

-- DROP TABLE IF EXISTS port_errors;
CREATE TABLE IF NOT EXISTS port_errors(
    switch_id int not null references switch(switch_id),
    p_date character varying(16),
    p_index int,
    p_ftx character varying(16),
    p_frx character varying(16),
    p_enc_in character varying(16),
    p_crc_err character varying(16),
    p_crc_geof character varying(16),
    p_too_short character varying(16),
    p_too_long character varying(16),
    p_bad_eof character varying(16),
    p_enc_out character varying(16),
    p_disc_c3 character varying(16),
    p_link_fail character varying(16),
    p_loss_sync character varying(16),
    p_loos_sig character varying(16),
    p_frjt character varying(16),
    p_fbsy character varying(16),
    p_c3timeout_tx character varying(16),
    p_c3timeout_rx character varying(16),
    p_pcs_err character varying(16),
    p_ucor_err character varying(16)
)

-- DROP TABLE IF EXISTS zones;
CREATE TABLE IF NOT EXISTS zones(
    zones_id int primary key,
    z_date character varying(16),
    z_name character varying(50)
)

-- DROP TABLE IF EXISTS alias;
CREATE TABLE IF NOT EXISTS alias(
    zoning_id int not null references zones(zones_id),
    a_date character varying(16),
    a_name character varying(50),
    a_wwn character varying(24)
)

--
sql = "INSERT INTO switch (sw_name,sw_type,sw_domain,sw_id,sw_wwn) " \
"VALUES (%(str)s,%(int)s,%(int)s,%(str)s,%(str)s) RETURNING switch_id", \
{'str':switchinfo[0], 'int':switchinfo[1], 'int':switchinfo[2], 'str':switchinfo[3], 'str':switchinfo[4]}


--
create user user_name with password 'password';
alter role user_name set client_encoding to 'utf8';
alter role user_name set default_transaction_isolation to 'read committed';
alter role user_name set timezone to 'UTC';

--
 datetime.date(2005, 11, 18) = 2005-11-18
['2020 03 24 0220']
['2020 04 28 0220']