import psycopg2
import ollama


def llama3_summary(book_title):
    # prompt tuning
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': 'write a summary of the book Harry potter in 100 characters',
        },
        {
            'role': 'assistant',
            'content': "Orphan Harry Potter discovers he's a wizard, attends Hogwarts School, and battles evil Lord Voldemort to save wizarding world."
        },
        {
            'role': 'user',
            'content': 'write a summary of the book ' + book_title + ' in 100 characters'
        }
    ])
    llama3_response = response['message']['content']
    return llama3_response


conn = psycopg2.connect(database="<DB NAME>",
                        user="<USERNAME>",
                        host='<HOST NAME>',
                        password="<PASSWORD>",
                        port=5432)

cur = conn.cursor()

cur.execute(""" SELECT * FROM books; """)
raw_data = cur.fetchall()
conn.commit()

for data in raw_data:
    if data[1] is not None:
        cur.execute("""UPDATE books SET summary=%(summary)s
        WHERE title=%(title)s; """,
                    {"title": data[1], "summary": llama3_summary(data[1])})

        conn.commit()

# close connections
cur.close()
conn.close()
