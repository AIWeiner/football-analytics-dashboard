import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Football Analysis App", layout="wide")

st.sidebar.title("⚽ Football Dashboard")
st.sidebar.markdown("Filter and analyze player performance")

# Upload file
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # ===== FILTER SECTION =====
    st.sidebar.header("Filters")
    team = st.sidebar.selectbox("Select Team", df["team"].unique())

    filtered_df = df[df["team"] == team].copy()
    filtered_df = filtered_df.sort_values(by="goals", ascending=False)

    # ===== MAIN LAYOUT =====
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

    with col2:
        st.subheader("Key Metrics")
        st.metric("Players", len(filtered_df))
        st.metric("Avg Goals", round(filtered_df["goals"].mean(), 2))
        st.metric("Avg Assists", round(filtered_df["assists"].mean(), 2))

    # ===== PLAYER SELECTION =====
    st.subheader("Player Analysis")
    player = st.selectbox("Select Player", filtered_df["player"])
    player_data = filtered_df[filtered_df["player"] == player]
    st.write(player_data)

    # ===== VISUALIZATION =====
    st.subheader("Goals Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["goals"], bins=5)
    ax.set_xlabel("Goals")
    ax.set_ylabel("Number of Players")
    st.pyplot(fig)

    # ===== ADVANCED METRICS =====
    st.subheader("Advanced Metrics")

    filtered_df["goals_per_90"] = filtered_df.apply(
        lambda row: row["goals"] / (row["minutes"] / 90) if row["minutes"] > 0 else 0,
        axis=1
    )

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
