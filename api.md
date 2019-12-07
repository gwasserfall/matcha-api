# Users

Get a users information

<details>
<summary>GET - /user/&ltint:id&gt</summary>

>### Example usage:

```javascript
axios.get("/user/1")
  .then(data => {
    // do stuff with data
  })
  .catch(err => {
    // err.message populated
  })
```

>Success (200) : Response

\* Will be missing if user inspects another without being matched

```json
{
    "id" : "1",
  * "fname" : "firstname",
  * "lname" : "lastname",
  * "email" : "email@domain.tld",
    "username" : "myusername",
    "bio" : "Biography in Markdown Syntax",
    "gender" : "male",
    "age" : 21,
  * "longitude" : 40.714,
  * "latitude" : -74.006,
    "heat" : 100,
  * "online" : false,
  * "date_joined" : 1575194400,
  * "date_lastseen" : 1575194400
}
```

>Faliure (404) : Response

```json
{
  "message" : "User Not Found"
}
```


</details>


<details>
<summary>POST - /users</summary>

>### Example usage:

```javascript
axios.post("/users", {username : "username", gender: "female"})
  .then(data => {
    // data is the newly created user account
  })
  .catch(err => {
    // err.message populated
  })
```

>Success (201) : Response

```json
{
    "id" : "1",
    "fname" : "firstname",
    "lname" : "lastname",
    "email" : "email@domain.tld",
    "username" : "username",
    "bio" : "Biography in Markdown Syntax",
    "gender" : "female",
    "age" : 21,
    "longitude" : 40.714,
    "latitude" : -74.006,
    "heat" : 100,
    "online" : false,
    "date_joined" : 1575194400,
    "date_lastseen" : 1575194400
}
```

>Faliure (400) : Response

```json
{
  "message" : "fname cannot be blank"
}
```


</details>


<details>
<summary>DELETE - /users</summary>

```json
{
  "username" : "example"
}
```
</details>


# Profile

<details>
<summary>GET - /user/&ltint:id&gt/profile</summary>

```json
{
  "username" : "example"
}
```
</details>

