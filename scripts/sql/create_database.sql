/* create database */

CREATE DATABASE psn_game_collection;

/* grant database access */

GRANT ALL ON psn_game_collection.* TO 'kgooding'@'%' IDENTIFIED BY "password";

/* switch to database */

USE psn_game_collection;

/* create database table - COLLECTION*/

CREATE TABLE COLLECTION (
title_id VARCHAR(255),
title VARCHAR(255),
first_played VARCHAR(255),
last_played VARCHAR(255),
platform VARCHAR(255),
play_count NUMERIC,
duration NUMERIC,
img_url VARCHAR(255)
);

/* view table columns */

SHOW COLUMNS FROM COLLECTION;

/* view table data */

SELECT * FROM COLLECTION;

/* create database table - PS4 */

CREATE TABLE PS4 (
title_id VARCHAR(255),
title VARCHAR(255),
first_played VARCHAR(255),
last_played VARCHAR(255),
platform VARCHAR(255),
play_count NUMERIC,
duration NUMERIC,
img_url VARCHAR(255)
);

/* view table columns */

SHOW COLUMNS FROM PS4;

/* view table data */

SELECT * FROM PS4;

/* create database table - PS5 */

CREATE TABLE PS5 (
title_id VARCHAR(255),
title VARCHAR(255),
first_played VARCHAR(255),
last_played VARCHAR(255),
platform VARCHAR(255),
play_count NUMERIC,
duration NUMERIC,
img_url VARCHAR(255)
);

/* view table columns */

SHOW COLUMNS FROM PS5;

/* view table data */

SELECT * FROM PS5;