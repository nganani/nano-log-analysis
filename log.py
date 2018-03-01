# Log Analysis project for nano degree
# Gathering information from a simple database
# Developer: Nir Ganani
#
# Note: since this project was all about database,
# I decided to do the heavy lifting in SQL, even
# though it made more sense in some cases to to it
# in python, to ensure, for example, that changing
# from postgres to mysql will not require using
# different string manupation functions and so on

# #!/usr/bin/env python3

import psycopg2  # postgres library
import datetime  # to allow nicer date format

# Connect to the news database
db = psycopg2.connect("dbname=news")
c = db.cursor()

# Task 1: Most popular 3 articles of all time
# a. select the top 3 from predefined view in the database
query = "SELECT article, views FROM article_view LIMIT 3;"
c.execute(query)
rows = c.fetchall()

# b. print it
base = "   {0}: {1} views"
print("")
print("Most popular 3 articles of all times:")
for row in rows:
    print(base.format(row[0], row[1]))

# Task 2: Most popular authors or all time
# a. select top authors from predefined view in the database
query = "SELECT * FROM author_view;"
c.execute(query)
rows = c.fetchall()

# b. print it
print("")
print("Most popular authors of all times:")
for row in rows:
    print(base.format(row[0], row[1]))

# Task 3: Days with errors > 1%
# a. select the top 3 from predefined view in the database
query = "SELECT * FROM rate WHERE rate > 1 ORDER BY rate;"
c.execute(query)
rows = c.fetchall()

# b. print it
base = "  {0}: {1}% error rate ({2} out of {3} requests)"
print("")
print("Days with errors > 1%:")
for row in rows:
    nice_date = row[0].strftime('%B %d, %Y')  # MMMM DD, YYY format
    print(base.format(nice_date, row[1], row[2], row[3]))

# Close database
db.close()
