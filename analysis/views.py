from django.shortcuts import render
# import mysql.connector
# import pandas as pd
import pyodbc
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def connect_to_database(server, database, uid, pwd, trusted_connection=False):
    connection_string = f"Driver={{SQL Server}};Server={server};Database={database};UID={uid};PWD={pwd};Trusted_Connection=no;"
    connection = pyodbc.connect(connection_string)
    return connection

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def index(request):
    return render(request, 'analysis/index.html')

def display_pivot_tables(request):
    server = 'PHSL-SAPB1-1'
    database = 'PHSL_LIVE_test'
    uid = 'sa'
    pwd = 'B1Admin@123'
    trusted_connection = 'no'

    connection = connect_to_database(server, database, uid, pwd, trusted_connection)

    # query the database 
    query1 = ' SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity'

    query2 = ' SELECT OPOR.DocDate AS PostDate, DocNum, CardName AS Vendor, OPOR.CardCode AS C_Code, ItemName, Quantity FROM OPOR JOIN POR1  ON OPOR.DocEntry = POR1.DocEntry JOIN OITM ON POR1.ItemCode = OITM.ItemCode WHERE year(OPOR.DocDate) = 2023 AND month(OPOR.DocDate) = 12'

    results1 = execute_query(connection, query1)
    results2 = execute_query(connection, query2)

    count_query = 'SELECT COUNT(DISTINCT DocNum) AS TotalDocNumCount FROM (SELECT DocNum FROM ORDR WHERE YEAR(DocDate) = 2023 AND MONTH(DocDate) = 12 UNION SELECT DocNum FROM OPOR WHERE YEAR(DocDate) = 2023 AND MONTH(DocDate) = 12) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query)
        total_doc_num_count = cursor.fetchone()[0]

    count_query1 = 'SELECT COUNT(DISTINCT Customer) AS Totalcustomers FROM (SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query1)
        total_customers = cursor.fetchone()[0]


    count_query2 = 'SELECT SUM(Quantity) AS TotalItems FROM (SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query2)
        total_quantity = cursor.fetchone()[0]

        count_query3 = 'SELECT COUNT(DISTINCT Quantity) AS TotalItems FROM (SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query3)
        total_products = cursor.fetchone()[0]

        count_query4 = 'SELECT COUNT(DISTINCT Quantity) AS TotalItems FROM (SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query4)
        total_cardcode = cursor.fetchone()[0]

    count_query5 = 'SELECT COUNT(DISTINCT Quantity) AS TotalItems FROM (SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query5)
        total_docs = cursor.fetchone()[0]



    connection.close()

    return render(request, 'analysis/results.html', {'total_doc_num_count': total_doc_num_count, 'total_customers': total_customers, 'total_quantity': total_quantity,
                                                     'total_cardcode': total_cardcode,  'results1': results1, 'total_products': total_products, 'total_docs': total_docs })

