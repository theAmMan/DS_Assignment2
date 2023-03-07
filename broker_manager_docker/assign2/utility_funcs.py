import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import docker

#A file for utility functions 
def get_link(port:int) -> str:
    base = "http://127.0.0.1:"
    base += str(port)
    # base += "/"
    return base

def create_database(id: int):
    con = psycopg2.connect(dbname='queue',
        user='postgres', host='localhost',
        password='eshamanideep25')

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

    cur = con.cursor()

    database_name = "queue"+str(id)

    #Try to create the database if it does not exist
    try: 
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(database_name))
            )
    except:
        #Do nothing as the database already exists 
        pass

def delete_database(id: int):
    con = psycopg2.connect(dbname='queue',
        user='postgres', host='localhost',
        password='eshamanideep25')

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

    cur = con.cursor()

    database_name = "queue"+str(id)

    #Try to create the database if it does not exist
    try: 
        cur.execute(sql.SQL("DELETE DATABASE {}").format(
                sql.Identifier(database_name))
            )
    except:
        #Do nothing as the database does not exist
        pass 

def run_broker_container(broker_id: int):
    client = docker.from_env()
    env_str = "NAME=queue"+str(broker_id)
    ports = {'8000/tcp':7000+broker_id}
    cont = client.containers.run('broker', environment = [env_str], ports = ports)
