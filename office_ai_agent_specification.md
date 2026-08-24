# Tài Liệu Đặc Tả Sản Phẩm và Kiến Trúc: GovDoc Hub (Trợ lý Xử lý Tài liệu Hành chính)

**Phiên bản:** 3.0 (Cập nhật chuẩn hóa cho việc bàn giao cho AI Coding Agent)
**Mục đích tài liệu:** Nguồn sự thật duy nhất (Single Source of Truth) để một AI Agent (như Google AI Studio / Cursor) đọc và lập trình ra sản phẩm hoàn chỉnh mà không cần tự suy diễn.

---

## 1. Tóm tắt điều hành (Executive Summary)
- **Tên dự án:** GovDoc Hub
- **Mô tả ngắn:** Một Ứng dụng Desktop chạy cục bộ (Tauri + FastAPI), hoạt động như một "Công cụ Tìm kiếm nội bộ kết hợp AI". Ứng dụng tự động đọc/index file tài liệu, cho phép người dùng tìm kiếm và thực hiện các tác vụ xử lý hàng loạt (Trích xuất Excel, Ghép báo cáo) qua 1 click chuột.
- **Giá trị cốt lõi:** Luồng AI cố định (Deterministic Pipelines) thông minh được thiết kế từ Google AI Studio, kết hợp với giao diện "Search-centric" cực kỳ dễ dùng (Zero-Tech Friendly).

## 2. Phân tích Người dùng & Hành vi (User Analysis)
- **Persona:** Cán bộ hành chính nhà nước. Hoàn toàn không biết IT, không biết Prompt Engineering.
- **Hành vi:** Giao diện tối giản. Chỉ cần Kéo thả file -> Tìm kiếm -> Bấm nút xuất Excel. Không chấp nhận thông báo lỗi kỹ thuật (Error 500).

## 3. Kiến trúc Sản phẩm & Kỹ thuật
**Kiến trúc tổng thể:**
- **Frontend:** Tauri (Rust) + React/Vite + TailwindCSS.
- **Backend:** FastAPI (Python 3.10+).
- **Data Layer:** Local RAG (ChromaDB), embedding bằng `BAAI/bge-m3`.
- **AI Core:** LangChain ReAct Agent kết nối với Google Gemini 1.5 Flash API (Online) hoặc Ollama Llama 3 (Offline).

**Cấu trúc thư mục (Folder Structure) đề xuất:**
```text
govdoc_hub/
├── src-tauri/               # Tauri Rust Core
├── src/                     # React Frontend
│   ├── components/          # UI Components (Search bar, File list)
│   ├── store/               # Zustand state management
│   └── App.tsx
└── backend/                 # FastAPI
    ├── main.py              # API Routes
    ├── rag_engine/          # ChromaDB, Embedding, Loaders
    └── agentic_pipelines/   # LangChain, Tools (Excel export)
```

## 4. API Contract & Data Schema (Backend <-> Frontend)
**1. API Upload & Index:** `POST /api/v1/index`
- *Request:* `multipart/form-data` (danh sách file).
- *Response:* `{"status": "success", "indexed_files": ["file1.pdf"]}`

**2. API Search:** `GET /api/v1/search?q={query}`
- *Response:* `{"results": [{"file_name": "...", "snippet": "..."}]}`

**3. API Extract to Excel:** `POST /api/v1/extract`
- *Request JSON:* `{"files": ["path1", "path2"], "action": "extract_licenses"}`
- *Response:* Trả về Binary File `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`.

## 5. Yêu cầu Chức năng & UX (Zero-Tech Standard)
- **Quản lý File & Xóa:** Phải có tính năng dọn dẹp bộ nhớ (Garbage Collection). Xóa file trên UI phải xóa trong ChromaDB.
- **Onboarding:** Bắt buộc có Intro.js / Tooltip hướng dẫn 3 bước khi mở app lần đầu.
- **Humanized Error Handling:** Tuyệt đối không hiện mã lỗi kỹ thuật. (VD: Thay vì "Rate limit exceeded" -> "Hệ thống đang phục vụ nhiều người, vui lòng thử lại sau 30s").
- **Auto-updater:** App tự động thông báo có bản mới và tải ngầm.

## 6. Kế hoạch Triển khai (3 Giai đoạn Chính)

### Giai đoạn 1: Lõi Backend RAG & Giao tiếp Dữ liệu
- **Mục tiêu:** Xây dựng hệ thống đọc file, băm văn bản (chunking) và tìm kiếm ngữ nghĩa độc lập.
- **Công việc:**
  - Setup thư mục `backend/`.
  - Khởi tạo FastAPI `main.py`.
  - Cài đặt ChromaDB cục bộ.
  - Viết script `pdfplumber` (đọc PDF utf-8) và `python-docx` (đọc Word).
- **Đầu ra:** REST API hoàn chỉnh, dùng Postman/Swagger test được việc up file và tìm ra text. Tiêu chí nghiệm thu: Tìm đúng đoạn text tiếng Việt có dấu.

### Giai đoạn 2: Trí tuệ AI Studio & Agentic Workflow
- **Mục tiêu:** Nhúng linh hồn AI vào ứng dụng, thiết lập luồng suy nghĩ ReAct.
- **Công việc:**
  - Viết file `agentic_pipelines/tools.py` định nghĩa các hàm: `export_to_excel`, `read_full_context`.
  - Sử dụng **Google AI Studio** để test và sinh ra System Prompt tốt nhất cho tác vụ "Chuyên viên hành chính".
  - Dùng LangChain `.with_structured_output()` để ép Gemini 1.5 Flash trả về chuẩn JSON.
  - Áp dụng `asyncio` và thư viện `Tenacity` (Exponential Backoff) để chống lỗi rớt mạng.
- **Đầu ra:** API `/api/v1/extract` hoạt động hoàn hảo, trả về file nhị phân `.xlsx` không bị hỏng (Dùng `io.BytesIO()`). 

### Giai đoạn 3: Frontend Tauri, Giao diện UX & Đóng gói
- **Mục tiêu:** Bọc API bằng giao diện siêu mượt và xuất file `.exe`.
- **Công việc:**
  - Khởi tạo `npm create tauri-app`.
  - Thiết kế UI "One-Window" với thanh Search ở giữa.
  - Quản lý trạng thái bằng Zustand (Loading, Success, Empty).
  - Viết màn hình Onboarding cho người mới.
  - Cấu hình PyInstaller gộp Backend Python vào file chạy của Tauri.
- **Đầu ra:** File cài đặt `.exe` hoạt động độc lập, nhấp đúp là chạy. Không lộ bất kỳ cửa sổ CMD (Terminal) nào ra ngoài.

## 7. Tiêu chuẩn Mã nguồn & Tránh lỗi (Mandatory Rules)
- **Luôn dùng `encoding='utf-8'`** khi đọc/ghi file.
- **Không ghi đĩa cho file xuất (Download):** Lưu file Excel vào RAM bằng `io.BytesIO()` rồi stream về Frontend để tránh lỗi phân quyền.
- **Giới hạn Context:** Ưu tiên nhồi toàn bộ text vào context của Gemini Flash. Nếu file quá dài (> 1 triệu token), tự động fallback về RAG.

---
*Phiên bản v3.0 - Nguồn sự thật duy nhất cho quá trình lập trình tự động.*
