import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='scraper',
    passwd='getmein123',
    db='craigslist')
cursor = mydb.cursor()

csv_data = csv.reader(file('craigslist.csv'))
header = True
for row in csv_data:
    if not header:
        cursor.execute('INSERT INTO cars(title, link) VALUES("%s", "%s")',
            row
        )
    header = False

mydb.commit()
cursor.close()
print "Done."
