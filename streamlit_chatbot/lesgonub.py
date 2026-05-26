import streamlit as st
import os
import pandas as pd
from datetime import datetime

# CRITICAL RULE: This must always remain the first execution command!
st.set_page_config(page_title="Sunway Viva Hub", page_icon="🎓", layout="wide")

# Custom CSS injection for an "Attractive yet Eye-Comfortable" Indigo & Warm Sand Palette
st.markdown("""
<style>
    /* Dark Mode Comfort: Deep charcoal with a warm undertone to completely remove stark white glare */
    .stApp { 
        background-color: #12141C; 
        color: #E2E8F0; 
    }
    
    /* Elegant, premium pop of Indigo for main page headings */
    h1 { font-family: 'Poppins', sans-serif; font-weight: 800; color: #818CF8 !important; }
    h2, h3, h4 { font-family: 'Poppins', sans-serif; font-weight: 700; color: #F1F5F9 !important; }
    
    /* Clean, soft custom cards to group content beautifully without harsh contrast */
    div[data-testid="stVScrollBlock"] > div {
        background-color: #1E2230 !important;
        border: 1px solid #2D334A !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }

    /* Muted background styling specifically for inputs and dropdown fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #161925 !important;
        color: #F1F5F9 !important;
        border: 1px solid #2D334A !important;
        border-radius: 10px;
    }
    
    /* Soft, glowing premium action buttons that stand out but remain calm */
    .stButton>button { 
        border-radius: 12px; 
        transition: all 0.2s ease; 
        background-color: #312E81 !important; 
        color: #C7D2FE !important;
        border: 1px solid #4338CA !important; 
    }
    .stButton>button:hover { 
        background-color: #4338CA !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 12px rgba(129, 140, 248, 0.3);
        transform: translateY(-1px); 
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INITIALIZATION ----------------
if "user" not in st.session_state: st.session_state.user = None
if "favorites" not in st.session_state: st.session_state.favorites = []
if "joined" not in st.session_state: st.session_state.joined = {}
if "popularity" not in st.session_state: st.session_state.popularity = {}
if "user_activities" not in st.session_state: st.session_state.user_activities = []
if "active_chat_partner" not in st.session_state: st.session_state.active_chat_partner = None

# FEATURE 3: Live System Notification Feed Array
if "notifications" not in st.session_state:
    st.session_state.notifications = [
        "🔔 Chloe Moss just listed an item in the Marketplace Foyer!",
        "🔔 System: Multiplier Bonus is currently active for all June tournament slots."
    ]

def add_notification(text):
    st.session_state.notifications.insert(0, f"🔔 {text}")
    if len(st.session_state.notifications) > 5:
        st.session_state.notifications.pop()

def get_chat_key(user1, user2):
    return "-between-".join(sorted([user1, user2]))

# CAMPUS COMMUNITIES DATA
clubs = {
    "⚽ Football Club": ("🏃‍♂️ Sports & Vigor", "Weekly turf matches, tactical analysis, and local university friendlies."),
    "🏀 Basketball Club": ("🏃‍♂️ Sports & Vigor", "High-energy court runs, 3v3 tournaments, and buzzer-beater memories."),
    "🏸 Badminton Club": ("🏃‍♂️ Sports & Vigor", "Smash rallies, mixed doubles matchups, and casual training sessions."),
    "🏐 Volleyball Club": ("🏃‍♂️ Sports & Vigor", "Spike training, team chemistry drills, and outdoor beach events."),
    "🎮 Esports Club": ("🏃‍♂️ Sports & Vigor", "LAN parties, competitive tournament streams, and casual gaming nights."),
    "💻 Dev & Programming": ("🧠 Brain Trust", "Hackathons, collective AI workspace jams, and UI/UX design workshops."),
    "🚀 Startup & Business": ("🧠 Brain Trust", "Pitch deck review circles, mock trading floors, and corporate networking trips."),
    "📈 Finance Innovation": ("🧠 Brain Trust", "Crypto analysis, portfolio asset simulators, and personal banking hacks."),
    "📐 Logic & Math Club": ("🧠 Brain Trust", "Algorithm design strategies, quantitative riddles, and research theory."),
    "🔬 Applied Science": ("🧠 Brain Trust", "Experimental chemistry labs, rocket building, and engineering workshops.")
}

tournaments = {
    "⚽ Football Club": "🏆 Sunway Mega Cup - June 10",
    "🏀 Basketball Club": "🏆 Mid-Semester Madness - June 15",
    "🏸 Badminton Club": "🏆 Smash Arena Open - June 20",
    "🎮 Esports Club": "🏆 Cyber-Titan LAN - June 25",
    "💻 Dev & Programming": "🏆 Code-Sprint Hackathon - June 30"
}

for c in clubs:
    if c not in st.session_state.popularity: st.session_state.popularity[c] = 5
    if c not in st.session_state.joined: st.session_state.joined[c] = False

# Pre-populate Marketplace Deals
if "marketplace_deals" not in st.session_state or not st.session_state.marketplace_deals:
    st.session_state.marketplace_deals = [
        {
            "id": 101, 
            "seller": "Chloe Moss", 
            "item": "Mechanical Keyboard (Custom Blue Switches)", 
            "club_tag": "🎮 Esports Club",
            "price": "RM 120 / Trade for Badminton Racket", 
            "condition": "Like New (Pre-loved)", 
            "details": "Super clicky, immaculate condition. Perfect for setup upgrades. Handoff at Sunway Cafeteria block after 4 PM."
        },
        {
            "id": 102, 
            "seller": "Daniel Raj", 
            "item": "Macroeconomics Reference Textbook + Past Year Notes", 
            "club_tag": "🚀 Startup & Business",
            "price": "Free! Just bring me an Iced Latte ☕", 
            "condition": "Fair Condition", 
            "details": "Includes all my handwritten chapter summaries for the upcoming mid-terms. Leaving it at Library Foyer."
        },
        {
            "id": 103, 
            "seller": "Sarah Lim", 
            "item": "Sunway University Hoodie (Size L)", 
            "club_tag": "⚽ Football Club",
            "price": "RM 45", 
            "condition": "Brand New (Sealed)", 
            "details": "Bought the wrong size during orientation week, never worn. Still has tags."
        }
    ]

if "chat_messages" not in st.session_state: 
    st.session_state.chat_messages = {}

# Default entries for events
if not st.session_state.user_activities:
    st.session_state.user_activities = [
        {"id": 1, "type": "Club Match", "host": "Chloe Moss", "club": "🏀 Basketball Club", "title": "Casual Evening Half-Court Run", "details": "Just bringing a basketball down to the main court. Need a solid group for 3v3 half-court, super chill vibes!", "time": "June 14, 6:00 PM", "attendees": ["Chloe Moss", "Daniel Raj"]}
    ]

# ---------------- SIDEBAR NAVIGATION & PORTAL DOOR ----------------
st.sidebar.markdown("<h1 style='text-align: center; color: #818CF8; font-size:2.2rem;'>✨ Sunway Viva</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94A3B8; font-size:0.9rem; margin-top:-15px;'>Your Ultimate College Clique Hub</p>", unsafe_allow_html=True)
st.sidebar.divider()

if not st.session_state.user:
    st.sidebar.subheader("👋 Grab Your Name Tag!")
    name = st.sidebar.text_input("What should the campus call you?", placeholder="e.g., Brandon Tan")
    if st.sidebar.button("Step Inside 🚪", use_container_width=True, type="primary"):
        if name.strip():
            st.session_state.user = name.strip()
            ck = get_chat_key(st.session_state.user, "Chloe Moss")
            if ck not in st.session_state.chat_messages or not st.session_state.chat_messages[ck]:
                st.session_state.chat_messages[ck] = [
                    {"sender": "Chloe Moss", "text": "Hey! Are you still down to trade for that mechanical keyboard?"},
                    {"sender": st.session_state.user, "text": "Yeah! Is it missing any keycaps?"},
                    {"sender": "Chloe Moss", "text": "Nope, fully intact! Let me know if you want to meet up near the cafeteria."}
                ]
            st.rerun()
else:
    st.sidebar.markdown(f"<div style='background-color:#1E2230; padding:12px; border-radius:12px; border:1px solid #334155; text-align:center;'>👑 Signed in as: <b style='color:#F43F5E;'>{st.session_state.user}</b></div>", unsafe_allow_html=True)
    st.write("")
    menu = st.sidebar.selectbox("🗺️ Where to hang out?", ["🏠 Common Room (Home)", "📣 Club Fair", "🎯 Squad Matchmaker", "🛍️ Peer Marketplace & Chat", "🏆 Leagues & Cups", "✨ My Watchlist & Schedule", "📊 Popularity Standings"])
    st.sidebar.divider()
    if st.sidebar.button("Sign Out 🏃‍♂️", use_container_width=True, type="secondary"):
        st.session_state.user = None
        st.session_state.active_chat_partner = None
        st.rerun()

# ---------------- GATED MAIN SYSTEM ACCESS ----------------
if not st.session_state.user:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%); padding:50px; border-radius:20px; text-align:center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #4338CA;">
            <h1 style="color:#818CF8 !important; margin:0; font-size:3rem;">🎓 Welcome to the Sunway Viva Lounge!</h1>
            <p style="color:#CBD5E1; font-size:1.2rem; margin-top:12px; opacity:0.95;">The ultimate collaborative spot to find your squad, plan weekend match drop-ins, and swap gear with fellow students.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("")
    col_img, col_txt = st.columns([1.4, 2])
    with col_img:
        st.markdown(
            """
            <div style="background-color:#1E2230; height:240px; border-radius:20px; display:flex; align-items:center; justify-content:center; text-align:center; padding:15px; border: 1px dashed #4338CA;">
                <p style="color:#94A3B8; font-weight:bold; margin:0;">📸 Campus Portal Live Assets Connected.</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col_txt:
        st.markdown("### 🔥 Life is Better Together")
        st.write("Don't just go through classes alone. Discover hidden groups, lock down competitive league slots, find carpool buddies, or score amazing pre-loved university equipment right from other students on campus.")
        st.warning("👉 **Slide over to the sidebar on your left, type your name, and step into the common room to see what's happening right now!**")
else:

    # ---------------- 🏠 THE COMMON ROOM (HOME) ----------------
    if menu == "🏠 Common Room (Home)":
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); padding: 35px; border-radius: 20px; margin-bottom: 25px; border: 1px solid #4338CA;">
                <h1 style="color: #C7D2FE !important; margin: 0; font-size:2.6rem;">👋 Yo, {st.session_state.user}!</h1>
                <p style="color: #94A3B8; font-size: 1.2rem; margin-top: 6px; margin-bottom: 0; opacity:0.9;">Grab a couch. Here's your personalized student portal feed today.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.markdown("#### 🔔 Real-time Campus Alerts")
        for alert in st.session_state.notifications[:3]:
            st.markdown(f"<div style='background-color:#161925; border: 1px solid #2D334A; padding:10px 15px; border-radius:10px; margin-bottom:8px; font-size:0.9rem; color:#CBD5E1;'>{alert}</div>", unsafe_allow_html=True)
        st.write("")
        
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            joined_count = sum(1 for v in st.session_state.joined.values() if v)
            st.markdown(f"<div style='background-color:#161925; border-radius:15px; padding:20px; border-left:6px solid #818CF8;'><h5 style='margin:0; color:#94A3B8;'>My Active Circles</h5><h2 style='margin:5px 0 0 0; color:#F1F5F9;'>💫 {joined_count} Joined</h2></div>", unsafe_allow_html=True)
        with cm2:
            st.markdown(f"<div style='background-color:#161925; border-radius:15px; padding:20px; border-left:6px solid #A78BFA;'><h5 style='margin:0; color:#94A3B8;'>My Saved Watchlist</h5><h2 style='margin:5px 0 0 0; color:#F1F5F9;'>💖 {len(st.session_state.favorites)} Clubs</h2></div>", unsafe_allow_html=True)
        with cm3:
            active_deals = sum(1 for d in st.session_state.marketplace_deals if d["seller"] == st.session_state.user)
            st.markdown(f"<div style='background-color:#161925; border-radius:15px; padding:20px; border-left:6px solid #F43F5E;'><h5 style='margin:0; color:#94A3B8;'>Live Items Listed</h5><h2 style='margin:5px 0 0 0; color:#F1F5F9;'>🎒 {active_deals} Active</h2></div>", unsafe_allow_html=True)
            
        st.write("")
        col_body_left, col_body_right = st.columns([2, 1.2])
        with col_body_left:
            st.markdown("### 📢 What's New Around Campus")
            st.info("💡 **Friendship Multiplier Bonus:** Joining a tournament slot under the **Leagues & Cups** tab gives your club **+2 extra standing score points** on the live public leaderboard graphs!")
            st.success("🤝 **Marketplace Foyer:** Friendly reminder to set up transaction delivery swap points in populated spaces like the Sunway Cafeteria or Library Foyer for maximum comfort and safe handoffs.")
            
            st.markdown("### ⚡ Dynamic Campus Hub Simulator")
            st.write("Adjust the slider parameters to simulate student coordination density and see how it impacts active student bonding scores across campus directories!")

            st.iframe(
                """
                <div id="widget-root" style="font-family: system-ui, -apple-system, sans-serif; background: #1E2230; border: 1px solid #2D334A; border-radius: 16px; padding: 20px; max-width: 100%; box-sizing: border-box;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h4 style="margin: 0; color: #F1F5F9; font-size: 1.1rem;">📊 Real-time Bonding & Density Sandbox</h4>
                        <span style="background: #312E81; color: #C7D2FE; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">Interactive Module</span>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <label style="display:block; font-size:0.85rem; color:#94A3B8; font-weight:600; margin-bottom:5px;">Estimated Daily Active Students:</label>
                        <input type="range" id="studentsRange" min="50" max="500" value="150" style="width:100%; accent-color:#818CF8;">
                        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#64748B; margin-top:2px;"><span>50</span><span id="studentVal" style="color:#818CF8; font-weight:bold;">150</span><span>500</span></div>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display:block; font-size:0.85rem; color:#94A3B8; font-weight:600; margin-bottom:5px;">Weekly Club Events Hosted:</label>
                        <input type="range" id="eventsRange" min="2" max="30" value="12" style="width:100%; accent-color:#A78BFA;">
                        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#64748B; margin-top:2px;"><span>2</span><span id="eventsVal" style="color:#A78BFA; font-weight:bold;">12</span><span>30</span></div>
                    </div>

                    <div style="background: #161925; padding: 15px; border-radius: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: center; margin-bottom:10px; border: 1px solid #2D334A;">
                        <div>
                            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">Campus Synergy Score</div>
                            <div id="synergyScore" style="font-size: 1.6rem; font-weight: 800; color: #818CF8; margin-top:4px;">1,800</div>
                        </div>
                        <div>
                            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">Community Pulse Rate</div>
                            <div id="pulseRate" style="font-size: 1.6rem; font-weight: 800; color: #F1F5F9; margin-top:4px;">Healthy ✨</div>
                        </div>
                    </div>
                </div>

                <script>
                    const studentsSlider = document.getElementById('studentsRange');
                    const eventsSlider = document.getElementById('eventsRange');
                    const studentVal = document.getElementById('studentVal');
                    const eventsVal = document.getElementById('eventsVal');
                    const synergyScore = document.getElementById('synergyScore');
                    const pulseRate = document.getElementById('pulseRate');

                    function recalculate() {
                        const s = parseInt(studentsSlider.value);
                        const e = parseInt(eventsSlider.value);
                        
                        studentVal.innerText = s;
                        eventsVal.innerText = e;
                        
                        const synergy = s * e;
                        synergyScore.innerText = synergy.toLocaleString();
                        
                        if (synergy < 1200) {
                            pulseRate.innerText = "Quiet ☕";
                            pulseRate.style.color = "#94A3B8";
                        } else if (synergy < 4000) {
                            pulseRate.innerText = "Vibrant ✨";
                            pulseRate.style.color = "#A78BFA";
                        } else {
                            pulseRate.innerText = "Electric 🔥";
                            pulseRate.style.color = "#F43F5E";
                        }
                    }

                    studentsSlider.addEventListener('input', recalculate);
                    eventsSlider.addEventListener('input', recalculate);
                    recalculate();
                </script>
                """,
                height=300,
            )
        with col_body_right:
            st.markdown("#### 📸 Campus Atmosphere")
            st.markdown(
                """
                <div style="background-color:#161925; height:220px; border-radius:20px; display:flex; align-items:center; justify-content:center; text-align:center; padding:15px; border: 1px solid #2D334A; margin-top:10px;">
                    <p style="color:#64748B; font-size:0.85rem; font-weight:bold; margin:0;">🎨 Club Lounge active context loaded. Post a squad run to rally teammates!</p>
                </div>
                """, unsafe_allow_html=True
            )

    # ---------------- 📣 CLUB FAIR DIRECTORY ----------------
    elif menu == "📣 Club Fair":
        st.title("📣 Step Up & Explore the Club Fair!")
        st.write("Browse current groups, monitor their live community metric stats, and register instantly to secure regular invites.")
        
        search = st.text_input("🔍 Filter spaces by name or target keyword...")
        
        for name, info in clubs.items():
            ctype, desc = info
            if search.lower() in name.lower() or search.lower() in ctype.lower():
                border_color = "#818CF8" if "Sports" in ctype else "#A78BFA"
                
                st.markdown(
                    f"""
                    <div style="background-color: #1E2230; border: 1px solid #2D334A; border-left: 6px solid {border_color}; padding: 18px; border-radius: 12px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="margin: 0; color:#F1F5F9;">{name}</h3>
                                <span style="background: #161925; padding: 2px 8px; border-radius: 8px; font-size: 0.8rem; font-weight: bold; color: #CBD5E1; border: 1px solid #2D334A;">🏷️ {ctype}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 0.9rem; font-weight: bold; color:#94A3B8;">Popularity Level</span>
                                <h3 style="margin:0; color:{border_color};">⭐ {st.session_state.popularity[name]}</h3>
                            </div>
                        </div>
                        <p style="margin: 10px 0 15px 0; color: #CBD5E1;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                
                b1, b2, b3 = st.columns([1, 1.5, 1])
                with b1:
                    if st.session_state.joined[name]:
                        if st.button(f"🔴 Leave Circle", key="lv_"+name, use_container_width=True):
                            st.session_state.popularity[name] = max(0, st.session_state.popularity[name] - 1)
                            st.session_state.joined[name] = False
                            st.rerun()
                    else:
                        if st.button(f"🟢 Join Circle", key="jn_"+name, type="primary", use_container_width=True):
                            st.session_state.popularity[name] += 1
                            st.session_state.joined[name] = True
                            add_notification(f"{st.session_state.user} officially joined the {name} circle!")
                            st.rerun()
                with b2:
                    if name in tournaments:
                        st.markdown(f"<div style='background-color:#161925; color:#F1F5F9; padding:6px; border-radius:10px; text-align:center; font-weight:bold; border:1px solid #2D334A;'>{tournaments[name]}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='text-align:center; margin-top:8px; color:#64748B; font-style:italic;'>📋 Regular scheduling only</p>", unsafe_allow_html=True)
                with b3:
                    is_fav = name in st.session_state.favorites
                    fav_label = "💝 Bookmarked" if is_fav else "🤍 Save to Watchlist"
                    if st.button(fav_label, key="fv_"+name, use_container_width=True):
                        if is_fav: st.session_state.favorites.remove(name)
                        else: st.session_state.favorites.append(name)
                        st.rerun()
                st.write("")

    # ---------------- 🎯 SQUAD MATCHMAKER (ACTIVITY BOARD) ----------------
    elif menu == "🎯 Squad Matchmaker":
        st.title("🎯 Squad Matchmaker & Ride-Share Board")
        st.write("Need numbers for a pickup game, study runs, or looking to catch/offer a lift to campus? Drop a card below!")
        
        with st.expander("✨ Post a New Coordination / Meetup / Carpool Card"):
            with st.form("new_activity", clear_on_submit=True):
                t_type = st.radio("Card Classification", ["Club Match/Study Run 🎯", "Campus Carpool/Ride-Share 🚗"], horizontal=True)
                t_title = st.text_input("📝 Card Title / Objective", placeholder="e.g., Driving from Subang Jaya / Split Court Run")
                t_club = st.selectbox("Associated Hub Circle Focus", list(clubs.keys()))
                t_time = st.text_input("🕒 Date, Time & Pickup/Meetup Spot", placeholder="e.g., Wed morning 8:30 AM / Complex Court 3")
                t_desc = st.text_area("🗒️ Extra logistics info for the squad", placeholder="e.g., 3 empty passenger slots available, hitch a ride!")
                
                if st.form_submit_button("Launch Event 🚀", type="primary"):
                    if t_title.strip() and t_time.strip():
                        card_kind = "Carpool" if "Carpool" in t_type else "Club Match"
                        st.session_state.user_activities.append({
                            "id": len(st.session_state.user_activities) + 1,
                            "type": card_kind,
                            "host": st.session_state.user,
                            "club": t_club,
                            "title": t_title.strip(),
                            "details": t_desc.strip(),
                            "time": t_time.strip(),
                            "attendees": [st.session_state.user]
                        })
                        add_notification(f"{st.session_state.user} created a new {card_kind}: '{t_title.strip()}'")
                        st.rerun()

        st.write("")
        
        f_tab1, f_tab2 = st.tabs(["🎯 All Club Run Activities", "🚗 Live Campus Carpools"])
        
        with f_tab1:
            for act in reversed(st.session_state.user_activities):
                if act.get("type", "Club Match") == "Club Match":
                    with st.container(border=True):
                        col_i, col_a = st.columns([3, 1])
                        with col_i:
                            st.markdown(f"### {act['title']}")
                            st.markdown(f"📂 Circle: **{act['club']}** | 👑 Host: ` {act['host']} `")
                            st.markdown(f"🕒 **Schedule:** {act['time']}")
                            if act['details']: st.info(act['details'])
                            st.markdown(f"👥 **Current Roster ({len(act['attendees'])}):** {', '.join([f'<b>{u}</b>' for u in act['attendees']])}", unsafe_allow_html=True)
                        with col_a:
                            st.write("")
                            if st.session_state.user in act["attendees"]:
                                if act["host"] == st.session_state.user:
                                    if st.button("🗑️ Scrap Event", key=f"scrp_{act['id']}", use_container_width=True):
                                        st.session_state.user_activities.remove(act)
                                        st.rerun()
                                else:
                                    if st.button("❌ Leave Squad", key=f"lv_sq_{act['id']}", use_container_width=True):
                                        act["attendees"].remove(st.session_state.user)
                                        st.rerun()
                            else:
                                if st.button("👟 Hop In!", key=f"hop_{act['id']}", type="primary", use_container_width=True):
                                    act["attendees"].append(st.session_state.user)
                                    add_notification(f"{st.session_state.user} joined squad: {act['title']}")
                                    st.rerun()

        with f_tab2:
            carpools = [a for a in st.session_state.user_activities if a.get("type") == "Carpool"]
            if not carpools:
                st.caption("No open student carpool paths are listed right now. Post one above!")
            for act in reversed(carpools):
                with st.container(border=True):
                    col_i, col_a = st.columns([3, 1])
                    with col_i:
                        st.markdown(f"### 🚗 {act['title']}")
                        st.markdown(f"📍 Route Core: **{act['club']} Hub Path** | 🛠️ Driver: ` {act['host']} `")
                        st.markdown(f"🕒 **Departure Coordinates:** {act['time']}")
                        if act['details']: st.warning(act['details'])
                        st.markdown(f"Passengers Buckled In ({len(act['attendees'])}): {', '.join([f'<b>{u}</b>' for u in act['attendees']])}", unsafe_allow_html=True)
                    with col_a:
                        st.write("")
                        if st.session_state.user in act["attendees"]:
                            if act["host"] == st.session_state.user:
                                if st.button("🗑️ Close Carpool", key=f"c_scrp_{act['id']}", use_container_width=True):
                                    st.session_state.user_activities.remove(act)
                                    st.rerun()
                            else:
                                if st.button("❌ Exit Carpool", key=f"c_lv_{act['id']}", use_container_width=True):
                                    act["attendees"].remove(st.session_state.user)
                                    st.rerun()
                        else:
                            if st.button("🛋️ Request Seat", key=f"c_hop_{act['id']}", type="primary", use_container_width=True):
                                act["attendees"].append(st.session_state.user)
                                add_notification(f"{st.session_state.user} booked a seat in {act['host']}'s carpool!")
                                st.rerun()

    # ---------------- 🛍️ MARKETPLACE & DIRECT PEER CHATS ----------------
    elif menu == "🛍️ Peer Marketplace & Chat":
        st.title("🛍️ Club-Specific Marketplace & Student Chat Room")
        st.write("Post gear specific to campus clubs, negotiate prices, or arrange immediate swap transactions with local peers.")
        st.write("")
        
        m_col, c_col = st.columns([1.6, 1.1])
        
        with m_col:
            st.markdown("### 🛒 Open Campus Gear Listings")
            
            with st.expander("🎒 List a New Gear for Trade / Sale"):
                with st.form("new_deal", clear_on_submit=True):
                    d_item = st.text_input("🎒 Item Title", placeholder="e.g., Yonex Astrox 99 Badminton Racket")
                    d_club = st.selectbox("Associated Club Circle", list(clubs.keys()))
                    d_price = st.text_input("💰 Price or Requested Trade item", placeholder="e.g., RM 150 / Swap with Basketball")
                    d_cond = st.selectbox("📊 Quality Metric", ["Brand New (Sealed)", "Like New (Pre-loved)", "Fair Condition", "Well Utilized"])
                    d_notes = st.text_area("🗒️ Description & Preferred Meetup Spot")
                    
                    if st.form_submit_button("List on Board 📦", type="primary"):
                        if d_item.strip() and d_price.strip():
                            st.session_state.marketplace_deals.append({
                                "id": len(st.session_state.marketplace_deals) + 1,
                                "seller": st.session_state.user,
                                "item": d_item.strip(),
                                "club_tag": d_club,
                                "price": d_price.strip(),
                                "condition": d_cond,
                                "details": d_notes.strip()
                            })
                            add_notification(f"Marketplace: {st.session_state.user} listed '{d_item.strip()}' for {d_price.strip()}!")
                            st.rerun()
            
            filter_club = st.selectbox("🔍 Filter items by specific Club Circle:", ["All Campus Gear"] + list(clubs.keys()))
            
            if not st.session_state.marketplace_deals:
                st.caption("No open gear trades listed on the campus board yet.")
            else:
                displayed_any = False
                for deal in reversed(st.session_state.marketplace_deals):
                    if filter_club != "All Campus Gear" and deal.get("club_tag") != filter_club:
                        continue
                        
                    displayed_any = True
                    with st.container(border=True):
                        dl, dr = st.columns([3, 1.2])
                        with dl:
                            st.markdown(f"#### {deal['item']}")
                            st.markdown(f"<span style='background-color:#161925; color:#818CF8; padding:4px 10px; border-radius:8px; font-size:0.8rem; font-weight:bold; border: 1px solid #2D334A;'>🎯 Assigned: {deal.get('club_tag', 'General')}</span>", unsafe_allow_html=True)
                            st.write("")
                            st.markdown(f"💰 Value: **{deal['price']}** | ⭐ Quality: `{deal['condition']}`")
                            st.caption(f"🎒 Posted by student: **{deal['seller']}**")
                            if deal['details']: st.write(deal['details'])
                        with dr:
                            st.write("")
                            if deal['seller'] == st.session_state.user:
                                if st.button("🗑️ Take Down", key=f"td_{deal['id']}", use_container_width=True):
                                    st.session_state.marketplace_deals.remove(deal)
                                    st.rerun()
                            else:
                                if st.button("💬 Chat 🤝", key=f"ch_{deal['id']}", type="primary", use_container_width=True):
                                    st.session_state.active_chat_partner = deal['seller']
                                    st.rerun()
                if not displayed_any:
                    st.info(f"No listings available specifically for {filter_club} right now.")

        with c_col:
            st.markdown("### 💬 Direct Student Messenger")
            
            all_users = set(d["seller"] for d in st.session_state.marketplace_deals if d["seller"] != st.session_state.user)
            all_users.update(act["host"] for act in st.session_state.user_activities if act["host"] != st.session_state.user)
            
            partner = st.selectbox(
                "Pick a student connection thread:",
                options=["Select Student"] + list(all_users),
                index=list(all_users).index(st.session_state.active_chat_partner) + 1 if st.session_state.active_chat_partner in all_users else 0
            )
            
            if partner != "Select Student":
                st.session_state.active_chat_partner = partner
                ck = get_chat_key(st.session_state.user, partner)
                if ck not in st.session_state.chat_messages: 
                    st.session_state.chat_messages[ck] = []
                
                with st.container(border=True):
                    st.markdown(f"🌟 **Conversation with: {partner}**")
                    st.divider()
                    if not st.session_state.chat_messages[ck]:
                        st.caption("No text history with this user.")
                    else:
                        for m in st.session_state.chat_messages[ck]:
                            if m["sender"] == st.session_state.user:
                                st.markdown(f"<div style='text-align: right; margin: 4px 0;'><span style='background-color:#4338CA; color:white; padding:6px 12px; border-radius:12px; display:inline-block;'><b>You:</b> {m['text']}</span></div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='text-align: left; margin: 4px 0;'><span style='background-color:#161925; color:#F1F5F9; padding:6px 12px; border-radius:12px; display:inline-block;'><b>{partner}:</b> {m['text']}</span></div>", unsafe_allow_html=True)
                
                with st.form("send_chat_msg", clear_on_submit=True):
                    msg_in = st.text_input("Type a message to peer...", placeholder="Hey! Interested in your item...")
                    if st.form_submit_button("Send 📩", use_container_width=True):
                        if msg_in.strip():
                            st.session_state.chat_messages[ck].append({"sender": st.session_state.user, "text": msg_in.strip()})
                            st.rerun()

    # ---------------- 🏆 LEAGUES & CUPS ----------------
    elif menu == "🏆 Leagues & Cups":
        st.title("🏆 Active Leagues & Multiplier Events")
        st.write("Register below to join official university club tournament brackets.")
        
        for club, tour in tournaments.items():
            with st.container(border=True):
                t1, t2 = st.columns([2, 1])
                with t1:
                    st.markdown(f"### {tour}")
                    st.caption(f"🎖️ Main Bracket Organizer: **{club}**")
                with t2:
                    tk = f"tour_reg_{club}"
                    if tk not in st.session_state: 
                        st.session_state[tk] = False
                    
                    if st.session_state[tk]:
                        st.markdown("<div style='background-color:#1E1B4B; color:#C7D2FE; padding:8px; border-radius:10px; font-weight:bold; text-align:center; border: 1px solid #4338CA;'>✅ Slot Locked In!</div>", unsafe_allow_html=True)
                    else:
                        if st.button("Secure Roster Slot 🎖️", key="bt_"+club, type="primary", use_container_width=True):
                            st.session_state[tk] = True
                            if club in st.session_state.popularity:
                                st.session_state.popularity[club] += 2
                            add_notification(f"{st.session_state.user} locked in a tournament slot for {club}!")
                            st.rerun()

    # ---------------- ✨ MY WATCHLIST & SCHEDULE ----------------
    elif menu == "✨ My Watchlist & Schedule":
        st.title("✨ My Personal Lounge Dashboard")
        st.write("Track your saved circles and view your upcoming aggregated calendar schedule metrics.")
        st.write("")
        
        tab_sch, tab_wl = st.tabs(["📅 My Personal Schedule", "💝 Saved Watchlist Circles"])
        
        with tab_sch:
            st.markdown("### 🕒 Your Upcoming Campus Commitments")
            my_agenda_events = []
            
            for club, tour in tournaments.items():
                if st.session_state.get(f"tour_reg_{club}"):
                    my_agenda_events.append({"type": "Tournament Bracket 🏆", "title": tour, "time": "See Tournament Bracket Day Details", "focus": club})
            
            for act in st.session_state.user_activities:
                if st.session_state.user in act["attendees"]:
                    kind = "Squad Run Match 🎯" if act.get("type") == "Club Match" else "Campus Carpool 🚗"
                    my_agenda_events.append({"type": kind, "title": act["title"], "time": act["time"], "focus": act["club"]})
            
            if not my_agenda_events:
                st.info("You haven't locked down any activity commitments or tournament slots yet. Join something in the tabs!")
            else:
                for evt in my_agenda_events:
                    st.markdown(
                        f"""
                        <div style="background-color: #161925; border: 1px solid #2D334A; padding: 15px; border-radius: 12px; margin-bottom: 10px;">
                            <span style="background: #312E81; color: #C7D2FE; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold;">{evt['type']}</span>
                            <h4 style="margin: 8px 0 4px 0;">{evt['title']}</h4>
                            <p style="margin: 0; font-size: 0.85rem; color: #94A3B8;">🕒 Time/Location: <b>{evt['time']}</b> | Hub: {evt['focus']}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
        
        with tab_wl:
            if not st.session_state.favorites:
                st.info("Your watchlist is empty right now! Head over to the 📣 **Club Fair** directory to bookmark clubs.")
            else:
                for fav_name in st.session_state.favorites:
                    if fav_name in clubs:
                        ctype, desc = clubs[fav_name]
                        with st.container(border=True):
                            wl_c1, wl_c2 = st.columns([3, 1])
                            with wl_c1:
                                st.markdown(f"### {fav_name}")
                                st.caption(f"🏷️ Category: **{ctype}** | ⭐ Current Popularity: `{st.session_state.popularity[fav_name]}`")
                                st.write(desc)
                            with wl_c2:
                                st.write("")
                                if st.button("❌ Remove Bookmark", key="rm_fav_"+fav_name, use_container_width=True):
                                    st.session_state.favorites.remove(fav_name)
                                    st.rerun()

    # ---------------- 📊 POPULARITY STANDINGS ----------------
    elif menu == "📊 Popularity Standings":
        st.title("📊 Public Club Popularity Standings Leaderboard")
        st.write("Live visual tracking of community coordination metrics based on student engagement parameters.")
        st.write("")
        
        chart_data = pd.DataFrame({
            "Club Community Name": list(st.session_state.popularity.keys()),
            "Popularity Score Rating": list(st.session_state.popularity.values())
        }).sort_values(by="Popularity Score Rating", ascending=False)
        
        st.bar_chart(data=chart_data, x="Club Community Name", y="Popularity Score Rating", color="#818CF8")
        
        st.markdown("### 🏆 Raw Leaderboard Directory Table Data")
        st.dataframe(chart_data, use_container_width=True, hide_index=True)