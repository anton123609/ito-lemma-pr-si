import streamlit as st

def show():
    # --- LAYOUT SETUP (Apple Style) ---
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        
        # --- TITLE ---
        st.markdown("<h1 style='text-align: center;'>The Derivation.</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>From deterministic to stochastic.</h3>", unsafe_allow_html=True)
        st.write("")
        
        st.divider()

        # --- STEP 1: SIMPLIFIED NOTATION ---
        st.header("1. Dictionary")
        st.write("""
        For what do the simplified notations stand for?
        """)
        
        # Kleine Legende
        st.info("Legend:")
        st.markdown("""
        * $f_t$: Change with **Time** - Partial derivative of f to t.
        * $f_x$: Change with **Price** - Partial derivative of f to x.
        * $f_{xx}$: The **Curvature** - Second partial derivative of f to x.
        """)

        st.write("")

        # --- STEP 2: THE MOVEMENT ---
        st.header("2. Differential equation for a general stock price ($dX$)")
        st.write("We assume our stock price $X$ follows a standard Stochastic Differential Equation (SDE):")
        st.latex(r'''
        dX = \mu \cdot dt + \sigma \cdot dW
        ''')
        st.caption("Drift ($\mu$) + Volatility ($\sigma$) $\\times$ Random Shock ($dW$).")

        st.divider()

        # --- STEP 3: TAYLOR EXPANSION ---
        st.header("3. Taylor Expansion (Simple Form)")
        st.write("We want to find the change (derivative) in the option price $df$. We need the Taylor Series up to the second order:")
        
        st.latex(r'''
        df = f_t \cdot dt + f_x \cdot dX + \frac{1}{2} f_{xx} \cdot (dX)^2 + \dots
        ''')
        
        st.write("The problem: We don't know the term $(dX)^2$ and potential higher orders.")

        st.write("")

        # --- STEP 4: THE CRITICAL STEP ---
        st.header("4. How to solve higher order terms")

        # A) Intuition
        st.subheader("A) The Intuition")
        st.write("Brownian Motion scales with the square root of time:")
        st.latex(r'''
        dW \approx \sqrt{dt}
        ''')
        st.write("")
        st.latex(r'''
        (dW)^2 \approx (\sqrt{dt})^2 = dt
        ''')

        # B) Proof (2nd Order)
        st.subheader("B) Solving $(dX)^2$ (2nd Order)")
        st.write("Expanding the squared SDE:")
        st.latex(r'''
        (dX)^2 = \mu^2 (dt)^2 + 2\mu\sigma (dt)(dW) + \sigma^2 (dW)^2
        ''')
        
        # Korrigierte Tabelle mit Raw-String (r""")
        st.markdown(r"""
        | Term | Result | Explanation |
        | :--- | :--- | :--- |
        | $(dt)^2$ | $0$ | Too small. |
        | $dt \cdot dW$ | $0$ | Too small. |
        | **$(dW)^2$** | **$dt$** | **Survives!** |
        """)
        
        st.write("Result: The term $(dX)^2$ becomes $\sigma^2 dt$.")

        # --- C) THE NUMBERS TEST ---
        st.subheader("C) Why $(dX)^3$ vanishes")
        st.write("Why do we delete $(dX)^3$ but keep $(dX)^2$? Let's simply plug in a small number.")
        
        st.write("Imagine a very small time step: **$dt = 0.01$** (1% of a year).")

        # Korrigierte Tabelle mit Raw-String (r""")
        st.markdown(r"""
        | Term | Formula | Value (if $dt=0.01$) | Decision |
        | :--- | :--- | :--- | :--- |
        | **Time** | $dt$ | **0.01** | Standard |
        | **2nd Order** | $(dX)^2 \approx dt$ | **0.01** | Relevant |
        | **3rd Order** | $(dX)^3 \approx dt^{1.5}$ | **0.001** | Too small |
        | **4th Order** | $(dX)^4 \approx dt^2$ | **0.0001** | Even smaller |
        """)
        
        st.info("""
        **Conclusion:** We only keep $(dX)^2$ because higher orders get too tiny to be considert as important.
        """)

        # D) Result
        st.subheader("D) The Final Survivor")
        st.write("Only one special term survives the limit process:")
        st.latex(r'''
        (dX)^2 = \sigma^2 \cdot dt
        ''')
        
        st.divider()

        # ==========================================
        # STEP 5: SUBSTITUTION
        # ==========================================
        st.header("5. Putting it together ")
        st.write("We put all our information from abouve into the Taylor Expansion.")

        # --- 5A: THE SKELETON ---
        st.subheader("A) Start with the Taylor Skeleton (from Step 3)")
        st.latex(r'''
        df = f_t dt + f_x \cdot \textcolor{blue}{dX} + \frac{1}{2} f_{xx} \cdot \textcolor{red}{(dX)^2}
        ''')
        st.caption("We have two placeholders to fill: Blue ($dX$) and Red ($(dX)^2$).")

        # --- 5B: QUADRATIC ---
        st.subheader("B) Plug in the Squared Term (Red)")
        st.write("We take our result from **Step 4D** and replace the end of the equation.")
        st.latex(r'''
        \textcolor{red}{(dX)^2} \longrightarrow \sigma^2 dt
        ''')
        st.write("Inserting this gives:")
        st.latex(r'''
        df = f_t dt + f_x \cdot \textcolor{blue}{dX} + \frac{1}{2} f_{xx} \cdot (\textcolor{red}{\sigma^2 dt})
        ''')

        # --- 5C: LINEAR ---
        st.subheader("C) Plug in the Linear Term (Blue)")
        st.write("We take the definition of the SDE from **Step 2**.")
        st.latex(r'''
        \textcolor{blue}{dX} \longrightarrow \mu dt + \sigma dW
        ''')
        st.write("Inserting this into the middle part:")
        st.latex(r'''
        df = f_t dt + f_x \cdot (\textcolor{blue}{\mu dt + \sigma dW}) + \frac{1}{2} f_{xx} \sigma^2 dt
        ''')

        # --- 5D: EXPANSION ---
        st.subheader("D) Distribute and Clean Up")
        st.write("We multiply out the bracket in the middle:")
        
        st.latex(r'''
        f_x \cdot (\mu dt + \sigma dW) = \mu f_x dt + \sigma f_x dW
        ''')
        
        st.write("This gives us the fully expanded raw equation:")
        st.latex(r'''
        df = f_t dt + \mu f_x dt + \sigma f_x dW + \frac{1}{2} f_{xx} \sigma^2 dt
        ''')
        
        st.success("All substitutions are complete. Now we just need to tidy up.")

        st.divider()

        # --- STEP 6: SORTING ---
        st.header("6. Sorting the Piles")
        st.write("We sort the terms from Step 5D into two groups: Deterministic ($dt$) and Stochastic ($dW$).")
        
        st.write("Group all terms containing **$dt$**:")
        st.latex(r'''
        \text{Trend} = \left( f_t + \mu f_x + \frac{1}{2} \sigma^2 f_{xx} \right) dt
        ''')

        st.write("Group all terms containing **$dW$**:")
        st.latex(r'''
        \text{Risk} = (\sigma f_x) dW
        ''')
        
        st.write("Combined:")
        st.latex(r'''
        df = \underbrace{(f_t + \mu f_x + \frac{1}{2} \sigma^2 f_{xx})}_{\text{Trend / Drift}} dt + \underbrace{(\sigma f_x)}_{\text{Risk}} dW
        ''')

        st.divider()

        # --- STEP 7: FINAL TRANSLATION ---
        st.header("7. The Final Formula")
        st.write("""
        We are done! Now we just translate our short notation back to the formal mathematical language.
        """)

        col_trans1, col_trans2 = st.columns(2)
        with col_trans1:
            st.markdown("**We wrote:**")
            st.latex(r"f_t")
            st.latex(r"f_x")
            st.latex(r"f_{xx}")
        with col_trans2:
            st.markdown("**Mathematical written:**")
            st.latex(r"\frac{\partial f}{\partial t}")
            st.latex(r"\frac{\partial f}{\partial x}")
            st.latex(r"\frac{\partial^2 f}{\partial x^2}")

        st.write("")
        st.warning("### Ito's Lemma")
        st.write("Substituting the fractions back in:")

        st.latex(r'''
        df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t
        ''')
        
        st.caption("q.e.d. - quod erat demonstrandum")