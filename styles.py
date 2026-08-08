# High-Contrast Minimalist Light iOS Theme CSS

IOS_LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Main Background & Root Setup */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #F8FAFC !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
    color: #0F172A !important;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}

[data-testid="stSidebar"] * {
    color: #0F172A !important;
}

/* Universal Typography & High-Contrast Colors */
h1, h2, h3, h4, h5, h6 {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.4px !important;
}

p, span, label, li, td, th {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif !important;
    color: #1E293B !important;
}

/* Form Field Labels & Radio Text */
div[data-testid="stMarkdownContainer"] p {
    color: #0F172A !important;
    font-weight: 600 !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #0F172A !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* High-Contrast Stat Pill Badges */
.badge-blue {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    display: inline-block !important;
    border: 1px solid #BAE6FD !important;
}

.badge-green {
    background-color: #DCFCE7 !important;
    color: #15803D !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    display: inline-block !important;
    border: 1px solid #BBF7D0 !important;
}

.badge-orange {
    background-color: #FFEDD5 !important;
    color: #C2410C !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    display: inline-block !important;
    border: 1px solid #FED7AA !important;
}

.badge-purple {
    background-color: #F3E8FF !important;
    color: #6B21A8 !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    display: inline-block !important;
    border: 1px solid #E9D5FF !important;
}

/* Custom Cards */
.profile-banner {
    background: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 24px !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
    margin-bottom: 24px !important;
}

.ios-sub-box {
    background: #F1F5F9 !important;
    border-radius: 14px !important;
    padding: 16px 18px !important;
    border: 1px solid #E2E8F0 !important;
    margin-bottom: 12px !important;
}

/* Progress Bar */
.ios-progress-bg {
    background: #E2E8F0 !important;
    border-radius: 10px !important;
    height: 12px !important;
    width: 100% !important;
    overflow: hidden !important;
    margin-top: 6px !important;
}

.ios-progress-fill {
    background: linear-gradient(90deg, #0284C7 0%, #16A34A 100%) !important;
    height: 100% !important;
    border-radius: 10px !important;
}

/* Streamlit Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
}

/* High-Contrast Inputs & Text Areas */
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    color: #0F172A !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}

div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
    border: 1.5px solid #94A3B8 !important;
}

div[data-baseweb="input"] > div:focus-within, div[data-baseweb="textarea"] > div:focus-within {
    border-color: #0284C7 !important;
    box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2) !important;
}

/* Primary Action Buttons */
div.stButton > button {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
}

div.stButton > button:hover {
    background-color: #0369A1 !important;
}

/* Tabs */
button[data-baseweb="tab"] p {
    font-weight: 700 !important;
    font-size: 1rem !important;
    color: #475569 !important;
}

button[aria-selected="true"][data-baseweb="tab"] p {
    color: #0284C7 !important;
}

/* Crisp Black Outline Stroke Checkboxes & Radio Circles */
div[data-baseweb="checkbox"] span:first-child,
div[data-baseweb="checkbox"] div:first-child {
    background-color: #FFFFFF !important;
    border: 2px solid #000000 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
}

div[data-baseweb="checkbox"] input:checked + div,
div[data-baseweb="checkbox"] input:checked + span {
    background-color: #000000 !important;
    border: 2px solid #000000 !important;
}

div[data-baseweb="radio"] span:first-child,
div[data-baseweb="radio"] div:first-child {
    background-color: #FFFFFF !important;
    border: 2px solid #000000 !important;
    border-radius: 50% !important;
}

div[data-baseweb="radio"] input:checked + div,
div[data-baseweb="radio"] input:checked + span {
    border: 2px solid #000000 !important;
    background-color: #000000 !important;
}

div[data-testid="stCheckbox"] label p {
    color: #0F172A !important;
    font-weight: 700 !important;
}

/* Hide Streamlit Menu/Footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

def inject_styles():
    import streamlit as st
    st.markdown(IOS_LIGHT_CSS, unsafe_allow_html=True)
