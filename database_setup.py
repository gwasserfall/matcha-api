import pymysql
import config

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
			age				INT,
			longitude		DECIMAL(11, 8),
			latitude		DECIMAL(11, 8),
			heat			INT					DEFAULT (0),
			online			TINYINT				DEFAULT (0),
			date_joined		TIMESTAMP		DEFAULT CURRENT_TIMESTAMP,
			date_lastseen	TIMESTAMP		DEFAULT CURRENT_TIMESTAMP
		)
	""")

	# print("Creating table user_images")
	# c.execute("""
	# 	CREATE TABLE IF NOT EXISTS user_images
	# 	(
	# 		id			INT				AUTO_INCREMENT PRIMARY KEY,
	# 		user_id		INT				NOT NULL,
	# 		image64		LONGTEXT		NOT NULL,
	# 		image_type	varchar(6)		NOT NULL
	# 	)
	# """)


	# print("Creating table user_preference")
	# c.execute("""
	# 	CREATE TABLE IF NOT EXISTS user_preference
	# 	(
	# 		id			INT AUTO_INCREMENT PRIMARY KEY,
	# 		user_id		INTEGER				NOT NULL,
	# 		interests	TEXT,
	# 		gender		TEXT,
	# 		radius		INTEGER,
	# 		age_from	INTEGER				DESFULT (18),
	# 		age_to		INTEGER				DEFAULT (122)
	# 	)
	# """)

# db.query("""
# 	CREATE TABLE IF NOT EXISTS profile_view
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
# 		viewer_id	INTEGER,
# 		viewee_id	INTEGER
# 	)
# """)

# db.query("""
# 	CREATE TABLE IF NOT EXISTS match
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
# 		matcher_id	INTEGER				NOT NULL,
# 		matchee_id	INTEGER				NOT NULL
# 	)
# """)

# db.query("""
# 	CREATE TABLE IF NOT EXISTS user_block
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		date		DATETIME			DEFAULT CURRENT_TIMESTAMP,
# 		blocker_id	INTEGER,
# 		blockee_id	INTEGER,
# 		active		INTEGER
# 	)
# """)

# db.query("""
# 	CREATE TABLE IF NOT EXISTS notification
# 	(
# 		id			INTEGER				AUTO INCREMENT,
# 		type		TEXT,
# 		message		TEXT,
# 		user_id		INTEGER,
# 		recieved	INTEGER				DEFAULT 0
# 	)
# """)