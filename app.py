import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

import time
import threading



# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = {
        'daily_intake': {},
        'streaks': 0,
        'achievements': [],
        'profile': {
            'name': '',
            'age': 25,
            'weight': 70,
            'activity': 'Moderate',
            'climate': 'Temperate'
        }
    }

# Load data from file if exists
DATA_FILE = 'hydration_data.json'
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        st.session_state.data = json.load(f)

def save_data():
    """Save data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.data, f)

def calculate_streak():
    """Calculate current streak"""
    streak = 0
    today = datetime.now().date()
    current_date = today
    
    while True:
        date_str = current_date.strftime('%Y-%m-%d')
        if date_str in st.session_state.data['daily_intake']:
            if st.session_state.data['daily_intake'][date_str] >= st.session_state.data.get('daily_goal', 3000):
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        else:
            break
    return streak

def update_achievements():
    """Update user achievements"""
    achievements = []
    total_days = len(st.session_state.data['daily_intake'])
    current_streak = calculate_streak()
    total_intake = sum(st.session_state.data['daily_intake'].values())

    if total_days >= 1:
        achievements.append("🎯 First Day Complete!")
    if total_days >= 7:
        achievements.append("🌟 Week Warrior")
    if total_days >= 30:
        achievements.append("💫 Monthly Master")
    if current_streak >= 3:
        achievements.append("🔥 3-Day Streak")
    if current_streak >= 7:
        achievements.append("⚡ 7-Day Streak")
    if total_intake >= 100000:
        achievements.append("🌊 100L Club Member")

    st.session_state.data['achievements'] = achievements

st.set_page_config(page_title="HydroTracker - Complete Hydration System", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body { font-family: 'Inter', 'Roboto', sans-serif; background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d2d2d 100%); color: #fff; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 30px; position: relative; }
        .header h1 { font-size: 3rem; margin: 20px 0 10px 0; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcd3c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 30px rgba(255, 107, 53, 0.3); }
        .header p { font-size: 1.2rem; opacity: 0.8; margin: 10px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
        .nav-tabs { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
        .nav-tab { padding: 12px 20px; background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%); border: 1px solid #4a4a4a; border-radius: 10px; color: #fff; cursor: pointer; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; }
        .nav-tab.active { background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); border-color: #ff6b35; box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3); }
        .main-card { background: linear-gradient(145deg, #1e1e1e, #2a2a2a); border-radius: 20px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1); margin-bottom: 20px; border: 1px solid rgba(255, 107, 53, 0.2); }
    </style>
""", unsafe_allow_html=True)


# --- Navigation Tabs ---
tabs = ["🏠 Welcome", "👤 Profile", "📚 Learn", "📈 Progress", "💧 Tracker"]

# Initialize selected tab in session state if not present
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "🏠 Welcome"

# Use the existing session state value for the radio button's default index
default_ix = tabs.index(st.session_state["selected_tab"])
selected_tab = st.radio("", tabs, horizontal=True, key="nav_tabs", index=default_ix)

# Update the session state to match the radio selection
st.session_state["selected_tab"] = selected_tab

# --- Welcome Page ---
if selected_tab == "🏠 Welcome":
    st.markdown('<div class="header"><h1>💧 HYDROTRACKER</h1><p>FUEL YOUR GAINS • DOMINATE YOUR HYDRATION</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## Welcome to HydroTracker")
    st.write("Your ultimate hydration companion for peak performance and optimal health. Track, learn, and dominate your hydration goals!")
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card"><div class="feature-icon">📊</div><h3>Smart Tracking</h3><p>Monitor your daily water intake with precision. Set personalized goals based on your age, activity level, and lifestyle.</p></div>
        <div class="feature-card"><div class="feature-icon">🎯</div><h3>Personal Goals</h3><p>Customized hydration targets that adapt to your unique needs. From athletes to office workers, we've got you covered.</p></div>
        <div class="feature-card"><div class="feature-icon">🏆</div><h3>Achievement System</h3><p>Celebrate milestones and build healthy habits with our motivational progress tracking and rewards system.</p></div>
        <div class="feature-card"><div class="feature-icon">📚</div><h3>Expert Knowledge</h3><p>Learn from science-backed hydration tips and discover how proper hydration boosts your performance and health.</p></div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 GET STARTED", key="get_started_btn", use_container_width=True):
            st.session_state["selected_tab"] = "👤 Profile"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Profile Page ---
elif selected_tab == "👤 Profile":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #ff6b35; margin-bottom: 30px; text-transform: uppercase; font-weight: 900;">⚙️ Your Profile</h2>', unsafe_allow_html=True)
    
    # Load current values from session state
    current_profile = st.session_state.data['profile']
    
    # Create input fields with current values
    name = st.text_input("Name", value=current_profile['name'])
    age = st.number_input("Age", min_value=6, max_value=100, value=current_profile['age'])
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=current_profile['weight'])
    activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "High", "Extreme"], 
                          index=["Sedentary", "Light", "Moderate", "High", "Extreme"].index(current_profile['activity']))
    climate = st.selectbox("Climate", ["Temperate", "Hot", "Humid", "Dry"],
                         index=["Temperate", "Hot", "Humid", "Dry"].index(current_profile['climate']))
    
    # Save changes when any value changes
    if (name != current_profile['name'] or 
        age != current_profile['age'] or 
        weight != current_profile['weight'] or 
        activity != current_profile['activity'] or
        climate != current_profile['climate']):
        
        st.session_state.data['profile'].update({
            'name': name,
            'age': age,
            'weight': weight,
            'activity': activity,
            'climate': climate
        })
        save_data()
        st.success("Profile updated successfully!")
    st.markdown("""
    <div class="profile-stats">
        <div class="stat-box"><h4>2500</h4><p>Recommended Daily Intake (ml)</p></div>
        <div class="stat-box"><h4>2000</h4><p>Baseline Requirement (ml)</p></div>
        <div class="stat-box"><h4>500</h4><p>Activity Bonus (ml)</p></div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📚 LEARN MORE", key="learn_more_btn", use_container_width=True):
            st.session_state["selected_tab"] = "📚 Learn"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Education Page ---
elif selected_tab == "📚 Learn":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #ff6b35; margin-bottom: 30px; text-transform: uppercase; font-weight: 900;">📚 Hydration Education</h2>', unsafe_allow_html=True)
    st.markdown("### 💪 Why Hydration Matters")
    st.info("Proper hydration can improve physical performance by up to 15%. Even mild dehydration (2% body weight loss) can significantly impact strength, endurance, and cognitive function.")
    st.info("Water is essential for protein synthesis and muscle recovery. Dehydrated muscles recover 23% slower than properly hydrated ones.")
    st.markdown("### 🎯 Hydration Benefits")
    st.markdown("""
    - 🧠 Mental Clarity: Improved focus and cognitive performance
    - 💪 Muscle Function: Enhanced strength and endurance
    - 🔥 Metabolism: Boosted metabolic rate and fat burning
    - ✨ Skin Health: Improved skin elasticity and appearance
    - 🛡️ Immune System: Stronger immune response
    - 😴 Sleep Quality: Better sleep and recovery
    """)
    st.markdown("### ⚡ Pro Tips for Athletes")
    st.info("Pre-Workout Hydration: 2-3 hours before: 500-600ml of water. 15-20 minutes before: 200-300ml of water.")
    st.info("During Exercise: Every 15-20 minutes: 150-250ml of fluid. For sessions >1 hour: Add electrolytes.")
    st.info("Post-Workout Recovery: Within 6 hours: Replace 150% of fluid lost through sweat. Quick check: Weigh yourself before/after - drink 500ml per pound lost.")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💧 START TRACKING", key="start_tracking_btn", use_container_width=True):
            st.session_state["selected_tab"] = "💧 Tracker"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Progress Page ---
elif selected_tab == "📈 Progress":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #ff6b35; margin-bottom: 30px; text-transform: uppercase; font-weight: 900;">📈 Your Progress</h2>', unsafe_allow_html=True)
    
    # Initialize the progress data if not exists
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {
            'streak': 0,
            'total_intake': 0,
            'best_day': 0,
            'days_tracked': 0
        }
    
    # Display stats in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Current Streak", f"{st.session_state.progress_data['streak']} days")
    with col2:
        st.metric("💧 Total Intake", f"{st.session_state.progress_data['total_intake']} ml")
    with col3:
        st.metric("🌟 Best Day", f"{st.session_state.progress_data['best_day']} ml")
    with col4:
        st.metric("� Days Tracked", f"{st.session_state.progress_data['days_tracked']} days")
    
    # Simple progress visualization
    st.markdown("### Last 7 Days")
    progress_data = [0, 1500, 2000, 2500, 3000, 2000, 1800]  # Example data
    st.bar_chart(progress_data)
    
    # Achievements section
    st.markdown("### 🏆 Achievements")
    achievements = [
        "🎯 First Day Complete!",
        "💪 Water Warrior",
        "🌊 Hydration Master",
        "⚡ 3-Day Streak"
    ]
    
    # Display achievements in a grid
    cols = st.columns(2)
    for i, achievement in enumerate(achievements):
        with cols[i % 2]:
            st.success(achievement)
    
    # Notification Bar (Browser-based)
    st.markdown("### ⏰ Hydration Notification")
    with st.expander("Enable Hydration Reminder", expanded=False):
        enable_notify = st.checkbox("Enable browser hydration notifications", key="notify_checkbox")
        interval = st.slider("Notification interval (minutes)", min_value=30, max_value=240, value=60, step=30)
        if st.button("Send Test Notification"):
            st.markdown("""
            <script>
            if (Notification && Notification.permission !== "denied") {
                Notification.requestPermission().then(function(permission) {
                    if(permission === "granted") {
                        new Notification("HydroTracker", {body: "Stay hydrated! Time to drink some water! 💧"});
                    }
                });
            }
            </script>
            """, unsafe_allow_html=True)
            st.success("Test browser notification sent! If you don't see it, check your browser notification settings.")
        st.info("You will receive reminders to drink water at the interval you set, as long as this tab is open and notifications are enabled.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tracker Page ---
elif selected_tab == "💧 Tracker":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 💧 Daily Tracker")
    
    # Get today's date
    today = datetime.now().date().strftime('%Y-%m-%d')
    
    # Initialize today's intake if not exists
    if today not in st.session_state.data['daily_intake']:
        st.session_state.data['daily_intake'][today] = 0
    
    # Settings section
    with st.expander("⚙️ Settings", expanded=False):
        age_group = st.selectbox("Age Group", 
                               ["Child (6-12 years)", "Teen (13-18 years)", 
                                "Adult (19-64 years)", "Senior (65+ years)"])
        daily_goal = st.number_input("Daily Goal (ml)", 
                                   min_value=500, max_value=5000, value=3000)
        if daily_goal != st.session_state.data.get('daily_goal', 3000):
            st.session_state.data['daily_goal'] = daily_goal
            save_data()
    
    # Display current progress
    current_intake = st.session_state.data['daily_intake'][today]
    remaining = daily_goal - current_intake
    
    # Progress metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👍 Current Intake", f"{current_intake}ml")
    with col2:
        st.metric("🎯 Daily Goal", f"{daily_goal}ml")
    with col3:
        st.metric("⏳ Remaining", f"{remaining}ml")
    
    # Progress bar
    progress = (current_intake / daily_goal) * 100 if daily_goal else 0
    st.progress(min(100, int(progress)))
    
    # Quick add buttons
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 10px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick Add")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🥤 +250ml", key="btn_250"):
            st.session_state.data['daily_intake'][today] = st.session_state.data['daily_intake'].get(today, 0) + 250
            save_data()
            st.rerun()
    with col2:
        if st.button("🍶 +500ml", key="btn_500"):
            st.session_state.data['daily_intake'][today] = st.session_state.data['daily_intake'].get(today, 0) + 500
            save_data()
            st.rerun()
    with col3:
        if st.button("🏋️ +750ml", key="btn_750"):
            st.session_state.data['daily_intake'][today] = st.session_state.data['daily_intake'].get(today, 0) + 750
            save_data()
            st.rerun()
    with col4:
        if st.button("🌊 +1000ml", key="btn_1000"):
            st.session_state.data['daily_intake'][today] = st.session_state.data['daily_intake'].get(today, 0) + 1000
            save_data()
            st.rerun()
    
    # Custom amount
    st.markdown("### 🎯 Custom Amount")
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_amount = st.number_input("Enter amount (ml)", 
                                      min_value=1, max_value=2000, value=100,
                                      key="custom_amount")
    with col2:
        if st.button("Add Custom", key="btn_custom"):
            st.session_state.data['daily_intake'][today] = st.session_state.data['daily_intake'].get(today, 0) + custom_amount
            save_data()
            st.rerun()
    
    # Reset button
    st.markdown("### ")  # Add some spacing
    if st.button("🔄 Reset Today's Intake", key="btn_reset", type="secondary"):
        st.session_state.data['daily_intake'][today] = 0
        save_data()
        st.rerun()
    
    # Tips and motivation
    with st.expander("💡 Daily Tips", expanded=False):
        st.info("🔥 WELCOME TO THE HYDRATION ZONE! Time to fuel your body and maximize your performance!")
        st.markdown("""
        #### 🏋️ PRO HYDRATION TIPS
        - 💪 Pre-workout: 500ml (2-3 hours before)
        - 🏃‍♂️ During workout: 200-300ml every 20 minutes
        - 🌟 Post-workout: Replace 150% of water lost
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
