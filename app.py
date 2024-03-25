#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import itertools
import dateutil.parser
import babel
from flask import Flask, abort, jsonify, render_template, request, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
from auth import AuthError, requires_auth
from flask_cors import CORS
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(db_URI="",test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object('config')
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  if db_URI:
      setup_db(app,db_URI)
  else:
      setup_db(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  #----------------------------------------------------------------------------#
  # Models.
  #----------------------------------------------------------------------------#

  def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

  app.jinja_env.filters['datetime'] = format_datetime

  #----------------------------------------------------------------------------#
  # Controllers.
  #----------------------------------------------------------------------------#

  @app.route('/')
  def index():
    return 'The Casting Agency is up and running!!'


  #  Movies
  #  ----------------------------------------------------------------

  @app.route('/movies')
  @requires_auth('get:movies')
  def movies(payload):
    try:
      movies = Movie.query.all()
      data = [
          {
              'id': movie.id,
              'name': movie.name,
              'release_date': movie.release_date,
          }
          for movie in movies]

      return jsonify({'success': True, 'movies':data, 'movies_count': len(data)})
    except:
      abort(500)


  @app.route('/movies/search', methods=['POST'])
  @requires_auth('get:movies')
  def search_movies(payload):
    try:
      query_string = request.form.get('search_term')
      movies = Movie.query.filter(Movie.name.ilike('%'+query_string+'%'))
      data = [
          {
              'id': movie.id,
              'name': movie.name,
              'release_date': movie.release_date,
          }
          for movie in movies]
      response = {'count': len(Movie.query.all()), 'data': data}
      return jsonify(response)
    except:
      abort(500)
      

  @app.route('/movies/<int:movie_id>')
  @requires_auth('get:movies')
  def show_movie(payload, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      if movie == None:
        abort(404)
      data = {
              'id': movie.id,
              'name': movie.name,
              'release_date': movie.release_date,
          }
      return jsonify({'movie': data})
    except:
      abort(500)

  #  Create Movie
  #  ----------------------------------------------------------------

  @app.route('/movies/create', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie_submission(payload):
    form = MovieForm(request.form, meta={'csrf': False})
    if form.validate():
      try:
        movie = Movie()
        form.populate_obj(movie)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
              'success': True,
              'created': movie.id
              })
      except:
        db.session.rollback()
        abort(500)
      finally:
        db.session.close()
    else:
      abort(500)
      

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      if movie == None:
        abort(404)
      db.session.delete(movie)
      db.session.commit()
      return jsonify({
              'success': True,
              'deleted': movie.id
              })
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()

  #  Actors
  #  ----------------------------------------------------------------

  @app.route('/actors')
  @requires_auth('get:actors')
  def actors(payload):
    try:
      actors = Actor.query.all()
      data = [
          {
              'id': actor.id,
              'name': actor.name,
              'gender': actor.gender,
              'age': actor.age
          }
          for actor in actors]
      return jsonify({'success': True, 'actors':data, 'actors_count': len(data)})
    except:
      abort(500)


  @app.route('/actors/search', methods=['POST'])
  @requires_auth('get:actors')
  def search_actors(payload):
    try:
      query_string = request.form.get('search_term')
      actors = Actor.query.filter(Actor.name.ilike('%'+query_string+'%'))
      data = [
        {
            'id': actor.id,
            'name': actor.name,
            'gender': actor.gender,
            'age': actor.age
        }
        for actor in actors]
      response = {'count': len(data), 'data': data}
      return jsonify(response)
    except:
      abort(500)


  @app.route('/actors/<int:actor_id>')
  @requires_auth('get:actors')
  def show_actor(payload, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      if actor == None:
        abort(404)
      data = {
            'id': actor.id,
            'name': actor.name,
            'gender': actor.gender,
            'age': actor.age
          }
      return jsonify({'actor': data})
    except:
      abort(500)

  #  Update
  #  ----------------------------------------------------------------

  @app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor_submission(payload, actor_id):
    form = ActorForm(request.form, meta={'csrf': False})
    if form.validate():
      try:
        actor = Actor.query.get(actor_id)
        form.populate_obj(actor)
        db.session.commit()
        data = {
            'id': actor.id,
            'name': actor.name,
            'gender': actor.gender,
            'age': actor.age
          }
        return jsonify({'actor': data})
      except:
        db.session.rollback()
        abort(500)
    else:
      abort(500)


  @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie_submission(payload, movie_id):
    form = MovieForm(request.form, meta={'csrf': False})
    if form.validate():
      try:
        movie = Movie.query.get(movie_id)
        form.populate_obj(movie)
        db.session.commit()
        data = {
              'id': movie.id,
              'name': movie.name,
              'release_date': movie.release_date,
          }
        return jsonify({'success': True, 'movie': data})
      except:
        db.session.rollback()
        abort(500)
    else:
      abort(500)
    

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      if actor == None:
        abort(404)
      db.session.delete(actor)
      db.session.commit()
      return jsonify({'success': True, 'deleted': actor_id})
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()

  #  Create Actor
  #  ----------------------------------------------------------------

  @app.route('/actors/create', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor_submission(payload):
    form = ActorForm(request.form, meta={'csrf': False})
    if form.validate():
      try:
        actor = Actor()
        form.populate_obj(actor)
        db.session.add(actor)
        db.session.commit()
        return jsonify({
              'success': True,
              'created': actor.id
              })
      except:
        db.session.rollback()
        abort(500)
      finally:
        db.session.close()

    else:
      abort(500)

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": "unauthorized"
      }), 401

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code

  @app.errorhandler(404)
  def not_found_error(error):
      return jsonify({
          "success": False,
          "message": 'Not found'
      }), 404


  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          "success": False,
          "message": 'Something went wrong'
      }), 500


  if not app.debug:
      file_handler = FileHandler('error.log')
      file_handler.setFormatter(
          Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
      )
      app.logger.setLevel(logging.INFO)
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)
      app.logger.info('errors')

  return app
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

app = create_app()

# Default port:
if __name__ == '__main__':
    # app.debug = True
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
