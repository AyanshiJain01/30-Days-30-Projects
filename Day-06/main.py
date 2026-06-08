import os
import pandas as pd
import matplotlib.pyplot as plt


# 1. Charts folder create karna
if not os.path.exists("charts"):
    os.makedirs("charts")


# 2. Dataset load karna
df = pd.read_csv("coding_activity.csv")


# 3. Date ko proper datetime format me convert karna
df["date"] = pd.to_datetime(df["date"], dayfirst=True)


# 4. Data ko date ke according sort karna
df = df.sort_values("date").reset_index(drop=True)


# 5. Month aur weekday columns banana
df["month"] = df["date"].dt.to_period("M").astype(str)
df["weekday"] = df["date"].dt.day_name()


# ==============================
# BASIC ANALYSIS
# ==============================

total_days = len(df)
total_problems = df["problems_solved"].sum()
total_hours = round(df["time_spent_minutes"].sum() / 60, 2)
avg_problems = round(df["problems_solved"].mean(), 2)
avg_time = round(df["time_spent_minutes"].mean(), 2)

total_contests = (df["contest_given"] == "Yes").sum()

best_day = df.loc[df["problems_solved"].idxmax()]
worst_day = df.loc[df["problems_solved"].idxmin()]


# ==============================
# STREAK ANALYSIS
# ==============================

unique_dates = sorted(df["date"].dt.date.unique())

current_streak = 1
longest_streak = 1

for i in range(1, len(unique_dates)):
    gap = (unique_dates[i] - unique_dates[i - 1]).days

    if gap == 1:
        current_streak += 1
    else:
        longest_streak = max(longest_streak, current_streak)
        current_streak = 1

longest_streak = max(longest_streak, current_streak)


# ==============================
# WEEKDAY ANALYSIS
# ==============================

weekday_analysis = df.groupby("weekday")["problems_solved"].sum()

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_analysis = weekday_analysis.reindex(weekday_order)

most_productive_weekday = weekday_analysis.idxmax()


# ==============================
# TOPIC STRENGTH ANALYSIS
# ==============================

topic_strength = df.groupby("topic")["problems_solved"].sum().sort_values(ascending=False)

strongest_topic = topic_strength.idxmax()
weakest_topic = topic_strength.idxmin()


# ==============================
# PLATFORM PERFORMANCE
# ==============================

platform_performance = df.groupby("platform")["problems_solved"].sum().sort_values(ascending=False)

top_platform = platform_performance.idxmax()
top_platform_percentage = round(
    (platform_performance.max() / total_problems) * 100, 2
)


# ==============================
# DIFFICULTY ANALYSIS
# ==============================

easy_total = df["easy"].sum()
medium_total = df["medium"].sum()
hard_total = df["hard"].sum()

hard_percentage = round((hard_total / total_problems) * 100, 2)


# Month-wise difficulty trend
difficulty_trend = df.groupby("month")[["easy", "medium", "hard"]].sum()


# ==============================
# MONTHLY GROWTH ANALYSIS
# ==============================

monthly_growth = df.groupby("month")["problems_solved"].sum()

best_month = monthly_growth.idxmax()

growth_percentage = round(
    ((monthly_growth.iloc[-1] - monthly_growth.iloc[0]) / monthly_growth.iloc[0]) * 100,
    2
)


# ==============================
# TIME VS PROBLEMS CORRELATION
# ==============================

correlation = round(
    df["time_spent_minutes"].corr(df["problems_solved"]),
    2
)


# ==============================
# CONTEST ANALYSIS
# ==============================

contest_df = df[df["contest_given"] == "Yes"].copy()

contest_df["rating_change"] = contest_df["rating"].diff()

avg_rating_gain = round(contest_df["rating_change"].mean(), 2)

best_contest = contest_df.loc[contest_df["rating_change"].idxmax()]
worst_contest = contest_df.loc[contest_df["rating_change"].idxmin()]

rating_growth = df["rating"].iloc[-1] - df["rating"].iloc[0]


# ==============================
# BURNOUT DETECTION
# Rule: time high but problems solved low
# ==============================

burnout_days = df[
    (df["time_spent_minutes"] >= 120) &
    (df["problems_solved"] <= 2)
]

burnout_count = len(burnout_days)


# ==============================
# FINAL REPORT
# ==============================

print("\n========== CODING ACTIVITY ANALYZER REPORT ==========\n")

print("----- Basic Overview -----")
print(f"Total Active Coding Days       : {total_days}")
print(f"Total Problems Solved          : {total_problems}")
print(f"Total Coding Hours             : {total_hours}")
print(f"Average Problems Per Day       : {avg_problems}")
print(f"Average Coding Time Per Day    : {avg_time} minutes")
print(f"Total Contests Given           : {total_contests}")

print("\n----- Streak Analysis -----")
print(f"Longest Coding Streak          : {longest_streak} days")

print("\n----- Productivity Analysis -----")
print(f"Best Coding Day                : {best_day['date'].date()} with {best_day['problems_solved']} problems")
print(f"Worst Coding Day               : {worst_day['date'].date()} with {worst_day['problems_solved']} problems")
print(f"Most Productive Weekday        : {most_productive_weekday}")

print("\n----- Topic Strength Analysis -----")
print(f"Strongest Topic                : {strongest_topic}")
print(f"Weakest Topic                  : {weakest_topic}")

print("\n----- Platform Performance -----")
print(f"Top Platform                   : {top_platform}")
print(f"{top_platform_percentage}% practice happened on {top_platform}")

print("\n----- Difficulty Analysis -----")
print(f"Easy Problems Solved           : {easy_total}")
print(f"Medium Problems Solved         : {medium_total}")
print(f"Hard Problems Solved           : {hard_total}")
print(f"Hard Problems Percentage       : {hard_percentage}%")

print("\n----- Monthly Growth Analysis -----")
print(f"Best Month                     : {best_month}")
print(f"Growth From First To Last Month: {growth_percentage}%")

print("\n----- Time vs Problems Analysis -----")
print(f"Correlation Value              : {correlation}")

if correlation > 0.5:
    print("Insight                        : More time spent generally led to more problems solved.")
elif correlation > 0:
    print("Insight                        : Time spent has a weak positive relation with problems solved.")
else:
    print("Insight                        : More time did not always mean more problems solved.")

print("\n----- Contest Analysis -----")
print(f"Starting Rating                : {df['rating'].iloc[0]}")
print(f"Current Rating                 : {df['rating'].iloc[-1]}")
print(f"Overall Rating Growth          : +{rating_growth}")
print(f"Average Rating Gain            : {avg_rating_gain}")
print(f"Best Contest Date              : {best_contest['date'].date()}")
print(f"Best Contest Rating Jump       : +{int(best_contest['rating_change'])}")
print(f"Worst Contest Date             : {worst_contest['date'].date()}")
print(f"Worst Contest Rating Change    : {int(worst_contest['rating_change'])}")

print("\n----- Burnout Detection -----")
print(f"Potential Burnout Days Found   : {burnout_count}")

if burnout_count > 0:
    print("Insight                        : Some days had high time spent but low output.")

print("\n======================================================")


# ==============================
# CHART 1: WEEKDAY ANALYSIS
# ==============================

plt.figure(figsize=(9, 5))
weekday_analysis.plot(kind="bar")
plt.title("Weekday-wise Problems Solved")
plt.xlabel("Weekday")
plt.ylabel("Problems Solved")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/weekday_analysis.png")
plt.close()


# ==============================
# CHART 2: TIME VS PROBLEMS
# ==============================

plt.figure(figsize=(8, 5))
plt.scatter(df["time_spent_minutes"], df["problems_solved"])
plt.title("Time Spent vs Problems Solved")
plt.xlabel("Time Spent (minutes)")
plt.ylabel("Problems Solved")
plt.tight_layout()
plt.savefig("charts/time_vs_problems.png")
plt.close()


# ==============================
# CHART 3: TOPIC STRENGTH
# ==============================

plt.figure(figsize=(10, 5))
topic_strength.plot(kind="bar")
plt.title("Topic Strength Analysis")
plt.xlabel("Topic")
plt.ylabel("Problems Solved")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/topic_strength.png")
plt.close()


# ==============================
# CHART 4: PLATFORM PERFORMANCE
# ==============================

plt.figure(figsize=(8, 5))
platform_performance.plot(kind="bar")
plt.title("Platform-wise Problems Solved")
plt.xlabel("Platform")
plt.ylabel("Problems Solved")
plt.tight_layout()
plt.savefig("charts/platform_performance.png")
plt.close()


# ==============================
# CHART 5: DIFFICULTY DISTRIBUTION
# ==============================

difficulty_values = [easy_total, medium_total, hard_total]
difficulty_labels = ["Easy", "Medium", "Hard"]

plt.figure(figsize=(7, 7))
plt.pie(difficulty_values, labels=difficulty_labels, autopct="%1.1f%%")
plt.title("Difficulty Distribution")
plt.tight_layout()
plt.savefig("charts/difficulty_distribution.png")
plt.close()


# ==============================
# CHART 6: DIFFICULTY TREND
# ==============================

plt.figure(figsize=(10, 5))
difficulty_trend.plot(kind="bar")
plt.title("Month-wise Difficulty Trend")
plt.xlabel("Month")
plt.ylabel("Problems Solved")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/difficulty_trend.png")
plt.close()


# ==============================
# CHART 7: MONTHLY GROWTH
# ==============================

plt.figure(figsize=(9, 5))
monthly_growth.plot(kind="bar")
plt.title("Monthly Growth Report")
plt.xlabel("Month")
plt.ylabel("Problems Solved")
plt.tight_layout()
plt.savefig("charts/monthly_growth.png")
plt.close()


# ==============================
# CHART 8: RATING GROWTH
# ==============================

plt.figure(figsize=(10, 5))
plt.plot(contest_df["date"], contest_df["rating"], marker="o")
plt.title("Contest Rating Growth")
plt.xlabel("Date")
plt.ylabel("Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/rating_growth.png")
plt.close()


# ==============================
# CHART 9: DAILY PROBLEMS TREND
# ==============================

plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["problems_solved"], marker="o")
plt.title("Daily Problems Solved Trend")
plt.xlabel("Date")
plt.ylabel("Problems Solved")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/daily_problems_trend.png")
plt.close()


# ==============================
# CHART 10: BURNOUT DAYS
# ==============================

if burnout_count > 0:
    plt.figure(figsize=(8, 5))
    plt.scatter(burnout_days["time_spent_minutes"], burnout_days["problems_solved"])
    plt.title("Potential Burnout Days")
    plt.xlabel("Time Spent (minutes)")
    plt.ylabel("Problems Solved")
    plt.tight_layout()
    plt.savefig("charts/burnout_days.png")
    plt.close()


print("\nCharts generated successfully inside the 'charts' folder.")