#!/usr/bin/env python
import psycopg2

dbname = "news"
db = psycopg2.connect(database=dbname)
c = db.cursor()
# The most popular three top_articles ..
c.execute('select * from top_articles limit 3')
top_articles = c.fetchall()
print("The most popular three articles are:\n")
count = 0
for row in top_articles:
    if count == 3:
        break
    print("{}. _____ {} views\n".format(row[0], row[1]))
    count += 1

# The most popular authors ..
c.execute('''\
    select authors.name, sum(top_articles.views) as auth_views
    from authors, top_articles, articles
    where top_articles.slug = articles.slug
    and articles.author = authors.id
    group by authors.name
    order by auth_views desc
    ''')
top_authors = c.fetchall()
print("The most popular authors are:\n")
for row in top_authors:
    print("- {} _____ {} views\n".format(row[0], row[1]))

# The days with error rate > 1 ..
c.execute('''\
    select day, cast(result as numeric(3,2)) as final_result
    from results where result > 1
    ''')
error_days = c.fetchall()
print("The days with error rate > 1 are:")
s = ""
for row in error_days:
    s = str(row[0].strftime('%d %B %Y'))
    print("- {} ____ {}% errors\n".format(s, row[1]))