# Users

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
<summary>PUT - /user/&ltint:id&gt</summary>

>### Example usage:

```javascript
axios.put("/users/1", {username : "newusername", gender: "other"})
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
    "username" : "newusername",
    "bio" : "Biography in Markdown Syntax",
    "gender" : "other",
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
  "message" : "Validation error raised"
}
```

>Faliure (404) : Response

```json
{
  "message" : "User not found"
}
```


</details>



<details>
<summary>DELETE - /user/&ltint:id&gt</summary>

### Example usage:

```javascript
axios.delete("/user/1")
  .then(data => {
    // empty data
  })
  .catch(err => {
    // err.message populated
  })
```

>Success (204) No Content : Response

```json

```

>Faliure (400) : Response

```json
{
  "message" : "Could not delete user"
}
```

>Faliure (404) : Response

```json
{
  "message" : "User not found"
}
```

</details>


# User Preferences

<details>
<summary>GET - /user/&ltint:id&gt/preferences</summary>

### Example usage:

```javascript
axios.post("/users")
  .then(data => {
    // data is the newly created user account
  })
  .catch(err => {
    // err.message populated
  })
```


</details>

# User Accounts

<details>
<summary>POST - /login</summary>

### Example usage:

#### Request Parameters

```json
{
  "username" : "username or email",
  "password" : "user password"
}
```


```javascript
axios.post("/users")
  .then(data => {
    // data is the newly created user account
  })
  .catch(err => {
    // err.message populated
  })
```

>Success (200) 

```json
{
  "access_token" : "jwt access token here"
}
```

>Faliure (401) : Response

```json
{
  "message" : "Failed to authenticate"
}
```

>Faliure (404) : Response

```json
{
  "message" : "User not found"
}
```

</details>