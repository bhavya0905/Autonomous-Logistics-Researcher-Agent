from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import Orchestrator

app = FastAPI()

orchestrator = Orchestrator()


class QueryRequest(BaseModel):
    query: str


@app.post("/research")
def run_research(request: QueryRequest):

    report = orchestrator.run(request.query)

    return {
        "query": request.query,
        "report": report
    }