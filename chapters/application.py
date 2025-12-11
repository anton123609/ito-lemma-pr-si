import streamlit as st
import numpy as np
import plotly.graph_objects as go

def show():
    # --- LAYOUT SETUP ---
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("<h1 style='text-align: center;'>Itôs Lemma intuitional</h1>", unsafe_allow_html=True)
        st.write("")
        st.divider()

        # ==========================================
        # 1. VISUAL INTUITION (THE FRACTAL NATURE)
        # ==========================================
        st.header("1. The Visual Intuition")
        
        st.write("""
        At first we have to make clear why the classical chainrule can not work in the world of randomness.
        """)

        st.subheader("The Microscope Test")
        st.write("""
        Imagine you have a magical microscope and you look at a curve.
        
        * **The Smooth World (Newton):** If you zoom in on a circle or a ball, eventually the edge looks like a **flat, straight line**.
        * **The Rough World (Ito):** If you zoom in on a coastline (or a stock price), you see bays and peninsulas. If you zoom further, you see rocks. Further? Grains of sand.
        """)

        st.info("**Interactive Experiment:** Draw a rectangle on the red chart to ZOOM IN. Do it 3, 4, or 5 times!")

        # --- DATEN GENERIERUNG (EXTREM HOHE DICHTE) ---
        # Wir simulieren 100.000 Ticks
        n_points = 100000 
        t = np.linspace(0, 1, n_points) 
        
        # 1. Smooth (Sinus)
        y_smooth = np.sin(t * 5) + 100 # +100 damit es vergleichbar aussieht
        
        # 2. Rough (Geometrische Brownsche Bewegung)
        dt = t[1] - t[0]
        np.random.seed(42) 
        random_shocks = np.random.normal(0, np.sqrt(dt), n_points)
        
        # HIER IST DIE ÄNDERUNG: Exponentialfunktion (startet bei 100, kann nicht negativ werden)
        y_rough = 100 * np.exp(np.cumsum(random_shocks))

        # --- CHARTS ---
        col_plot1, col_plot2 = st.columns(2)

        with col_plot1:
            st.markdown("**A) The Smooth World**")
            st.caption("Like a ball or a table edge")
            fig1 = go.Figure()
            # Scattergl erlaubt mehr Performance bei vielen Punkten
            fig1.add_trace(go.Scattergl(x=t, y=y_smooth, mode='lines', line=dict(color='#007AFF', width=2), name='Smooth'))
            fig1.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), template="plotly_white", xaxis_title="Time", yaxis_title="Value")
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write("**Zoom Effect:** It becomes boring. It becomes a straight line.")

        with col_plot2:
            st.markdown("**B) The Rough World**")
            st.caption("Like a Stock Price (Positive)")
            fig2 = go.Figure()
            # Scattergl für 100.000 Punkte
            fig2.add_trace(go.Scattergl(x=t, y=y_rough, mode='lines', line=dict(color='#ff4b4b', width=1), name='Rough'))
            fig2.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), template="plotly_white", xaxis_title="Time", yaxis_title="Price ($)")
            st.plotly_chart(fig2, use_container_width=True)
            
            st.write("**Zoom Effect:** New jitters appear! It never gets straight.")

        # --- INTUITIVE ERKLÄRUNG ---
        st.write("")
        st.subheader("Why does this break normal math?")
        
        st.write("""
        In normal math, we calculate speed (derivative) by asking: *"In which direction is the point moving right now?"*
        
        * **Smooth:** We zoom in, see a straight line, and define the direction. Easy.
        * **Rough:** We zoom in, but the point jitters up and down infinite times. **It has no clear direction!**
        """)

        st.warning("""
        **The Problem:** Because the curve shakes infinitely fast, it covers more "distance" than a smooth curve.
        **The Solution:** This extra shaking creates the extra term in Ito's Lemma ($\sigma^2$). It is the "energy" of the shake.
        """)

        st.divider()

        # ==========================================
        # 2. ANSWERING THE THESIS (MATH COMPARISON)
        # ==========================================
        st.header("2. The Thesis Answered (Mathematically)")
        
        st.write("""
        Now we can translate this visual problem into formulas using our **Simplified Notation** ($f_t, f_x$).
        """)

        col_class, col_ito = st.columns(2)

        with col_class:
            st.info("**Classical Chain Rule**")
            st.caption("Assumes the curve becomes straight")
            st.latex(r'''
            df = f_t \cdot dt + f_x \cdot dx
            ''')
            st.write("It ignores the shaking space.")
            st.error("Result: WRONG")

        with col_ito:
            st.success("**Stochastic Chain Rule (Ito)**")
            st.caption("Accepts the infinite shaking")
            st.latex(r'''
            df = f_t \cdot dt + f_x \cdot dx + \textcolor{red}{\frac{1}{2} f_{xx} (dx)^2}
            ''')
            st.write("It adds the energy of the shaking.")
            st.success("Result: CORRECT")

        st.divider()

        # ==========================================
        # 3. INTERACTIVE VISUALIZATION (MONTE CARLO)
        # ==========================================
        st.header("3. Interactive Proof (Monte Carlo)")
        st.write("Let's prove this dynamically. You are the market maker.")
        st.write("Adjust **Trend** and **Risk** to see how the models diverge.")

        col_input1, col_input2 = st.columns(2)
        with col_input1:
            mu_input = st.slider("Drift (Trend $\mu$)", min_value=-0.2, max_value=0.5, value=0.20, step=0.01, format="%.2f")
        with col_input2:
            sigma_input = st.slider("Volatility (Risk $\sigma$)", min_value=0.01, max_value=0.90, value=0.40, step=0.01, format="%.2f")

        S0 = 100.0
        days = 252
        dt = 1/252
        N_SIM = 10000 
        
        if st.button("Re-Roll Randomness 🎲"):
            st.toast("New parallel universes generated.")

        # Mathematik
        random_shocks = np.random.normal(0, np.sqrt(dt), (days, N_SIM))
        W = np.cumsum(random_shocks, axis=0)
        t_vec = np.linspace(0, 1, days).reshape(-1, 1)
        
        # Modelle
        naive_paths = S0 * np.exp(mu_input * t_vec + sigma_input * W)
        ito_paths = S0 * np.exp((mu_input - 0.5 * sigma_input**2) * t_vec + sigma_input * W)
        
        naive_mean = np.mean(naive_paths, axis=1)
        ito_mean = np.mean(ito_paths, axis=1)
        theoretical_trend = S0 * np.exp(mu_input * np.linspace(0, 1, days))

        # Chart
        fig = go.Figure()
        for i in range(50):
            fig.add_trace(go.Scatter(y=ito_paths[:, i], mode='lines', line=dict(color='lightgrey', width=0.5), opacity=0.1, showlegend=False, hoverinfo='skip'))
        
        fig.add_trace(go.Scatter(y=naive_mean, mode='lines', name='Naive Model (Classical)', line=dict(color='#ff4b4b', width=4, dash='dash')))
        fig.add_trace(go.Scatter(y=ito_mean, mode='lines', name='Ito Model (Correct)', line=dict(color='#76b900', width=4)))
        fig.add_trace(go.Scatter(y=theoretical_trend, mode='lines', name='Target (Law)', line=dict(color='black', width=3, dash='dot')))

        fig.update_layout(title=f"Simulation with Volatility: {sigma_input:.0%}", xaxis_title="Time", yaxis_title="Price", template="plotly_white", height=500, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig, use_container_width=True)

        # Ergebnisse
        final_target = theoretical_trend[-1]
        final_naive = naive_mean[-1]
        final_ito = ito_mean[-1]
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.error(f"**Classical Error:** +${final_naive - final_target:.2f}")
        with col_res2:
            st.success(f"**Ito Accuracy:** ${final_ito - final_target:.2f}")

        st.divider()

        # ==========================================
        # 4. DEEP DIVE: VOLATILITY DRAG
        # ==========================================
        st.header("4. Deep Dive: The Volatility Drag")
        st.write("""
        We observed that the Red Line (Classical Rule) always ends up **higher** than reality. 
        It implies that volatility creates money out of thin air. In reality, volatility destroys value.
        """)

        st.subheader("A) The Intuition: Why averages lie")
        st.write("Imagine you start with **$100**.")

        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.markdown("**Scenario 1: No Volatility**")
            st.write("Year 1: +0%")
            st.write("Year 2: +0%")
            st.metric("Result", "$100")
            st.caption("Arithmetic Average: 0%")

        with col_ex2:
            st.markdown("**Scenario 2: High Volatility**")
            st.write("Year 1: +50% ($150)")
            st.write("Year 2: -50% ($75)")
            st.metric("Result", "$75", delta="-25%", delta_color="inverse")
            st.caption("Arithmetic Average: 0%")

        st.warning("""
        **The Intuitive Trap:** The arithmetic average of +50% and -50% is **0%**. 
        But the real money result is **-25%**. 
        Standard calculus sees the 0%. Ito calculus sees the -25%.
        """)

        st.write("")

        st.subheader("B) The Mathematical Formula")
        st.write("Ito's Lemma gives us the exact formula to correct this error.")
        
        st.latex(r'''
        \underbrace{\mu_{\text{geo}}}_{\text{Real Growth}} = \underbrace{\mu_{\text{arith}}}_{\text{Average Return}} - \underbrace{\frac{1}{2}\sigma^2}_{\text{Volatility Drag}}
        ''')

        st.write("")

        st.subheader("C) Calculation for your Simulation")
        drag = 0.5 * sigma_input**2
        geo_drift = mu_input - drag
        
        st.write(f"Based on your slider settings ($\mu = {mu_input:.2%}$, $\sigma = {sigma_input:.2%}$):")
        
        st.latex(rf'''
        \text{{Real Growth}} = {mu_input:.2f} - \frac{{1}}{{2}}({sigma_input:.2f})^2
        ''')
        
        st.latex(rf'''
        \text{{Real Growth}} = {mu_input:.2f} - {drag:.4f} = \mathbf{{{geo_drift:.2%}}}
        ''')

        st.success(f"""
        **Final Verdict:**
        The difference of **{drag:.2%}** per year is exactly the Volatility Drag. 
        **Ito's Lemma is simply the tool that finds this hidden cost.**
        """)