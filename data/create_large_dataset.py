import os
import sys
import psycopg2

datafile = sys.argv[1]
i = 1
with open(datafile, 'r') as df:
    try:
        connection = psycopg2.connect(user="postgres",
                                            password="",
                                            host="localhost",
                                            port="5432",
                                            database="postgres")
    
        for line in df:
            line = line.strip()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO players VALUES (%s,%s)"""
            name = "Document"+str(i)
            i = i+1
            record_to_insert = (name, line)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
        # print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
