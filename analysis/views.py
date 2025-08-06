from errno import EINPROGRESS
from itertools import count
from django.shortcuts import render
# import mysql.connector
# import pandas as pd
import pyodbc
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime

def connect_to_database(server, database, uid, pwd, trusted_connection=False):
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server};Database={database};UID={uid};PWD={pwd};Trusted_Connection=no;TrustServerCertificate=yes;"
    connection = pyodbc.connect(connection_string)
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def index(request):
    return render(request, 'analysis/index.html')


def view(request):
    server = ''
    database = ''
    uid = ''
    pwd = ''
    trusted_connection = 'no'

    connection = connect_to_database(server, database, uid, pwd, trusted_connection)
    with connection.cursor() as cursor:
        # Execute the stored procedure with parameters
        cursor.execute(" exec Report ")

        # Fetch the results from the stored procedure
        result_set = cursor.fetchall()


    # Extracting specific fields from the result set
   
    data_to_display = [
        
        {
            'Order_Date': row[11].strftime("%Y-%m-%d") if row[11] is not None else 'Inprogress',       # Assuming the 5th column is 'Customer Name'
            'Order_No': row[0],     # Assuming the 15th column is 'Invoice No'
            'Customer_Name': row[4],        # Assuming the 4th column is 'SO Posting Date'
            'Time_OrderReceived': row[6],
            'Posting_Time': row[12],
            'Created_By': row[10],
            'Delivery_No': row[14] if row[14] is not None else 'Inprogress',
            'Delivery_DateTime': row[16] if row[16] is not None else 'Inprogress',
            'Invoice_No': row[19] if row[19] is not None else 'Inprogress',
            'Invoice_Date': row[20].strftime("%Y-%m-%d") if row[20] is not None else 'Inprogress',
            'Invoice_Time': row[22] if row[22] is not None else 'Inprogress',
            'Percentage_Supplied': f"{round(row[9] * 100, 0)}%"
                              # Assuming the 13th column is 'Quantity'
        }
        
        for row in result_set if round(row[9] * 100, 0) != 100
        
    ]

    count_query1 = """ SELECT COUNT(*) as ApprovedCount FROM (
                    SELECT DISTINCT T0.[DocEntry], /*T0.Draftentry,T0.[WddCode],*/T0.[DocDate],T1.[CardName], T0.[Status],  Case when T0.[Status]='W' then 'Pending' 
                    When T0.[Status]='Y' then 'Approved' when T0.[Status]='N' then 'Rejected' When T0.[Status]='A' then 'Generated' else 'Null' end as State
                    ,CASE WHEN LEN(T0."CreateTime") = 6 THEN LEFT(T0."CreateTime", 2) + ':' + RIGHT(LEFT(T0."CreateTime", 4),2)
                    WHEN LEN(T0."CreateTime") = 5 THEN LEFT(T0."CreateTime",1) + ':' + RIGHT(LEFT(T0."CreateTime",3),2) 
                    ELSE LEFT(T0."CreateTime",1) + ':' + RIGHT(T0."CreateTime",2) END AS 'Time'
                    FROM OWDD T0 
                    INNER JOIN ODRF T1 ON T0.[Draftentry]=T1.[DocEntry]
                    WHERE T0.[CreateDate]= CONVERT(varchar(8), GETDATE(), 112) 
                    and  T0.[ObjType] =17 
                    and T0.[Status] = 'Y' and T0.DocEntry is not null
					)A """
    with connection.cursor() as cursor:
        cursor.execute(count_query1)
        approved = cursor.fetchone()

    approved = approved[0] if approved else None

    count_query2 = """ SELECT COUNT(*) as NOTAPPROVED FROM (
                   SELECT DISTINCT T0.[DocEntry], T0.Draftentry,T0.[WddCode],T0.[DocDate],T1.[CardName], T0.[Status],  Case when T0.[Status]='W' then 'Pending' 
                   When T0.[Status]='Y' then 'Approved' when T0.[Status]='N' then 'Rejected' When T0.[Status]='A' then 'Generated' else 'Null' end as State
                   ,CASE WHEN LEN(T0."CreateTime") = 6 THEN LEFT(T0."CreateTime", 2) + ':' + RIGHT(LEFT(T0."CreateTime", 4),2)
                   WHEN LEN(T0."CreateTime") = 5 THEN LEFT(T0."CreateTime",1) + ':' + RIGHT(LEFT(T0."CreateTime",3),2) 
                   ELSE LEFT(T0."CreateTime",1) + ':' + RIGHT(T0."CreateTime",2) END AS 'Time'
                   FROM OWDD T0 
                   INNER JOIN ODRF T1 ON T0.[Draftentry]=T1.[DocEntry]
                   WHERE T0.[CreateDate]= CONVERT(varchar(8), GETDATE(), 112) 
                   and  T0.[ObjType] =17 
                   and T0.[Status] = 'W')A """
    with connection.cursor() as cursor:
        cursor.execute(count_query2)
        not_approved = cursor.fetchone()

    not_approved =  not_approved[0] if  not_approved else None



    count_query3 = """ SELECT COUNT([Order Number])[picking] from 
                   (SELECT DISTINCT T0.[DocNum][Order Number]
                   FROM ORDR T0  
                   WHERE T0.[Series] not in (216,205,192) and T0.DocStatus='o' and  T0.DocDate= CONVERT(varchar(8), GETDATE(), 112)
                   )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query3)
        picking = cursor.fetchone()

    picking = picking[0] if picking else None

    count_query9 = """ SELECT COUNT([Order Number])[picking] from 
                   (SELECT DISTINCT T0.[DocNum][Order Number]
                   FROM ORDR T0  
                   WHERE T0.[Series] not in (216,205,192) and T0.DocStatus='o' and  T0.DocDate>= DATEADD(WEEK, DATEDIFF(WEEK, 0, GETDATE()), 0) -- Start of current week
                   )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query9)
        weekly_ODRD = cursor.fetchone()

    weekly_ODRD = weekly_ODRD[0] if weekly_ODRD else None



    count_query4 = """ SELECT COUNT([Order Number])[picked] from 
                   (SELECT DISTINCT T0.[DocNum][Order Number]
                    FROM ODLN T0  

                    WHERE T0.[Series] not in (216,205,192) and /*T0.DocStatus='c' and*/  T0.DocDate= CONVERT(varchar(8), GETDATE(), 112)
                   )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query4)
        Picked = cursor.fetchone()

    Picked = Picked[0] if Picked else None


    count_query5 = """ SELECT
    CASE
        WHEN SUM([Open invoices]) < 0 THEN 0
        ELSE SUM([Open invoices])
    END AS [Pending Invoice]
FROM (
    SELECT
        -COUNT([Order Number]) AS [Open invoices]
    FROM (
        SELECT DISTINCT T0.[DocNum] AS [Order Number]
        FROM OINV T0  
        WHERE T0.[Series] <> 183  AND T0.DocDate = CONVERT(varchar(8), GETDATE(), 112)
    ) A

    UNION ALL

    SELECT
        COUNT([Order Number]) AS [picked]
    FROM (
        SELECT DISTINCT T0.[DocNum] AS [Order Number]
        FROM ODLN T0  
        WHERE T0.[Series] NOT IN (216, 205, 192) /*AND T0.DocStatus = 'c'*/ AND T0.DocDate = CONVERT(varchar(8), GETDATE(), 112)
    ) A
) M;
 """
    with connection.cursor() as cursor:
        cursor.execute(count_query5)
        pending = cursor.fetchone()

    pending = pending[0] if pending else None

    count_query6 = """ SELECT COUNT([Order Number])[Open invoices] from 
                      (
                      SELECT DISTINCT T0.[DocNum][Order Number]
                      FROM OINV T0  

                      WHERE T0.[Series] <>183 and T0.DocDate= CONVERT(varchar(8), GETDATE(), 112)
                      )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query6)
        invoiced = cursor.fetchone()

    invoiced = invoiced[0] if invoiced else None



    count_query7 = """ SELECT COUNT(*) as Rejected FROM (
                       SELECT DISTINCT T0.[DocEntry], T0.Draftentry,T0.[WddCode],T0.[DocDate],T1.[CardName], T0.[Status],  Case when T0.[Status]='W' then 'Pending' 
                        When T0.[Status]='Y' then 'Approved' when T0.[Status]='N' then 'Rejected' When T0.[Status]='A' then 'Generated' else 'Null' end as State
                        ,CASE WHEN LEN(T0."CreateTime") = 6 THEN LEFT(T0."CreateTime", 2) + ':' + RIGHT(LEFT(T0."CreateTime", 4),2)
                        WHEN LEN(T0."CreateTime") = 5 THEN LEFT(T0."CreateTime",1) + ':' + RIGHT(LEFT(T0."CreateTime",3),2) 
                        ELSE LEFT(T0."CreateTime",1) + ':' + RIGHT(T0."CreateTime",2) END AS 'Time'
                        FROM OWDD T0 
                        INNER JOIN ODRF T1 ON T0.[Draftentry]=T1.[DocEntry]
                        WHERE T0.[CreateDate]=CONVERT(varchar(8), GETDATE(), 112) 
                        and  T0.[ObjType] =17 
                        and T0.[Status] = 'N')A """
    with connection.cursor() as cursor:
        cursor.execute(count_query7)
        Rejected = cursor.fetchone()

    Rejected = Rejected[0] if Rejected else None


   




    # Calculate counts
    # docnum_count = len(set(row[1] for row in result_set))  # Assuming the 2nd column is 'DocNum' 'docnum_count': docnum_count, 'quantity_count': quantity_count
    # quantity_count = sum(int(row[12]) for row in result_set)    # Assuming the 13th column is 'Quantity'
    # Assuming the 13th column is 'Quantity'

    return render(request, 'analysis/count.html', {'data_to_display': data_to_display, 'not_approved':  not_approved, 'approved': approved, 'pending': pending,'weekly_ODRD':weekly_ODRD, 'picking': picking, 'Picked': Picked, 'Rejected': Rejected, 'invoiced':invoiced})

