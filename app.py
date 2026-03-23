import streamlit as st
from agents.orchestrator import Orchestrator

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "status" not in st.session_state:
    st.session_state.status = "Idle"

if "logs" not in st.session_state:
    st.session_state.logs = []

if "report" not in st.session_state:
    st.session_state.report = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "citations" not in st.session_state:
    st.session_state.citations = []

# ---------------------------
# STATE HELPERS
# ---------------------------

def update_status(status, message=""):
    st.session_state.status = status
    st.session_state.status_message = message

def log_event(message):
    st.session_state.logs.append(message)

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🤖",
    layout="wide"
)

# -----------------------
# STYLES (clean modern)
# -----------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.metric-card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.title("🤖 Autonomous Research Agent")
st.caption("AI-powered research system")

# -----------------------
# INPUT (ALWAYS VISIBLE)
# -----------------------
query = st.text_input("🔍 Enter your research query")

run_button = st.button("🚀 Run Research")

# ---------------------------
# SIDEBAR: SYSTEM STATUS
# ---------------------------
with st.sidebar:
    st.markdown("## ⚙️ System Status")

    status = st.session_state.get("status", "Idle")
    message = st.session_state.get("status_message", "")

    st.markdown(f"**Stage:** {status}")
    if message:
        st.caption(message)

    st.markdown("## 🧠 Execution Trace")

    logs = st.session_state.get("logs", [])

    if logs:
        for log in logs[-10:]:  # last 10 logs only
            st.write(log)
    else:
        st.caption("No activity yet")

# -----------------------
# RUN LOGIC
# -----------------------
if run_button:
    if not query:
        st.warning("Please enter a query")
    else:
        orchestrator = Orchestrator()

        update_status("Planning", "Expanding query...")
        log_event("🧠 Planning queries")

        orchestrator = Orchestrator()

        with st.spinner("Running research pipeline..."):

            update_status("Researching", "Searching & scraping...")
            log_event("🔍 Searching web")
    
            report = orchestrator.run(query)  # keep this for now

            update_status("Completed", "Report generated")
            log_event("✅ Report generation complete")

        st.session_state.report = report

        st.success("Research completed")

        # -----------------------
        # FORMAT REPORT
        # -----------------------
        formatted_report = report.replace("\n", "<br>")

        # -----------------------
        # LAYOUT
        # -----------------------
        col1, col2 = st.columns([3, 1])

        # -----------------------
        # REPORT
        # -----------------------
        with col1:
            st.markdown("## 📄 Research Report")

            st.markdown(f"""
            <div class="card">
            {formatted_report}
            </div>
            """, unsafe_allow_html=True)

        # -----------------------
        # SIDE PANEL
        # -----------------------
        with col2:

            # ---- CITATIONS ----
            st.markdown("## 🔗 Citations")

            # Simple extraction (placeholder)
            citations = []
            for line in report.split("\n"):
                if "http" in line:
                    citations.append(line)

            if citations:
                for c in citations:
                    st.markdown(f"- {c}")
            else:
                st.info("No citation links found")

            # ---- METRICS ----
            st.markdown("## 📊 Evaluation")

            # Replace with real evaluator later
            evaluation = {
                "quality": 0.78,
                "relevance": 0.64,
                "coverage": 1.0,
                "hallucination": 0.52
            }

            def metric(title, value):
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{title}</h4>
                    <h2>{value:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)

            metric("Quality", evaluation["quality"])
            metric("Relevance", evaluation["relevance"])
            metric("Coverage", evaluation["coverage"])
            metric("Hallucination Risk", evaluation["hallucination"])

            st.markdown("### 📈 Progress")

            st.progress(evaluation["quality"])
            st.progress(evaluation["relevance"])
            st.progress(evaluation["coverage"])