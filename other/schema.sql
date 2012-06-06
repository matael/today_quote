-- SQL Table for quotes

CREATE TABLE `quotes` (
	id INTEGER PRIMARY KEY,
	author VARCHAR,
	quote VARCHAR,
	vote_up INTEGER,
	vote_down INTEGER
);
