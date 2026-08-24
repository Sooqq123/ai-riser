from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from google import genai
from google.genai import types, errors
router = APIRouter()

class ExtractRequest(BaseModel):
    files: List[str]
    action: str
    provider: Optional[str] = "gemini"
    api_key: Optional[str] = None

@router.post("/extract")
async def extract_data(request: ExtractRequest):    
    app = FastAPI(title="GovDoc Hub API")
    
    # Khởi tạo Gemini Client
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Lỗi khởi tạo Gemini Client: {e}")
    
    # Schema đầu ra (Giữ nguyên cấu trúc)
    class DocumentExtraction(BaseModel):
        so_quyet_dinh: str | None = Field(
            description="Số quyết định hoặc số hiệu của văn bản (VD: 123/QĐ-UBND). Trả về null nếu không tìm thấy."
        )
        ngay_ban_hanh: str | None = Field(
            description="Ngày tháng năm ban hành văn bản. Trả về null nếu không tìm thấy."
        )
        co_quan_ky: str | None = Field(
            description="Tên cơ quan nhà nước ban hành hoặc người ký văn bản. Trả về null nếu không tìm thấy."
        )
    
    @app.post("/api/extract-pdf", response_model=DocumentExtraction)
    async def extract_pdf_info(file: UploadFile = File(...)):
        # 1. Kiểm tra định dạng file (hỗ trợ PDF, PNG, JPG, JPEG)
        allowed_types = ["application/pdf", "image/png", "image/jpeg", "image/jpg"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF hoặc file ảnh.")
    
        # 2. Đọc nội dung file thành bytes
        file_bytes = await file.read()
        
        # 3. Đóng gói file cho Gemini
        # Gemini 1.5 hỗ trợ truyền trực tiếp file dưới dạng bytes thông qua types.Part
        document_part = types.Part.from_bytes(
            data=file_bytes,
            mime_type=file.content_type
        )
        
        prompt = "Hãy đọc tài liệu đính kèm này (có thể là bản scan có mộc đỏ) và trích xuất các thông tin hành chính yêu cầu."
    
        # 4. Cơ chế xử lý lỗi Rate Limit (429) với Exponential Backoff
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            try:
                # Sử dụng model gemini-1.5-pro chuyên trị các tác vụ suy luận phức tạp và đọc tài liệu scan
                response = client.models.generate_content(
                    model='gemini-1.5-pro', 
                    contents=[document_part, prompt], # Truyền cả file và prompt
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=DocumentExtraction,
                        temperature=0.0,
                    )
                )
                
                # Nếu thành công, parse JSON và trả về
                extracted_data = json.loads(response.text)
                return extracted_data
                
            except errors.APIError as e:
                # Kiểm tra lỗi Rate Limit (Quota Exceeded / 429)
                if e.code == 429 or "429" in str(e):
                    if attempt < MAX_RETRIES - 1:
                        # Chờ 2s, 4s, 8s... trước khi thử lại
                        sleep_time = 2 ** (attempt + 1)
                        print(f"Bị Rate Limit (429). Đang chờ {sleep_time} giây để thử lại (Lần {attempt + 1}/{MAX_RETRIES})...")
                        time.sleep(sleep_time)
                    else:
                        print("Đã thử lại nhiều lần nhưng vẫn bị Rate Limit.")
                        raise HTTPException(status_code=429, detail="Hệ thống AI đang quá tải. Vui lòng thử lại sau.")
                else:
                    # Nếu là lỗi khác (ví dụ 400 Bad Request, 500 Internal Error) thì văng lỗi luôn
                    raise HTTPException(status_code=500, detail=f"Lỗi API: {str(e)}")
            except Exception as e:
                 raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    
    return {
        "status": "success", 
        "message": f"Triggered extraction for {len(request.files)} files using {request.provider}."
    }
