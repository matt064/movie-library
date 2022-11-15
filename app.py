from flask import Flask, jsonify
from models import movies
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)
app.config["SECRET_KEY"] = "mateo"


@app.route("/api/movies/", methods=["GET"])
def todos_list_api_v1():
    #wyswietlenie wszystkich filmow
    return jsonify(movies.all())


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    #wyswietlenie pojedynczego filmu
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    return jsonify({"movie": movie})


@app.route("/api/movies/", methods=["POST"])
def create_movie():
    #utworzenie nowego wpisu w bibliotece
    movie = {
        'id': movies.all()[-1]['id'] + 1,
        'title': request.json["title"],
        'genre': request.json['genre'],
        'watched': False
    }
    movies.create(movie)
    return jsonify({'movie': movie}), 201


@app.route("/api/movies/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    #usuniecie filmu ze zbioru
    result = movies.delete(movie_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    #nadpisanie wybranego elementy slownika
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'watched' in data and not isinstance(data.get('watched'), bool)
    ]):
        abort(400)
    movie = {
        'title': data.get('title', movie['title']),
        'genre': data.get('genre', movie['genre']),
        'watched': data.get('watched', movie['watched'])
    }
    movies.update(movie_id, movie)
    return jsonify({'movie': movie})



@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


if __name__ == "__main__":
    app.run(debug=True)