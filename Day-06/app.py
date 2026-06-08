import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Coding Activity Analyzer",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Coding Activity Analyzer Dashboard")
st.write("Analyze 6 months of coding activity using Python, Pandas, Streamlit and Plotly.")

df = pd.read_csv("coding_activity.csv")
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
df = df.sort_values("date")

df["month"] = df["date"].dt.to_period("M").astype(str)
df["weekday"] = df["date"].dt.day_name()

st.sidebar.header("Filters")

platform_filter = st.sidebar.multiselect(
    "Select Platform",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)

topic_filter = st.sidebar.multiselect(
    "Select Topic",
    options=df["topic"].unique(),
    default=df["topic"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["topic"].isin(topic_filter)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

total_problems = filtered_df["problems_solved"].sum()
total_hours = round(filtered_df["time_spent_minutes"].sum() / 60, 2)
avg_problems = round(filtered_df["problems_solved"].mean(), 2)
total_contests = (filtered_df["contest_given"] == "Yes").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Problems", total_problems)
col2.metric("Coding Hours", total_hours)
col3.metric("Avg Problems/Day", avg_problems)
col4.metric("Contests Given", total_contests)

st.divider()

col5, col6 = st.columns(2)

with col5:
    platform_data = filtered_df.groupby("platform")["problems_solved"].sum().reset_index()
    fig = px.bar(
        platform_data,
        x="platform",
        y="problems_solved",
        title="Platform-wise Problems Solved"
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    difficulty_data = pd.DataFrame({
        "difficulty": ["Easy", "Medium", "Hard"],
        "count": [
            filtered_df["easy"].sum(),
            filtered_df["medium"].sum(),
            filtered_df["hard"].sum()
        ]
    })

    fig = px.pie(
        difficulty_data,
        names="difficulty",
        values="count",
        title="Difficulty Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    monthly_data = filtered_df.groupby("month")["problems_solved"].sum().reset_index()
    fig = px.bar(
        monthly_data,
        x="month",
        y="problems_solved",
        title="Monthly Growth Report"
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:
    topic_data = filtered_df.groupby("topic")["problems_solved"].sum().reset_index()
    fig = px.bar(
        topic_data,
        x="topic",
        y="problems_solved",
        title="Topic Strength Analysis"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Daily Problems Solved Trend")

fig = px.line(
    filtered_df,
    x="date",
    y="problems_solved",
    markers=True,
    title="Daily Coding Progress"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("⏱️ Time Spent vs Problems Solved")

fig = px.scatter(
    filtered_df,
    x="time_spent_minutes",
    y="problems_solved",
    color="platform",
    size="problems_solved",
    title="Time vs Productivity"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Contest Rating Growth")

contest_df = filtered_df[filtered_df["contest_given"] == "Yes"]

if not contest_df.empty:
    fig = px.line(
        contest_df,
        x="date",
        y="rating",
        markers=True,
        title="Contest Rating Growth"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No contest data available for selected filters.")

st.subheader("🔥 Smart Insights")

if not filtered_df.empty:
    strongest_topic = filtered_df.groupby("topic")["problems_solved"].sum().idxmax()
    top_platform = filtered_df.groupby("platform")["problems_solved"].sum().idxmax()
    best_day = filtered_df.loc[filtered_df["problems_solved"].idxmax()]
    correlation = round(
        filtered_df["time_spent_minutes"].corr(filtered_df["problems_solved"]),
        2
    )

    burnout_days = filtered_df[
        (filtered_df["time_spent_minutes"] >= 120) &
        (filtered_df["problems_solved"] <= 2)
    ]

    st.success(f"Strongest Topic: {strongest_topic}")
    st.info(f"Most Used Platform: {top_platform}")
    st.warning(f"Best Coding Day: {best_day['date'].date()} with {best_day['problems_solved']} problems")
    st.write(f"Time vs Problems Correlation: **{correlation}**")
    st.write(f"Potential Burnout Days Found: **{len(burnout_days)}**")

st.subheader("📄 Filtered Dataset")
st.dataframe(filtered_df)