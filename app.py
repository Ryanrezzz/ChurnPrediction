import streamlit as st
import joblib
import numpy as np
import pandas as pd


st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1.25rem;
    }
    
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .segment-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-champion {
        background: #ECFDF5;
        color: #059669;
    }
    
    .badge-loyal {
        background: #EFF6FF;
        color: #2563EB;
    }
    
    .badge-at-risk {
        background: #FFF7ED;
        color: #EA580C;
    }
    
    .badge-hibernating {
        background: #FEF2F2;
        color: #DC2626;
    }
    
    .badge-lost {
        background: #F3F4F6;
        color: #6B7280;
    }
    
    .segment-description {
        color: #4B5563;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    .churn-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .churn-value {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .churn-low { color: #059669; }
    .churn-medium { color: #EA580C; }
    .churn-high { color: #DC2626; }
    
    .churn-description {
        color: #4B5563;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    .action-box {
        background: #F3F4F6;
        border-radius: 12px;
        padding: 1.25rem;
        border-left: 3px solid #3B82F6;
    }
    
    .action-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #3B82F6;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .action-text {
        color: #1F2937;
        font-size: 0.95rem;
        font-weight: 500;
    }
    

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    

    .stNumberInput label p,
    .stSelectbox label p,
    .stTextInput label p,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    

    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 0.5rem 0.75rem;
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    

    .stButton > button {
        background: #1a1a2e;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 0.95rem;
        width: 100%;
        margin-top: 1rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #2d2d44;
        transform: translateY(-1px);
    }
    
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    try:
        segment_model = joblib.load('segment_model.pkl')
        churn_model = joblib.load('churn_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return segment_model, churn_model, scaler
    except:
        return None, None, None

segment_model, churn_model, scaler = load_models()


SEGMENT_INFO = {
    0: {"name": "Inactive Customer", "class": "lost"},
    1: {"name": "Frequent Shopper", "class": "champion"},
    2: {"name": "Active Customer", "class": "champion"},
    3: {"name": "Lost Customer", "class": "lost"},
    4: {"name": "Top Customer", "class": "champion"},
    5: {"name": "Regular Buyer", "class": "loyal"},
    6: {"name": "Big Spender", "class": "at-risk"}
}


st.markdown('<p class="main-header">ChurnRadar</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Detect churn risk and segment customers instantly</p>', unsafe_allow_html=True)


st.markdown('<p class="section-title">Customer Profile</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    days_since = st.number_input("Days since last purchase", min_value=0, max_value=1000, value=30)
    total_orders = st.number_input("Total orders", min_value=1, max_value=500, value=10)
    total_spent = st.number_input("Total spent ($)", min_value=0.0, max_value=50000.0, value=500.0, step=10.0)

with col2:
    age = st.number_input("Customer age", min_value=18, max_value=100, value=35)
    account_age = st.number_input("Account age (days)", min_value=0, max_value=730, value=240)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col3:
    device = st.selectbox("Primary device", ["Mobile", "Desktop", "Tablet"])
    country = st.selectbox("Country", ["Australia", "Brazil", "Canada", "France", "Germany", "India", "Japan", "South Korea", "United Kingdom", "United States"])
    category = st.selectbox("Favorite category", ["Beauty", "Books", "Electronics", "Fashion", "Groceries", "Home & Garden", "Sports", "Toys"])
    is_premium = st.selectbox("Premium member", ["No", "Yes"])


avg_order = total_spent / total_orders if total_orders > 0 else 0


gender_map = {"Female": 0, "Male": 1, "Other": 2}
device_map = {"Desktop": 0, "Mobile": 1, "Tablet": 2}
country_map = {"Australia": 0, "Brazil": 1, "Canada": 2, "France": 3, "Germany": 4, "India": 5, "Japan": 6, "South Korea": 7, "United Kingdom": 8, "United States": 9}
category_map = {"Beauty": 0, "Books": 1, "Electronics": 2, "Fashion": 3, "Groceries": 4, "Home & Garden": 5, "Sports": 6, "Toys": 7}
premium_map = {"No": 0, "Yes": 1}


analyze = st.button("Analyze Customer")


if analyze:
    if segment_model is None:
        st.error("Models not found. Please ensure segment_model.pkl, churn_model.pkl, and scaler.pkl are in the same directory.")
    else:
        churn_input = np.array([[
            days_since,
            account_age,
            country_map[country],
            age,
            gender_map[gender],
            device_map[device],
            category_map[category],
            total_orders,
            total_spent,
            avg_order,
            premium_map[is_premium]
        ]])
        
        churn_prob = churn_model.predict_proba(churn_input)[0][1] * 100
        
        segment_input = np.array([[
            days_since,
            account_age,
            country_map[country],
            age,
            gender_map[gender],
            device_map[device],
            category_map[category],
            total_orders,
            total_spent,
            avg_order,
            premium_map[is_premium],
            0
        ]])

        
        segment_pred = segment_model.predict(segment_input)[0]
        segment_info = SEGMENT_INFO.get(segment_pred, {"name": "Unknown", "class": "lost"})
        
        if churn_prob < 30:
            churn_class = "churn-low"
            churn_status = "Low"
            churn_desc = "This customer is likely to stay"
        elif churn_prob < 60:
            churn_class = "churn-medium"
            churn_status = "Medium"
            churn_desc = "Some risk of leaving, monitor closely"
        else:
            churn_class = "churn-high"
            churn_status = "High"
            churn_desc = "May leave soon without intervention"
        
        st.markdown('<p class="section-title">📊 Customer Segment — KMeans Clustering</p>', unsafe_allow_html=True)
        st.markdown(f'<span class="segment-badge badge-{segment_info["class"]}">{segment_info["name"]}</span>', unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">⚠️ Churn Risk Prediction — XGBoost</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="churn-value {churn_class}">{churn_prob:.0f}% — {churn_status}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="churn-description">"{churn_desc}"</p>', unsafe_allow_html=True)
