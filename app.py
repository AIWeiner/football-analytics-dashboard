import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.info("⚠️ If the app takes a few seconds to load, it's waking up from sleep.")
st.set_page_config(page_title="Football Analysis App", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: white;
        }
        .stMetric {
            background-color: #1c1f26;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)


st.title("⚽ Football Performance Dashboard")
st.subheader("Team Analysis")

# Upload file
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:

    df = pd.read_csv(file)

    st.sidebar.title("⚽ Football Dashboard")
    st.sidebar.markdown("Filter and analyze player performance")

 # ===== FILTER SECTION =====
    st.sidebar.header("Filters")

    team = st.sidebar.selectbox("Select Team", df["team"].unique())

    filtered_df = df[df["team"] == team]
    filtered_df = filtered_df.sort_values(by="goals", ascending=False)
    tab1, tab2 = st.tabs(["📊 Overview", "👤 Player Analysis"])

    # ===== MAIN LAYOUT =====
    
   with tab1:
    col1, col2, col3 = st.columns(3)

    col1.metric("Players", len(filtered_df))
    col2.metric("Avg Goals", round(filtered_df["goals"].mean(), 2))
    col3.metric("Avg Assists", round(filtered_df["assists"].mean(), 2))

    st.subheader("Top Players")

    top_players = filtered_df.sort_values(by="goals", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(top_players["player"], top_players["goals"])
    st.pyplot(fig)
       
    # ===== PLAYER SELECTION =====
with tab2:
    player = st.selectbox("Select Player", filtered_df["player"])

    player_data = filtered_df[filtered_df["player"] == player]

    st.write(player_data)

    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df["goals"], filtered_df["assists"])

    for i, txt in enumerate(filtered_df["player"]):
        ax2.annotate(txt, (filtered_df["goals"].iloc[i], filtered_df["assists"].iloc[i]))

    ax2.set_xlabel("Goals")
    ax2.set_ylabel("Assists")

    st.pyplot(fig2)

    # ===== VISUALIZATION =====
    st.subheader("Goals Distribution")

    fig, ax = plt.subplots()
    ax.hist(filtered_df["goals"], bins=5)
    ax.set_xlabel("Goals")
    ax.set_ylabel("Number of Players")

    st.pyplot(fig)

    # ===== ADVANCED METRICS =====
    st.subheader("Advanced Metrics")

    # Avoid division by zero
    filtered_df = filtered_df.copy()
    filtered_df["goals_per_90"] = filtered_df["goals"] / (filtered_df["minutes"] / 90)

    st.dataframe(filtered_df)

    # ===== SCATTER PLOT =====
    st.subheader("Goals vs Assists")

    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df["goals"], filtered_df["assists"])

    for i, txt in enumerate(filtered_df["player"]):
        ax2.annotate(txt, (filtered_df["goals"].iloc[i], filtered_df["assists"].iloc[i]))

    ax2.set_xlabel("Goals")
    ax2.set_ylabel("Assists")

    st.pyplot(fig2)

    # ===== TOP PLAYERS =====
    st.subheader("Top 10 Goal Scorers")

    top_players = filtered_df.sort_values(by="goals", ascending=False).head(10)

    fig3, ax3 = plt.subplots()
    ax3.barh(top_players["player"], top_players["goals"])
    ax3.set_xlabel("Goals")

    st.pyplot(fig3)



    
