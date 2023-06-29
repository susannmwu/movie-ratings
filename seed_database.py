"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# We are using os.system to automatically dropdb and createdb for us
os.system("dropdb ratings")
os.system("createdb ratings")

# Connect to the databases by calling db.create_all
model.connect_to_db(server.app)
model.db.create_all()

# load data/movies.json and save as a variable called movie_data
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    db_movie = crud.create_movie(title, overview, release_date, poster_path)

    # TODO: create a movie here and append it to movies_in_db
    movies_in_db.append(db_movie)

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        # choosing a random movie from our list called movies_in_db
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()
