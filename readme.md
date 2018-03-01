# Log Analysis project for nano degree
### Gathering information from a simple database
Developer: Nir Ganani

## Overview
Part of Full Stack Web Developer Nanodegree course. Three printouts were
requested here, based on a given database:
1. Most popular three articles of all time
2. Most popular authors or all time
3. Days that had more than 1% error rate in them

### How to run this code
Install postgres if not already installed, create empty database called 'news'
and upload the data into it. then, clone this GitHub repo to your local machine.
See below the process to do so:
1. install PostgresSQL on your machine see
[here](https://wiki.postgresql.org/wiki/Detailed_installation_guides){:target="_blank"}
for more details.
2. Use the command ```psql -d postgres``` to enter the defult database. If you
encounter issue with your credentials and permissions in postgres, see [this](https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge){:target="_blank"}
article that may help.
3. Create new database named 'news', using this command ```CREATE DATABASE news;```
4. Next, download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
You will need to unzip this file after downloading it. The file inside is
called ```newsdata.sql```.
5. Use the command psql -d news -f newsdata.sql to upload it
6. Finally, to run the code, simply type ```python3 log.py``` in the cloned local folder.
Code was written with python 3 in mind, but should work just file on python 2.
You should get the response shown in the ```output.txt``` in this git repo

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
Slug and views, counted from the logs.
```
create view hits as
select substring(path from 10) as slug, count(path)
from log
where (status = '200 OK') and (position('/article/' in path) = 1)
group by path
order by count desc;
```
This view  ‘almost’ solved item 1, but it does not have the real article name,
only the slug. We will fix this, using the ‘article_view’ below.

### View 2: err (‘table’ # 5)
Counts how many errors ('not OK') and total requests per day.
```
create view err as
select time::date as date, COUNT(CASE WHEN status != '200 OK' THEN 1 ELSE NULL END) AS errors, count(*) as total
from log
group by date
order by errors desc;
```

### View 3: rate (‘Table’ #6)
Create error rate from the errors. this could be easily done in python, but
as said above, I tried to maximize the training in SQL so created another view,
even though it is not efficient or best practice here.
```
Create view rate as
Select date, round((errors*1.00/total*100), 2) as rate, errors, total
From err
Group by date, errors, total
Order by rate desc;
```

### View 4: article_view (‘table’ #7)
Article view helps task 1 (popular articles) and 2 (popular authors). For
the latter, author_view will aggregate multiple articles written by the
same author from this view.
```
Create view article_view as
select hit_art.title as article, authors.name as author, hit_art.count as views
from (hits join articles
on hits.slug = articles.slug)
as hit_art
join authors
on hit_art.author = authors.id
order by count desc;
```

### View 5: author_view (‘table’ #8)
Aggregates multiple articles written by the same author from the above view.
```
Create view author_view as
select author, sum(views) as views
from article_view
group by author
order by views desc;
```
