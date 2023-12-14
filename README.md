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

   
