Ensure you have a ".env" file in the main project directory. They following env vars will need
to be in this file in order for the project to run.

```
ENV=dev
DB_HOST=127.0.0.1
DB_USERNAME=user
DB_PASSWORD=pass
DB_DATABASE=matcha

WEBHOOK_SECRET=somesecretthatisnotthisstringoftext
```


Install backend python libraries and start dev server.

```
pip3 -r requirements.txt

# Ensure MySQL is up and running.

python3 app.py

```

Import MySQL database.
```
Log into MySQL and run "create database matcha"


python3 database_setup.py
```


Install Frontend node libraries and start dev server

```
cd matcha-vue

npm install

npm run serve
```