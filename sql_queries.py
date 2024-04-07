import sqlite3

conn = sqlite3.connect("the_database.db")
cur = conn.cursor()

# check that tables exist
cur.execute("SELECT * FROM films")
print(cur.fetchall())

cur.execute("SELECT * FROM genre")
print(cur.fetchall())

cur.execute("SELECT * FROM scores")
print(cur.fetchall())

cur.execute("SELECT * FROM imdb")
print(cur.fetchall())

cur.execute("SELECT * FROM earnings")
print(cur.fetchall())

# queries
print("////////////////////////////////// query //////////////////////////////////")
# 1
cur.execute("""SELECT genre.name AS genre, AVG(earnings.world_gross) AS mean_world_gross,
                AVG((scores.critics + scores.audience)/2) AS score
                FROM earnings
                JOIN genre ON earnings.film_id = genre.film_id
                JOIN scores ON scores.film_id = genre.film_id
                GROUP BY genre.name""")
print(cur.fetchall())
