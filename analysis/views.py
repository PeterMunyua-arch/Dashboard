from itertools import count
from django.shortcuts import render
# import mysql.connector
# import pandas as pd
import pyodbc
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime

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
    database = 'zz_ptl_test'
    uid = 'sa'
    pwd = 'B1Admin@123'
    trusted_connection = 'no'

    connection = connect_to_database(server, database, uid, pwd, trusted_connection)

    # query the database 
    query3 = " PREPARE PTL_Order_Tracker_Report '20231213', '20231213' SELECT "

    # query1 = ' SELECT ORDR.DocDate AS PostDate,  DocNum, CardName AS Customer, ORDR.CardCode AS C_Code, Quantity FROM ORDR JOIN RDR1  ON ORDR.DocEntry = RDR1.DocEntry JOIN OITM ON RDR1.ItemCode = OITM.ItemCode  WHERE year(ORDR.DocDate) = 2023 AND month(ORDR.DocDate) = 12 GROUP BY ORDR.DocDate, DocNum, CardName, ORDR.CardCode, Quantity'

    # query2 = ' SELECT OPOR.DocDate AS PostDate, DocNum, CardName AS Vendor, OPOR.CardCode AS C_Code, ItemName, Quantity FROM OPOR JOIN POR1  ON OPOR.DocEntry = POR1.DocEntry JOIN OITM ON POR1.ItemCode = OITM.ItemCode WHERE year(OPOR.DocDate) = 2023 AND month(OPOR.DocDate) = 12'

    # results1 = execute_query(connection, query1)
    #results3 = execute_query(connection, query3)

    count_query10 = "exec PTL_Order_Tracker_Report '20231213', '20231213'"
    with connection.cursor() as cursor:
        cursor.execute(count_query10)
        orders = cursor.fetchall()

        columns = ['DocNum', 'SeriesName', 'SO Posting Date', 'CardCode', 'Customer Name', 'NumAtCard', 'Time Order Received',
               'Sales Order Value', 'Invoice Value', '% Supplied', 'Created By', 'Sales Order Added Date',
               'Sales Order Added Time', 'Sales Order Added By', 'Delivery Doc Num', 'Delivery Added Date',
               'Delivery Added Time', 'Picked By', 'Confirmed By', 'Invoice No', 'Invoice Date', 'Invoice Creation Date',
               'Invoice Creation Time']

    #count_query9 = "exec PTL_Order_Tracker_Report '20231213', '20231213'; SELECT COUNT(DISTINCT SeriesName) AS SeriesNameCount FROM SeriesName;"
   # with connection.cursor() as cursor:
        #cursor.execute(count_query9)
        #series_name_count = cursor.fetchone()[0]

    count_query15 = "exec PTL_Order_Tracker_Report '20231213', '20231213' SELECT COUNT(*) AS SeriesCount FROM SeriesName;"
    with connection.cursor() as cursor:
        cursor.execute(count_query15)
        series_count = cursor.fetchall()


    count_query8 = "exec PTL_Order_Tracker_Report '20231213', '20231213' SELECT COUNT(DISTINCT CustomerName) AS Customers FROM CustomerName"
    with connection.cursor() as cursor:
        cursor.execute(count_query8)
        customers = cursor.fetchone()[0]

    count_query7 = " DECLARE @count INT; exec PTL_Order_Tracker_Report'20231213', '20231213'; @SeriesName = @count OUTPUT; SELECT @count AS Series;"
    with connection.cursor() as cursor:
        cursor.execute(count_query7)
        series_name_count = cursor.fetchone()[0]

#DECLARE @count INT;

#EXEC uspFindProductByModel
   # @model_year = 2018,
   # @product_count = @count OUTPUT;    


    # count_query11 = "SELECT COUNT(DISTINCT DocNum) AS TotalInvoices FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
    #with connection.cursor() as cursor:
       # cursor.execute(count_query11)
       # total_invoices = cursor.fetchone()[0]

    

    #count_query = "SELECT COUNT(DISTINCT DocNum) AS TotalInvoices FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
    #with connection.cursor() as cursor:
        #cursor.execute(count_query)
       # total_invoices = cursor.fetchone()[0]

    #count_query1 = "SELECT COUNT(DISTINCT Customer Name) AS Totalcustomers FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
   # with connection.cursor() as cursor:
       # cursor.execute(count_query1)
       # total_customers = cursor.fetchone()[0] 'tota
       # l_invoices': total_invoices, 'total_customers': total_customers, 'total_invoices': total_invoices
 

    
    connection.close()

    return render(request, 'analysis/results.html', { 'orders': orders, 'columns': columns, 'series_count': series_count, 'customers': customers })


def view(request):
    server = 'PHSL-SAPB1-1'
    database = 'zz_ptl_test'
    uid = 'sa'
    pwd = 'B1Admin@123'
    trusted_connection = 'no'

    connection = connect_to_database(server, database, uid, pwd, trusted_connection)
    with connection.cursor() as cursor:
        # Execute the stored procedure with parameters
        cursor.execute(" exec PTL_Order_Tracker_Report '20231213', '20231213' ")

        # Fetch the results from the stored procedure
        result_set = cursor.fetchall()


    # Extracting specific fields from the result set
   
    data_to_display = [
        
        {
            'Order_Date': row[11].strftime("%Y-%m-%d") if row[11] else None,       # Assuming the 5th column is 'Customer Name'
            'Order_No': row[0],     # Assuming the 15th column is 'Invoice No'
            'Customer_Name': row[4],        # Assuming the 4th column is 'SO Posting Date'
            'Time_OrderReceived': row[6],
            'Posting_Time': row[12],
            'Created_By': row[10],
            'Delivery_No': row[14],
            'Delivery_DateTime': row[16],
            'Invoice_No': row[19],
            'Invoice_Date': row[20].strftime("%Y-%m-%d") if row[20] else None,
            'Invoice_Time': row[22],
            'Percentage_Supplied': f"{round(row[9], 2)}%"
                              # Assuming the 13th column is 'Quantity'
        }
        for row in result_set
        
    ]

    count_query1 = """ SELECT COUNT(*) as ApprovedCount FROM (
                    SELECT DISTINCT T0.[DocEntry], T0.Draftentry,T0.[WddCode],T0.[DocDate],T1.[CardName], T0.[Status],  Case when T0.[Status]='W' then 'Pending' 
                    When T0.[Status]='Y' then 'Approved' when T0.[Status]='N' then 'Rejected' When T0.[Status]='A' then 'Generated' else 'Null' end as State
                    ,CASE WHEN LEN(T0."CreateTime") = 6 THEN LEFT(T0."CreateTime", 2) + ':' + RIGHT(LEFT(T0."CreateTime", 4),2)
                    WHEN LEN(T0."CreateTime") = 5 THEN LEFT(T0."CreateTime",1) + ':' + RIGHT(LEFT(T0."CreateTime",3),2) 
                    ELSE LEFT(T0."CreateTime",1) + ':' + RIGHT(T0."CreateTime",2) END AS 'Time'
                    FROM OWDD T0 
                    INNER JOIN ODRF T1 ON T0.[Draftentry]=T1.[DocEntry]
                    WHERE T0.[CreateDate]='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112) 
                    and  T0.[ObjType] =17 
                    and T0.[Status] = 'Y')A """
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
                   WHERE T0.[CreateDate]='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112) 
                   and  T0.[ObjType] =17 
                   and T0.[Status] = 'W')A """
    with connection.cursor() as cursor:
        cursor.execute(count_query2)
        not_approved = cursor.fetchone()

    not_approved =  not_approved[0] if  not_approved else None



    count_query3 = """ SELECT COUNT([Order Number])[picking] from 
                   (SELECT DISTINCT T0.[DocNum][Order Number]
                   FROM ODLN T0  
                   WHERE T0.[Series] not in (216,205,192) and T0.DocStatus='o' and  T0.DocDate='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112)
                   )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query3)
        picking = cursor.fetchone()

    picking = picking[0] if picking else None


    count_query4 = """ SELECT COUNT([Order Number])[picked] from 
                   (SELECT DISTINCT T0.[DocNum][Order Number]
                    FROM ODLN T0  

                    WHERE T0.[Series] not in (216,205,192) and T0.DocStatus='c' and  T0.DocDate='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112)
                   )A """
    with connection.cursor() as cursor:
        cursor.execute(count_query4)
        Picked = cursor.fetchone()

    Picked = Picked[0] if Picked else None


    count_query5 = """ SELECT SUM([Not Invoiced])[Pending Invoice] FROM (
                   SELECT COUNT([Order Number])[Not Invoiced] from 
                   (
                   SELECT DISTINCT T0.[DocNum][Order Number]
                   FROM ORDR T0  

                   WHERE T0.[Series] not in (216,205,192) and T0.DocStatus='o' and  T0.DocDate='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112)
                   )A


                  UNION ALL

                  SELECT COUNT([Order Number])[Open invoices] from 
                  (
                  SELECT DISTINCT T0.[DocNum][Order Number]
                  FROM OINV T0  

                  WHERE T0.[Series] <>183  and T0.DocDate='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112)
                  )A

                  )M """
    with connection.cursor() as cursor:
        cursor.execute(count_query5)
        pending = cursor.fetchone()

    pending = pending[0] if pending else None

    count_query6 = """ SELECT COUNT([Order Number])[Open invoices] from 
                      (
                      SELECT DISTINCT T0.[DocNum][Order Number]
                      FROM OINV T0  

                      WHERE T0.[Series] <>183  and T0.DocDate='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112)
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
                        WHERE T0.[CreateDate]='20231213' ---UNCOMMENT ON GO LIVE CONVERT(varchar(8), GETDATE(), 112) 
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

    return render(request, 'analysis/count.html', {'data_to_display': data_to_display, 'not_approved':  not_approved, 'approved': approved, 'pending': pending, 'picking': picking, 'Picked': Picked, 'Rejected': Rejected, 'invoiced':invoiced})



from django.shortcuts import render
from django.db import connection

def your_view(request):
    # Assuming you have a date range, replace these with your desired values
    from_date = '2023-12-13'
    to_date = '2023-12-13'

    with connection.cursor() as cursor:
        # Execute the stored procedure with parameters
        cursor.execute("EXEC PTL_Order_Tracker_Report %s, %s", [from_date, to_date])

        # Fetch the results from the stored procedure
        result_set = cursor.fetchall()

    # Extracting specific fields from the result set
    data_to_display = [
        {
            'customer_name': row[4],       # Assuming the 5th column is 'Customer Name'
            'invoice_number': row[14],     # Assuming the 15th column is 'Invoice No'
            'posting_date': row[3],        # Assuming the 4th column is 'SO Posting Date'
            'quantity': row[12],           # Assuming the 13th column is 'Quantity'
        }
        for row in result_set
    ]

    # Calculate counts
    #docnum_count = len(set(row[1] for row in result_set))  # Assuming the 2nd column is 'DocNum'
    #quantity_count = sum(row[12] for row in result_set)    # Assuming the 13th column is 'Quantity'

    cursor.execute("""
            SELECT
                COUNT(DISTINCT DocNum) AS DocNumCount,
                SUM(Quantity) AS QuantityCount
            FROM (
                EXEC PTL_Order_Tracker_Report %s, %s
            ) AS SubqueryResult
        """, [from_date, to_date])

    counts = cursor.fetchone()
    docnum_count = counts[0]
    quantity_count = counts[1]

    return render(request, 'your_template.html', {'data_to_display': data_to_display, 'docnum_count': docnum_count, 'quantity_count': quantity_count})
