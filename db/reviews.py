import psycopg2

conn = psycopg2.connect(database="<DB NAME>",
                        user="<USERNAME>",
                        host='<HOST NAME>',
                        password="<PASSWORD>",
                        port=5432)

cur = conn.cursor()

# create books reviews
cur.execute("""CREATE TABLE IF NOT EXISTS reviews(
            id INT PRIMARY KEY,
            book_id INT,
            user_id VARCHAR(20),
            review_text VARCHAR(100),
            rating INT,
            FOREIGN KEY(book_id) references books(id));""")


# insert value in reviews
cur.execute("""INSERT INTO reviews(id, book_id, user_id, review_text, rating)
VALUES (%(review_id)s,%(book_id)s,%(user_id)s,%(review_text)s,%(rating)s); """,
            {"review_id": 2123131, "book_id": 4, "user_id": "hishamp3", "review_text": "good old fairytale",
             "rating": 4})

conn.commit()

# get all reviews
cur.execute(""" SELECT * FROM reviews; """)
raw_data = cur.fetchall()

print(raw_data)

# close connections
cur.close()
conn.close()
