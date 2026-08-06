import streamlit as st
import pickle
import requests

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------------
# 2. Custom CSS Injection (Poppins Font & Glowing Red Button)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* Global Font & Background */
    .stApp {
        font-family: 'Poppins', sans-serif !important;
        background-color: #0d0e15;
        color: #ffffff;
    }
    
    /* Layout Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }
    
    /* Glowing Red Button Fix (Overrides Streamlit White Button) */
    .stButton > button {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0.65rem 1.8rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(225, 29, 72, 0.4) !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(225, 29, 72, 0.6) !important;
        color: #ffffff !important;
    }
    
    /* Selectbox Dropdown Styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #151722 !important;
        border: 1px solid #232538 !important;
        color: white !important;
        border-radius: 12px !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Hero Banner Container */
    .hero-banner {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        min-height: 380px;
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: flex-end;
        border: 1px solid #232538;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, #0d0e15 12%, rgba(13,14,21,0.65) 60%, transparent 100%),
                    linear-gradient(90deg, #0d0e15 25%, transparent 85%);
    }
    .hero-details {
        position: relative;
        z-index: 2;
        padding: 32px;
        max-width: 700px;
    }
    
    /* Poster Cards */
    .poster-card {
        background: #151722;
        border: 1px solid #232538;
        border-radius: 16px;
        padding: 10px;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .poster-card:hover {
        transform: translateY(-6px);
        border-color: #e11d48;
    }
    .poster-img {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
        border-radius: 12px;
    }
    .poster-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 14px;
        margin-top: 8px;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Badges & Metadata Tags */
    .match-badge {
        background-color: #e11d48;
        color: white;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .meta-tag {
        color: #94a3b8;
        font-size: 13px;
        margin-right: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Helper Functions & OMDb Data Fetching
# ---------------------------------------------------------
def fetch_movie_details_omdb(title):
    """Fetch movie metadata from OMDb API using movie title."""
    api_key = "92fdf4d1"  # <-- Paste your OMDb API key here
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("Response") == "True":
            poster = data.get("Poster") if data.get("Poster") != "N/A" else "https://via.placeholder.com/500x750"
            rating = data.get("imdbRating", "N/A")
            year = data.get("Year", "N/A")
            runtime = data.get("Runtime", "N/A")
            genres = data.get("Genre", "N/A")
            overview = data.get("Plot", "No plot summary available.")
            
            return {
                'poster': poster,
                'rating': rating,
                'year': year,
                'runtime': runtime,
                'genres': genres,
                'overview': overview
            }
        else:
            return None
    except Exception:
        return None

# ---------------------------------------------------------
# 4. Load Pickles
# ---------------------------------------------------------
try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: Ensure 'movies.pkl' and 'similarity.pkl' exist in your project folder.")
    st.stop()

# ---------------------------------------------------------
# 5. User Interface
# ---------------------------------------------------------
st.title("🎬 CineMatch")
st.caption("Personalized AI Recommendations")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend Movies"):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    
    selected_details = fetch_movie_details_omdb(selected_movie_name)
    
    # Hero Banner Display
    if selected_details:
        st.markdown(f"""
        <div class="hero-banner" style="background-image: url('{selected_details['poster']}');">
            <div class="hero-overlay"></div>
            <div class="hero-details">
                <span class="match-badge">⭐ {selected_details['rating']} IMDb Rating</span>
                <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.3rem; font-weight: 700; margin: 4px 0 10px 0; color: #fff;">{selected_movie_name}</h1>
                <p style="margin-bottom: 12px;">
                    <span class="meta-tag">📅 {selected_details['year']}</span>
                    <span class="meta-tag">⏱️ {selected_details['runtime']}</span>
                    <span class="meta-tag">🏷️ {selected_details['genres']}</span>
                </p>
                <p style="color: #cbd5e1; font-size: 13.5px; line-height: 1.5;">{selected_details['overview']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Recommendation Rail Section
    st.markdown("### Movies you'll love")
    
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        rec_index = distances[idx + 1][0]
        rec_title = movies.iloc[rec_index].title
        
        details = fetch_movie_details_omdb(rec_title)
        poster_url = details['poster'] if details else "https://via.placeholder.com/500x750"
        
        with col:
            st.markdown(f"""
            <div class="poster-card">
                <img src="{poster_url}" class="poster-img" alt="{rec_title}">
                <div class="poster-title">{rec_title}</div>
            </div>
            """, unsafe_allow_html=True)
