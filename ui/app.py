import streamlit as st
from agents.orchestrator import Orchestrator

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS (MODERN UI)
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #0f1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.metric-card {
    background: linear-gradient(135deg, #1c1f26, #2a2f3a);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

h1, h2, h3 {
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("🤖 Autonomous Research Agent")
st.caption("AI-powered logistic research system")

# -------------------------------
# INPUT
# -------------------------------
query = st.text_input("🔍 Enter your research query")

run_button = st.button("🚀 Run Research")

# -------------------------------
# INIT AGENT
# -------------------------------
orchestrator = Orchestrator()

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if run_button and query:

    with st.spinner("Running research pipeline..."):
        report = orchestrator.run(query)

    st.success("Research Completed")

    # -------------------------------
    # LAYOUT: 2 COLUMN
    # -------------------------------
    col1, col2 = st.columns([3, 1])

    # -------------------------------
    # LEFT: REPORT
    # -------------------------------
    with col1:
        st.markdown("## 📄 Research Report")
        formatted_report = report.replace("\n", "<br>")

        st.markdown(f"""
        <div class="card">
        {formatted_report}
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # RIGHT: SIDEBAR INFO
    # -------------------------------
    with col2:

        # ---- CITATIONS ----
        st.markdown("## 🔗 Citations")

        # Extract URLs from context (simple placeholder logic)
        # Replace later with real citation manager
        citations = []

        for line in report.split("\n"):
            if "http" in line:
                citations.append(line)

        if citations:
            for c in citations:
                st.markdown(f"- {c}")
        else:
            st.info("No explicit citation links found")

        # ---- METRICS ----
        st.markdown("## 📊 Evaluation")

        # Fake or integrate real evaluator output here
        # Replace with actual evaluation call if needed
        evaluation = {
            "quality_score": 0.78,
            "retrieval_relevance": 0.64,
            "evidence_coverage": 1.0,
            "hallucination_risk": 0.52
        }

        def metric_card(title, value):
            st.markdown(f"""
            <div class="metric-card">
                <h4>{title}</h4>
                <h2>{value:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        metric_card("Quality", evaluation["quality_score"])
        metric_card("Relevance", evaluation["retrieval_relevance"])
        metric_card("Coverage", evaluation["evidence_coverage"])
        metric_card("Hallucination Risk", evaluation["hallucination_risk"])

        st.markdown("### 📈 Details")

        st.progress(evaluation["quality_score"])
        st.progress(evaluation["retrieval_relevance"])
        st.progress(evaluation["evidence_coverage"])