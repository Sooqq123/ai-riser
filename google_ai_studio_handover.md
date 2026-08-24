# Bộ Tài Liệu Bàn Giao Triển Khai (Handover Package)
**Dự án:** GovDoc Hub
**Người chuẩn bị:** AI Riser Software Architect (Antigravity)
**Người tiếp nhận:** Google AI Studio / AI Coding Agent

---

## 1. Tóm tắt Hệ thống & Nguồn sự thật (Single Source of Truth)
Toàn bộ yêu cầu, kiến trúc, API Contract, thiết kế UI/UX và kế hoạch chia 3 giai đoạn đã được cô đọng và khóa lại trong file đặc tả duy nhất:
👉 **[office_ai_agent_specification.md](file:///C:/Users/Hi%20Windows%2011%20Home/.gemini/antigravity/brain/8a1a4d9a-f815-4abe-9ffa-1a2831e0dfa5/office_ai_agent_specification.md)**

*Tất cả các hành động lập trình bắt buộc phải đối chiếu với file này. Không được tạo thêm tài liệu mâu thuẫn.*

## 2. Danh sách các thành phần đã chuẩn bị
- [x] **Kiến trúc hệ thống:** Tauri (Frontend) + FastAPI (Backend) + Local RAG.
- [x] **API Contract:** Định nghĩa rõ Request/Response cho 3 API cốt lõi (Index, Search, Extract).
- [x] **Luồng 3 Giai đoạn triển khai:**
  - GĐ 1: Backend RAG & VectorDB.
  - GĐ 2: Agentic Workflow & Google Gemini Integration.
  - GĐ 3: Tauri Frontend & Packaging.
- [x] **Tiêu chuẩn xử lý lỗi (Zero-Tech Standard):** Bắt buộc dịch lỗi sang ngôn ngữ bình dân, dùng `utf-8`, xử lý luồng nhị phân bằng `io.BytesIO()`.

## 3. Danh sách Giả định & Quyết định Kỹ thuật (Assumptions & Decisions)
1. **Decision:** Tránh dùng mô hình đa tác tử tự trị (Autonomous Multi-Agent) vì tính khó kiểm soát đối với văn bản nhà nước. Thay bằng Deterministic Pipelines (cơ chế ReAct có giám sát).
2. **Decision:** Bỏ qua ElectronJS, chọn Tauri để giảm dung lượng file cài đặt xuống dưới 30MB, phù hợp với máy tính văn phòng cấu hình yếu.
3. **Assumption:** Máy tính của người dùng có kết nối Internet cơ bản để gọi API Gemini 1.5 Flash (Chế độ Nhanh). Nếu mất mạng, hệ thống dự phòng bằng Ollama cục bộ.

## 4. Kế hoạch Kiểm thử (Testing Plan)
- **Unit Test:** Kiểm tra hàm đọc PDF tiếng Việt xem có bị vỡ font không. Kiểm tra hàm Parser JSON xem có xử lý được JSON bị thiếu dấu phẩy không.
- **Integration Test:** Gọi API `/api/v1/extract` bằng Postman để đảm bảo file nhị phân `.xlsx` tải về mở được thành công trên Microsoft Excel.
- **E2E Test:** Khởi chạy file `.exe`, kéo thả 1 folder, gõ lệnh tìm kiếm và bấm nút trích xuất. Tất cả phải diễn ra mượt mà không hiện console log.

---

## 5. PROMPT TRIỂN KHAI HOÀN CHỈNH (Dành cho Google AI Studio / Coding Agent)

*Hãy copy toàn bộ khung dưới đây và dán vào Google AI Studio hoặc Cursor/Windsurf để bắt đầu lập trình:*

```markdown
Bạn là một AI Software Engineer Fullstack cấp cao. Nhiệm vụ của bạn là lập trình dự án "GovDoc Hub" dựa trên Tài liệu Đặc tả đã được phê duyệt.

[YÊU CẦU BẮT BUỘC TRƯỚC KHI BẮT ĐẦU]
1. Đọc kỹ và ghi nhớ toàn bộ file `office_ai_agent_specification.md`.
2. Tuyệt đối KHÔNG tự ý thay đổi Mục tiêu, Phạm vi dự án, hoặc Cấu trúc 3 Giai đoạn đã đề ra.
3. KHÔNG được bỏ qua các tiêu chuẩn kỹ thuật (đặc biệt là Encoding UTF-8, cấu trúc io.BytesIO() và cơ chế Humanized Error Handling).

[QUY TRÌNH THỰC THI CHẶT CHẼ]
- Bạn phải code tuần tự theo đúng 3 Giai đoạn đã vạch ra trong PRD (Từ GĐ1 -> GĐ2 -> GĐ3). Không được nhảy cóc.
- Khi làm việc ở mỗi Giai đoạn:
  1. Triển khai trực tiếp (Viết code thật, tạo file thật), KHÔNG CHỈ mô tả lý thuyết hay viết mã giả (pseudocode).
  2. Viết Unit Test và chạy kiểm thử ngay sau khi hoàn thành một module (ví dụ: Test API bằng `pytest` hoặc curl).
  3. Nếu phát hiện lỗi (ví dụ file Excel tải về bị hỏng), bạn phải tự động debug và sửa lỗi ngay lập tức.
  4. Bạn không được tuyên bố "Đã hoàn thành Giai đoạn X" nếu chưa chứng minh được code vượt qua Tiêu chí Nghiệm thu (Acceptance Criteria).

[BÁO CÁO SAU MỖI GIAI ĐOẠN]
Sau khi hoàn thành một giai đoạn, bạn phải dừng lại và in ra một Báo cáo ngắn bao gồm:
- Các file đã tạo/sửa.
- Giả định bạn tự đặt ra (nếu có).
- Giới hạn kỹ thuật hoặc phần chưa hoàn thành (nếu có).
- Trạng thái kiểm thử (Pass/Fail).
- Xin phép người dùng để chuyển sang Giai đoạn tiếp theo.

Hãy bắt đầu ngay bằng việc khởi tạo cấu trúc thư mục cho Giai đoạn 1 (Backend FastAPI & RAG)!
```
