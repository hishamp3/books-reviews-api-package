import psycopg2

conn = psycopg2.connect(database="<DB NAME>",
                        user="<USERNAME>",
                        host='<HOST NAME>',
                        password="<PASSWORD>",
                        port=5432)

cur = conn.cursor()

# create books table
cur.execute("""CREATE TABLE IF NOT EXISTS books(
            id INT PRIMARY KEY,
            title VARCHAR (50),
            author VARCHAR (20),
            genre VARCHAR (20),
            year_published VARCHAR(4),
            summary VARCHAR(200));""")

# add sample entry
book_id = 3
title = "Harry Potter"
author = "JK Rowling"
genre = "Adventure"
year_published = "1996"
summary = ""

cur.execute("""INSERT INTO books(id, title, author, genre, year_published, summary)
VALUES (%(book_id)s,%(title)s,%(author)s,%(genre)s,%(year_published)s,%(summary)s); """,
            {"book_id": book_id, "title": title, "author": author, "genre": genre, "year_published": year_published,
             "summary": summary})

conn.commit()

# get all books
cur.execute(""" SELECT * FROM books; """)
raw_data = cur.fetchall()
conn.commit()

print(raw_data)

# close connections
cur.close()
conn.close()
