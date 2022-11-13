# imdb-app
Django app for searching movies

# Project Documentation :wave::wave:

## Python Requirements :memo:

- Python 3.8+

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
1. Create .env file and :key: ```SECRET_KEY = <YOUR_SECRET_KEY>```
2. Use python manage.py migrate
3. Use```python manage.py collectstatic –no-input```
4. Create superuser - python manage.py createsuperuser
5. To load data into database sqlite3, open python manage shell using ```python manage.py shell```and write the following script
```python
from search_app.load_json import load_movies_data
load_movies_data()
```
6. To create users, open python manage shell using ```python manage.py shell```and write the following script
```python
from search_app.create_users import create_users
create_users()
```
_**Note: Make 2 users with 1 user being admin and 1 without admin**_

## Running the project :checkered_flag:

Now run the app using command ```python manage.py runserver```

## Testing :hourglass:

For testing run command ```python manage.py test search_app```

### Heroku API testing

For heroku api testing try the following commands

1. **To open Django Administration** :link: [Admin Pannel](https://imdb-app-job.herokuapp.com/admin/ "Django Administration")


   Credentials
   username: "admin" and password: "admin"

_**Here you would be able to see different tables of users, movies and genres**_

2. **For testing Create, Update, Delete** (For Read check Search Api testing)

- **Create** :arrow_right: Send a `POST` request in Postman using endpoint `movies_create/`

   Example, https://imdb-app-job.herokuapp.com/movies_create/

   Using authentication credentials `username: “anurag1” and password: “Anurag@123”)` post data as given below
```python
data_send = {
   "movie_popularity": 80,
   "director": "Nolan",
   "genres": [
         "Action",
         "Comedy",
         "Romantic"
       ],
   "imdb_rating":7.5,
   "movie_name": "Spider Man"
   }
```
   You should get a status code of `201` for successful request
   Using an unknown authentication credentials such as
   username: “anurag2” and password: “Anurag@123”, you would get a `403` permission denied error

- **Update** :arrow_right: Send a `PUT` request in Postman using endpoint `movies_update/`

   Example, https://imdb-app-job.herokuapp.com/movies_delete/2 where "2" is the ID of the movie that you need to update

   Using the authentication credentials `username: “anurag1” and password: “Anurag@123”)` and send a put request with the data as given below
```python
data_send = {
   "movie_popularity": 80,
   "director": "Nolan AS",
   "genres": [
         "Action",
         "Comedy",
         "Romantic"
       ],
   "imdb_rating":7.5,
   "movie_name": "Spider Man 2"
   }
```
   You should get a status code of 200 for successful request

- **Delete** :arrow_right: Send a `DELETE` request in Postman using endpoint `movies_delete/` and authentication credentials
 `username: “anurag1” and password: “Anurag@123”)`. Example, https://imdb-app-job.herokuapp.com/movies_delete/2 where "2" is the ID of the movie


   You should get a status code of 200 for successful request

3. **For testing search api**

   To search for movies use the endpoint `/search_movie/`. Example https://imdb-app-job.herokuapp.com/search_movie/?page=1
  
   And you can add the parameters in the url using & operator and adding one or more valid parameters

   List of valid parameters:

  - '**search_name**' : To filter the movies using movie name
  
  - '**search_director**' : To filter the movies using the director's name
  
  - '**search_rating**' : To filter the movies having rating greater than and equal to required rating
  
  - '**search_popularity**' : To filter the movies having popularity greater than and equal to required popularity
  
  - '**search_genre**' : To filter the movies having the searched genre

  - '**paginator_len**' : used to specify the number of movies in a page
  
  - '**paginator_req**' : used to specify if pagination is required or not (`yes` for required else `no` for not required, default pagination is enabled with 10 movies)

  - '**page**' : add page number while using pagination


## Steps for heroku deployment
Use the following commands to deploy on heroku

Login into heroku container using
```shell
heroku container:login
```

Build a docker image of the project in the current directory using
```shell
docker build -t registry.heroku.com/imdb-app-job/web .
```

Push the project docker image on the heroku container
```shell
sudo docker push registry.heroku.com/imdb-app-job/web
```

Release the new image in the heroku app using
```shell
heroku container:release -a imdb-app-job web
```



