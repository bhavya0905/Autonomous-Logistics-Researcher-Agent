from agents.orchestrator import Orchestrator
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from tools.knowledge_extractor import KnowledgeExtractor
from memory.chunker import SemanticChunker
from tools.knowledge_store import KnowledgeStore
from memory.retriever import Retriever


def run_ingestion_test(query):

    print("\n=== SEARCH TEST ===")
    search = SearchTool()
    urls = search.search(query)

    print("Found URLs:", urls[:3])

    scraper = WebScraper()
    extractor = KnowledgeExtractor()
    chunker = SemanticChunker()
    store = KnowledgeStore()

    for url in urls[:3]:

        print(f"\nScraping: {url}")

        page = scraper.scrape(url)

        if not page:
            print("Failed scraping")
            continue

        doc = extractor.extract(page)

        if not doc:
            print("Extractor rejected page")
            continue

        chunks = chunker.chunk(doc)

        print("Chunks created:", len(chunks))

        store.store_document(chunks)

    print("\n=== INGESTION COMPLETE ===")


def run_retrieval_test(query):

    print("\n=== RETRIEVAL TEST ===")

    retriever = Retriever()

    docs = retriever.retrieve(query)

    print("Retrieved documents:", len(docs))

    for d in docs[:3]:
        print("\n---")
        print("TYPE:", type(d))
        print(d)

def run_full_agent_test(query):

    print("\n=== FULL AGENT TEST ===")

    orchestrator = Orchestrator()

    report = orchestrator.run(query)

    print("\n=== FINAL REPORT ===\n")
    print(report)


if __name__ == "__main__":

    query = "How are customs duties calculated"

    run_ingestion_test(query)

    run_retrieval_test(query)

    run_full_agent_test(query)