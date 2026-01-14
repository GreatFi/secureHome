from django.db import connection
import time

connection.cursor().execute("DISCARD ALL")

sql = """
EXPLAIN ANALYZE
SELECT * FROM "Secur_listproperties" 
WHERE lga = 'enugu-north' AND prop_choices = 'rent'
"""

start = time.time()
with connection.cursor() as cursor:
    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row[0])
        
end = time.time()
print(f"\nQuery took: {(end - start)*1000:.2f} milliseconds")