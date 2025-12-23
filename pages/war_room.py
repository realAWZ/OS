import streamlit as st
import requests

st.set_page_config(page_title="War Room", page_icon="🏈")

st.title("🏈 The Parlay Prophet")
st.markdown("### AI-Assisted Matchup Analyzer")

# --- INPUTS ---
col1, col2 = st.columns(2)
player_name = col1.text_input("Player Name:", "Saquon Barkley")
position = col2.selectbox("Position:", ["RB", "WR", "QB", "TE"])

col3, col4 = st.columns(2)
# We assume the user checks the matchup rank manually for now
opp_rank = col3.slider("Opponent Defense Rank (32=Worst, 1=Best)", 1, 32, 16)
stadium_city = col4.text_input("Stadium City:", "Green Bay")

# --- WEATHER ENGINE (Borrowed from Lawn Enforcer) ---
weather_score = 0
weather_desc = "Dome/Fair"

if stadium_city:
    try:
        # Geocode
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={stadium_city}&count=1").json()
        if "results" in geo:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            
            # Weather
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph").json()
            curr = w['current']
            
            temp = curr['temperature_2m']
            wind = curr['wind_speed_10m']
            rain = curr['rain']
            
            # FOOTBALL WEATHER LOGIC
            # High wind kills passing (QB/WR bad), helps rushing (RB good)
            if wind > 15:
                weather_desc = f"High Winds ({wind}mph)"
                if position in ["QB", "WR"]:
                    weather_score -= 20 # Downgrade passing
                elif position == "RB":
                    weather_score += 10 # Upgrade rushing (volume play)
            
            # Rain makes ball slippery (Turnover risk)
            if rain > 0:
                weather_desc = "Raining"
                weather_score -= 10
            
            # Snow (Cold)
            if temp < 32:
                weather_desc = "Freezing"
                if position == "QB": weather_score -= 15
                
            st.info(f"🏟️ **Stadium Conditions:** {temp}°F | {weather_desc}")
            
    except:
        st.warning("Could not pull stadium weather.")

# --- THE PROPHET ALGORITHM ---
# Base Score (0-100)
prediction = 50 

# 1. Matchup Logic
# If defense is Rank 32 (Bad), we add points. If Rank 1 (Good), we subtract.
matchup_bonus = (opp_rank - 16) * 1.5 
prediction += matchup_bonus

# 2. Weather Logic
prediction += weather_score

# --- VERDICT ---
st.divider()
st.subheader("🔮 THE PREDICTION")

if prediction > 75:
    st.success(f"## 🚀 SMASH START ({int(prediction)}/100)")
    st.write(f"**Why:** {player_name} has a prime matchup against a Rank {opp_rank} defense.")
    if weather_score > 0: st.write(f"**Bonus:** Weather favors this position ({weather_desc}).")
    
elif prediction < 40:
    st.error(f"## 🛑 SIT / FADE ({int(prediction)}/100)")
    st.write(f"**Why:** Tough matchup (Rank {opp_rank}).")
    if weather_score < 0: st.write(f"**Warning:** Weather is bad for {position}s today.")
    
else:
    st.warning(f"## ⚖️ FLEX OPTION ({int(prediction)}/100)")
    st.write("Decent floor, but don't expect a ceiling game.")
