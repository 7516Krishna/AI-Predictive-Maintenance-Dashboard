import streamlit as st
import pandas as pd
from src.chat_engine import generate_response
from src.visualizer import plot_data
from src.data_preprocessing import process_nasa_pipeline

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Predictive Maintenance System",
    layout="wide"
)

# -----------------------------
# PROFESSIONAL WHITE UI + FIXES 🔥
# -----------------------------
st.markdown("""
<style>

/* GLOBAL TEXT FIX */
* {
    color: #000000 !important;
}

/* App background */
.stApp {
    background-color: #ffffff !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f4f6f9 !important;
}

/* FORCE FILE UPLOADER TEXT 🔥 */
[data-testid="stFileUploader"] * {
    color: #000000 !important;
    opacity: 1 !important;
}

/* Upload label (VERY IMPORTANT) */
[data-testid="stFileUploader"] label {
    color: #1f4e79 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

/* Upload instructions text */
[data-testid="stFileUploader"] span {
    color: #000000 !important;
}

/* Upload box background */
[data-testid="stFileUploader"] section {
    background-color: #ffffff !important;
}

/* Uploaded file name */
[data-testid="stFileUploader"] div {
    color: #000000 !important;
}

/* Buttons */
.stButton>button {
    background-color: #1f77b4 !important;
    color: white !important;
    border-radius: 8px;
}

/* Headers */
h1 {
    color: #1f4e79 !important;
}
h2, h3 {
    color: #333333 !important;
}

/* Alerts */
.stAlert {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🏭 AI-Powered Predictive Maintenance Dashboard")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or NASA TXT file",
    type=["csv", "txt"]
)

# -----------------------------
# LOAD DATA
# -----------------------------
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".txt"):
            df = process_nasa_pipeline(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state["data"] = df
        st.sidebar.success("✅ Dataset Loaded Successfully")

    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")

# -----------------------------
# MAIN DASHBOARD
# -----------------------------
if "data" in st.session_state:

    df = st.session_state["data"]

    # -----------------------------
    # KPI CARDS 🔥
    # -----------------------------
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='card'>📁 Rows<br><h3>{df.shape[0]}</h3></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>📊 Columns<br><h3>{df.shape[1]}</h3></div>", unsafe_allow_html=True)

    if "failure" in df.columns:
        failure_count = df["failure"].sum()
        col3.markdown(f"<div class='card'>🚨 Failures<br><h3>{failure_count}</h3></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='card'>✅ Normal<br><h3>{len(df) - failure_count}</h3></div>", unsafe_allow_html=True)
    else:
        col3.markdown(f"<div class='card'>⚠️ No Failure Column</div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='card'>-</div>", unsafe_allow_html=True)

    st.divider()

    # -----------------------------
    # MAIN LAYOUT
    # -----------------------------
    left, right = st.columns([2, 1])

    # LEFT SIDE
    with left:
        st.subheader("📊 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        st.subheader("📈 Sensor Dashboard")
        plot_data(df)

    # RIGHT SIDE
    with right:
        st.subheader("📌 Dataset Info")

        st.markdown(f"""
        <div class='card'>
        <b>Total Rows:</b> {df.shape[0]} <br>
        <b>Total Columns:</b> {df.shape[1]}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📋 Columns")

        st.markdown(f"""
        <div class='card'>
        {", ".join(df.columns)}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

# -----------------------------
# CHAT SECTION
# -----------------------------
st.subheader("💬 AI Data Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask questions about your dataset...")

if user_input:
    st.session_state.chat.append(("user", user_input))

    response = generate_response(
        user_input,
        st.session_state.get("data")
    )

    st.session_state.chat.append(("assistant", response))

# DISPLAY CHAT
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("🚀 AI + IoT Predictive Maintenance | Portfolio Project")