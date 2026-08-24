from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ExtractRequest(BaseModel):
    files: List[str]
    action: str
    provider: Optional[str] = "gemini"
    api_key: Optional[str] = None

@router.post("/extract")
async def extract_data(request: ExtractRequest):
    # TODO: Implement LangChain ReAct agent extraction logic
    # Nếu request.api_key có giá trị, sử dụng key này thay vì key mặc định của hệ thống
    # Tùy theo request.provider, khởi tạo model tương ứng (ChatGoogleGenerativeAI, ChatOpenAI, ChatAnthropic)
    
    return {
        "status": "success", 
        "message": f"Triggered extraction for {len(request.files)} files using {request.provider}."
    }
