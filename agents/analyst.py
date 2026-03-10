from langchain_openai import ChatOpenAI
from memory.vector_db import VectorDB
from config.settings import get_settings


class AnalystAgent:

    def __init__(self):

        self.settings = get_settings()

        self.vector_db = VectorDB()

        self.llm = ChatOpenAI(
            model=self.settings.MODEL_NAME,
            temperature=0.2
        )

    def retrieve_documents(self, query: str, k: int = 5):

        results = self.vector_db.search(query, n_results=k)

        docs = results[0] if results else []

        return docs

    def build_context(self, documents):

        context = "\n\n".join(documents)

        return context

    def build_prompt(self, query, context):

        prompt = f"""
You are a logistics industry analyst.

Using the provided research material, analyze logistics trends and insights.

Research Material:
{context}

User Query:
{query}

Provide structured insights including:

1. Key logistics trends
2. Risks or challenges
3. Opportunities
4. Strategic insights
"""

        return prompt

    def analyze(self, query):

        documents = self.retrieve_documents(query)

        context = self.build_context(documents)

        prompt = self.build_prompt(query, context)

        response = self.llm.invoke(prompt)

        return response.content