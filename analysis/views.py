from django.shortcuts import render
import mysql.connector
import pandas as pd
import pyodbc

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

def create_pivot_table(data, index_column, values_column):
    pivot_table = pd.pivot_table(data, index=index_column, values=values_column)
    return pivot_table

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
    query1 = ' SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 9 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity'

    query2 = ' SELECT OPOR.DocDate AS PostDate, DocNum, CardName AS Vendor, OPOR.CardCode AS C_Code, ItemName, Quantity FROM OPOR JOIN POR1  ON OPOR.DocEntry = POR1.DocEntry JOIN OITM ON POR1.ItemCode = OITM.ItemCode WHERE year(OPOR.DocDate) = 2023 AND month(OPOR.DocDate) = 9'

    results1 = execute_query(connection, query1)
    results2 = execute_query(connection, query2)

    count_query = 'SELECT COUNT(DISTINCT DocNum) AS TotalDocNumCount FROM (SELECT DocNum FROM ORDR WHERE YEAR(DocDate) = 2023 AND MONTH(DocDate) = 9 UNION SELECT DocNum FROM OPOR WHERE YEAR(DocDate) = 2023 AND MONTH(DocDate) = 9) AS CombinedDocs'
    with connection.cursor() as cursor:
        cursor.execute(count_query)
        total_doc_num_count = cursor.fetchone()[0]


    count_query1 = 'SELECT COUNT(DISTINCT CardName) AS TotalCustomers FROM (SELECT DocNum FROM ORDR WHERE YEAR(DocDate) = 2023 AND MONTH(DocDate) = 9) '
    with connetion.cursor() as cursor:
        cursor.execute(count_query1)
        total_customers = cursor.fetchall()[0]


    

# Assuming you have already executed the SQL queries and obtained results1 and results2

# Convert query results into dataframes with custom column names
    # df1 = pd.DataFrame(results1, columns=["PostDate", "DocNum", "Customer", "C_Code", "ItemName", "Quantity"])
    # df2 = pd.DataFrame(results2, columns=["PostDate", "DocNum", "Vendor", "C_Code", "ItemName", "Quantity"])

    # print("Columns of df1:", df1.columns)
    # print("Columns of df2:", df2.columns)

# Create pivot tables with custom column names
    # pivot_table1 = pd.pivot_table(df1, index=["PostDate", "DocNum", "Customer", "C_Code"], values="Quantity", aggfunc="sum", fill_value=0)
    # pivot_table2 = pd.pivot_table(df2, index=["PostDate", "DocNum", "Vendor", "C_Code"], values="Quantity", aggfunc="sum", fill_value=0)


    # convert query results into dataframes
    # df1 = pd.DataFrame(results1, columns=["Column1", "Column2", ])
    # df2 = pd.DataFrame(results2, columns=["Column1", "Column2", ])

    # create pivot tables 
    # pivot_table1 = create_pivot_table(df1, index_column="IndexColumn", values_column="ValueColumn")
    # pivot_table2 = create_pivot_table(df2, index_column="IndexColumn", values_column="ValueColumn")

    connection.close()

    # render HTML Templates with the pivot tables 
    # return render(request, 'analysis/pivot_tables.html', {'pivot_table1': pivot_table1, 'pivot_table2': pivot_table2})

    return render(request, 'analysis/results.html', {'total_doc_num_count': total_doc_num_count, 'total_customers': total_customers})

from django.shortcuts import render
import pandas as pd
import plotly.express as px

def display_sales_analysis(request):
    server = 'PHSL-SAPB1-1'
    database = 'PHSL_LIVE_test'
    uid = 'sa'
    pwd = 'B1Admin@123'
    trusted_connection = 'no'

    connection = connect_to_database(server, database, uid, pwd, trusted_connection)

    # query the database 
    query1 = ' SELECT ORDR.DocDate AS PostDate, DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, ItemName, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 '

    query2 = ' SELECT OPOR.DocDate AS PostDate, DocNum, CardName AS Vendor, OPOR.CardCode AS C_Code, ItemName, Quantity FROM OPOR JOIN POR1  ON OPOR.DocEntry = POR1.DocEntry JOIN OITM ON POR1.ItemCode = OITM.ItemCode WHERE year(OPOR.DocDate) = 2023'

    results1 = execute_query(connection, query1)
    results2 = execute_query(connection, query2)
    # Assuming you have the results1 data
    # You can create a DataFrame from the results
    df1 = pd.DataFrame(results1, columns=["ORDR_PostDate", "ORDR_DocNum", "ORDR_Customer", "ORDR_C_Code", "OITM_ItemName", "RDR1_Quantity"])

    # Preprocess data
    df1['ORDR_PostDate'] = pd.to_datetime(df1['ORDR_PostDate'])
    df1[ 'Year' ] = df1['ORDR_PostDate'].dt.year

    # Group by year and sum sales
    total_sales_by_year = df1.groupby('Year')['RDR1_Quantity'].sum().reset_index()

    # Create a bar chart
    chart = px.bar(total_sales_by_year, x='Year', y='RDR1_Quantity', title='Total Sales by Year')

    # Convert chart to HTML
    chart_html = chart.to_html(full_html=False)

    # Render HTML Templates with the chart
    return render(request, 'analysis/sales_analysis.html', {'chart_html': chart_html})
