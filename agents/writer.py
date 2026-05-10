from langchain_groq import ChatGroq
from config.settings import get_settings
from utils.logger import logger


class WriterAgent:
    def __init__(self):
        self.settings = get_settings()

        self.llm = ChatGroq(
            model=self.settings.MODEL_NAME,
            temperature=0,
            groq_api_key=self.settings.GROQ_API_KEY
        )

    # --------------------------------------------------
    # MAIN WRITE FUNCTION
    # --------------------------------------------------
    def write_report(self, query: str, context: str):
        prompt = self._build_prompt(query, context)

        response = self.llm.invoke(prompt)

        return response.content

    # --------------------------------------------------
    # PROMPT BUILDER (CRITICAL)
    # --------------------------------------------------
    def _build_prompt(self, query: str, context: str):
        return f"""
You are a research analyst, not a content writer.

Your job is to produce a structured, evidence-based report.

---

STRICT RULES:

1. Every claim MUST be grounded in the provided context
2. You MUST cite chunk IDs like [1], [2]
3. DO NOT repeat the same idea across sections
4. If multiple chunks say the same thing → merge into ONE insight
5. If information conflicts → explicitly highlight it
6. DO NOT use generic filler language
7. DO NOT summarize blindly — synthesize insights

---

INPUT:

User Query:
{query}

Context Chunks:
{context}

---

OUTPUT FORMAT:

# Overview
- Max 4–5 lines
- High-level understanding of topic

# Key Findings
- Bullet points
- Each bullet MUST include citations

# Detailed Analysis
- Group by themes (not chunks)
- Each paragraph MUST include citations

# Contradictions / Gaps
- Conflicting claims OR missing areas

# Conclusion
- Final synthesized insight
- NOT a summary

---

IMPORTANT:
- If a claim has no citation → DO NOT include it
- Prefer fewer high-quality insights over many weak ones
"""