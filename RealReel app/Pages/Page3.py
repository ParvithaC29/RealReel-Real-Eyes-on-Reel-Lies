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

result = st.session_state.get("result", None)

st.markdown("<h1>Analysis Result</h1>", unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    if result:
        verdict = result["verdict"]
        confidence = result["confidence"]

        if verdict == "REAL":
            st.success("✅ AUTHENTIC MEDIA")
        else:
            st.error("❌ DEEPFAKE DETECTED")

        st.markdown(f"""
        <h2>{confidence}% Confidence</h2>
        <p class="subtext">
        Detection based on temporal inconsistencies,
        facial artifact patterns, and texture analysis.
        </p>
        """, unsafe_allow_html=True)

    else:
        st.warning("No analysis found.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

center = st.columns(3)
with center[1]:
    if st.button("Analyze Another"):
        st.switch_page("pages/1_Upload.py")
