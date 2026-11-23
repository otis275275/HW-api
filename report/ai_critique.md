# AI Critique (Phê Bình & Đánh Giá AI)

**MSSV:** 23120228 | **Thành viên:** M4  
**Phân hệ:** HW06 – API Testing (EShop SUT)

---

### Phê bình và Đánh giá Hợp tác với AI (200–300 từ)

Trong quá trình thực hiện bài tập kiểm thử API cho hệ thống EShop, AI (Google DeepMind Antigravity) đã thể hiện khả năng vượt trội trong việc phân rã đặc tả API và tự động hóa sinh các ca kiểm thử theo phân hoạch tương đương (Domain Partitioning), kiểm tra giá trị biên (Boundary Value Analysis) và đối chiếu JSON Schema hợp đồng. Tuy nhiên, AI bộc lộ những điểm khiếm khuyết và thiên vị (bias) rõ rệt:

1. **Điểm AI làm sai hoặc thiếu sót:** Khi sinh kịch bản cho endpoint `/api/apply-coupon`, AI ban đầu giả định mã nguồn xử lý đúng toán tử $\ge$ và công thức phần trăm thông thường, do đó không tự phát hiện được lỗi so sánh ngặt `total_amount > min_order_amount` hay công thức lỗi `(1 - discount_value)` nếu không được yêu cầu đối chiếu trực tiếp với mã nguồn backend. Tương tự, tại phân hệ quản trị `/api/admin/users`, AI mặc định rằng việc có token là đủ điều kiện xác thực, bỏ sót lỗ hổng kiểm soát truy cập (Broken Access Control - SEC-03) khi middleware chỉ giải mã JWT mà không hề kiểm tra vai trò `role === 'admin'`. Ngoài ra, AI thường bỏ qua các trạng thái phụ thuộc thời gian (Time-based State) như thời hạn hết hạn của OTP hay khả năng chống tấn công vét cạn (Brute-force).

2. **Nguyên nhân thất bại của AI:** AI bị giới hạn bởi tư duy "Happy-Path" và có xu hướng tin tưởng vào tài liệu đặc tả hơn là hoài nghi mã nguồn thực tế. AI không thể tự động hình dung các kịch bản bất đồng bộ (Race Condition) và quan hệ toàn vẹn dữ liệu đa bảng (Cross-table Foreign Key Integrity) nếu không có sự can thiệp của con người.

3. **Bài học nguyên tắc rút ra:** Hợp tác hiệu quả với AI đòi hỏi nguyên tắc **"Human-in-the-Loop & Zero-Trust Verification"** (Con người giám sát và kiểm chứng không tin tưởng tuyệt đối). AI là một trợ thủ đắc lực giúp mở rộng phạm vi và tăng tốc độ viết kịch bản, nhưng kỹ sư kiểm thử phải giữ vai trò then chốt trong việc phân tích rủi ro an ninh, tư duy nghịch đảo và hiệu chỉnh các giả định sai lầm của mô hình.
