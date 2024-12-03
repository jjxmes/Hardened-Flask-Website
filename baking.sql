

CREATE TABLE IF NOT EXISTS new_user
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	age INTEGER,
	phoneNumber TEXT,
	securityLevel INTEGER,
	password TEXT

);

CREATE TABLE IF NOT EXISTS contest_results
(
	entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	nameOfItem TEXT,
	numExcellentVotes INTEGER,
	numOkVotes INTEGER,
	numBadVotes INTEGER,
	FOREIGN KEY (user_id) REFERENCES new_user(id)
);

INSERT INTO contest_results (user_id, nameOfItem, numExcellentVotes, numOkVotes, numBadVotes) VALUES (1, 'Whoot Whoot Brownies', 1, 2, 4);
INSERT INTO contest_results (user_id, nameOfItem, numExcellentVotes, numOkVotes, numBadVotes) VALUES (2, 'Cho Chip Cookies', 4, 1, 2);
INSERT INTO contest_results (user_id, nameOfItem, numExcellentVotes, numOkVotes, numBadVotes) VALUES (3, 'Cho Cakes', 2, 4, 1);
INSERT INTO contest_results (user_id, nameOfItem, numExcellentVotes, numOkVotes, numBadVotes) VALUES (1, 'Sugar Cookies', 2, 2, 1);