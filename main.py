import sqlite3
import requests
import sys
import json
import pandas as pd

con = sqlite3.connect("the_database.db")
cur = con.cursor()

# create tables
cur.execute("""
            CREATE TABLE films (
            film_id INT PRIMARY KEY,
            name VARCHAR(50)
            ); """)

cur.execute("""
            CREATE TABLE genre (
            film_id INT,
            name VARCHAR(20)
            ); """)

cur.execute("""
            CREATE TABLE scores (
            film_id INT,
            critics INT,
            audience INT
            ); """)

cur.execute("""
            CREATE TABLE imdb (
            film_id INT,
            imdb_id VARCHAR(10)
            ); """)

cur.execute("""
            CREATE TABLE earnings (
            film_id INT,
            opening_weekend FLOAT,
            domestic_gross FLOAT,
            foreign_gross FLOAT,
            world_gross FLOAT
            ); """)

# make data sources usable
try:
    df = pd.read_csv("HollywoodMovies.csv")
except FileNotFoundError:
    print("Please supply the HollywoodMovies.csv file", file=sys.stderr)
    sys.exit(1)

cur.execute('ATTACH DATABASE "sakila_master.db" AS sakila')

# prep to fill tables
# use sakila table to get the desired genre names
cur.execute("SELECT name FROM sakila.category")
categories = [row[0] for row in cur.fetchall()]

for i in range(50):
    # populate films
    cur.execute("INSERT INTO films (film_id,name) VALUES (?,?)", (i, df["Movie"].iloc[i]))

    # populate genre
    genre = ""
    if df["Genre"].iloc[i] in categories:
        genre = df["Genre"].iloc[i]
    else:
        genre = None
    cur.execute("INSERT INTO genre (film_id,name) VALUES (?,?)", (i, genre))

    # populate scores
    cur.execute("INSERT INTO scores (film_id, critics, audience) VALUES (?,?,?)",
                (i, df["RottenTomatoes"].iloc[i], df["AudienceScore"].iloc[i]))

    # populate earnings
    ow = df["OpeningWeekend"].iloc[i]
    dg = df["DomesticGross"].iloc[i]
    fg = df["ForeignGross"].iloc[i]
    wg = df["WorldGross"].iloc[i]
    cur.execute("""INSERT INTO earnings (film_id,
                                        opening_weekend,
                                        domestic_gross,
                                        foreign_gross,
                                        world_gross) VALUES (?,?,?,?,?) """,
                (i, ow, dg, fg, wg))

    # populate imdb
    key = "c86d7e72"
    try:
        response = requests.get(f"http://www.omdbapi.com/?apikey={key}&s={df['Movie'].iloc[i]}")
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("movie not found", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException:
        print("api call failed", file=sys.stderr)
        sys.exit(1)
    data = response.json()

    imdb = ""
    # handle if movie does not exist
    if data["Response"] == "True":
        imdb = data["Search"][0]["imdbID"]
    else:
        imdb = None

    cur.execute("INSERT INTO imdb (film_id, imdb_id) VALUES (?,?)", (i, imdb))

con.commit()
con.close()
