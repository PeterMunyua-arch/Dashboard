from django.shortcuts import render
import mysql.connector
import pandas as pd

def connect_to_database(host, user, password, database, trusted_connection=False):
    connection = mysql.connector.connect(
        host=host,
        user=user, 
        password=password,
        database=database,
        trusted_connection=False
    )

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def create_pivot_table(data, index_column, values_column):
    pivot_table = pd.pivot_table(data, index=index_column, values=values_column)
    return pivot_table

def index(request):
    return render(request, 'analysis/index.html')

def display_pivot_tables(request):
    host = ''
    user = ''
    password = ''
    database = ''
    trusted_connection = False

    connection = connect_to_database(host, user, password, database, trusted_connection)

    # query the database 
    query1 = 'SELECT * FROM ODLN'
    query2 = 'SELECT * FROM DLN1'

    results1 = execute_query(connection, query1)
    results2 = execute_query(connection, query2)

    # convert query results into dataframes
    df1 = pd.DataFrame(results1, columns=["Column1", "Column2", ])
    df2 = pd.DataFrame(results2, columns=["Column1", "Column2", ])

    # create pivot tables 
    pivot_table1 = create_pivot_table(df1, index_column="IndexColumn", values_column="ValueColumn")
    pivot_table2 = create_pivot_table(df2, index_column="IndexColumn", values_column="ValueColumn")

    connection.close()

    # render HTML Templates with the pivot tables 
    return render(request, 'analysis/pivot_tables.html')