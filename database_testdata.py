import pymysql
import config

db = pymysql.connect(**config.database)

"""
Users test data
"""
users = [
        {
                "fname" : "Henry",
                "lname" : "Johnson",
                "email" : "henry.johnson@mailthing.com",
                "username" : "hjohnson",
                "passhash" : "5f01ee0b6c8afcae94bd07a55d993746891343a90c28e9dadfd195ddd820dabb:12585f7d8230418aad80bb7c3b726b9a",
                "bio" : "Some stuff with new\nlines and \t\t tabs and stuff",
                "gender" : "male",
                "dob" : "2000-01-01",
                "longitude" : "10.0001",
                "latitude" : "11.00002"
        },
        {
                "fname" : "Mary",
                "lname" : "Fitzpatrick",
                "email" : "mfitz88@gmail.com",
                "username" : "mfitzzz",
                "passhash" : "5f01ee0b6c8afcae94bd07a55d993746891343a90c28e9dadfd195ddd820dabb:12585f7d8230418aad80bb7c3b726b9a",
                "bio" : "Some stuff with new\nlines and \t\t tabs and stuff",
                "gender" : "female",
                "dob" : "1988-09-01",
                "longitude" : "11.0001",
                "latitude" : "12.00002"
        },
        {
                "fname" : "Shauna",
                "lname" : "van Staden",
                "email" : "beezknees@yahoo.co.uk",
                "username" : "shauna123",
                "passhash" : "5f01ee0b6c8afcae94bd07a55d993746891343a90c28e9dadfd195ddd820dabb:12585f7d8230418aad80bb7c3b726b9a",
                "bio" : "Some stuff with new\nlines and \t\t tabs and stuff",
                "gender" : "other",
                "dob" : "2000-11-21",
                "longitude" : "11.0001",
                "latitude" : "12.00002"
        }
]

with db.cursor() as c:
    c.execute("DELETE FROM users")
    db.commit()

    for user in users:
        c.execute("INSERT INTO users ({keys}) VALUES ({vals})".format(
                keys=", ".join(user.keys()),
                vals=", ".join(["'{}'".format(x) for x in user.values()])
        ))
        db.commit()


from base64 import encode
