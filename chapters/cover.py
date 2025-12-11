import streamlit as st

def show():
    # --- LAYOUT SETUP ---
    # Wir nutzen 3 Spalten, damit der Inhalt schön mittig zentriert ist
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        
        # --- 1. TITEL & SUBTITEL ---
        st.write("") # Etwas Abstand nach oben
        st.markdown("<h1 style='text-align: center; font-size: 4em;'>Ito's Lemma</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>Journal Review Group 8</h3>", unsafe_allow_html=True)
        
        st.divider()

        # --- 2. NAMEN ---
        st.markdown("<p style='text-align: center; font-size: 1.2em; font-weight: bold;'>Presented by:</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.5em;'>Anton Jungbauer, Julian Bauer, Leander Friedmann, Emil Höfer, Luca Russo, Abdoulie Njie</p>", unsafe_allow_html=True)
        
        st.write("") # Abstand
        st.write("") 

        # --- 3. THESE (Hervorgehoben) ---
        st.info("### Core Thesis")
        st.markdown("""
        > The classical chain rule isn't working in the world of randomness.""")

        st.write("")
        st.divider()

        # --- 4. ABSTRACT ---
        st.header("Abstract")
        st.write("""HIER EINFÜGEN
        """)

        st.write("")
        st.write("")

        # --- 5. QUELLEN (SOURCES) ---
        # Ein "Expander" ist gut für Quellen, damit sie nicht so viel Platz wegnehmen, 
        # aber aufklappbar sind.
        with st.expander("References / Sources"):
            st.markdown("""
            * **Hull, John C.** - *Options, Futures, and Other Derivatives*
            * **Shreve, Steven** - *Stochastic Calculus for Finance II*
            * **Yahoo Finance** (for Historical Data)
            * [Weitere Quelle hier einfügen]
            """)
            
        st.write("")
        st.caption("Project Presentation • 2026")