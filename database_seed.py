from database import pool
from datetime import datetime
from random import random, randint, choice, choices

from helpers.genders import genders
from sample.bio import bios
from sample.interests import interests

import base64
import requests

pool.init()


# connection = pool.get_conn()

# with connection.cursor() as c:
#     print("Truncating tables")
#     c.execute("TRUNCATE TABLE block_requests")
#     c.execute("TRUNCATE TABLE images")
#     c.execute("TRUNCATE TABLE matches")
#     c.execute("TRUNCATE TABLE messages")
#     c.execute("TRUNCATE TABLE users")
#     c.execute("TRUNCATE TABLE views")
current_id = 1

with connection.cursor() as c:
    


    
r = requests.get("https://randomuser.me/api/?nat=gb,us&results=500")


for user in r.json()["results"]:
    
    fname = user["name"]["first"]
    lname = user["name"]["last"]

    print(f"Adding {fname} {lname}")

    email = user["email"].split("@")

    email_part1 = email[0] + str(randint(0, 9999))
    email_part2 = email[0]

    email = email_part1 + "@" + email_part2

    email_verified = 1
    username = user["login"]["username"] + str(randint(0, 9999))
    passhash = "not a real hash :("
    bio = choice(bios)
    gender = choice([user["gender"], "other"])
    dob = user["dob"]["date"][:-14]
    latitude= round(-33 + random(), 8)
    longitude = round(18 + random(), 8)
    preferences = choices(["male", "female", "other"], k=randint(1,3))
    interests = choices(interests, k=randint(2,10))

    img_url = user["picture"]["large"]
    response = requests.get(img_url)
    img_type = img_url.split(".")[-1]

    image64 = base64.b64encode(response.content).decode("utf-8")

    with connection.cursor() as c:
        c.execute("""INSERT INTO users 
            (fname, lname, email, email_verified, username, passhash, bio, gender, dob, latitude, longitude, preferences, interests)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fname, lname, email, email_verified, 
                username, passhash, bio, gender, dob, latitude, longitude, 
                ",".join(preferences), ",".join(interests)
            ))
        c.execute("""INSERT INTO images (user_id, is_primary, image_type, image64)
            VALUES (%s, %s, %s, %s)
        """, (current_id, 1, img_type, image64))

    current_id += 1


pool.release(connection)



