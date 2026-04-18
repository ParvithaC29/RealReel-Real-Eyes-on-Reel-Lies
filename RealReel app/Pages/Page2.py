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

st.markdown("<h1>Upload Media</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Upload a video or image to analyze authenticity.</p>", unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["mp4", "avi", "mov", "jpg", "png"]
    )

    if uploaded_file:
        st.success("File uploaded successfully ✅")

        if st.button("Analyze", key="analyze"):
            st.session_state["result"] = {
                "verdict": "DEEPFAKE",
                "confidence": 87
            }
            st.switch_page("pages/2_Result.py")

    st.markdown("</div>", unsafe_allow_html=True)
