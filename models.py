import json

class Movies():
    def __init__(self):
        try:
            with open("movies.json", "r") as f:
                self.movies = json.load(f)
        except FileNotFoundError:
            self.movies = []
    

    def all(self):
        return self.movies


    def get(self, id):
        movie = [movie for movie in self.all() if movie['id'] == id]
        if movie:
            return movie[0]
        return []


    def create(self, data):
        self.movies.append(data)
        self.save_all()

    
    def delete(self, id):
        movie = self.get(id)
        if movie:
            self.movies.remove(movie)
            self.save_all()
            return True
        return False
    

    def save_all(self):
        with open("movies.json", "w") as f:
            json.dump(self.movies, f)


    def update(self, id, data):
        movie = self.get(id)
        if movie:
            index = self.movies.index(movie)
            self.movies[index] = data
            self.save_all()
            return True
        return False

  
movies = Movies()
