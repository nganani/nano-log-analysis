# Log Analysis project for nano degree
### Gathering information from a simple database
Developer: Nir Ganani

## Overview
Part of Full Stack Web Developer Nanodegree course. Three printouts were
requested here, based on a given database:
1. Most popular three articles of all time
2. Most popular authors or all time
3. Days that had more than 1% error rate in them

### Note
Since this project was all about learning about relational databases and SQL,
I decided to do the heavy lifting in SQL, even
though it made more sense in some cases to to it
in python. For example, it would probably made much more sense to do the string
manipulation in python and not in SQL as a. it is more rebust and b. it
removes the dependency on string functions that are in many cases different
between databases and will therefore make it harder to port this code.

## views
As said above, I mostly used SQL to 'solve' the three tasks requested and in
order to make it cleaner, I used several views to help make the SQL and the
python code cleaner and more orgenized, easy to maintain and understand.
Below are the views I used.

### View 1: hits (‘table’ #4)
'''create view hits as
select substring(path from 10) as slug, count(path)
from log
where (status = '200 OK') and (position('/article/' in path) = 1)
group by path
order by count desc;'''
