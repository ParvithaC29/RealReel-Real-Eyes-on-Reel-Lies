import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0B0E11;
    color: #E6EEF5;
}

.glass {
    background: rgba(20,35,50,0.55);
    backdrop-filter: blur(14px);
    padding: 45px;
    border-radius: 20px;
}

h1 {
    color: #3A6F8F;
}

.subtext {
    color: #9FB3C8;
}

.cta {
    background-color: #00C2FF;
    color: #0B0E11;
    padding: 12px 30px;
    border-radius: 10px;
    font-weight: 600;
    border: none;
}
.cta:hover {
    background-color: #1AD1FF;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="height:15vh"></div>

<center>
<div class="glass" style="width:420px;">
    <img src="assets/realreel_logo.png" width="160">
    <h1>RealReel</h1>
    <p class="subtext">Reveal what’s real. Expose deepfakes.</p>
</div>
</center>

<div style="height:25px"></div>

<center>
    <a href="/Upload" target="_self">
        <button class="cta">Start Detection</button>
    </a>
</center>
""", unsafe_allow_html=True)
