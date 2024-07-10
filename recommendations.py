from fastapi import FastAPI
from mangum import Mangum
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import psycopg2
import pandas as pd

app = FastAPI()
handler = Mangum(app)

conn = psycopg2.connect(database="<DB NAME>",
                        user="<USERNAME>",
                        host='<HOST NAME>',
                        password="<PASSWORD>",
                        port=5432)

cur = conn.cursor()


@app.get("/recommendations")
async def GetRecommendations():
    cur.execute(""" SELECT id,title,genre FROM books; """, )
    genre_data = cur.fetchall()

    cur.execute(""" SELECT book_id,rating FROM reviews; """)
    ratings_data = cur.fetchall()

    # create dataframes
    genre_df = pd.DataFrame(genre_data, columns=['id', 'title', 'genre'])
    ratings_df = pd.DataFrame(ratings_data, columns=['id', 'ratings'])

    # merge frames
    merge_df = pd.merge(genre_df, ratings_df, on='id')
    final_df = merge_df.groupby(['title', 'genre'], as_index=False).mean()

    # encoding
    genre_l1 = preprocessing.LabelEncoder()
    final_df['genre'] = genre_l1.fit_transform(final_df['genre'])

    title_l1 = preprocessing.LabelEncoder()
    final_df['title'] = title_l1.fit_transform(final_df['title'])

    x_train = final_df[['genre', 'ratings']]
    y_train = final_df['title']

    # model
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(x_train, y_train)

    # test set with 4.5 avg rating for all genres
    test_genre = list(x_train['genre'].unique())
    test_ratings = [4.5 for _ in range(len(test_genre))]

    x_test = pd.DataFrame(data={'genre': test_genre, 'ratings': test_ratings})
    recommendations = clf.predict(x_test)

    # close connections
    cur.close()
    conn.close()

    recommendations = title_l1.inverse_transform(recommendations)
    return {"message": "success", "avg rating": 4.5, "recommendations": list(set(recommendations))}
