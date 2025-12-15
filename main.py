import streamlit as st
import streamlit.components.v1 as components
import qrcode
from io import BytesIO
import time # NEU: Für den zwingenden Reload des Skripts

# Importiere deine Kapitel
from chapters import cover, intro, derivation, application 

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Ito's Lemma Presentation",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. NAVIGATION & SCROLL LOGIC ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Cover"

st.sidebar.title("Navigation")

# Radio Button
selection = st.sidebar.radio("Go to chapter:", [
    "Cover", 
    "Introduction", 
    "The Derivation", 
    "Visualisation and conclusion"
], key="nav_selection")

# --- DER FIX ---
# Wir prüfen, ob sich die Seite geändert hat
if st.session_state.current_page != selection:
    st.session_state.current_page = selection
    
    # Wir benutzen einen Platzhalter, um das JS ganz oben einzufügen
    placeholder = st.empty()
    
    with placeholder:
        # Der Trick: Ein sich ändernder Key (time.time()), damit Streamlit das Skript 
        # GARANTIERT neu ausführt und nicht cached.
        components.html(
            f"""
                <script>
                    // 1. Fokus vom Sidebar-Button entfernen (damit Browser nicht zurückspringt)
                    if (window.parent.document.activeElement) {{
                        window.parent.document.activeElement.blur();
                    }}
                    // 2. Hart nach oben scrollen
                    window.parent.scrollTo(0, 0);
                </script>
            """,
            height=0,
            width=0,
        )

# --- 3. QR CODE ---
st.sidebar.divider()

# Link zu deiner App
app_url = "https://jr8-itoslemma.streamlit.app/"

qr_image = qrcode.make(app_url)
img_buffer = BytesIO()
qr_image.save(img_buffer, format="PNG")
img_buffer.seek(0)

st.sidebar.image(img_buffer, caption="Scan Presentation", width=140)
st.sidebar.caption("Journal Review 8 • 2026")

# --- 4. MAIN CONTENT ---
if selection == "Cover":
    cover.show()
elif selection == "Introduction":
    intro.show()
elif selection == "The Derivation":
    derivation.show()
elif selection == "Visualisation and conclusion":
    application.show()