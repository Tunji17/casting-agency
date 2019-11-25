# Backend API For Casting Agency App

## Motivation for project

This is the capstone project for the udacity full stack nanodegree program.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, create a database and add an env variable 'DATABASE_URL' which is your postgres connection url,
run migrations using:

```bash

flask db init
flask db migrate
flask db upgrade
```

## Running the server

From within the your directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=src/app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `src/app.py` directs flask to use the app.py` file to run the application.

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models

Movies with attributes title and release date
Actors with attributes name, age and gender

## Roles

Casting Assistant

- view:actors
- view:movies

Casting Director

- All permissions a Casting Assistant has
- create:actor
- delete:actor
- update:actor
- update:movie

Executive Producer

- All permissions a Casting Director has
- add:movie
- delete:movie

## Endpoints

GET '/actors'

reponse = [
  {
    name: tunji,
    age: 25,
    gender: male
  },
  {
    name: alice,
    age: 22,
    gender: non-binary
  },
  {
    name: bob,
    age: 27,
    gender: female
  }
]

GET '/movies'

response = [
  {
    title: See
    release_date: 12th November 2019
  },
  {
    title: Jurassic Park
    release_date: 12th july 2018
  }
]
POST '/actors'

payload = {
    name: tunji,
    age: 25,
    gender: male
  }
response = {
  success: True,
}

POST '/movies'

payload = {
    title: See
    release_date: 12th November 2019
  }
response = {
  success: True,
}

PATCH '/actors/<int:actor_id>'

payload = {
    name: teejay,
    age: 25,
    gender: male
  }
response = {
  success: True,
}

PATCH '/movies/<int:movie_id>'
payload = {
    title: His Dark Material
    release_date: 12th November 2019
  }
response = {
  success: True,
}

DELETE '/actors/<int:actor_id>'

response = {
  success: True,
  deleted: actor_id
}

DELETE '/movies/<int:movie_id>'

response = {
  success: True,
  deleted: movie_id
}

## Testing

To run the tests, run
Working jwt tokens from auth0 for casting agent, casting director and executive producer is declared in the test file
this can be used to make requests to the endpoints.

```bash

python3 src/test_app.py
```

### Deployment

The running application is deployed on heroku  with base url

```bash
https://casting-agency-flask.herokuapp.com/
```
