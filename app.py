import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="MedTimer", page_icon="💊", layout="centered")

st.title("💊 MedTimer: Daily Medicine Reminder App")

# Initialize session state
if 'med_list' not in st.session_state:
    st.session_state.med_list = []

if 'taken_today' not in st.session_state:
    st.session_state.taken_today = set()

if 'week_data' not in st.session_state:
    # Holds daily total meds & taken meds for the week
    st.session_state.week_data = []

# Input section
st.header("➕ Add your medicines and times")
with st.form(key="add_med_form"):
    med_name = st.text_input("Medicine name")
    med_time = st.time_input("Time to take")
    submitted = st.form_submit_button("Add medicine")
    if submitted and med_name:
        st.session_state.med_list.append({
            'name': med_name,
            'time': med_time
        })
        st.success(f"Added {med_name} at {med_time.strftime('%H:%M')}")

# Display daily checklist
st.header("📋 Today's checklist")
now = datetime.now()

if st.session_state.med_list:
    for idx, med in enumerate(st.session_state.med_list):
        scheduled_dt = now.replace(hour=med['time'].hour, minute=med['time'].minute, second=0, microsecond=0)
        # If scheduled time has passed, and not taken, mark as missed
        status = ""
        if med['name'] in st.session_state.taken_today:
            status = "✅ Taken"
        elif now > scheduled_dt + timedelta(minutes=30):  # 30 min grace
            status = "❌ Missed"
        elif now >= scheduled_dt:
            status = "⏰ Due now"
        else:
            mins = int((scheduled_dt - now).total_seconds() / 60)
            status = f"🕒 Upcoming in {mins} min"

        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**{med['name']}** at {med['time'].strftime('%H:%M')} — {status}")
        with col2:
            if med['name'] not in st.session_state.taken_today:
                if st.button(f"Mark as taken ✅", key=f"btn_{idx}"):
                    st.session_state.taken_today.add(med['name'])

# Weekly adherence score (simple: taken today vs total meds)
st.header("📊 Weekly adherence score")
total_doses = len(st.session_state.med_list)
taken = len(st.session_state.taken_today)

if total_doses > 0:
    score_today = int((taken / total_doses) * 100)
else:
    score_today = 0

# Append today's score to week_data if not already added (simulate daily tracking)
if len(st.session_state.week_data) < 7:
    if st.button("📅 Save today's score to week"):
        st.session_state.week_data.append(score_today)
        st.session_state.taken_today.clear()
        st.success("Today's score saved. Start fresh for tomorrow!")

if st.session_state.week_data:
    st.write("**Scores this week:**", st.session_state.week_data)
    avg_score = sum(st.session_state.week_data) / len(st.session_state.week_data)
    st.write(f"**Average adherence:** {avg_score:.1f}%")

else:
    st.info("No weekly data yet. Save today's score to start tracking.")

st.caption("⚙ Built with Python, Streamlit and datetime — lightweight, local, and API-free.")

