import psycopg2, sys
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
import os

print("Getting environment variable...")
database_name = os.environ["NAME"]

con = psycopg2.connect(dbname='queue',
      user='postgres', host='host.docker.internal',
      password='eshamanideep25')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()

#Try to create the database if it does not exist
try: 
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database_name))
        )

except:
    print("Database already exists")

#Communicate with the django app about the 
f = open("database_info.txt", "w")
f.write(sys.argv[1])
f.close()