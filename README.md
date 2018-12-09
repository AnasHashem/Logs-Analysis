# Logs-Analysis
## Project Description
* This is a reporting tool that is built using a news website database, and a python script. The news 
database structure is as follows:
- It contains 3 tables which are: artictles, authors and log.
- "log" table contains information about the visits to the website and the views of articles.
- It uses 4 views as descirbed below.
The tool calculates stats about:
1: The most popular three articles.
2: The most popular authors.
3: The days with error rate > 1.
The tool uses python programming language and postgre sql database system.

## System Requirments 
-python3
-vagrant 2.20
-virtual box
-cloning this repo https://github.com/udacity/fullstack-nanodegree-vm
-adding the folder to the vagrant directory  
-Importing it to postgr sql using this command 'psql -d news -f newsdata.sql'
-Connecting to the database using 'psql -d news'

## Running the Tool
Run the tool by typing the following in the command line of vagrant virtual 'python Log\ Analysis.py'
The output is in console.


Used views:
1: The most popular three articles.
---------------------------------------------------------------------------------
create view top_articles as select articles.slug, count(*) as views
from log join articles on log.path like '%' || articles.slug 
where status = '200 OK' and path != '/'
group by articles.slug order by views desc;


3: The days with error rate > 1.
---------------------------------------------------------------------------------
create view all_visits as select date(time) as day, count(*) as visits from log 
	group by day order by day;
---------------------------------------------------------------------------------
create view error_visits as select date(time) as day, count(*) as errors from log
	where status = '404 NOT FOUND'
	group by day order by day;
---------------------------------------------------------------------------------
create view results as select all_visits.day, (cast(error_visits.errors as float(2))/all_visits.visits)*100
as result from all_visits, error_visits 
where all_visits.day = error_visits.day;
---------------------------------------------------------------------------------
