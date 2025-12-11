import streamlit as st
# NEU: 'cover' importieren
from chapters import cover, intro, derivation, application 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ito's Lemma Presentation",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- NAVIGATION (Sidebar) ---
st.sidebar.title("Navigation")

# NEU: "Start / Cover" als erster Punkt in der Liste
selection = st.sidebar.radio("Go to chapter:", [
    "Cover", 
    "Introduction", 
    "The Derivation", 
    "Intuitions and thesis answer"
])

# --- MAIN APP LOGIC ---
if selection == "Cover":     # NEU
    cover.show()
elif selection == "Introduction":
    intro.show()
elif selection == "The Derivation":
    derivation.show()
elif selection == "Intuitions and thesis answer":
    application.show()

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("Journal Review 8 • 2026")