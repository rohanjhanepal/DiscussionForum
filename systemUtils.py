import csv , sqlite3 



DB_FNAME = 'db.sqlite3'

conn = sqlite3.connect(DB_FNAME)
cur = conn.cursor()


posts = cur.execute("SELECT * FROM forum_post")

for i in posts:
    print(i)
    category = conn.cursor().execute("SELECT * FROM forum_category where id = {}".format(i[6]))
    subcategory = conn.cursor().execute("SELECT * FROM forum_subcategory where id = {}".format(i[7]))

    print(category.fetchone())
    print(subcategory.fetchone()) 

