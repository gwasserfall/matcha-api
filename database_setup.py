import pymysql
import config

from pprint import pprint

db = pymysql.connect(**config.database)

with db.cursor() as c:
	print("Creating table users.")
	c.execute("""
		CREATE TABLE IF NOT EXISTS users 
		(
			id 				INT AUTO_INCREMENT PRIMARY KEY,
			fname			varchar(256)	NOT NULL,
			lname			varchar(256),
			email			varchar(256)	NOT NULL UNIQUE,
			username		varchar(256)	NOT NULL UNIQUE,
			passhash		LONGTEXT		NOT NULL,
			bio				LONGTEXT,
			gender			ENUM('male', 'female', 'other'),
			dob				DATE,
			longitude		DECIMAL(11, 8),
			latitude		DECIMAL(11, 8),
			heat			INT					DEFAULT (0),
			online			TINYINT				DEFAULT (0),
			date_joined		TIMESTAMP		DEFAULT CURRENT_TIMESTAMP,
			date_lastseen	TIMESTAMP		DEFAULT CURRENT_TIMESTAMP,
			deleted			TINYINT			DEFAULT (0)
		)
	""")

	print("Creating table images")
	c.execute("""
		CREATE TABLE IF NOT EXISTS images
		(
			id			INT				AUTO_INCREMENT PRIMARY KEY,
			user_id		INT				NOT NULL,
			image64		LONGTEXT		NOT NULL,
			image_type	varchar(6)		NOT NULL
		)
	""")


	print("Creating table user_preferences")
	c.execute("""
		CREATE TABLE IF NOT EXISTS user_preferences
		(
			id			INT AUTO_INCREMENT PRIMARY KEY,
			user_id		INTEGER				NOT NULL,
			interests	TEXT,
			radius		INTEGER,
			age_from	INTEGER				DEFAULT (18),
			age_to		INTEGER				DEFAULT (122)
		)
	""")

	print("Creating table gender_preference")
	c.execute("""
		CREATE TABLE IF NOT EXISTS gender_preference
		(
			id			INT AUTO_INCREMENT PRIMARY KEY,
			user_id		INTEGER				NOT NULL,
			gender		ENUM('male', 'female', 'other')
		)
	""")

# db.query("""
# 	CREATE TABLE IF NOT EXISTS profile_view
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
# 		viewer_id	INTEGER,
# 		viewee_id	INTEGER
# 	)
# """)

with db.cursor() as c:
	c.execute("""
		CREATE TABLE IF NOT EXISTS matches
		(
			id			INT 				AUTO_INCREMENT PRIMARY KEY,
			date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
			matcher_id	INTEGER				NOT NULL,
			matchee_id	INTEGER				NOT NULL
		)
	""")

# db.query("""
# 	CREATE TABLE IF NOT EXISTS user_blocks
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
# 		blocker_id	INTEGER,
# 		blockee_id	INTEGER,
# 		active		INTEGER
# 	)
# """)

# db.query("""
# 	CREATE TABLE IF NOT EXISTS notifications
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		type		TEXT,
# 		message		TEXT,
# 		user_id		INTEGER,
# 		recieved	INTEGER				DEFAULT 0
# 	)
# """)

with db.cursor() as c:
	c.execute("""
		CREATE TABLE IF NOT EXISTS messages
		(
			id			INT 				AUTO_INCREMENT PRIMARY KEY,
			to_id		INT,
			from_id		INT,
			timestamp	DATETIME			DEFAULT CURRENT_TIMESTAMP,
			message		TEXT,
			seen		INT				DEFAULT(0)
		)
	""")



