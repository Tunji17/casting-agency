import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from pprint import pprint
from flask_moment import Moment
from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
      return response
  
  setup_db(app)

  @app.route('/callback')
  def get_token():
      access_token = request.args.get('access_token')
      return jsonify({
        'access_token': access_token,

      })
  
  @app.route('/actors')
  @requires_auth('view:actors')
  def get_actors(jwt):
      all_actors = Actor.query.order_by(Actor.id).all()
      formatted_response = [actor.format() for actor in all_actors]
      return jsonify({
          'actors': formatted_response,
      })

  @app.route('/movies')
  @requires_auth('view:movies')
  def get_movies(jwt):
      all_movies = Movie.query.order_by(Movie.id).all()
      formatted_response = [movie.format() for movie in all_movies]
      return jsonify({
          'movies': formatted_response,
      })

  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actor')
  def create_actors(jwt):
      data = request.get_json()
      name = data.get('name')
      age = data.get('age')
      gender = data.get('gender')
      try:
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
        })
      except Exception:
        abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def create_movies(jwt):
      data = request.get_json()
      title = data.get('title')
      release_date = data.get('release_date')
      try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
        })
      except Exception:
        abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('update:actor')
  def update_actors(jwt, actor_id):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        try:
            get_actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if get_actor is None:
                abort(404)
            if name and age and gender is None:
                abort(422)
            if name is not None:
              get_actor.name = name
            if age is not None:
              get_actor.age = age
            if gender is not None:
              get_actor.gender = gender
            get_actor.update()
            return jsonify({
                'success': True,
            })
        except Exception:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('update:movie')
  def update_movies(jwt, movie_id):
        data = request.get_json()
        title = data.get('title')
        release_date = data.get('release_date')
        try:
            get_movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if get_movie is None:
                abort(404)
            if title and release_date is None:
                abort(422)
            if title is not None:
              get_movie.title = title
            if release_date is not None:
              get_movie.release_date = release_date
            get_movie.update()
            return jsonify({
                'success': True,
            })
        except Exception:
          abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(jwt, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          if actor is None:
              abort(404)
          actor.delete()
          return jsonify({
              'success': True,
              'deleted': actor_id,
          })
      except Exception:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(jwt, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          if movie is None:
              abort(404)
          movie.delete()
          return jsonify({
              'success': True,
              'deleted': movie_id,
          })
      except Exception:
          abort(422)

    # Error Handling
  '''
  Example error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": 422,
                      "message": "unprocessable request"
                      }), 422


  @app.errorhandler(401)
  def not_authorized(error):
      return jsonify({
                      "success": False,
                      "error": 401,
                      "message": "not authorized"
                      }), 401


  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
                      "success": False,
                      "error": 404,
                      "message": "resource not found"
                      }), 404


  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
                      "success": False,
                      "error": 500,
                      "message": "internal server error"
                      }), 500

  return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)