import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    file_path = os.path.join(BASE_DIR, 'dataset', 'google_hotel_data_clean_v2.csv')

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")

    df = pd.read_csv(file_path)

    df.rename(columns=lambda x: x.strip().lower(), inplace=True)

    df.rename(columns={'hotel_name': 'resort_id', 'hotel_rating': 'rating', 'city': 'location'}, inplace=True)

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)

    feature_columns = [col for col in df.columns if "feature" in col]
    df['amenities'] = df[feature_columns].fillna('').agg(' '.join, axis=1)

    return df


# ✅ Content-Based Filtering Recommendation
def content_based_recommend(resort_name, num_recommendations=5):
    df = load_data()

    if resort_name not in df['resort_id'].values:
        return f"Error: Resort '{resort_name}' not found!"

    vectorizer = TfidfVectorizer(stop_words='english')
    amenities_matrix = vectorizer.fit_transform(df['amenities'])

    cosine_sim = cosine_similarity(amenities_matrix, amenities_matrix)

    idx = df[df['resort_id'] == resort_name].index
    if len(idx) == 0:
        return "Error: Resort not found in dataset"

    idx = idx[0]  # Get first match
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

    resort_indices = [i[0] for i in sim_scores]
    return df.iloc[resort_indices][['resort_id', 'location', 'rating', 'amenities']]


def collaborative_recommend(resort_name, num_recommendations=5):
    df = load_data()

    if resort_name not in df['resort_id'].values:
        return f"Error: Resort '{resort_name}' not found!"

    df['user_id'] = range(len(df))  

    user_resort_matrix = df.pivot(index='user_id', columns='resort_id', values='rating').fillna(0)

    if resort_name not in user_resort_matrix.columns:
        return "Error: No ratings found for this resort!"

    resort_sparse = csr_matrix(user_resort_matrix.values)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(resort_sparse)

    resort_index = user_resort_matrix.columns.get_loc(resort_name)
    query_vector = user_resort_matrix.iloc[:, resort_index].values.reshape(1, -1)

    num_features = user_resort_matrix.shape[1]
    if query_vector.shape[1] != num_features:
        return f"Error: Feature dimension mismatch! Expected {num_features}, but input has {query_vector.shape[1]}."

    distances, indices = model_knn.kneighbors(query_vector, n_neighbors=min(num_features, num_recommendations+1))

    recommended_resorts = [user_resort_matrix.columns[i] for i in indices.flatten()[1:]]

    return df[df['resort_id'].isin(recommended_resorts)][['resort_id', 'location', 'rating']]
