import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Zosche OS", page_icon="🧬", layout="wide")

st.title("🧬 Zosche OS: The Lab")
st.caption(f"Current Date: {datetime.date.today()}")

# --- 1. THE DAILY PROTOCOL ---
st.subheader("📝 Daily Protocol")

# Create a simple dataframe for the checklist
# In a real V2, we would connect this to Google Sheets to save it forever.
data = {
    "Task": ["Creatine (5g)", "Water (1 Gallon)", "Read (10 Pages)", "Workout", "Face Routine"],
    "Status": [False, False, False, False, False],
    "Notes": ["", "", "Book: 48 Laws", "Push Day", ""]
}
df = pd.DataFrame(data)

# The Editor - You can actually click these boxes!
edited_df = st.data_editor(
    df,
    column_config={
        "Status": st.column_config.CheckboxColumn("Done", help="Check when complete", default=False)
    },
    hide_index=True,
    num_rows="fixed"
)

# Progress Bar Calculation
completed = edited_df["Status"].sum()
total = len(edited_df)
progress = completed / total
st.progress(progress, text=f"Daily Completion: {int(progress*100)}%")

if progress == 1.0:
    st.success("🔥 PROTOCOL COMPLETE. 1% BETTER TODAY.")

st.divider()

# --- 2. ACADEMIC SNIPER ---
st.subheader("🎓 GPA Defense")
col1, col2, col3 = st.columns(3)
current_gpa = col1.number_input("Current GPA", value=3.90)
goal_gpa = col2.number_input("Goal GPA", value=4.0)
credits = col3.number_input("Credits Remaining", value=15)

# Simple projection logic
if goal_gpa > current_gpa:
    req_score = "STRAIGHT A's"
    st.info(f"Target: You need **{req_score}** to hit {goal_gpa}.")
else:
    st.success("You are cruising. Maintain course.")
