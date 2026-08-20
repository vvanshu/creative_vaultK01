import streamlit as st
import os

# Set page config for wide, clean, full-screen viewport (v1.2.3)
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
    
    /* Lock the main Streamlit container to 100vh and hide its overflow */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        overflow: hidden !important;
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove padding and margin from the Streamlit vertical block and elements */
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlock"] > div {
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
        height: 100vh !important;
        width: 100% !important;
    }
    
    /* Remove padding around the main block container */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Make the iframe container take up full view height */
    div[data-testid="stHtml"], div.element-container {
        width: 100% !important;
        height: 100vh !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }
    
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

def load_bundled_html():
    import base64
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "iris-quest", "index.html")
    css_path = os.path.join(base_dir, "iris-quest", "styles.css")
    js_path = os.path.join(base_dir, "iris-quest", "app.js")
    manifest_path = os.path.join(base_dir, "iris-quest", "manifest.json")
    
    # Read core files
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = f.read()
        
    import re
    # Replace relative links with embedded content
    # Remove stylesheet link tag and inject inline style tag
    css_tag = '<style>\n' + css + '\n</style>'
    html = re.sub(r'<link\s+rel=["\']stylesheet["\']\s+href=["\']styles\.css(?:\?[^"\']*)?["\']\s*/?>', lambda _: css_tag, html)
    html = html.replace('<link rel="stylesheet" href="styles.css" />', css_tag)
    html = html.replace('<link rel="stylesheet" href="styles.css">', css_tag)
    
    # Remove app.js src script tag and inject inline script tag
    js_tag = '<script type="text/babel">\n' + js + '\n</script>'
    html = re.sub(r'<script\s+type=["\']text/babel["\']\s+src=["\']app\.js(?:\?[^"\']*)?["\']\s*></script>', lambda _: js_tag, html)
    html = html.replace('<script type="text/babel" src="app.js"></script>', js_tag)
    
    # Embed manifest.json as base64 data URI to support PWA standalone mode inside Streamlit iframes
    manifest_base64 = base64.b64encode(manifest.encode("utf-8")).decode("utf-8")
    manifest_tag = f'<link rel="manifest" href="data:application/json;base64,{manifest_base64}" />'
    html = re.sub(r'<link\s+rel=["\']manifest["\']\s+href=["\']manifest\.json(?:\?[^"\']*)?["\']\s*/?>', lambda _: manifest_tag, html)
    html = html.replace('<link rel="manifest" href="manifest.json" />', manifest_tag)
    html = html.replace('<link rel="manifest" href="manifest.json">', manifest_tag)
    
    # Update PWA theme metadata & title to match Odyssey RPG specifications
    html = html.replace('<meta name="theme-color" content="#5856D6" />', '<meta name="theme-color" content="#18181b" />')
    html = html.replace('<meta name="theme-color" content="#5856D6">', '<meta name="theme-color" content="#18181b" />')
    html = html.replace('<meta name="apple-mobile-web-app-title" content="ODYSSEY" />', '<meta name="apple-mobile-web-app-title" content="Odyssey RPG" />')
    html = html.replace('<title>ODYSSEY — Personal Journey System</title>', '<title>Odyssey RPG</title>')
    
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
