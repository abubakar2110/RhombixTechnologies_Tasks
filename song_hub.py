import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("D:\\data1.csv")  

if 'playlist' not in st.session_state:
    st.session_state.playlist = []

data = load_data()

if not {'song_title', 'song_id', 'URL'}.issubset(data.columns):
    st.error("Dataset is missing required columns: 'song_title', 'song_id', 'URL'")
    st.stop()

st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stHeader {
        font-size: 26px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 15px;
    }
    .stSongList {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stPlaylist {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 My Music Platform �")

search_query = st.text_input("🔍 Search for a song by title:")

if search_query:
    filtered_data = data[data['song_title'].str.contains(search_query, case=False, na=False)]
else:
    filtered_data = data
    
st.markdown('<div class="stHeader">🎶 Songs List</div>', unsafe_allow_html=True)

with st.container():
    for index, row in filtered_data.iterrows():
        unique_key = f"song_{index}_{row['song_id']}"
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🎵 {row['song_title']}")
        with col2:
            if st.button("▶ Play", key=unique_key):
                # Add the song to the playlist
                if len(st.session_state.playlist) >= 10:
                    st.session_state.playlist.pop(0)
                st.session_state.playlist.append(row['song_title'])

                st.success(f"🎧 Now Playing: **{row['song_title']}**")
                st.markdown(f"[Play on Spotify]({row['URL']})", unsafe_allow_html=True)

# Display the last 10 played songs in the sidebar
with st.sidebar:
    st.markdown('<div class="stHeader">📜 Last 10 Played Songs</div>', unsafe_allow_html=True)
    if st.session_state.playlist:
        st.markdown('<div class="stPlaylist">', unsafe_allow_html=True)
        for song in reversed(st.session_state.playlist):
            st.write(f"🎶 {song}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No songs played yet. Start playing some music! 🎼")