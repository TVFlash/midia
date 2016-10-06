CREATE TYPE feed AS (
	type text,
	source text,
	click_count bigint
);

CREATE TABLE users (
	user_id bigint PRIMARY KEY,
	feeds feed[]
);