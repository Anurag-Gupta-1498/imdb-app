# imdb-app
Django app for searching movies

#Project Documentation :wave::wave:

##Python Requirements :memo:

- Python - 3.7 +

## Project Setup :wrench:

### Cloning the repo
1. Clone the repository using```git clone https://github.com/Anurag-Gupta-1498/imdb-app.git```
2. Switch to branch master using ```git checkout master```

### Creating a virtual environment
1. Create virtual environment using ```python3/python -m venv env```

2. Activate virtual env using ```source env/bin/activate (ubuntu)```

### Installing requirements
1. Install requirements.txt file using  - ```pip install -r requirements.txt```

### Django project setup
1. Create .env file and :key: SECRET_KEY = <YOUR_SECRET_KEY>
2. Use python manage.py migrate

3. Use
```python manage.py collectstatic –no-input```

4. Create superuser - python manage.py createsuperuser

   After that run 2 scripts -
  
   To load data into database sqlite3
   Open python manage shell and write the following script-
   From search_app.load_json import load_movies_data
   load_movies_data()
   To create users -
   Open python manage shell and write the following script-
   From search_app.create_users import create_users
   create_users()
   Make 2 users with 1 user being admin and 1 without admin

##Running the project :checkered_flag:
Now run the app using command ```python manage.py runserver```

## Testing :hourglass:

For testing run command ```python manage.py test search_app```

### Heroku API testing

For heroku api testing try the following commands

To open Django Administration :link: [Admin Pannel](https://imdb-app-job.herokuapp.com/admin/ "Django Administration")
  
   Credentials
   username: "admin" and password: "admin"

