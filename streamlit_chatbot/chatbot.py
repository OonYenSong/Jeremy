import streamlit as st

st.set_page_config(page_title="Sunway Club Info", page_icon="🏫", layout="wide")

# ---------------- CLUB DATA ----------------
clubs = {
    "Football Club": {
        "type": "Sport",
        "description": "Futsal/Football club focusing on teamwork, stamina, and competitive matches.",
        "activities": "Weekly training, friendly matches, tournaments"
    },
    "Basketball Club": {
        "type": "Sport",
        "description": "Fast-paced sport focused on teamwork and scoring skills.",
        "activities": "Training sessions, inter-college matches"
    },
    "Badminton Club": {
        "type": "Sport",
        "description": "Racket sport played in singles or doubles.",
        "activities": "Training, friendly games, competitions"
    },
    "Volleyball Club": {
        "type": "Sport",
        "description": "Team sport focusing on coordination and reflexes.",
        "activities": "Practice sessions and campus tournaments"
    },
    "Esports Club": {
        "type": "Sport",
        "description": "Competitive gaming across multiple titles.",
        "activities": "Gaming tournaments and scrims"
    },
    "Programming Club": {
        "type": "Academic",
        "description": "Learn coding, app development, and problem solving.",
        "activities": "Coding workshops, hackathons, projects"
    },
    "Business Club": {
        "type": "Academic",
        "description": "Learn entrepreneurship, marketing, and business strategy.",
        "activities": "Business talks, case competitions"
    },
    "Accounting & Finance Society": {
        "type": "Academic",
        "description": "Focus on accounting principles and financial knowledge.",
        "activities": "Workshops, career talks, competitions"
    },
    "Mathematics Club": {
        "type": "Academic",
        "description": "Explore advanced math concepts and problem solving.",
        "activities": "Math challenges, study sessions"
    },
    "Science Club": {
        "type": "Academic",
        "description": "Covers physics, chemistry, and general science activities.",
        "activities": "Experiments, science fairs, seminars"
    }
}

# ---------------- TITLE ----------------
st.title("🏫 Sunway Club Information Portal")
st.markdown("Browse all clubs and learn more about their activities and focus areas.")

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("Filter Clubs")

filter_type = st.sidebar.selectbox("Choose Category", ["All", "Sport", "Academic"])

# ---------------- CLUB LIST ----------------
st.header("📌 Clubs")

for club_name, info in clubs.items():

    if filter_type == "All" or info["type"] == filter_type:

        with st.expander(club_name):
            st.write("**Type:**", info["type"])
            st.write("**Description:**", info["description"])
            st.write("**Activities:**", info["activities"])