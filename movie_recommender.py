import pandas as pd
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load dataset
movies = pd.read_csv("tmdb_5000_movies.csv")


# Select required columns
movies = movies[['title', 'overview', 'genres', 'keywords']]


# Convert genres and keywords from text format


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return " ".join(L)


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


# Remove missing values
movies.dropna(inplace=True)


# Combine features


movies['tags'] = (
    movies['overview']
    + " "
    + movies['genres']
    + " "
    + movies['keywords']
)


# Convert text into vectors

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)


vectors = cv.fit_transform(
    movies['tags']
)


# Calculate similarity

similarity = cosine_similarity(vectors)


# Save files

pickle.dump(
    movies,
    open("movies.pkl", "wb")
)


pickle.dump(
    similarity,
    open("similarity.pkl", "wb")
)


print("Recommendation model created successfully!")