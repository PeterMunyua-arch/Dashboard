USE [zz_ptl_test]
GO
/****** Object:  StoredProcedure [dbo].[PTL_Order_Tracker_Report]    Script Date: 12/14/2023 12:33:04 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Joash Tumbo
-- Create date: 21.01.22
-- Description:	Order Tracker
-- =============================================

ALTER Procedure [dbo].[PTL_Order_Tracker_Report]

    @FromDate DATETIME, 
	@ToDate DATETIME 
--exec PTL_Order_Tracker_Report '20230530', '20230530'
As
BEGIN


SELECT DISTINCT  A.[DocNum],A.[SeriesName], A.[SO Posting Date],A.CardCode, A.[Customer Name], A.[NumAtCard],/*A.[Date Order Received],*/ A.[Time Order Received],/*A.[Sales Order Status],*/A.[Sales Order Value],A.[Invoice Value],
A.[% Supplied],
A.[Created By],
A.[Sales Order Added Date],A.[Sales Order Added Time],
A.[Sales Order Added By],A.[Delivery Doc Num], A.[Delivery Added Date],
A.[Delivery Added Time],
A.[Picked By],A.[Confirmed By],
A.[Invoice No], A.[Invoice Date],
A.[Invoice Creation Date],A.[Invoice Creation Time]---A.[Invoice created by]
FROM
(

SELECT DISTINCT T1.DocEntry,N1.[SeriesName],  T1.[DocNum], T1.[DocDate] as 'SO Posting Date',--T1.[U_R_Date][Date Order Received], 

Case WHEN LEN(T1.[U_TR_Received]) = 4 THEN LEFT(T1.[U_TR_Received],2) + ':' + RIGHT(T1.[U_TR_Received],2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
ELSE LEFT(T1.[U_TR_Received],1) + ':' + RIGHT(T1.[U_TR_Received],2) /*+ ':00 AM'*/ END AS [Time Order Received],

T1.CardCode, T1.[CardName] as 'Customer Name', T1.[NumAtCard], 
--Case when T1.WddStatus='Y' then 'Approved'when T1.WddStatus='P' THEN 'Generated' when T1.WddStatus='N' then 'Rejected' when T1.WddStatus='W' then 'Pending' Else 'Without Approval' end as [Sales Order Status], 
T1.[DocTotal][Sales Order Value],T5.[DocTotal][Invoice Value], 

Case when T5.DocTotal>=1 then (T5.DocTotal/nullif(T1.DocTotal,0)) else 0 end as  [% Supplied]--,T15.[CreateDate][Date Draft Order Created], 

-----test time for create----

---CASE WHEN LEN(T15.[CreateTime]) = 6 THEN LEFT(T15.[CreateTime], 2) + ':' + RIGHT(LEFT(T15.[CreateTime], 4),2) /*+ ':' + RIGHT(T1."CreateTS",2) + CASE WHEN LEFT(T1."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END*/
--Case WHEN LEN(T15.[CreateTime]) = 4 THEN LEFT(T15.[CreateTime],2) + ':' + RIGHT(T15.[CreateTime],2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
--ELSE LEFT(T15.[CreateTime],1) + ':' + RIGHT(T15.[CreateTime],2) /*+ ':00 AM'*/ END AS [Time Draft Order Created],
---T15.[CreateTime][Time Draft Order Created],,0)





,T30.[U_NAME] AS 'Created By'---,T16.[UpdateDate][Credit Approval Date], 

--Case WHEN LEN(T16.[UpdateTime]) = 4 THEN LEFT(T16.[UpdateTime],2) + ':' + RIGHT(T16.[UpdateTime],2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
--ELSE LEFT(T16.[UpdateTime],1) + ':' + RIGHT(T16.[UpdateTime],2) /*+ ':00 AM'*/ END AS [Credit Approval Time],

--T17.[U_NAME][Approved By],
,T1.[CreateDate][Sales Order Added Date],


/*CASE WHEN LEN(T1."CreateTS") = 6 THEN LEFT(T1."CreateTS", 2) + ':' + RIGHT(LEFT(T1."CreateTS", 4),2) + ':' + RIGHT(T1."CreateTS",2) + CASE WHEN LEFT(T1."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END
WHEN LEN(T1."CreateTS") = 5 THEN LEFT(T1."CreateTS",1) + ':' + RIGHT(LEFT(T1."CreateTS",3),2) + ':' + RIGHT(T1."CreateTS",2) + ' AM' 
ELSE LEFT(T1."CreateTS",1) + ':' + RIGHT(T1."CreateTS",2) + ':00 AM' END AS 'Sales Order Added Time',*/

CASE WHEN LEN(T1."CreateTS") = 6 THEN LEFT(T1."CreateTS", 2) + ':' + RIGHT(LEFT(T1."CreateTS", 4),2) /*+ ':' + RIGHT(T1."CreateTS",2) + CASE WHEN LEFT(T1."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END*/
WHEN LEN(T1."CreateTS") = 5 THEN LEFT(T1."CreateTS",1) + ':' + RIGHT(LEFT(T1."CreateTS",3),2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
ELSE LEFT(T1."CreateTS",1) + ':' + RIGHT(T1."CreateTS",2) /*+ ':00 AM'*/ END AS 'Sales Order Added Time',

T1."CreateTS" [TEST],






T30.[U_NAME][Sales Order Added By],

T3.DocNum as 'Delivery Doc Num', 

T3.[CreateDate][Delivery Added Date],

---Drop----

/*CASE WHEN LEN(T3."CreateTS") = 6 THEN LEFT(T3."CreateTS", 2) + + RIGHT(LEFT(T3."CreateTS", 4),2) + ':' + RIGHT(T3."CreateTS",2) + CASE WHEN LEFT(T3."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END
WHEN LEN(T3."CreateTS") = 5 THEN LEFT(T3."CreateTS",1) + ':' + RIGHT(LEFT(T3."CreateTS",3),2) + ':' + RIGHT(T3."CreateTS",2) + ' AM' 
ELSE LEFT(T3."CreateTS",1) + ':' + RIGHT(T3."CreateTS",2) + ':00 AM' END AS --TT,*/


CASE WHEN LEN(T3."CreateTS") = 6 THEN LEFT(T3."CreateTS", 2) + ':' + RIGHT(LEFT(T3."CreateTS", 4),2) /*+ ':' + RIGHT(T1."CreateTS",2) + CASE WHEN LEFT(T1."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END*/
WHEN LEN(T3."CreateTS") = 5 THEN LEFT(T3."CreateTS",1) + ':' + RIGHT(LEFT(T3."CreateTS",3),2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
ELSE LEFT(T3."CreateTS",1) + ':' + RIGHT(T3."CreateTS",2) /*+ ':00 AM'*/ END AS 'Delivery Added Time',


--T32.[U_NAME]

--' '[Delivery created by],' '[Delivery Picked By],
---' '[Delivery Note Printed Date],' '[Delivery Note Printed Time],


/*T12.DocNum AS 'Return No', T12.DocDate as 'Return Date',*/
T3.[U_ReqName][Picked By], T3.[U_DocAppName][Confirmed By],
T4.Docentry as 'InvEntry' , T5.DocNum as 'Invoice No', T5.DocDate as 'Invoice Date',
T5.[CreateDate][Invoice Creation Date],


----drop------
/*CASE WHEN LEN(T5."CreateTS") = 6 THEN LEFT(T5."CreateTS", 2) + ':' + RIGHT(LEFT(T5."CreateTS", 4),2) + ':' + RIGHT(T5."CreateTS",2) + CASE WHEN LEFT(T5."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END
WHEN LEN(T5."CreateTS") = 5 THEN LEFT(T5."CreateTS",1) + ':' + RIGHT(LEFT(T5."CreateTS",3),2) + ':' + RIGHT(T5."CreateTS",2) + ' AM' 
ELSE LEFT(T5."CreateTS",1) + ':' + RIGHT(T5."CreateTS",2) + ':00 AM' END AS 'Invoice Creation Time',*/


CASE WHEN LEN(T5."CreateTS") = 6 THEN LEFT(T5."CreateTS", 2) + ':' + RIGHT(LEFT(T5."CreateTS", 4),2) /*+ ':' + RIGHT(T1."CreateTS",2) + CASE WHEN LEFT(T1."CreateTS",2) >= 12 THEN ' PM' ELSE ' AM' END*/
WHEN LEN(T5."CreateTS") = 5 THEN LEFT(T5."CreateTS",1) + ':' + RIGHT(LEFT(T5."CreateTS",3),2) /*+ ':' + RIGHT(T1."CreateTS",2) + ' AM'*/ 
ELSE LEFT(T5."CreateTS",1) + ':' + RIGHT(T5."CreateTS",2) /*+ ':00 AM'*/ END AS 'Invoice Creation Time',


---T33.[U_NAME][Invoice created by],' '[Invoice Added By],



T5.DocTotal,T5.PaidToDate as 'Applied Amt',--T15.DocEntry[Draftkey],
T7.DocNum as 'Credit Note No.', T7.DocDate as 'Credit Note date'

/*T21.[U_SDate][Trip Start Date], T21.[U_STime][Trip Start Time], ' '[Dispatched Time], T21.[DocNum][Trip Number], T21.[U_VCode][Vehicle Code], T21.[U_DName][Driver Name], T21.[U_Trns][Transporter], T21.[U_EWayBNo][Courier Way Bill No.],
T21.[U_DelDate][Delivered Date],T21.[U_LTime][Delivered Time],T20.[U_Status][Status]*/


FROM RDR1 T0 INNER JOIN ORDR T1 ON T0.DocEntry = T1.DocEntry
left outer join DLN1 T2 on T2.BaseEntry = T0.DocEntry --and T2.BaseLine = T0.Linenum
left outer join ODLN T3 on T2.DocEntry = T3.DocEntry
left Outer join INV1 T4 on T4.BaseEntry = T3.DocEntry and /*T4.BaseLine = T2.Linenum and*/ T4.BaseType = 15
OR (T4.Basetype=17 and T4.BaseEntry=T0.DocEntry /*and T4.BaseLine=T0.LineNum*/)
LEFT outer join RDN1 T11 on T11.BaseEntry = T2.DocEntry --and T11.BaseLine = T2.LineNum
LEFT outer join ORDN T12 on T11.DocEntry = T12.DocEntry
--left join OWDD T15 on t1.docentry = t15.docentry 
--left outer join WDD1 T16 on T16.[WddCode] = T15.[WddCode] 
--INNER JOIN OUSR T17 ON T16.UserID = T17.USERID 
LEFT join OUSR T30 ON t1.UserSign = T30.USERID
LEFT join OUSR T32 ON t3.UserSign = T32.USERID

left outer join OINV T5 on T5.DocEntry = T4.DocEntry
left Outer join RIN1 T6 on T6.BaseEntry = T5.DocEntry --and T6.BaseLine = T4.Linenum
left outer join ORIN T7 on T6.DocEntry = T7.DocEntry
left outer join OITM T8 on T0.ItemCode = T8.ItemCode
left outer join OSLP T9 on T9.SlpCode = T1.SlpCode
--left outer join OHEM T10 on T10.empID = T1.OwnerCode
---INNER JOIN [dbo].[@AK_TDRC_C0] T20 ON T5.DocEntry= T20.[U_InvEntry]
---Inner join [dbo].[@AK_TRPM_HD]  T21 ON T21.[U_DREntry]=T20.[DocEntry] 
---LEFT join OUSR T33 ON t5.UserSign = T33.USERID 
INNER JOIN NNM1 N1 ON T1.Series = N1.Series


WHERE 
T1.[DocDate] >=@FromDate and T1.[DocDate] <=@ToDate AND N1.Series NOT IN (191,215,204) AND T1.[U_DocType]='SO' --AND T0.[TargetType]=15 and  T2.[TargetType]=13 --and T4.Docentry is not null ---and /*and T16.Status='Y'*/  T15.ObjType=17 AND T16.[UpdateTime] IS NOT NULL
Group by T1.DocEntry, T1.DocNum,T1.DocDate,T1.DocStatus,T1.CardName, T9.SlpName,/*T10.firstName,*/T8.FrgnName, T3.DocNum --T15.[CreateTime],T10.firstName,T16.[UpdateDate]
,T5.DocNum/*,T15.DocEntry*/ ,T1.WddStatus, T5.DocDate, T5.DocStatus , T5.DocTotal,T5.PaidToDate ,T1.CardCode,T1.[NumAtCard],T1.[DocTotal],T5.[DocTotal],--T15.[CreateDate],T16.[UpdateTime],T17.[U_NAME],
T7.DocNum , T7.DocDate ,T12.DocNum,T12.DocDate,T1.[CreateDate],T1."CreateTS",T3."CreateTS",T3.[CreateDate],T5."CreateTS",T5.[CreateDate],T4.Docentry,/*T21.[U_SDate], T21.[U_STime], T21.[U_DelDate], 
T21.[DocNum], T21.[U_VCode], T21.[U_DName], T21.[U_Trns], T21.[U_EWayBNo], T21.[U_LTime],T20.[U_Status],*//*T15.[Status],*/T30.[U_NAME],T32.[U_NAME],/*T33.[U_NAME],T1.[U_R_Date],*/ T1.[U_TR_Received],N1.[SeriesName],T3.[U_ReqName], T3.[U_DocAppName])A


---where A.[Invoice No] IS NOT NULL
END

--exec PTL_Order_Tracker_Report '20220101', '20220131'

To run the project :
git clone project
then run python manage.py runserver in a python virtual environment

instalations required:
1. Django
2. python
3. anaconda
4. git cmd
5. channels
6. pyodbc
7.     count_query10 = "exec PTL_Order_Tracker_Report '20231213', '20231213'"
    with connection.cursor() as cursor:
        cursor.execute(count_query10)
        orders = cursor.fetchall()

        columns = ['DocNum', 'SeriesName', 'SO Posting Date', 'CardCode', 'Customer Name', 'NumAtCard', 'Time Order Received',
               'Sales Order Value', 'Invoice Value', '% Supplied', 'Created By', 'Sales Order Added Date',
               'Sales Order Added Time', 'Sales Order Added By', 'Delivery Doc Num', 'Delivery Added Date',
               'Delivery Added Time', 'Picked By', 'Confirmed By', 'Invoice No', 'Invoice Date', 'Invoice Creation Date',
               'Invoice Creation Time']


    count_query11 = "SELECT COUNT(DISTINCT DocNum) AS TotalInvoices FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
    with connection.cursor() as cursor:
        cursor.execute(count_query11)
        total_invoices = cursor.fetchone()[0]

    #count_query = "SELECT COUNT(DISTINCT DocNum) AS TotalInvoices FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
    #with connection.cursor() as cursor:
        #cursor.execute(count_query)
       # total_invoices = cursor.fetchone()[0]

    #count_query1 = "SELECT COUNT(DISTINCT Customer Name) AS Totalcustomers FROM (exec PTL_Order_Tracker_Report '20231213', '20231213') AS CombinedDocs"
   # with connection.cursor() as cursor:
       # cursor.execute(count_query1)
       # total_customers = cursor.fetchone()[0] 'total_invoices': total_invoices, 'total_customers': total_customers,


   count_query11 = """
    DECLARE @TotalInvoices INT;
    EXEC dbo.PTL_Order_Tracker_Report '20231213', '20231213';
    SELECT @TotalInvoices AS TotalInvoices;
"""

with connection.cursor() as cursor:
    cursor.execute(count_query11)
    total_invoices = cursor.fetchone()[0]


count_query11 = "DECLARE @TotalInvoices INT; EXEC @TotalInvoices = PTL_Order_Tracker_Report '20231213', '20231213'; SELECT @TotalInvoices AS TotalInvoices;"

with connection.cursor() as cursor:
    cursor.execute(count_query11)
    total_invoices = cursor.fetchone()[0]

# Now you can use total_invoices in your code


count_query11 = "DECLARE @TotalInvoices INT; EXEC @TotalInvoices = PTL_Order_Tracker_Report '20231213', '20231213'; SELECT @TotalInvoices AS TotalInvoices;"







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
            'customer_name': row[4],       # Assuming the 5th column is 'Customer Name'
            'invoice_number': row[14],     # Assuming the 15th column is 'Invoice No'
            'posting_date': row[3],        # Assuming the 4th column is 'SO Posting Date'
            'quantity': row[12],           # Assuming the 13th column is 'Quantity'
        }
        for row in result_set
    ]

    cursor.execute("""
            SELECT
                COUNT(DISTINCT DocNum) AS DocNumCount,
                SUM(Quantity) AS QuantityCount
            FROM (
                exec PTL_Order_Tracker_Report '20231213', '20231213'
            ) AS SubqueryResult
        """)

    counts = cursor.fetchone()
    docnum_count = counts[0]
    quantity_count = counts[1]

    # Calculate counts
    # docnum_count = len(set(row[1] for row in result_set))  # Assuming the 2nd column is 'DocNum' 'docnum_count': docnum_count, 'quantity_count': quantity_count
    # quantity_count = sum(int(row[12]) for row in result_set)    # Assuming the 13th column is 'Quantity'
    # Assuming the 13th column is 'Quantity'

    return render(request, 'analysis/count.html', {'data_to_display': data_to_display, 'quantity_count': quantity_count, 'docnum_count': docnum_count})



<!-- your_template.html -->
<html>
<head>
    <title>Your Template</title>
</head>
<body>
    <h1>Data to Display</h1>
    <table>
        <thead>
            <tr>
                <th>Customer Name</th>
                <th>Invoice Number</th>
                <th>Posting Date</th>
                <th>Quantity</th>
            </tr>
        </thead>
        <tbody>
            {% for data in data_to_display %}
                <tr>
                    <td>{{ data.customer_name }}</td>
                    <td>{{ data.invoice_number }}</td>
                    <td>{{ data.posting_date }}</td>
                    <td>{{ data.quantity }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

    <h2>Counts</h2>
    <p>DocNum Count: {{ docnum_count }}</p>
    <p>Quantity Count: {{ quantity_count }}</p>
</body>
</html>




   
