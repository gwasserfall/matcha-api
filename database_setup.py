import pymysql
import config
import copy

from pprint import pprint

# Create database if not exists
conf = copy.deepcopy(config.database)
conf.pop("db", None)

with pymysql.connect(**conf) as db:
    db._defer_warnings = True
    db.execute("CREATE DATABASE IF NOT EXISTS matcha")
    print("Creating database 'matcha' if it doesn't exist")


db = pymysql.connect(**config.database)

with db.cursor() as c:
    c._defer_warnings = True
    print("Creating table users.")
    c.execute("""
        CREATE TABLE IF NOT EXISTS users
        (
            id                  INT                 AUTO_INCREMENT PRIMARY KEY,
            fname               varchar(256)        NOT NULL,
            lname               varchar(256),
            email               varchar(256)        NOT NULL UNIQUE,
            email_verified      BOOLEAN             DEFAULT (0),
            username            varchar(256)        NOT NULL UNIQUE,
            passhash            LONGTEXT            NOT NULL,
            bio                 LONGTEXT,
            gender              TEXT,
            dob                 DATE,
            longitude           DECIMAL(11, 8),
            latitude            DECIMAL(11, 8),
            heat                INT                 DEFAULT (0),
            online              BOOLEAN             DEFAULT (0),
            preferences         LONGTEXT,
            interests           LONGTEXT,
            date_joined         TIMESTAMP           DEFAULT CURRENT_TIMESTAMP,
            date_lastseen       TIMESTAMP           DEFAULT CURRENT_TIMESTAMP,
            deleted             BOOLEAN             DEFAULT (0),
            is_admin            BOOLEAN             DEFAULT (0)
        )
    """)


    print("Creating table validations")
    c.execute("""
        CREATE TABLE IF NOT EXISTS validations
        (
            id          INT          AUTO_INCREMENT PRIMARY KEY,
            user_id     INT          NOT NULL,
            code        LONGTEXT     NOT NULL
        )
    """)

    print("Creating table messages")
    c.execute("""
            CREATE TABLE IF NOT EXISTS messages
            (
                    id                      INT                             AUTO_INCREMENT PRIMARY KEY,
                    to_id           INT,
                    from_id         INT,
                    timestamp       DATETIME                        DEFAULT CURRENT_TIMESTAMP,
                    message         TEXT,
                    seen            INT                             DEFAULT(0)
            )
    """)


    print("Creating table images")
    c.execute("""
            CREATE TABLE IF NOT EXISTS images
            (
                    id                      INT                             AUTO_INCREMENT PRIMARY KEY,
                    is_primary BOOLEAN                                      DEFAULT (0),
                    user_id         INT                             NOT NULL,
                    image64         LONGTEXT                NOT NULL,
                    image_type      varchar(6)              NOT NULL
            )
     """)

    print("Creating table global_interests")
    c.execute("""
            CREATE TABLE IF NOT EXISTS global_interests
            (
                    id                              INT AUTO_INCREMENT PRIMARY KEY,
                    interest        TEXT
            )
    """)

    print("Creating table matches")
    c.execute("""
    CREATE TABLE IF NOT EXISTS matches
    (
            id                      INT                             AUTO_INCREMENT PRIMARY KEY,
            date            DATETIME                        DEFAULT CURRENT_TIMESTAMP,
            matcher_id      INTEGER                         NOT NULL,
            matchee_id      INTEGER                         NOT NULL,
            rating          INTEGER                         DEFAULT(0)
    )
    """)

    print("Creating table block_requests")
    c.execute("""
    CREATE TABLE IF NOT EXISTS block_requests
    (
            id              INTEGER                         AUTO_INCREMENT PRIMARY KEY,
            reporter_id     INTEGER                         NOT NULL,
            reported_id     INTEGER                         NOT NULL,
            reason          LONGTEXT                        NOT NULL,
            reviewed        BOOLEAN                         DEFAULT(0),
            blocked         BOOLEAN                         DEFAULT(0),
            admin_comments  LONGTEXT                        
    )
    """)
    
    # print("Creating table gender_preference")
    # c.execute("""
    #       CREATE TABLE IF NOT EXISTS gender_preference
    #       (
    #               id                      INT AUTO_INCREMENT PRIMARY KEY,
    #               user_id         INTEGER                         NOT NULL,
    #               gender          ENUM('male', 'female', 'other')
    #       )
    # """)

# db.query("""
#       CREATE TABLE IF NOT EXISTS profile_view
#       (
#               id                      INTEGER                         AUTO INCREMENT,
#               date            DATETIME                        DEFAULT CURRENT_TIMESTAMP,
#               viewer_id       INTEGER,
#               viewee_id       INTEGER
#       )
# """)




# db.query("""
#       CREATE TABLE IF NOT EXISTS user_blocks
#       (
#               id                      INTEGER                         AUTO INCREMENT,
#               date            DATETIME                        DEFAULT CURRENT_TIMESTAMP,
#               blocker_id      INTEGER,
#               blockee_id      INTEGER,
#               active          INTEGER
#       )
# """)

# db.query("""
#       CREATE TABLE IF NOT EXISTS notifications
#       (
#               id                      INTEGER                         AUTO INCREMENT,
#               type            TEXT,
#               message         TEXT,
#               user_id         INTEGER,
#               recieved        INTEGER                         DEFAULT 0
#       )
# """)
