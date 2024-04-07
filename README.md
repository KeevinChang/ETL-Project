# ETL-Project

Process:
I began first by searching for a relational database that I would want to work with
as I felt that would be the most difficult step in this project. After deciding upon the Sakila
database, I sought out a CSV file and public API that related to movies. I settled on a Hollywood Movies
CSV file and found a simple public API in OMDB.

Code:
- import sqlite in python
- connect/create database to store my tables
- initially create the tables, allowing all to share film_id to allow for connections between tables
- open csv file with error handling in case file is not in the proper directory
- establish connection to sakila database and attach so both databases can be used at the same time
- begin inserting values
- for api call, allow key to be an easily changeable value for any user and the request updates dynamically with iterations
- commit changes to data base and close connection
