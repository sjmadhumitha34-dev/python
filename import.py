import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="RFM Customer Segment Calculator",
    page_icon="📊",
    layout="wide"
)

# Title & Intro
st.title("📊 Interactive RFM Customer Segment Calculator")
st.markdown("Enter transaction metrics below to compute RFM scores and determine customer segments.")

# Sidebar Controls for Input
st.sidebar.header("📥 Customer Metrics Input")

recency_input = st.sidebar.number_input(
    "Recency (Days since last purchase)", 
    min_value=1, max_value=365, value=25, step=1,
    help="Fewer days indicate higher engagement."
)

frequency_input = st.sidebar.number_input(
    "Frequency (Total number of orders)", 
    min_value=1, max_value=100, value=8, step=1,
    help="Higher order counts indicate strong loyalty."
)

monetary_input = st.sidebar.number_input(
    "Monetary Value ($ Total Spend)", 
    min_value=1.0, max_value=50000.0, value=1250.0, step=50.0,
    help="Higher total spend indicates greater customer value."
)

# Scoring Logic (1 to 5 scale)
def calculate_r_score(r):
    if r <= 30: return 5
    elif r <= 60: return 4
    elif r <= 90: return 3
    elif r <= 180: return 2
    else: return 1

def calculate_f_score(f):
    if f >= 12: return 5
    elif f >= 7: return 4
    elif f >= 4: return 3
    elif f >= 2: return 2
    else: return 1

def calculate_m_score(m):
    if m >= 2000: return 5
    elif m >= 1000: return 4
    elif m >= 500: return 3
    elif m >= 150: return 2
    else: return 1

# Compute Scores
r_score = calculate_r_score(recency_input)
f_score = calculate_f_score(frequency_input)
m_score = calculate_m_score(monetary_input)
rfm_combined = f"{r_score}{f_score}{m_score}"

# Segment Mapping Function
def assign_segment(r, f, m):
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions / VIPs", "🏆", "Reward loyalty, provide exclusive early access, and offer premium VIP support."
    elif r >= 3 and f >= 3:
        return "Loyal Customers", "💙", "Upsell higher-value products, recommend subscriptions, and encourage reviews."
    elif r >= 4 and f <= 2:
        return "New / Promising", "🌱", "Send welcoming onboarding emails, offer introductory discounts, and provide product guides."
    elif r <= 2 and f >= 3:
        return "At-Risk / Need Attention", "⚠️", "Send personalized re-engagement offers, win-back emails, and satisfaction surveys."
    elif r <= 2 and f <= 2:
        return "Hibernating / Lost", "💤", "Run aggressive discount campaigns or minimize direct ad spend on this segment."
    else:
        return "Potential Loyalists", "📈", "Offer membership programs and recommend complementary items."

segment, icon, strategy = assign_segment(r_score, f_score, m_score)

# Display Metrics & Scores
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Recency Score", f"{r_score} / 5", f"{recency_input} Days")
with col2:
    st.metric("Frequency Score", f"{f_score} / 5", f"{frequency_input} Orders")
with col3:
    st.metric("Monetary Score", f"{m_score} / 5", f"${monetary_input:,.2f}")
with col4:
    st.metric("Combined RFM Code", rfm_combined)

st.markdown("---")

# Layout: Segment Diagnosis & Radar Plot
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader(f"Segment Designation: {icon} {segment}")
    st.info(f"**Recommended Strategy:**\n\n{strategy}")
    
    # Score Breakdown Table
    score_df = pd.DataFrame({
        "Metric": ["Recency (R)", "Frequency (F)", "Monetary (M)"],
        "Raw Value": [f"{recency_input} days", f"{frequency_input} orders", f"${monetary_input:,.2f}"],
        "Score": [r_score, f_score, m_score]
    })
    st.table(score_df)

with right_col:
    st.subheader("RFM Score Radar Profile")
    
    fig = go.Figure(data=go.Scatterpolar(
        r=[r_score, f_score, m_score],
        theta=['Recency', 'Frequency', 'Monetary'],
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.4)',
        line_color='rgb(31, 119, 180)',
        marker=dict(size=10)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=30, b=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)
