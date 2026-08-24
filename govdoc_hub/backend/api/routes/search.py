from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
async def search_documents(q: str):
    # TODO: Implement local semantic search via ChromaDB here
    return {
        "status": "success",
        "query": q,
        "results": [
            {"file_name": "placeholder_doc.pdf", "snippet": "This is a placeholder result."}
        ]
    }
