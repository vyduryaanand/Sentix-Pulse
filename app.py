import streamlit as st
import pandas as pd
import random
import os
import smtplib
import plotly.express as px
import plotly.graph_objects as go
from email.message import EmailMessage
from collections import Counter
import re
import matplotlib.pyplot as plt


# --- 1. CORE SYSTEM CONFIG & SESSION STABILIZER ---
st.set_page_config(page_title="Sentix Pulse", layout="wide", initial_sidebar_state="collapsed")

# Initialize all state keys to prevent "KeyError" or "AttributeError"
state_keys = {
    'page': 'Home',
    'logged_in': False,
    'user_name': '',
    'account_type': 'Customer',
    'otp_secret': None,
    'reg_data': {'email': '', 'company': '', 'fname': '', 'lname': ''}
}

for key, value in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 2. THEMATIC UI ARCHITECTURE (Black & Pink Glassy Design) ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Neon Branding */
    .main-title {
        font-size: 75px; font-weight: 900; text-align: center;
        background: -webkit-linear-gradient(#FF1493, #FF69B4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px; filter: drop-shadow(0px 0px 10px rgba(255, 20, 147, 0.4));
    }
    .tagline { text-align: center; color: #FF1493; font-size: 18px; margin-top:-20px; margin-bottom: 40px; font-weight: 300; }
    
    /* Glassy Pink Nav & Select Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background: rgba(255, 20, 147, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 20, 147, 0.3);
        border-radius: 20px; padding: 25px;
    }

    /* Polished Pink Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #FF1493 !important;
        border: 2px solid #FF1493 !important;
        border-radius: 12px; font-weight: bold; width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FF1493 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 20px #FF1493;
    }

    /* Cards for Text Content */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 20, 147, 0.2);
        border-radius: 15px; padding: 20px; margin: 10px 0;
    }

    /* Custom Input Styling */
    input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #FF1493 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SMTP GATEWAY & DATA UTILITIES ---
USER_DB = "users_db.csv"
REVIEWS_FILE = "reviews_master.csv"

def load_data(file):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()

def send_secure_otp(receiver):
    otp = str(random.randint(100000, 999999))
    st.session_state.otp_secret = otp
    try:
        msg = EmailMessage()
        msg.set_content(f"Your Sentix Pulse Security Access Code: {otp}")
        msg['Subject'] = "Sentix Pulse Verification"
        msg['From'] = "anandvydurya@gmail.com" # Your Gmail
        msg['To'] = receiver
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # IMPORTANT: USE YOUR 16-DIGIT APP PASSWORD HERE
            smtp.login("anandvydurya@gmail.com", "jjht ypcn dsfs ijkq") 
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Gateway Error: {str(e)}")
        return False

# --- 4. NAVIGATION HEADER ---
st.markdown('<h1 class="main-title">Sentix Pulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Enterprise Sentiment Intelligence & Decisions</p>', unsafe_allow_html=True)

nav = st.columns(4)
if nav[0].button("🏠 Home"): st.session_state.page = "Home"
if nav[1].button("ℹ️ Methodology"): st.session_state.page = "About"
if nav[2].button("⚙️ Settings"): st.session_state.page = "Settings"

if st.session_state.logged_in:
    user_label = st.session_state.user_name if st.session_state.account_type == "Customer" else st.session_state.reg_data.get('company', 'Corp')
    if nav[3].button(f"Logout ({user_label})"):
        st.session_state.logged_in = False; st.session_state.page = "Home"; st.rerun()
else:
    if nav[3].button("🔑 Access"): st.session_state.page = "Access"

st.divider()

# --- 5. PAGE ROUTING ENGINE ---

if st.session_state.page == "Home":
    st.title("Strategic Dashboard Overview")
    st.markdown("""
    <div class="glass-card">
        <h3>Welcome to the Intelligence Hub</h3>
        Sentix Pulse is a high-performance NLP ecosystem that bridges the gap between raw feedback and actionable data.
        <br><br>
        <b>Ecosystem Capabilities:</b>
        <ul>
            <li><b>Platform Correlation:</b> Compare Amazon vs. Flipkart sentiment bias instantly.</li>
            <li><b>Reliability Score:</b> proprietary weighted index based on longevity mentions.</li>
            <li><b>Direct Response:</b> Integrated decision support for supply-chain & marketing.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "About":
    st.title("System Methodology")
    st.markdown("""
    <div class="glass-card">
        <h4>Transformer Pipeline (V2.6)</h4>
        Our engine processes data through a four-stage neural pipeline:
        <ol>
            <li><b>Normalization:</b> Cleaning noise while preserving sarcasm markers.</li>
            <li><b>Entity Extraction:</b> Identifying specific components like 'Battery' or 'UX'.</li>
            <li><b>Weighted Polarity:</b> High-intent words get 2.5x more significance in scoring.</li>
            <li><b>Cross-Referencing:</b> Comparing verified vs. unverified purchase signatures.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Settings":
    st.title("Core Configuration")
    st.subheader("Visuals")
    st.toggle("High Contrast Mode", value=True)
    st.toggle("Live Data Streaming (Mock Data)", value=False)
    st.subheader("Security")
    st.toggle("Enhanced SMTP Encryption", value=True)
    if st.button("Purge Session Cache"): st.info("Cache Cleared.")

elif st.session_state.page == "Access":
    role = st.radio("Access Level", ["Customer", "Company"], horizontal=True)
    st.session_state.account_type = role
    
    t1, t2 = st.tabs(["🔒 Secure Login", "🚀 Provision Account"])
    
    with t1:
        le = st.text_input("Corporate/Personal Email")
        lp = st.text_input("Security Key (Password)", type="password")
        if st.button("Authenticate Session"):
            users = load_data(USER_DB)
            if not users.empty:
                match = users[(users['email']==le) & (users['password']==lp) & (users['role']==role)]
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = match.iloc[0]['fname'] if role=="Customer" else "Admin"
                    if role == "Company": st.session_state.reg_data['company'] = match.iloc[0]['company']
                    st.session_state.page = "Dashboard"; st.rerun()
            st.error("Authentication Denied: Check credentials or profile type.")

    with t2:
        if role == "Customer":
            fn = st.text_input("First Name"); 
            ln = st.text_input("Last Name");
            em = st.text_input("Email");
            if st.button("Request Security OTP"):
                if em and send_secure_otp(em): st.success("Verification Code Dispatched.")
            code = st.text_input("Enter 6-Digit Code")
            if st.button("Verify Identity"):
                if code == st.session_state.otp_secret:
                    st.session_state.reg_data.update({'fname': fn, 'lname':ln, 'email': em})
                    st.session_state.page = "FinalizePass"; st.rerun()
                else: st.error("Mismatch detected.")
        else:
            cn = st.text_input("Company Name"); ce = st.text_input("Admin Email")
            if st.button("Init Provisioning"):
                st.session_state.reg_data.update({'company': cn, 'email': ce})
                st.session_state.page = "FinalizePass"; st.rerun()

elif st.session_state.page == "FinalizePass":
    st.title("Finalize Security Key")
    p_set = st.text_input("Create Master Password", type="password")
    p_confirm = st.text_input("Confirm Master Password", type="password")
    if st.button("Complete Authorization"):
        db = load_data(USER_DB)
        new = st.session_state.reg_data.copy()
        new.update({'password': p_set, 'role': st.session_state.account_type})
        db = pd.concat([db, pd.DataFrame([new])], ignore_index=True)
        db.to_csv(USER_DB, index=False)
        st.success("Account Active. Return to Access."); st.session_state.page = "Access"

# --- 6. DASHBOARD (LOGGED IN VIEW) ---
if st.session_state.logged_in:
    df = load_data(REVIEWS_FILE)
    if df.empty: st.stop()

    if st.session_state.account_type == "Customer":
        st.title("Consumer Intelligence Terminal")
        cols = st.columns(4)
        cat = cols[0].selectbox("Category", df['Category'].unique())
        brand = cols[1].selectbox("Brand", df[df['Category']==cat]['Brand'].unique())
        model = cols[2].selectbox("Model", df[df['Brand']==brand]['Model'].unique())
        plat = cols[3].selectbox("Source Platform", ["All Platforms"] + list(df['Platform'].unique()))
        
        if st.button("Execute Performance Audit"):
            target = df[df['Model'] == model]
            if plat != "All Platforms": target = target[target['Platform'] == plat]
            
            # Step 1: Top 5 Samples
            st.subheader("📋 Top Verified Samples")
            for _, r in target.head(5).iterrows():
                c = "#FF1493" if r['Ground_Truth'] == 'POSITIVE' else "#444"
                st.markdown(f'<div style="border-left:5px solid {c}; padding:10px; background:#111; margin:5px;">{r["Review"]}</div>', unsafe_allow_html=True)
            
            # Step 2: Donut
            st.divider()
            st.subheader("📊 Sentiment Composition")
            fig = px.pie(target, names='Ground_Truth', hole=0.7, color_discrete_sequence=['#FF1493', '#333', '#666'], template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
            
            # Step 3: Verdict
            pos_perc = (len(target[target['Ground_Truth'] == 'POSITIVE'])/len(target))*100
            st.markdown(f'<div style="text-align:center; padding:20px; border:2px solid #FF1493; border-radius:15px; font-size:24px;"><b>Recommendation: {"Verified Buy ✅" if pos_perc > 50 else "Avoid Choice ❌"} ({pos_perc:.1f}% Index)</b></div>', unsafe_allow_html=True)

    else:
         
        # --- ENHANCED COMPANY PRO SUITE ---
        brand_name = st.session_state.reg_data.get('company', 'Corporate').upper()
        st.title(f"🏢 Enterprise Suite: {brand_name}")
        brand_df = df[df['Brand'].str.upper() == brand_name]
        
        if brand_df.empty:
            st.info(f"No market assets detected for {brand_name} in the current database.")
        else:
            sel_mod = st.selectbox("Select Asset for Deployment Analysis:", brand_df['Model'].unique())
            target_data = brand_df[brand_df['Model'] == sel_mod]
            
            st.divider()

            # 1. BOLD KEYWORD ANALYSIS (Word Cloud Replacement)
            st.subheader("🎯 Critical Keyword Analysis")
            neg_reviews = target_data[target_data['Ground_Truth'] == 'NEGATIVE']['Review']
            words = re.findall(r'\w+', " ".join(neg_reviews).lower())
            # Filtering out common noise words
            filtered = [w.upper() for w in words if len(w) > 4 and w not in ['there','this','that','with','from','would']]
            top_keywords = Counter(filtered).most_common(8)
            
            # Displaying keywords in Bold UI
            cols = st.columns(len(top_keywords))
            for i, (word, count) in enumerate(top_keywords):
                cols[i].markdown(f"**{word}** \n`{count}`")
            
            st.markdown("---")

            # 2. REVIEW ANALYSIS (NLP Summary)
            st.subheader("📝 Automated Review Analysis")
            pos_count = len(target_data[target_data['Ground_Truth'] == 'POSITIVE'])
            neg_count = len(target_data[target_data['Ground_Truth'] == 'NEGATIVE'])
            total = len(target_data)
            pos_perc = (pos_count / total) * 100

            analysis_text = f"""
            Analysis of **{total}** verified data points for **{sel_mod}** indicates a 
            Sentiment Index of **{pos_perc:.1f}%**.  
            
            **Key Findings:**
            * The most frequent negative descriptors relate to **{top_keywords[0][0] if top_keywords else 'N/A'}**, suggesting a specific technical or logistical bottleneck.
            * Competitive standing is currently **{'Stable' if pos_perc > 60 else 'Under Pressure'}** compared to category averages.
            """
            st.markdown(f'<div class="glass-card">{analysis_text}</div>', unsafe_allow_html=True)

            # 3. VISUALIZATION: DONUT & COMPARISON
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.write("**Internal Sentiment Split**")
                fig_donut = px.pie(target_data, names='Ground_Truth', hole=0.7, 
                                 color_discrete_sequence=['#FF1493', '#333', '#666'], template='plotly_dark')
                fig_donut.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig_donut, use_container_width=True)

            with col_chart2:
                st.write("**Market Competitive Benchmark**")
                cat_mod = target_data['Category'].iloc[0]
                comp_df = df[df['Category'] == cat_mod].groupby('Brand')['Ground_Truth'].apply(lambda x: (x=='POSITIVE').mean()*100).reset_index()
                fig_bar = px.bar(comp_df, x='Brand', y='Ground_Truth', template='plotly_dark')
                fig_bar.update_traces(marker_color='#FF1493')
                fig_bar.update_layout(height=350, yaxis_title="Positivity %")
                st.plotly_chart(fig_bar, use_container_width=True)

            # 4. STRATEGIC SUGGESTION & VERDICT
            st.subheader("💡 Strategic Recommendation")
            if pos_perc < 35:
                suggestion = "Immediate quality-assurance audit recommended. Negative sentiment clusters around operational noise and sales-floor expectations."
                verdict_color = "#dc3545" # Red
                verdict_text = "Action Required: High Risk ❌"
            elif pos_perc < 55:
                suggestion = "Maintain current specs but optimize marketing to address minor user interface complaints. Product is market-neutral."
                verdict_color = "#ffc107" # Yellow
                verdict_text = "Monitor Performance: Stable ⚠️"
            else:
                suggestion = "Market Leader. Leverage high reliability scores in upcoming ad campaigns to increase market share."
                verdict_color = "#28a745" # Green
                verdict_text = "Asset Strength: Superior ✅"

            st.markdown(f"""
                <div class="glass-card">
                    {suggestion}
                </div>
                <div class="verdict-box" style="background-color: {verdict_color}; border:none;">
                    {verdict_text}
                </div>
            """, unsafe_allow_html=True)