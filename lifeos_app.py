import streamlit as st
import os

# Set page config for wide, clean, full-screen viewport (v1.1.3)
st.set_page_config(
    page_title="IRIS QUEST — RPG Productivity",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit components and force iframe to take full screen height
st.markdown("""
<style>
    /* Hide Streamlit header, footer, and menu */
    [data-testid="stHeader"], footer, #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Remove padding around the main block container */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        height: 100vh !important;
    }
    
    /* Make the iframe container take up full view height */
    div[data-testid="stHtml"] {
        width: 100% !important;
        height: 100vh !important;
    }
    
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

def load_bundled_html():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "iris-quest", "index.html")
    css_path = os.path.join(base_dir, "iris-quest", "styles.css")
    js_path = os.path.join(base_dir, "iris-quest", "app.js")
    
    # Read core files
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
        
    # Replace relative links with embedded content
    # Remove stylesheet link tag and inject inline style tag
    css_tag = '<style>\n' + css + '\n</style>'
    html = html.replace('<link rel="stylesheet" href="styles.css" />', css_tag)
    html = html.replace('<link rel="stylesheet" href="styles.css">', css_tag)
    
    # Remove app.js src script tag and inject inline script tag
    js_tag = '<script type="text/babel">\n' + js + '\n</script>'
    html = html.replace('<script type="text/babel" src="app.js"></script>', js_tag)
    html = html.replace('<script type="text/babel" src="app.js"></script>', js_tag)
    
    return html

def main():
    try:
        bundled_html = load_bundled_html()
        # Serve the React application inside Streamlit's iframe
        st.components.v1.html(bundled_html, height=1200, scrolling=True)
    except Exception as e:
        st.error(f"Error loading React bundle: {e}")

if __name__ == "__main__":
    main()
