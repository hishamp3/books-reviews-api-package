from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
import psycopg2


class Book:
    def __init__(self, book_id, title, author, genre, year_published, summary):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year_published = year_published
        self.summary = summary


class Review:
    def __init__(self, review_id, user_id, review_text, rating):
        self.review_id = review_id
        self.user_id = user_id
        self.review_text = review_text
        self.rating = rating


class Item(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    year_published: str
    summary: str


class ReviewItem(BaseModel):
    review_id: int
    book_id: int
    user_id: str
    review_text: str
    rating: int


app = FastAPI()
handler = Mangum(app)

conn = psycopg2.connect(database="<DB NAME>",
                        user="<USERNAME>",
                        host='<HOST NAME>',
                        password="<PASSWORD>",
                        port=5432)

cur = conn.cursor()


@app.get("/books")
async def GetAllBooks():
    # SELECT query
    cur.execute(""" SELECT * FROM books; """)
    raw_data = cur.fetchall()

    if raw_data:
        myBooks = [Book(data[0], data[1], data[2], data[3], data[4], data[5]).__dict__ for data in raw_data]
        return {
            "message": "success", "books": myBooks
        }

    else:
        return {
            "message": "No books available"
        }


@app.get("/books/{book_id}")
async def GetBook(book_id: int):
    # SELECT query
    cur.execute(""" SELECT * FROM books WHERE id=%(book_id)s; """, {"book_id": book_id})
    raw_data = cur.fetchall()

    if raw_data:
        data = raw_data[0]
        return {
            "message": "success", "bookId": book_id, "title": data[1], "author": data[2], "genre": data[3],
            "year_published": data[4], "summary": data[5]
        }

    else:
        return {
            "message": "Book ID " + str(book_id) + " not available"
        }


@app.post("/books")
async def AddBook(book_obj: Item):
    # INSERT query
    cur.execute("""INSERT INTO books(id, title, author, genre, year_published, summary)
    VALUES (%(book_id)s,%(title)s,%(author)s,%(genre)s,%(year_published)s,%(summary)s); """,
                {"book_id": book_obj.book_id, "title": book_obj.title, "author": book_obj.author,
                 "genre": book_obj.genre, "year_published": book_obj.year_published,
                 "summary": book_obj.summary})

    conn.commit()
    if cur:
        return {
            "message": "success", "status": 200
        }

    else:
        return {
            "message": "failed"
        }


@app.put("/books/{book_id}")
async def UpdateBook(book_id: int, book_obj: Item):
    # UPDATE query
    cur.execute("""UPDATE books SET title=%(title)s, author=%(author)s, 
    genre=%(genre)s, year_published=%(year_published)s, summary=%(summary)s
        WHERE id=%(book_id)s; """,
                {"book_id": book_id, "title": book_obj.title, "author": book_obj.author,
                 "genre": book_obj.genre, "year_published": book_obj.year_published,
                 "summary": book_obj.summary})

    conn.commit()
    if cur:
        return {
            "message": "success", "status": 200
        }

    else:
        return {
            "message": "failed"
        }


@app.delete("/books/{book_id}")
async def DeleteBook(book_id: int):
    # DELETE query
    cur.execute("""DELETE FROM books WHERE id=%(book_id)s; """,
                {"book_id": book_id})

    conn.commit()
    if cur:
        return {
            "message": "success", "status": 200
        }

    else:
        return {
            "message": "failed"
        }


@app.get("/books/{book_id}/reviews")
async def GetReviews(book_id: int):
    # SELECT query
    cur.execute(""" SELECT * FROM reviews WHERE book_id=%(book_id)s; """, {"book_id": book_id})
    raw_data = cur.fetchall()
    conn.commit()

    if raw_data:
        myReviews = [Review(data[0], data[2], data[3], data[4]).__dict__ for data in raw_data]
        return {
            "message": "success", "book_id": book_id, "reviews": myReviews
        }

    else:
        return {
            "message": "No books available"
        }


@app.post("/books/{book_id}/reviews")
async def AddReview(review_obj: ReviewItem):
    # INSERT query
    cur.execute("""INSERT INTO reviews(id, book_id, user_id, review_text, rating)
    VALUES (%(review_id)s,%(book_id)s,%(user_id)s,%(review_text)s,%(rating)s); """,
                {"review_id": review_obj.review_id, "book_id": review_obj.book_id, "user_id": review_obj.user_id,
                 "review_text": review_obj.review_text,
                 "rating": review_obj.rating})

    conn.commit()
    if cur:
        return {
            "message": "success", "status": 200
        }

    else:
        return {
            "message": "failed"
        }


@app.get("/books/{book_id}/summary")
async def GetSummaryRating(book_id: int):
    # summary
    cur.execute(""" SELECT summary FROM books WHERE id=%(book_id)s; """, {"book_id": book_id})
    summary_data = cur.fetchall()
    conn.commit()

    # ratings
    cur.execute(""" SELECT * FROM reviews WHERE book_id=%(book_id)s; """,
                {"book_id": book_id})
    ratings_data = cur.fetchall()
    conn.commit()

    if summary_data or ratings_data:
        ratings = [data[4] for data in ratings_data if isinstance(data[4], int)]
        return {
            "message": "success", "summary": summary_data, "average_ratings": sum(ratings) / len(ratings)
        }

    else:
        return {
            "message": "No data available"
        }
