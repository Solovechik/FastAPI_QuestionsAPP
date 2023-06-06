GRANT ALL PRIVILEGES ON DATABASE bewise TO bewiseusr;
CREATE TABLE IF NOT EXISTS Questions(
	id SERIAL primary key, 
	text VARCHAR(200) not null,
	answer VARCHAR(100) not null,
	created_at TIMESTAMP not null
	);
